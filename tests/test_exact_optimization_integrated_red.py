"""AT-TDD Phase 1 Red: LISS-0089 exact optimization contract.

The suite fixes the immutable operation/proof boundary before implementation.
It uses only repository-local literals and deterministic exact witnesses.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.exact_optimization import (  # type: ignore
        OperationGraph,
        OperationNode,
        OptimizationCandidate,
        ProofWitness,
        optimize_graph,
    )

    return locals()


def _node(api, node_id, kind, operands=(0,), parameters=(), provenance=True):
    return api["OperationNode"](
        node_id=node_id,
        kind=kind,
        operands=operands,
        parameters=parameters,
        provenance=(f"source.{node_id}", "physics.fixture", "semantic.fixture")
        if provenance
        else (),
    )


def _graph(api, nodes):
    return api["OperationGraph"](
        schema_version=1,
        nodes=tuple(nodes),
        roots=tuple(node.node_id for node in nodes),
        repetitions=("symbolic.region.0",),
    )


def _candidate(api, family, input_ids, output_ids, *, exact=True, conditions=()):
    return api["OptimizationCandidate"](
        candidate_id=f"candidate.{family}",
        family=family,
        input_ids=tuple(input_ids),
        output_ids=tuple(output_ids),
        side_conditions=tuple(conditions),
        policy_id="policy.exact.v1",
        exact=exact,
    )


def _witness(api, law, input_ids, output_ids, *, complete=True):
    return api["ProofWitness"](
        witness_id=f"witness.{law}",
        law=law,
        input_ids=tuple(input_ids),
        output_ids=tuple(output_ids),
        side_conditions=("operand_identity",) if complete else (),
        provenance=("source.fixture", "physics.fixture", "semantic.fixture")
        if complete
        else (),
        equivalence="exact" if complete else "",
    )


def test_inverse_cancellation_is_accepted_with_exact_witness() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "x", "X"), _node(api, "x_dg", "X_dagger")])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "inverse_cancellation", ("x", "x_dg"), ()),),
        (_witness(api, "inverse", ("x", "x_dg"), ()),),
    )
    assert result.accepted_families == ("inverse_cancellation",)
    assert result.proof_witnesses[0].equivalence == "exact"


def test_same_axis_rotation_merge_is_accepted() -> None:
    api = _load_api()
    graph = _graph(
        api,
        [
            _node(api, "r0", "RZ", parameters=("theta_a",)),
            _node(api, "r1", "RZ", parameters=("theta_b",)),
        ],
    )
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "rotation_merge", ("r0", "r1"), ("r_merged",), conditions=("same_axis",)),),
        (_witness(api, "rotation_addition", ("r0", "r1"), ("r_merged",)),),
    )
    assert result.accepted_families == ("rotation_merge",)
    assert result.transformed_graph.nodes[0].parameters == ("theta_a+theta_b",)


def test_commutation_requires_a_closed_witness() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "a", "X", (0,)), _node(api, "b", "Z", (1,))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "commutation", ("a", "b"), ("b", "a"), conditions=("disjoint_operands",)),),
        (_witness(api, "commutation", ("a", "b"), ("b", "a")),),
    )
    assert result.accepted_families == ("commutation",)
    assert [node.node_id for node in result.transformed_graph.nodes] == ["b", "a"]


def test_controlled_adjoint_specialization_retains_polarity_evidence() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "u", "U", (1,)), _node(api, "c", "CONTROL", (0, 1))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "controlled_adjoint", ("u", "c"), ("cu_dg",), conditions=("polarity=positive", "acting_space=0,1")),),
        (_witness(api, "controlled_adjoint", ("u", "c"), ("cu_dg",)),),
    )
    assert result.accepted_families == ("controlled_adjoint",)
    assert "polarity=positive" in result.proof_witnesses[0].side_conditions


def test_ancilla_reuse_requires_closed_discharge_evidence() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "anc", "ANCILLA", (2,)), _node(api, "u", "U", (0, 2))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "ancilla_reuse", ("anc", "u"), ("u_reused",), conditions=("discharged",)),),
        (_witness(api, "ancilla_discharge", ("anc", "u"), ("u_reused")),),
    )
    assert result.accepted_families == ("ancilla_reuse",)


def test_live_ancilla_reuse_is_rejected_without_discharge_witness() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "anc", "ANCILLA", (2,)), _node(api, "u", "U", (0, 2))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "ancilla_reuse", ("anc", "u"), ("u_reused",)),),
        (),
    )
    assert "OPT_ANCILLA_INVALID" in result.diagnostic_codes


def test_missing_provenance_is_rejected_without_mutating_source() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "x", "X", provenance=False)])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "inverse_cancellation", ("x",), ()),),
        (),
    )
    assert "OPT_PROVENANCE_INCOMPLETE" in result.diagnostic_codes
    assert result.source_graph is graph


def test_mismatched_rotation_axis_or_operand_is_rejected() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "r0", "RX", (0,)), _node(api, "r1", "RZ", (1,))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "rotation_merge", ("r0", "r1"), ("merged",), conditions=("same_axis",)),),
        (_witness(api, "rotation_addition", ("r0", "r1"), ("merged",)),),
    )
    assert "OPT_TRANSFORM_INVALID" in result.diagnostic_codes


def test_unproved_reordering_is_rejected_and_source_order_remains() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "a", "X", (0,)), _node(api, "b", "Z", (0,))])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "commutation", ("a", "b"), ("b", "a")),),
        (),
    )
    assert "OPT_PROOF_REQUIRED" in result.diagnostic_codes
    assert [node.node_id for node in result.transformed_graph.nodes] == ["a", "b"]


def test_approximate_or_provider_policy_is_never_presented_as_exact() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "x", "X")])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "provider_native_rewrite", ("x",), (), exact=False),),
        (_witness(api, "provider_cost", ("x",), (), complete=False),),
    )
    assert "OPT_POLICY_INVALID" in result.diagnostic_codes
    assert result.accepted_families == ()


def test_differential_mismatch_blocks_output() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "x", "X")])
    result = api["optimize_graph"](
        graph,
        (_candidate(api, "inverse_cancellation", ("x",), ()),),
        (_witness(api, "inverse", ("x",), (), complete=False),),
        exact_observable_before="probability:0.5",
        exact_observable_after="probability:0.25",
    )
    assert "OPT_DIFFERENTIAL_MISMATCH" in result.diagnostic_codes
    assert result.accepted_families == ()


def test_symbolic_repetition_is_compact_and_diagnostics_are_deterministic() -> None:
    api = _load_api()
    graph = _graph(api, [_node(api, "x", "X")])
    candidate = _candidate(api, "inverse_cancellation", ("x",), ())
    first = api["optimize_graph"](graph, (candidate,), ())
    second = api["optimize_graph"](graph, (candidate,), ())
    assert graph.repetitions == ("symbolic.region.0",)
    assert first.diagnostic_codes == second.diagnostic_codes
    assert first.to_dict() == second.to_dict()


if __name__ == "__main__":
    tests = tuple(
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
        else:
            print(f"pass {test.__name__}")
    print(f"\n{len(tests) - failures} passed, {failures} failed")
    raise SystemExit(1 if failures else 0)
