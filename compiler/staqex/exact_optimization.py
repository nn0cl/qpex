"""Provider-neutral exact optimization for LISS-0089.

This module records algebraic transformations and their proof witnesses. It
does not choose providers, route to hardware, or perform approximate rewrites.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any


@dataclass(frozen=True)
class OperationNode:
    node_id: str
    kind: str
    operands: tuple[int, ...]
    parameters: tuple[str, ...]
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class OperationGraph:
    schema_version: int
    nodes: tuple[OperationNode, ...]
    roots: tuple[str, ...]
    repetitions: tuple[str, ...]


@dataclass(frozen=True)
class OptimizationCandidate:
    candidate_id: str
    family: str
    input_ids: tuple[str, ...]
    output_ids: tuple[str, ...]
    side_conditions: tuple[str, ...] = ()
    policy_id: str = "policy.exact.v1"
    exact: bool = True


@dataclass(frozen=True)
class ProofWitness:
    witness_id: str
    law: str
    input_ids: tuple[str, ...]
    output_ids: tuple[str, ...]
    side_conditions: tuple[str, ...]
    provenance: tuple[str, ...]
    equivalence: str


@dataclass(frozen=True)
class OptimizationResult:
    source_graph: OperationGraph
    transformed_graph: OperationGraph
    accepted_families: tuple[str, ...]
    proof_witnesses: tuple[ProofWitness, ...]
    rejected_candidates: tuple[str, ...]
    diagnostic_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _node_map(graph: OperationGraph) -> dict[str, OperationNode]:
    return {node.node_id: node for node in graph.nodes}


def _replace_nodes(
    graph: OperationGraph,
    nodes: tuple[OperationNode, ...],
) -> OperationGraph:
    return OperationGraph(
        schema_version=graph.schema_version,
        nodes=nodes,
        roots=tuple(node.node_id for node in nodes),
        repetitions=graph.repetitions,
    )


def _provenance_complete(graph: OperationGraph) -> bool:
    return bool(graph.nodes) and all(node.provenance for node in graph.nodes)


def _witness_map(witnesses: tuple[ProofWitness, ...]) -> dict[tuple[str, ...], ProofWitness]:
    return {witness.input_ids: witness for witness in witnesses}


def _witness_for(
    candidate: OptimizationCandidate,
    witnesses: dict[tuple[str, ...], ProofWitness],
) -> ProofWitness | None:
    witness = witnesses.get(candidate.input_ids)
    if witness is None or witness.equivalence != "exact" or not witness.provenance:
        return None
    return witness


def _rotation_is_valid(
    candidate: OptimizationCandidate,
    nodes: dict[str, OperationNode],
) -> bool:
    inputs = [nodes.get(node_id) for node_id in candidate.input_ids]
    if len(inputs) != 2 or any(node is None for node in inputs):
        return False
    first, second = inputs
    assert first is not None and second is not None
    return (
        first.kind == second.kind
        and first.kind in {"RX", "RY", "RZ"}
        and first.operands == second.operands
        and "same_axis" in candidate.side_conditions
    )


def _commutation_is_valid(
    candidate: OptimizationCandidate,
    nodes: dict[str, OperationNode],
) -> bool:
    inputs = [nodes.get(node_id) for node_id in candidate.input_ids]
    if len(inputs) != 2 or any(node is None for node in inputs):
        return False
    assert inputs[0] is not None and inputs[1] is not None
    return bool(set(inputs[0].operands).isdisjoint(inputs[1].operands))


def _transformed_nodes(
    graph: OperationGraph,
    candidate: OptimizationCandidate,
) -> tuple[OperationNode, ...]:
    nodes = list(graph.nodes)
    by_id = _node_map(graph)
    if candidate.family == "inverse_cancellation":
        return tuple(node for node in nodes if node.node_id not in candidate.input_ids)
    if candidate.family == "rotation_merge":
        first = by_id[candidate.input_ids[0]]
        second = by_id[candidate.input_ids[1]]
        merged = OperationNode(
            node_id=candidate.output_ids[0],
            kind=first.kind,
            operands=first.operands,
            parameters=("+".join((*first.parameters, *second.parameters)),),
            provenance=first.provenance + second.provenance,
        )
        return tuple(
            merged if node.node_id == candidate.input_ids[0]
            else node
            for node in nodes
            if node.node_id != candidate.input_ids[1]
        )
    if candidate.family == "commutation":
        reordered = {node.node_id: node for node in nodes}
        ordered = [reordered[node_id] for node_id in candidate.output_ids]
        remainder = [node for node in nodes if node.node_id not in candidate.input_ids]
        return tuple(ordered + remainder)
    if candidate.family in {"controlled_adjoint", "ancilla_reuse"}:
        inputs = [by_id[node_id] for node_id in candidate.input_ids]
        result = OperationNode(
            node_id=candidate.output_ids[0],
            kind=candidate.family.upper(),
            operands=tuple(operand for node in inputs for operand in node.operands),
            parameters=tuple(parameter for node in inputs for parameter in node.parameters),
            provenance=tuple(value for node in inputs for value in node.provenance),
        )
        return tuple(
            result if node.node_id == candidate.input_ids[0]
            else node
            for node in nodes
            if node.node_id not in candidate.input_ids[1:]
        )
    return graph.nodes


def _candidate_diagnostics(
    candidate: OptimizationCandidate,
    nodes: dict[str, OperationNode],
    witness: ProofWitness | None,
    exact_observable_before: str | None,
    exact_observable_after: str | None,
) -> list[str]:
    codes: list[str] = []
    if not candidate.exact or "provider" in candidate.family.casefold():
        codes.append("OPT_POLICY_INVALID")
    if witness is None:
        codes.append("OPT_PROOF_REQUIRED")
    if candidate.family == "rotation_merge" and not _rotation_is_valid(candidate, nodes):
        codes.append("OPT_TRANSFORM_INVALID")
    if candidate.family == "commutation" and witness is not None and not _commutation_is_valid(candidate, nodes):
        codes.append("OPT_TRANSFORM_INVALID")
    if candidate.family == "ancilla_reuse" and (
        witness is None or "discharged" not in candidate.side_conditions
    ):
        codes.append("OPT_ANCILLA_INVALID")
    if (
        exact_observable_before is not None
        and exact_observable_after is not None
        and exact_observable_before != exact_observable_after
    ):
        codes.append("OPT_DIFFERENTIAL_MISMATCH")
    return codes


def _merge_witness(
    candidate: OptimizationCandidate,
    witness: ProofWitness,
) -> ProofWitness:
    return replace(
        witness,
        side_conditions=tuple(
            dict.fromkeys(candidate.side_conditions + witness.side_conditions)
        ),
    )


def optimize_graph(
    graph: OperationGraph,
    candidates: tuple[OptimizationCandidate, ...],
    witnesses: tuple[ProofWitness, ...],
    *,
    exact_observable_before: str | None = None,
    exact_observable_after: str | None = None,
) -> OptimizationResult:
    """Apply only exact, witnessed transformations to an immutable graph."""

    nodes = _node_map(graph)
    witness_by_inputs = _witness_map(witnesses)
    transformed = graph
    accepted: list[str] = []
    accepted_witnesses: list[ProofWitness] = []
    rejected: list[str] = []
    diagnostics: list[str] = []

    if not _provenance_complete(graph):
        diagnostics.append("OPT_PROVENANCE_INCOMPLETE")

    for candidate in candidates:
        witness = _witness_for(candidate, witness_by_inputs)
        candidate_codes = _candidate_diagnostics(
            candidate,
            nodes,
            witness,
            exact_observable_before,
            exact_observable_after,
        )

        if candidate_codes:
            diagnostics.extend(candidate_codes)
            rejected.append(candidate.candidate_id)
            continue

        transformed = _replace_nodes(transformed, _transformed_nodes(transformed, candidate))
        accepted.append(candidate.family)
        assert witness is not None
        accepted_witnesses.append(_merge_witness(candidate, witness))

    return OptimizationResult(
        source_graph=graph,
        transformed_graph=transformed,
        accepted_families=tuple(accepted),
        proof_witnesses=tuple(accepted_witnesses),
        rejected_candidates=tuple(rejected),
        diagnostic_codes=tuple(sorted(set(diagnostics))),
    )
