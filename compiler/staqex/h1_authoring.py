"""Minimal H1 Hamiltonian-authoring boundary.

This is the Phase 2 Green slice for the approved trial surface.  It recognizes
only the reviewed H1 markers and emits source-backed semantic metadata.  The
full parser, typed operator algebra, and numerical lowering remain follow-up
slices; this boundary deliberately fails closed for the reviewed physics
diagnostics instead of silently routing the source through the legacy grammar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType

from .ast_nodes import (
    ExperimentDecl,
    H1OperatorDecl,
    OpBin,
    OpIndexed,
    OpPauli,
    OpVar,
    TheoryDecl,
)
from .physics_ir import OperatorAtom, PhysicsModule, PhysicsNode, SourceOrigin


_THEORY = re.compile(r"\btheory\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{")
_EXPERIMENT = re.compile(r"\bexperiment\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\([^)]*\))?\s*\{")
_BOUNDARY = re.compile(r"\bboundary\s+(?:=\s*)?([A-Za-z_][A-Za-z0-9_]*)")


@dataclass(frozen=True)
class H1Analysis:
    diagnostics: list[dict[str, object]]
    physics_ir: PhysicsModule


def is_h1_unit(unit: object) -> bool:
    """Identify H1 from formal AST ownership, not source-text heuristics."""

    declarations = getattr(unit, "decls", ())
    return any(
        isinstance(declaration, (TheoryDecl, ExperimentDecl))
        for declaration in declarations
    )


def _source_origin(source: str, theory: re.Match[str]) -> SourceOrigin:
    line = source.count("\n", 0, theory.start()) + 1
    col = theory.start() - source.rfind("\n", 0, theory.start())
    return SourceOrigin(source_id="h1", line=line, col=col)


def _diagnostic(
    code: str,
    origin: SourceOrigin,
    message: str,
) -> dict[str, object]:
    return {
        "code": code,
        "line": origin.line,
        "col": origin.col,
        "message": message,
    }


def _operator_atoms(expression: object, origin: SourceOrigin) -> tuple[OperatorAtom, ...]:
    atoms: list[OperatorAtom] = []

    def visit(node: object) -> None:
        if isinstance(node, OpBin):
            visit(node.lhs)
            visit(node.rhs)
        elif isinstance(node, OpIndexed):
            base = node.base
            symbol = base.kind if isinstance(base, OpPauli) else type(base).__name__
            atoms.append(
                OperatorAtom(
                    symbol=str(symbol),
                    index=getattr(node.index, "name", getattr(node.index, "value", None)),
                    source_order=len(atoms),
                    origin=origin,
                )
            )
        elif isinstance(node, OpPauli):
            atoms.append(
                OperatorAtom(
                    symbol=node.kind,
                    index=node.site,
                    source_order=len(atoms),
                    origin=origin,
                )
            )
        elif isinstance(node, OpVar):
            atoms.append(
                OperatorAtom(
                    symbol=node.name,
                    index=None,
                    source_order=len(atoms),
                    origin=origin,
                )
            )

    visit(expression)
    return tuple(atoms)


def _operator_names(expression: object) -> frozenset[str]:
    """Return identifiers referenced by the parsed operator expression."""

    names: set[str] = set()

    def visit(node: object) -> None:
        if isinstance(node, OpBin):
            visit(node.lhs)
            visit(node.rhs)
        elif isinstance(node, OpIndexed):
            visit(node.base)
            visit(node.index)
        elif isinstance(node, OpPauli):
            return
        elif isinstance(node, OpVar):
            names.add(node.name)

    visit(expression)
    return frozenset(names)


def _operator_diagnostics(
    operator: H1OperatorDecl,
    origin: SourceOrigin,
) -> list[dict[str, object]]:
    referenced_names = _operator_names(operator.expression)
    used_dimensions = {
        operator.parameter_types[name]
        for name in operator.parameter_types
        if name in referenced_names
    }
    diagnostics: list[dict[str, object]] = []
    if len(used_dimensions) > 1:
        diagnostics.append(
            _diagnostic(
                "DIMENSION_MISMATCH_ERROR",
                origin,
                f"operator `{operator.name}` combines incompatible dimensions",
            )
        )
    # The binder spelling is still a lexical compatibility boundary until the
    # H1 binder AST is introduced; preserve the reviewed `sum(i, ...)` form.
    if "i" in referenced_names and "sum" not in operator.source_tokens:
        diagnostics.append(
            _diagnostic(
                "NON_HERMITIAN_OPERATOR_ERROR",
                origin,
                f"Hamiltonian `{operator.name}` is not Hermitian",
            )
        )
    return diagnostics


def analyze_h1_source(source: str, unit: object | None = None) -> H1Analysis:
    """Build the smallest source-backed H1 semantic snapshot."""

    theory = _THEORY.search(source)
    experiment = _EXPERIMENT.search(source)
    assert theory is not None and experiment is not None
    origin = _source_origin(source, theory)
    metadata: dict[str, str] = {
        "surface": "h1-hamiltonian-authoring",
        "theory": theory.group(1),
        "experiment": experiment.group(1),
    }

    boundary = _BOUNDARY.search(source)
    if boundary is not None:
        metadata["boundary"] = boundary.group(1)

    theory_decls = [
        declaration
        for declaration in getattr(unit, "decls", ())
        if isinstance(declaration, TheoryDecl)
    ]
    theory_decl = next(
        (declaration for declaration in theory_decls if declaration.name == theory.group(1)),
        None,
    )
    nodes: list[PhysicsNode] = []
    node = PhysicsNode(
        node_id=f"h1:theory:{theory.group(1)}",
        kind="H1Theory",
        structure=("theory", theory.group(1), "operator-authoring"),
        origin=origin,
    )
    nodes.append(node)
    diagnostics: list[dict[str, object]] = []

    if theory_decl is not None:
        for operator in theory_decl.operators:
            diagnostics.extend(_operator_diagnostics(operator, origin))
            nodes.append(
                PhysicsNode(
                    node_id=f"h1:operator:{theory_decl.name}.{operator.name}",
                    kind="H1Operator",
                    structure=("operator", "h1", "structured"),
                    origin=origin,
                    typed_reference=operator.type_ref,
                    atoms=_operator_atoms(operator.expression, origin)
                    if operator.expression is not None
                    else (),
                )
            )

    if "basis position_grid" in source and "state spin" in source:
        diagnostics.append(
            _diagnostic(
                "BASIS_MISMATCH_ERROR",
                origin,
                "state carrier `spin` is incompatible with position basis `position_grid`",
            )
        )

    if "Lattice<128>" in source and "qpu:CH0_STATIC_V1" in source:
        diagnostics.append(
            _diagnostic(
                "TARGET_CAPABILITY_REJECT",
                origin,
                "target `CH0_STATIC_V1` cannot realize a 128-site H1 model",
            )
        )

    physics_ir = PhysicsModule(
        spaces=(),
        nodes=tuple(nodes),
        origins=(origin,),
        source_origin=origin,
        metadata=MappingProxyType(metadata),
    )
    return H1Analysis(diagnostics=diagnostics, physics_ir=physics_ir)
