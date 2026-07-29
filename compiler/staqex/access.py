"""Access control (ADR 0058 revised — Rust/Go/Python style).

Visibility:
  - default (`module`) — same compilation module only
  - `pub` — cross-module / library API
  - leading `_` / `private` — class-private (or same-file for top-level)

`protected` is Forbidden (no inheritance). Java `module-info` exports are
advisory only — not required for local multi-file scripts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .ast_nodes import ModuleInfoDecl, Visibility


def same_package(a: list[str] | None, b: list[str] | None) -> bool:
    if not a or not b:
        return a == b
    return list(a) == list(b)


def package_key(pkg: list[str] | None) -> str:
    return ".".join(pkg) if pkg else ""


def normalize_visibility(visibility: Visibility | str) -> str:
    """Map legacy aliases onto the modern three-tier model."""
    if visibility == "package":
        return "module"
    if visibility == "protected":
        # Inheritance access removed — treat as module-private if it slips through.
        return "module"
    return str(visibility)


def is_underscore_private(name: str) -> bool:
    return name.startswith("_") and not name.startswith("__")


def effective_member_visibility(name: str, declared: Visibility | str = "module") -> str:
    if is_underscore_private(name):
        return "private"
    return normalize_visibility(declared)


def can_access(
    *,
    visibility: Visibility | str,
    decl_package: list[str] | None,
    use_package: list[str] | None,
    same_class: bool = False,
    is_subclass: bool = False,  # ignored — no inheritance
    same_module: bool = True,
    package_exported: bool = True,  # ignored — exports not enforced
    same_file: bool = False,
) -> bool:
    """Return True if a use-site may see a declaration with `visibility`."""
    _ = is_subclass, package_exported, decl_package, use_package
    vis = normalize_visibility(visibility)

    if same_class:
        return True

    if vis == "private":
        # Top-level private / `_`: same file only; members need same_class.
        return same_file

    if vis == "module":
        return same_module

    # public
    return True


def access_violation(
    *,
    visibility: Visibility | str,
    name: str,
    decl_package: list[str] | None,
    use_package: list[str] | None,
    span_line: int = 1,
    span_col: int = 1,
    same_class: bool = False,
    is_subclass: bool = False,
    same_module: bool = True,
    package_exported: bool = True,
    same_file: bool = False,
) -> dict[str, Any] | None:
    if can_access(
        visibility=visibility,
        decl_package=decl_package,
        use_package=use_package,
        same_class=same_class,
        is_subclass=is_subclass,
        same_module=same_module,
        package_exported=package_exported,
        same_file=same_file,
    ):
        return None
    vis = normalize_visibility(visibility)
    if vis == "private" or is_underscore_private(name):
        code = "PRIVATE_ACCESS_VIOLATION_ERROR"
    elif vis == "module":
        code = "MODULE_PRIVATE_ACCESS_ERROR"
    else:
        code = "ACCESS_CONTROL_VIOLATION_ERROR"
    return {
        "code": code,
        "line": span_line,
        "col": span_col,
        "message": (
            f"cannot access `{name}` with visibility `{vis}` "
            f"from package `{package_key(use_package) or '<unnamed>'}`"
        ),
    }


def find_module_info(start: Path) -> tuple[Path | None, ModuleInfoDecl | None, list[dict[str, Any]]]:
    """Walk parents for optional `module-info.sqx` (legacy / advisory metadata)."""
    from .lexer import Lexer
    from .parser import ParseError, Parser

    diags: list[dict[str, Any]] = []
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for _ in range(32):
        candidate = cur / "module-info.sqx"
        if candidate.is_file():
            source = candidate.read_text(encoding="utf-8")
            lexer = Lexer(source)
            tokens, lex_diags = lexer.tokenize()
            diags.extend(lex_diags)
            try:
                parser = Parser(tokens)
                info = parser.parse_module_info()
                diags.extend(parser.diagnostics)
                return cur, info, diags
            except ParseError as e:
                diags.append(
                    {
                        "code": "PARSE_ERROR",
                        "line": e.line,
                        "col": e.col,
                        "message": f"module-info.sqx: {e.message}",
                    }
                )
                return cur, None, diags
        if cur.parent == cur:
            break
        cur = cur.parent
    return None, None, diags


def resolve_export_package(module_name: list[str], export_path: list[str]) -> str:
    """Normalize export to a full package key (legacy helper)."""
    if not export_path:
        return ".".join(module_name)
    if (
        len(export_path) >= len(module_name)
        and export_path[: len(module_name)] == module_name
    ):
        return ".".join(export_path)
    return ".".join([*module_name, *export_path])


def is_package_exported(info: ModuleInfoDecl | None, package: list[str] | None) -> bool:
    """Always True — exports are not enforced (physicist-noise-free scripts)."""
    _ = info, package
    return True
