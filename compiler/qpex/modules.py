"""User-module import resolution (ADR 0054) + encapsulation (ADR 0058).

`compile_path(entry)` walks `import` edges and merges accessible library
symbols into the entry compilation unit. Visibility: `pub` / default module /
leading `_` (no Java exports ceremony).

Cross-module: only `pub` symbols merge; use of a skipped module-private name
from another module yields `MODULE_PRIVATE_ACCESS_ERROR`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .access import find_module_info, normalize_visibility, same_package
from .ast_nodes import (
    Attr,
    Call,
    ClassDecl,
    CompilationUnit,
    EnumDecl,
    FunDecl,
    ImportDecl,
    MainDecl,
    StateBind,
    StructDecl,
    Var,
    Visibility,
)
from .lexer import Lexer
from .parser import ParseError, Parser


@dataclass
class ModuleGraph:
    """Loaded units keyed by resolved file path."""

    units: dict[Path, CompilationUnit] = field(default_factory=dict)
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    order: list[Path] = field(default_factory=list)  # deps-first
    module_root: dict[Path, Path | None] = field(default_factory=dict)
    hidden: dict[str, dict[str, Any]] = field(default_factory=dict)


def _parse_file(path: Path) -> tuple[CompilationUnit | None, list[dict[str, Any]]]:
    source = path.read_text(encoding="utf-8")
    lexer = Lexer(source)
    tokens, lex_diags = lexer.tokenize()
    diags: list[dict[str, Any]] = list(lex_diags)
    try:
        parser = Parser(tokens)
        unit = parser.parse()
        diags.extend(parser.diagnostics)
        return unit, diags
    except ParseError as e:
        diags.append(
            {
                "code": "PARSE_ERROR",
                "line": e.line,
                "col": e.col,
                "message": f"{path.name}: {e.message}",
            }
        )
        return None, diags


def _is_stdlib_import(imp: ImportDecl) -> bool:
    path = tuple(p for p in imp.path if p != "*")
    if not path:
        return False
    if path[0] == "qpex":
        return True
    return False


def resolve_import_path(
    imp: ImportDecl,
    *,
    entry_package: list[str],
    entry_dir: Path,
) -> Path | None:
    """Map `import a.b.c.mod` → `entry_dir/…/mod.qpex` under the entry package."""
    if _is_stdlib_import(imp):
        return None
    parts = [p for p in imp.path if p != "*"]
    if not parts:
        return None
    i = 0
    while i < len(parts) and i < len(entry_package) and parts[i] == entry_package[i]:
        i += 1
    rel = parts[i:]
    if not rel:
        return None
    *dirs, stem = rel
    candidate = entry_dir.joinpath(*dirs, f"{stem}.qpex")
    if candidate.is_file():
        return candidate.resolve()
    matches = list(entry_dir.rglob(f"{stem}.qpex"))
    if len(matches) == 1:
        return matches[0].resolve()
    return None


def _pkg(unit: CompilationUnit) -> list[str] | None:
    return list(unit.package.path) if unit.package else None


def _visible_across(
    vis: Visibility,
    *,
    decl_pkg: list[str] | None,
    use_pkg: list[str] | None,
    same_file: bool,
    same_module: bool = True,
) -> bool:
    _ = decl_pkg, use_pkg
    v = normalize_visibility(vis)
    if v == "private":
        return same_file
    if v == "module":
        return same_module
    return True  # public


def _decl_names(decl: Any) -> list[str]:
    names: list[str] = []
    n = getattr(decl, "name", None)
    q = getattr(decl, "qualified_name", None)
    if isinstance(n, str):
        names.append(n)
    if isinstance(q, str) and q not in names:
        names.append(q)
    return names


def _collect_entry_refs(unit: CompilationUnit) -> set[str]:
    refs: set[str] = set()

    def add_expr(expr: Any) -> None:
        if expr is None:
            return
        if isinstance(expr, Var):
            refs.add(expr.name)
            return
        if isinstance(expr, Attr):
            cur: Any = expr
            parts: list[str] = []
            while isinstance(cur, Attr):
                parts.append(cur.name)
                cur = cur.obj
            if isinstance(cur, Var):
                parts.append(cur.name)
                parts.reverse()
                refs.add(parts[0])
                refs.add(".".join(parts))
            add_expr(expr.obj)
            return
        if isinstance(expr, Call):
            add_expr(expr.callee)
            for a in expr.args:
                add_expr(a)
            return
        for v in getattr(expr, "__dict__", {}).values():
            if isinstance(v, list):
                for it in v:
                    add_expr(it)
            else:
                add_expr(v)

    if unit.main is not None:
        for stmt in unit.main.body.stmts:
            if isinstance(stmt, StateBind):
                add_expr(stmt.expr)
            else:
                add_expr(getattr(stmt, "expr", None))
                add_expr(getattr(stmt, "target", None))
                add_expr(getattr(stmt, "value", None))
    return refs


def load_module_graph(entry: Path) -> ModuleGraph:
    entry = entry.resolve()
    graph = ModuleGraph()
    if not entry.is_file():
        graph.diagnostics.append(
            {
                "code": "MODULE_NOT_FOUND_ERROR",
                "line": 1,
                "col": 1,
                "message": f"entry file not found: {entry}",
            }
        )
        return graph

    entry_unit, diags = _parse_file(entry)
    graph.diagnostics.extend(diags)
    if entry_unit is None:
        return graph

    entry_package = list(entry_unit.package.path) if entry_unit.package else []
    entry_dir = entry.parent
    graph.units[entry] = entry_unit

    entry_mod_root, _entry_mod, mod_diags = find_module_info(entry)
    graph.diagnostics.extend(mod_diags)
    graph.module_root[entry] = entry_mod_root

    visiting: set[Path] = set()
    done: set[Path] = set()

    def visit(path: Path) -> None:
        if path in done:
            return
        if path in visiting:
            graph.diagnostics.append(
                {
                    "code": "MODULE_CYCLE_ERROR",
                    "line": 1,
                    "col": 1,
                    "message": f"import cycle involving {path.name}",
                }
            )
            return
        visiting.add(path)
        unit = graph.units.get(path)
        if unit is None:
            unit, d2 = _parse_file(path)
            graph.diagnostics.extend(d2)
            if unit is None:
                visiting.discard(path)
                return
            graph.units[path] = unit
        if path not in graph.module_root:
            root, _info, d_m = find_module_info(path)
            graph.diagnostics.extend(d_m)
            graph.module_root[path] = root
        pkg = list(unit.package.path) if unit.package else entry_package
        for imp in unit.imports:
            if _is_stdlib_import(imp):
                continue
            target = resolve_import_path(
                imp, entry_package=pkg if pkg else entry_package, entry_dir=entry_dir
            )
            if target is None:
                target = resolve_import_path(
                    imp, entry_package=entry_package, entry_dir=entry_dir
                )
            if target is None:
                graph.diagnostics.append(
                    {
                        "code": "MODULE_NOT_FOUND_ERROR",
                        "line": imp.span.line,
                        "col": imp.span.col,
                        "message": (
                            f"cannot resolve import `{'.'.join(imp.path)}` "
                            f"from {path.name}"
                        ),
                    }
                )
                continue

            if target not in graph.units:
                u2, d3 = _parse_file(target)
                graph.diagnostics.extend(d3)
                if u2 is None:
                    continue
                graph.units[target] = u2
            tgt_root, _tgt_mod, d4 = find_module_info(target)
            graph.diagnostics.extend(d4)
            graph.module_root[target] = tgt_root
            visit(target)
        visiting.discard(path)
        done.add(path)
        graph.order.append(path)

    visit(entry)
    return graph


def merge_modules(entry: Path, graph: ModuleGraph) -> CompilationUnit | None:
    """Deps-first merge of accessible decls + Operator/field harvest."""
    if entry not in graph.units:
        return None
    entry_unit = graph.units[entry]
    entry_pkg = _pkg(entry_unit)
    entry_root = graph.module_root.get(entry)
    merged_decls: list[Any] = []
    harvested_ops: list[StateBind] = []
    harvested_fields: list[StateBind] = []
    entry_refs = _collect_entry_refs(entry_unit)

    for path in graph.order:
        if path == entry:
            continue
        unit = graph.units[path]
        unit_pkg = _pkg(unit)
        same_file = False
        dep_root = graph.module_root.get(path)
        same_module = dep_root == entry_root
        for decl in unit.decls:
            vis: Visibility = getattr(decl, "visibility", "module")  # type: ignore[assignment]
            if not _visible_across(
                vis,
                decl_pkg=unit_pkg,
                use_pkg=entry_pkg,
                same_file=same_file,
                same_module=same_module,
            ):
                for n in _decl_names(decl):
                    graph.hidden[n] = {
                        "visibility": normalize_visibility(vis),
                        "path": str(path),
                    }
                    short = n.split(".")[-1]
                    if n in entry_refs or short in entry_refs:
                        graph.diagnostics.append(
                            {
                                "code": "MODULE_PRIVATE_ACCESS_ERROR",
                                "line": 1,
                                "col": 1,
                                "message": (
                                    f"cannot access module-private `{n}` from "
                                    f"another module (mark `pub` to export)"
                                ),
                            }
                        )
                continue
            if isinstance(decl, ClassDecl):
                merged_decls.append(decl)
                if vis == "public" or same_package(unit_pkg, entry_pkg) or same_module:
                    for f in decl.fields or []:
                        harvested_fields.append(f)
            elif isinstance(decl, (EnumDecl, StructDecl)):
                merged_decls.append(decl)
            elif isinstance(decl, FunDecl):
                if decl.visibility == "public" or (
                    decl.visibility in {"module", "package"} and same_module
                ):
                    merged_decls.append(decl)
                    if decl.visibility == "public":
                        for stmt in decl.body.stmts:
                            if (
                                isinstance(stmt, StateBind)
                                and stmt.ty is not None
                                and stmt.ty.name == "Operator"
                            ):
                                harvested_ops.append(stmt)

    for decl in entry_unit.decls:
        merged_decls.append(decl)

    main = entry_unit.main
    if main is not None and (harvested_fields or harvested_ops):
        new_stmts = list(harvested_fields) + list(harvested_ops) + list(main.body.stmts)
        from .ast_nodes import Block

        main = MainDecl(
            params=main.params,
            body=Block(stmts=new_stmts, span=main.body.span),
            span=main.span,
        )

    return CompilationUnit(
        package=entry_unit.package,
        imports=entry_unit.imports,
        decls=merged_decls,
        main=main,
        span=entry_unit.span,
    )
