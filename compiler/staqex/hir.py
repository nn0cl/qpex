"""Immutable phase-resolved typed HIR view (LISS-0080).

Additive extraction from TypeChecker — no evaluator rewire in Slices A–D.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .ast_nodes import (
    Block,
    CompilationUnit,
    FunDecl,
    Measure,
    ScientificScopeContract,
    ScientificScopeDecl,
    StateBind,
    Var,
)
from .typecheck import Ty, TypeChecker

_KERNEL_PHASE = "kernel"

_KNOWN_PHASES = frozenset({
    "theory", "experiment", "workflow", "execution", "report",
    "system", _KERNEL_PHASE,
})

_KNOWN_EFFECTS = frozenset({"Measure", "Snapshot", "Inspect", "Host"})


@dataclass(frozen=True, slots=True)
class HirSpan:
    """Decl-level source location."""

    line: int
    col: int


@dataclass(frozen=True, slots=True)
class HirDecl:
    """Top-level declaration with resolved scientific phase, effects, and span."""

    name: str
    phase: str
    effects: frozenset[str] = field(default_factory=frozenset)
    span: HirSpan | None = None


@dataclass(frozen=True, slots=True)
class HirModule:
    """Immutable HIR module snapshot (symbols + typed expression map)."""

    symbols: Mapping[str, Ty]
    typed: Mapping[int, Ty]
    declarations: Mapping[str, HirDecl]


def _span_from(ast_node: Any) -> HirSpan | None:
    s = getattr(ast_node, "span", None)
    if s is None:
        return None
    return HirSpan(line=s.line, col=s.col)


def _build_declarations(
    checker: TypeChecker,
    scope_contracts: Mapping[str, ScientificScopeContract] | None,
    unit: CompilationUnit | None,
) -> Mapping[str, HirDecl]:
    decls: dict[str, HirDecl] = {}

    # Build name→span index from AST decls when unit is available.
    span_index: dict[str, HirSpan | None] = {}
    if unit is not None:
        for d in unit.decls:
            name = getattr(d, "name", None)
            if name:
                span_index[name] = _span_from(d)
        if unit.main is not None:
            span_index["main"] = _span_from(unit.main)

    if scope_contracts:
        for name, contract in scope_contracts.items():
            decls[name] = HirDecl(
                name=name,
                phase=contract.kind,
                effects=frozenset(),
                span=span_index.get(name),
            )

    for name in checker.fun_returns:
        if "." in name or name in decls:
            continue
        effects = checker.fun_effects.get(name, frozenset())
        decls[name] = HirDecl(
            name=name,
            phase=_KERNEL_PHASE,
            effects=frozenset(effects),
            span=span_index.get(name),
        )

    if checker.has_entry_main and "main" not in decls:
        decls["main"] = HirDecl(
            name="main",
            phase=_KERNEL_PHASE,
            effects=frozenset(),
            span=span_index.get("main"),
        )

    return MappingProxyType(decls)


def build_hir(
    checker: TypeChecker,
    *,
    scope_contracts: Mapping[str, ScientificScopeContract] | None = None,
    unit: CompilationUnit | None = None,
) -> HirModule:
    """Build an immutable HIR view from a completed TypeChecker.

    Slice A: symbol table + typed expression map.
    Slice B: declaration phases from sealed scientific-scope contracts.
    Slice C: explicit ``effects {…}`` declarations on each HIR decl.
    Slice D: decl-level source provenance via optional ``unit``.
    """
    return HirModule(
        symbols=MappingProxyType(dict(checker.env)),
        typed=MappingProxyType(dict(checker.typed)),
        declarations=_build_declarations(checker, scope_contracts, unit),
    )


_VERIFIER_DIAGNOSTICS_CODE = "HIR_INVARIANT_ERROR"
_LINEAR_DUPLICATE_USE = "LINEAR_DUPLICATE_USE"


def verify_hir(module: HirModule) -> list[dict]:
    """Lightweight HIR invariant checker.

    Returns a list of diagnostic dicts (empty means valid).
    Checks that all declaration phases and effects are known values.
    """
    diags: list[dict] = []
    for name, decl in module.declarations.items():
        if decl.phase not in _KNOWN_PHASES:
            diags.append({
                "code": _VERIFIER_DIAGNOSTICS_CODE,
                "message": (
                    f"HIR decl '{name}' has unknown phase '{decl.phase}'; "
                    f"expected one of {sorted(_KNOWN_PHASES)}"
                ),
            })
        unknown_effects = decl.effects - _KNOWN_EFFECTS
        if unknown_effects:
            diags.append({
                "code": _VERIFIER_DIAGNOSTICS_CODE,
                "message": (
                    f"HIR decl '{name}' has unknown effect(s) "
                    f"{sorted(unknown_effects)}; "
                    f"expected subset of {sorted(_KNOWN_EFFECTS)}"
                ),
            })
    return diags


@dataclass
class _LinearUseState:
    """Per-block alias roots and consumed quantum-state roots."""

    aliases: dict[str, str]
    consumed: set[str]


def _linear_duplicate_use_diag(span: Any, message: str) -> dict:
    return {
        "code": _LINEAR_DUPLICATE_USE,
        "line": span.line,
        "col": span.col,
        "message": message,
    }


def _is_state_binding(name: str, module: HirModule) -> bool:
    ty = module.symbols.get(name)
    return ty is not None and ty.kind == "State"


def _linear_root(name: str, aliases: Mapping[str, str]) -> str:
    root = aliases.get(name, name)
    while root in aliases and aliases[root] != root:
        root = aliases[root]
    return root


class HirLinearVerifier:
    """Minimal HIR-level linear-use verifier for quantum state consumption.

    Slice A rejects rebinding an existing ``State`` value under a new name
    (``State alias = q``) and records duplicate terminal ``measure`` uses of
    the same linear root within one block.
    """

    def verify(
        self,
        module: HirModule,
        *,
        unit: CompilationUnit | None = None,
    ) -> list[dict]:
        if unit is None:
            return []

        diags: list[dict] = []
        for block in _linear_blocks(unit):
            diags.extend(self._verify_block(block, module))
        return diags

    def _verify_block(self, block: Block, module: HirModule) -> list[dict]:
        state = _LinearUseState(aliases={}, consumed=set())
        diags: list[dict] = []

        for stmt in block.stmts:
            if isinstance(stmt, StateBind):
                diag = self._check_state_alias_bind(stmt, module, state)
                if diag is not None:
                    diags.append(diag)
            elif isinstance(stmt, Measure) and isinstance(stmt.expr, Var):
                diags.extend(self._check_measure(stmt, state))

        return diags

    def _check_state_alias_bind(
        self,
        stmt: StateBind,
        module: HirModule,
        state: _LinearUseState,
    ) -> dict | None:
        if len(stmt.names) != 1:
            return None

        bound_name = stmt.names[0]
        if not _is_state_binding(bound_name, module):
            return None

        state.aliases.setdefault(bound_name, bound_name)
        if not isinstance(stmt.expr, Var):
            return None
        if not _is_state_binding(stmt.expr.name, module):
            return None

        root = _linear_root(stmt.expr.name, state.aliases)
        state.aliases[bound_name] = root
        if stmt.expr.name == bound_name:
            return None

        return _linear_duplicate_use_diag(
            stmt.span,
            (
                f"quantum state `{stmt.expr.name}` cannot be rebound as "
                f"`{bound_name}`; root `{root}` is linear"
            ),
        )

    def _check_measure(self, stmt: Measure, state: _LinearUseState) -> list[dict]:
        root = _linear_root(stmt.expr.name, state.aliases)
        if root in state.consumed:
            return [
                _linear_duplicate_use_diag(
                    stmt.span,
                    (
                        f"quantum state `{stmt.expr.name}` reuses consumed root "
                        f"`{root}`"
                    ),
                )
            ]

        state.consumed.add(root)
        return []


def _linear_blocks(unit: CompilationUnit) -> list[Block]:
    blocks: list[Block] = []
    if unit.main is not None:
        blocks.append(unit.main.body)
    for decl in unit.decls:
        if isinstance(decl, FunDecl):
            blocks.append(decl.body)
    return blocks
