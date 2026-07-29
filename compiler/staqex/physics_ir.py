"""Immutable Physics IR boundary for LISS-0081 Slices A through D.

This slice provides the smallest domain DTO surface needed to establish the
Physics IR boundary. It intentionally does not lower HIR, expand gates, or
evaluate formulas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PHYSICS_IR_PROVENANCE_ERROR = "PHYSICS_IR_PROVENANCE_ERROR"
PHYSICS_IR_DOMAIN_ERROR = "PHYSICS_IR_DOMAIN_ERROR"
PHYSICS_IR_STATISTICS_ERROR = "PHYSICS_IR_STATISTICS_ERROR"
PHYSICS_IR_FAMILY_ERROR = "PHYSICS_IR_FAMILY_ERROR"
PhysicsDiagnostic = dict[str, str]
_FORMULA_FAMILIES = frozenset({
    "ising",
    "heisenberg",
    "hubbard",
    "molecular_electronic",
    "oscillator",
    "lindblad",
})


@dataclass(frozen=True, slots=True)
class SourceOrigin:
    """Source identity and location retained by every Physics IR root/node."""

    source_id: str
    line: int
    col: int


@dataclass(frozen=True, slots=True)
class HilbertSpace:
    """A named Hilbert-space carrier with ordered tensor-factor metadata."""

    name: str
    factors: tuple[object, ...]
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class BinderNode:
    """A mathematical binder retained without finite expansion."""

    kind: str
    variables: tuple[str, ...]
    domain: object
    constraints: tuple[object, ...]
    body: object
    origin: SourceOrigin
    source_order: int = 0


@dataclass(frozen=True, slots=True)
class Statistics:
    """Particle/operator statistics policy retained by an operator node."""

    family: str
    policy: str


@dataclass(frozen=True, slots=True)
class OperatorAtom:
    """One source-ordered algebra atom."""

    symbol: str
    index: object
    source_order: int
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class ChannelNode:
    """A channel/evolution relation retained without numerical execution."""

    operation: str
    input_domain: object
    output_domain: object
    operands: tuple[object, ...]
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class MeasurementIntent:
    """A typed observation request, distinct from a runtime measurement result."""

    observable: str
    povm: str
    domain: object
    outcome: str
    mode: str
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class InitialCondition:
    """An ordered initial-state preparation relation."""

    target: str
    domain: object
    preparation: object
    source_order: int
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class SymmetryNode:
    """A named symmetry or conservation law declaration."""

    law_kind: str
    name: str
    operands: tuple[object, ...]
    domain: object
    source_order: int
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class InspectionRecord:
    """Stable, read-only summary of one formula-family node."""

    family: str | None
    node_id: str
    structure: tuple[object, ...]
    source_origin: SourceOrigin | None


@dataclass(frozen=True, slots=True)
class PhysicsNode:
    """Stable source-backed node emitted by the HIR lowering boundary."""

    node_id: str
    kind: str
    structure: tuple[object, ...]
    origin: SourceOrigin
    typed_reference: object | None = None
    atoms: tuple[OperatorAtom, ...] = ()


@dataclass(frozen=True, slots=True)
class PhysicsModule:
    """Immutable Physics IR module snapshot."""

    spaces: tuple[HilbertSpace, ...]
    nodes: tuple[object, ...]
    origins: tuple[SourceOrigin, ...]


@dataclass(frozen=True, slots=True)
class PhysicsInspection:
    """Deterministic inspection projection for an immutable Physics module."""

    module: PhysicsModule
    records: tuple[InspectionRecord, ...]


def _provenance_diagnostic() -> PhysicsDiagnostic:
    return {
        "code": PHYSICS_IR_PROVENANCE_ERROR,
        "message": "Physics IR module has no source ancestry",
    }


def _domain_diagnostic(message: str) -> PhysicsDiagnostic:
    return {"code": PHYSICS_IR_DOMAIN_ERROR, "message": message}


def _statistics_diagnostic() -> PhysicsDiagnostic:
    return {
        "code": PHYSICS_IR_STATISTICS_ERROR,
        "message": "Physics IR operator has no statistics reference",
    }


def _node_diagnostics(node: object) -> list[PhysicsDiagnostic]:
    if not isinstance(node, dict):
        return []

    diagnostics: list[PhysicsDiagnostic] = []
    if node.get("kind") == "Binder" and node.get("domain") is None:
        diagnostics.append(
            _domain_diagnostic("Physics IR binder has no domain reference")
        )
    if node.get("kind") == "Channel" and node.get("input_domain") is None:
        diagnostics.append(
            _domain_diagnostic("Physics IR channel has no input domain reference")
        )
    if node.get("kind") == "Symmetry" and node.get("domain") is None:
        diagnostics.append(
            _domain_diagnostic("Physics IR symmetry has no domain reference")
        )
    if (
        node.get("kind") == "Operator"
        and "statistics" in node
        and node.get("statistics") is None
    ):
        diagnostics.append(_statistics_diagnostic())
    return diagnostics


def build_physics_ir(hir: Any, *, unit: Any = None) -> PhysicsModule:
    """Build a minimal Physics IR root from an explicit immutable HIR input.

    The builder records declaration-level and approved typed-source structure.
    It is intentionally not wired into ``compile_source`` or the evaluator.
    """

    nodes: list[PhysicsNode] = []
    for name, declaration in hir.declarations.items():
        node = _physics_node_for_declaration(name, declaration, unit=unit)
        if node is not None:
            nodes.append(node)

    if unit is not None and getattr(unit, "main", None) is not None:
        nodes.extend(_typed_nodes_from_main(unit.main.body.stmts, unit=unit))

    origins = tuple(node.origin for node in nodes)
    return PhysicsModule(spaces=(), nodes=tuple(nodes), origins=origins)


def _physics_node_for_declaration(
    name: str,
    declaration: Any,
    *,
    unit: Any = None,
) -> PhysicsNode | None:
    span = declaration.span
    if span is None:
        return None
    return PhysicsNode(
        node_id=f"decl:{name}",
        kind="Declaration",
        structure=("typed", declaration.phase, "provenance"),
        origin=_source_origin_for_span(span, unit),
    )


def _source_id_from_unit(unit: Any) -> str:
    package = getattr(unit, "package", None)
    package_name = getattr(package, "name", None)
    return str(package_name) if package_name else "hir"


def _source_origin_for_span(span: Any, unit: Any) -> SourceOrigin:
    return SourceOrigin(
        source_id=_source_id_from_unit(unit),
        line=span.line,
        col=span.col,
    )


def _typed_nodes_from_main(statements: list[Any], *, unit: Any) -> list[Any]:
    nodes: list[Any] = []
    for source_order, statement in enumerate(statements):
        ty = getattr(statement, "ty", None)
        if ty is None or not getattr(statement, "names", None):
            continue
        name = statement.names[0]
        origin = _source_origin_for_span(statement.span, unit)
        if ty.name == "Operator":
            atoms = tuple(_operator_atoms(statement.expr, origin))
            nodes.append(_operator_node(name, ty, atoms, origin))
            binder = _binder_node(statement.expr, origin, source_order)
            if binder is not None:
                nodes.append(binder)
        elif ty.name == "Channel":
            args = getattr(ty, "args", [])
            nodes.append(_channel_node(name, statement.expr, args, origin))
    return nodes


def _operator_node(
    name: str,
    type_ref: Any,
    atoms: tuple[OperatorAtom, ...],
    origin: SourceOrigin,
) -> PhysicsNode:
    return PhysicsNode(
        node_id=f"operator:{name}",
        kind="Operator",
        structure=("operator", "typed", "provenance"),
        origin=origin,
        typed_reference=type_ref,
        atoms=atoms,
    )


def _channel_node(
    name: str,
    expression: Any,
    type_args: list[Any],
    origin: SourceOrigin,
) -> ChannelNode:
    return ChannelNode(
        operation=type(expression).__name__,
        input_domain=type_args[0].name if len(type_args) > 0 else None,
        output_domain=type_args[1].name if len(type_args) > 1 else None,
        operands=(name,),
        origin=origin,
    )


def _operator_atoms(expr: Any, origin: SourceOrigin) -> list[OperatorAtom]:
    atoms: list[OperatorAtom] = []

    def visit(node: Any) -> None:
        if node is None:
            return
        if hasattr(node, "lhs") and hasattr(node, "rhs"):
            visit(node.lhs)
            visit(node.rhs)
            return
        if hasattr(node, "base") and hasattr(node, "index"):
            base = node.base
            symbol = getattr(base, "kind", getattr(base, "name", type(base).__name__))
            atoms.append(
                OperatorAtom(
                    symbol=str(symbol),
                    index=getattr(node.index, "name", node.index),
                    source_order=len(atoms),
                    origin=origin,
                )
            )
            return
        symbol = getattr(node, "kind", getattr(node, "name", None))
        if symbol is not None and type(node).__name__ in {"OpPauli", "OpVar"}:
            atoms.append(
                OperatorAtom(
                    symbol=str(symbol),
                    index=getattr(node, "site", None),
                    source_order=len(atoms),
                    origin=origin,
                )
            )

    visit(expr)
    return atoms


def _binder_node(
    expr: Any,
    origin: SourceOrigin,
    source_order: int,
) -> BinderNode | None:
    if type(expr).__name__ != "OpBinder":
        return None
    return BinderNode(
        kind=expr.kind,
        variables=(expr.variable,),
        domain=expr.domain,
        constraints=(() if expr.guard is None else (expr.guard,)),
        body=expr.body,
        origin=origin,
        source_order=source_order,
    )


def verify_physics_ir(module: PhysicsModule) -> list[PhysicsDiagnostic]:
    """Return named diagnostics for invalid Slice A–C invariants.

    A Physics IR module must retain at least one source origin. Slice B also
    checks explicit domain and statistics references, while Slice C extends
    domain checks to channels and symmetries. Later slices add unit invariants.
    """

    diagnostics: list[PhysicsDiagnostic] = []
    if not module.origins:
        diagnostics.append(_provenance_diagnostic())
    for node in module.nodes:
        diagnostics.extend(_node_diagnostics(node))
    return diagnostics


def inspect_physics_ir(module: PhysicsModule) -> PhysicsInspection:
    """Project formula nodes into a deterministic, read-only inspection view."""

    records: list[InspectionRecord] = []
    for node in module.nodes:
        if not isinstance(node, dict):
            continue
        records.append(_inspection_record(node))
    return PhysicsInspection(module=module, records=tuple(records))


def _inspection_record(node: dict) -> InspectionRecord:
    structure = node.get("structure", ())
    if not isinstance(structure, tuple):
        structure = tuple(structure) if isinstance(structure, list) else ()
    return InspectionRecord(
        family=node.get("family"),
        node_id=str(node.get("node_id", "")),
        structure=structure,
        source_origin=node.get("origin"),
    )


def verify_physics_inspection(
    inspection: PhysicsInspection,
) -> list[PhysicsDiagnostic]:
    """Return named diagnostics for missing family/provenance inspection data."""

    diagnostics: list[PhysicsDiagnostic] = []
    for record in inspection.records:
        if record.family not in _FORMULA_FAMILIES:
            diagnostics.append(_family_diagnostic(record.family))
        if record.source_origin is None:
            diagnostics.append(_inspection_provenance_diagnostic(record.node_id))
    return diagnostics


def _family_diagnostic(family: str | None) -> PhysicsDiagnostic:
    return {
        "code": PHYSICS_IR_FAMILY_ERROR,
        "message": f"unsupported Physics IR formula family: {family!r}",
    }


def _inspection_provenance_diagnostic(node_id: str) -> PhysicsDiagnostic:
    return {
        "code": PHYSICS_IR_PROVENANCE_ERROR,
        "message": f"inspection record `{node_id}` has no source ancestry",
    }
