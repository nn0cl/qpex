"""Immutable phase-resolved typed HIR view (LISS-0080).

Additive extraction from TypeChecker — no evaluator rewire in Slices A–D.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .ast_nodes import (
    Attr,
    BinOp,
    Block,
    Call,
    CompilationUnit,
    DynamicQpuStmt,
    ForEachStmt,
    FunDecl,
    Inspect,
    KetLit,
    ListExpr,
    Measure,
    Pipe,
    ScientificScopeContract,
    Span,
    StateBind,
    TupleExpr,
    UnaryNot,
    Vacuum,
    Var,
    WhenExpr,
)
from .typecheck import Ty, TypeChecker
from .runtime.uncompute import LINEAR_UNCOMPUTE_AMPLITUDE_TOL

_KERNEL_PHASE = "kernel"

# LISS-0114 Slice B / R1: authoritative linear consume kinds.
# Gate / apply / hadamard rebinds are intentionally *not* consumes.
LINEAR_CONSUME_KINDS = frozenset({
    "measure",
    "static_uncompute_zero_reset",
})

# LISS-0114 Slice C / R2: alias policy (Adjudicator-locked 2026-07-29).
# "strict" → ``State alias = q`` is LINEAR_DUPLICATE_USE (no silent rename).
LINEAR_ALIAS_POLICY = "strict"

# LISS-0114 Slice D / R4: linear carriers at module-symbol + Type-First heads.
# DensityState is stored as Ty(kind="Object", payload="DensityState").
LINEAR_CARRIER_KINDS = frozenset({"State", "DensityState"})

# LINEAR_UNCOMPUTE_AMPLITUDE_TOL imported from runtime.uncompute (Slice F).

_KNOWN_PHASES = frozenset({
    "theory", "experiment", "workflow", "execution", "report",
    "system", _KERNEL_PHASE,
})

_KNOWN_EFFECTS = frozenset({"Measure", "Snapshot", "Inspect", "Host", "Uncompute"})
_LINEAR_DUPLICATE_USE = "LINEAR_DUPLICATE_USE"
_LINEAR_IMPLICIT_DISCARD = "LINEAR_IMPLICIT_DISCARD"
_UNCOMPUTE_WITNESS_MISSING = "UNCOMPUTE_WITNESS_MISSING"


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
    linear_diagnostics: tuple[dict, ...] = ()


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
    Slice C: ``effects {…}`` plus static Uncompute witnesses from ``unit``.
    Slice D: decl-level source provenance via optional ``unit``.
    """
    symbols = MappingProxyType(dict(checker.env))
    typed = MappingProxyType(dict(checker.typed))
    decls = dict(_build_declarations(checker, scope_contracts, unit))

    if unit is not None:
        # Provisional Slice C: static |0>/vacuum rebind witnesses (R9).
        for name in _scopes_with_uncompute_witness(unit, symbols):
            if name not in decls:
                continue
            decl = decls[name]
            decls[name] = HirDecl(
                name=decl.name,
                phase=decl.phase,
                effects=frozenset(decl.effects | {"Uncompute"}),
                span=decl.span,
            )

    module = HirModule(
        symbols=symbols,
        typed=typed,
        declarations=MappingProxyType(decls),
    )
    if unit is None:
        return module

    # Slice D: wire HirLinearVerifier into build_hir.
    linear_diags = tuple(HirLinearVerifier().verify(module, unit=unit))
    return HirModule(
        symbols=module.symbols,
        typed=module.typed,
        declarations=module.declarations,
        linear_diagnostics=linear_diags,
    )


_VERIFIER_DIAGNOSTICS_CODE = "HIR_INVARIANT_ERROR"


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
    """Per-block alias roots, introduced State roots, and consumed roots."""

    aliases: dict[str, str]
    introduced: dict[str, Span]
    consumed: set[str]
    uncompute_witnessed: bool = False


def _linear_diag(code: str, span: Span, message: str) -> dict:
    return {
        "code": code,
        "line": span.line,
        "col": span.col,
        "message": message,
    }


def is_linear_carrier_ty(ty: Ty) -> bool:
    """True when ``ty`` is a linear quantum carrier (State or DensityState)."""
    if ty.kind == "State":
        return True
    return ty.kind == "Object" and ty.payload == "DensityState"


def _is_state_binding(name: str, module_symbols: Mapping[str, Ty]) -> bool:
    ty = module_symbols.get(name)
    return ty is not None and is_linear_carrier_ty(ty)


def _stmt_binds_state(
    stmt: StateBind,
    module_symbols: Mapping[str, Ty],
    state: _LinearUseState,
) -> bool:
    """True when the bind is a linear State (symbols and/or Type-First head).

    Fun-local names are often absent from TypeChecker.env after check_unit
    (R10); fall back to ``State`` / ``DensityState`` type heads and in-block
    introductions.
    """
    if len(stmt.names) != 1:
        return False
    name = stmt.names[0]
    if stmt.ty is not None and stmt.ty.name in {"State", "DensityState"}:
        return True
    if name in state.introduced or name in state.aliases:
        return True
    return _is_state_binding(name, module_symbols)


def _is_state_var_alias(
    expr: object,
    module_symbols: Mapping[str, Ty],
    state: _LinearUseState,
) -> bool:
    if not isinstance(expr, Var):
        return False
    if expr.name in state.introduced or expr.name in state.aliases:
        return True
    return _is_state_binding(expr.name, module_symbols)


def _is_zero_reset(expr: object) -> bool:
    """Static uncompute witness: Vacuum or ket |0> (R9 provisional)."""
    if isinstance(expr, Vacuum):
        return True
    return isinstance(expr, KetLit) and expr.label == "0"


def _linear_root(name: str, aliases: Mapping[str, str]) -> str:
    root = aliases.get(name, name)
    while root in aliases and aliases[root] != root:
        root = aliases[root]
    return root


def _linear_scopes(unit: CompilationUnit) -> list[tuple[str, Block]]:
    scopes: list[tuple[str, Block]] = []
    if unit.main is not None:
        scopes.append(("main", unit.main.body))
    for decl in unit.decls:
        if isinstance(decl, FunDecl):
            scopes.append((decl.name, decl.body))
    return scopes


def _source_declared_uncompute(unit: CompilationUnit) -> set[str]:
    names: set[str] = set()
    for decl in unit.decls:
        if isinstance(decl, FunDecl) and "Uncompute" in decl.effects:
            names.add(decl.name)
    return names


def _analyze_block(
    block: Block,
    module_symbols: Mapping[str, Ty],
) -> tuple[list[dict], _LinearUseState]:
    state = _LinearUseState(aliases={}, introduced={}, consumed=set())
    diags: list[dict] = []

    for stmt in block.stmts:
        if isinstance(stmt, StateBind):
            diag = _check_state_bind(stmt, module_symbols, state)
            if diag is not None:
                diags.append(diag)
            # LISS-0114 Slice E: when / inspect uses consume outer roots.
            _consume_when_linear_uses(stmt.expr, state)
            _consume_inspect_linear_uses(stmt.expr, state)
        elif isinstance(stmt, Measure) and isinstance(stmt.expr, Var):
            diags.extend(_check_measure(stmt, state))
        elif isinstance(stmt, (ForEachStmt, DynamicQpuStmt)):
            nested_diags, nested = _analyze_block(stmt.body, module_symbols)
            diags.extend(nested_diags)
            state.consumed |= nested.consumed
            if nested.uncompute_witnessed:
                state.uncompute_witnessed = True

    diags.extend(_discard_diags(state))
    return diags, state


def _mark_linear_var_use(expr: object, state: _LinearUseState) -> None:
    if not isinstance(expr, Var):
        return
    root = _linear_root(expr.name, state.aliases)
    if root in state.introduced or expr.name in state.aliases:
        state.consumed.add(root)


def _expr_children(expr: object) -> tuple[object, ...]:
    if isinstance(expr, WhenExpr):
        return (expr.ctrl, *(arm.body for arm in expr.arms))
    if isinstance(expr, Call):
        return tuple(expr.args)
    if isinstance(expr, BinOp):
        return (expr.left, expr.right)
    if isinstance(expr, Pipe):
        return (expr.lhs, expr.rhs)
    if isinstance(expr, Attr):
        return (expr.obj,)
    if isinstance(expr, Inspect):
        return (expr.expr,)
    if isinstance(expr, UnaryNot):
        return (expr.expr,)
    if isinstance(expr, (TupleExpr, ListExpr)):
        return tuple(expr.items)
    return ()


def _mark_all_linear_vars(expr: object, state: _LinearUseState) -> None:
    if isinstance(expr, WhenExpr):
        _consume_when_linear_uses(expr, state)
        return
    if isinstance(expr, Var):
        _mark_linear_var_use(expr, state)
        return
    for child in _expr_children(expr):
        _mark_all_linear_vars(child, state)


def _consume_when_linear_uses(expr: object, state: _LinearUseState) -> None:
    """Consume linear roots used as ``when`` scrutinee or arm values (Slice E)."""
    if isinstance(expr, WhenExpr):
        _mark_linear_var_use(expr.ctrl, state)
        for arm in expr.arms:
            _mark_all_linear_vars(arm.body, state)
        return
    for child in _expr_children(expr):
        _consume_when_linear_uses(child, state)


def _consume_inspect_linear_uses(expr: object, state: _LinearUseState) -> None:
    """``inspect(x)`` uses ``x`` for linear lifetime (non-destructive view)."""
    if isinstance(expr, Inspect):
        _mark_all_linear_vars(expr.expr, state)
        return
    for child in _expr_children(expr):
        _consume_inspect_linear_uses(child, state)


def _check_state_bind(
    stmt: StateBind,
    module_symbols: Mapping[str, Ty],
    state: _LinearUseState,
) -> dict | None:
    if len(stmt.names) != 1:
        return None

    bound_name = stmt.names[0]
    if not _stmt_binds_state(stmt, module_symbols, state):
        return None

    # Same-name reset to |0>/vacuum: static uncompute witness (Slice C / R9).
    if bound_name in state.introduced and _is_zero_reset(stmt.expr):
        root = _linear_root(bound_name, state.aliases)
        state.consumed.add(root)
        state.uncompute_witnessed = True
        return None

    state.aliases.setdefault(bound_name, bound_name)

    if not _is_state_var_alias(stmt.expr, module_symbols, state):
        state.introduced.setdefault(bound_name, stmt.span)
        return None

    assert isinstance(stmt.expr, Var)
    root = _linear_root(stmt.expr.name, state.aliases)
    state.aliases[bound_name] = root
    if stmt.expr.name == bound_name:
        return None

    return _linear_diag(
        _LINEAR_DUPLICATE_USE,
        stmt.span,
        (
            f"quantum state `{stmt.expr.name}` cannot be rebound as "
            f"`{bound_name}`; root `{root}` is linear"
        ),
    )


def _check_measure(stmt: Measure, state: _LinearUseState) -> list[dict]:
    assert isinstance(stmt.expr, Var)
    root = _linear_root(stmt.expr.name, state.aliases)
    if root in state.consumed:
        return [
            _linear_diag(
                _LINEAR_DUPLICATE_USE,
                stmt.span,
                (
                    f"quantum state `{stmt.expr.name}` reuses consumed root "
                    f"`{root}`"
                ),
            )
        ]

    state.consumed.add(root)
    return []


def _discard_diags(state: _LinearUseState) -> list[dict]:
    return [
        _linear_diag(
            _LINEAR_IMPLICIT_DISCARD,
            span,
            (
                f"quantum state `{root}` is discarded without measure "
                f"or uncomputation"
            ),
        )
        for root, span in state.introduced.items()
        if root not in state.consumed
    ]


def _scopes_with_uncompute_witness(
    unit: CompilationUnit,
    module_symbols: Mapping[str, Ty],
) -> set[str]:
    names: set[str] = set()
    for scope_name, block in _linear_scopes(unit):
        _, state = _analyze_block(block, module_symbols)
        if state.uncompute_witnessed:
            names.add(scope_name)
    return names


class HirLinearVerifier:
    """HIR-level linear-use verifier for quantum state consumption.

    Slice A: reject ``State`` alias rebinding; track duplicate ``measure``.
    Slice B: reject introduced ``State`` roots left unconsumed at block exit.
    Slice C: static ``|0>`` / vacuum rebind as uncompute witness; require a
    witness when source declares ``effects { Uncompute }`` (R9 provisional).

    Consumption (see ``LINEAR_CONSUME_KINDS``): ``measure`` and same-name
    ``|0>`` / vacuum rebind only for bind-level kinds. Slice E additionally
    treats ``when`` scrutinee/arm Vars and ``inspect`` operands as uses.
    Gate / ``hadamard`` / ``apply`` rebinds do not consume (LISS-0114 B).
    """

    def verify(
        self,
        module: HirModule,
        *,
        unit: CompilationUnit | None = None,
    ) -> list[dict]:
        if unit is None:
            return []

        declared = _source_declared_uncompute(unit)
        diags: list[dict] = []
        for scope_name, block in _linear_scopes(unit):
            block_diags, state = _analyze_block(block, module.symbols)
            diags.extend(block_diags)

            if scope_name in declared and not state.uncompute_witnessed:
                decl = module.declarations.get(scope_name)
                line = decl.span.line if decl is not None and decl.span else 1
                col = decl.span.col if decl is not None and decl.span else 1
                diags.append({
                    "code": _UNCOMPUTE_WITNESS_MISSING,
                    "line": line,
                    "col": col,
                    "message": (
                        f"`{scope_name}` declares effect Uncompute but has no "
                        f"static |0>/vacuum uncompute witness"
                    ),
                })

        return diags
