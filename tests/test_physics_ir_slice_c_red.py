"""AT-TDD Phase 1 Red: LISS-0081 Slice C — channels and physical intent."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice C Green must extend the focused Physics IR API."""
    from compiler.staqex.physics_ir import (
        ChannelNode,
        InitialCondition,
        MeasurementIntent,
        PhysicsModule,
        SourceOrigin,
        SymmetryNode,
        verify_physics_ir,
    )

    return (
        ChannelNode,
        InitialCondition,
        MeasurementIntent,
        PhysicsModule,
        SourceOrigin,
        SymmetryNode,
        verify_physics_ir,
    )


def test_channel_node_preserves_domains_operation_operands_and_origin() -> None:
    ChannelNode, _, _, _, SourceOrigin, _, _ = _load_api()

    origin = SourceOrigin(source_id="open-system.staqex", line=12, col=5)
    channel = ChannelNode(
        operation="Lindblad",
        input_domain="QubitRegister<2>",
        output_domain="QubitRegister<2>",
        operands=("H", "jumps"),
        origin=origin,
    )

    assert channel.operation == "Lindblad"
    assert channel.input_domain == "QubitRegister<2>"
    assert channel.output_domain == "QubitRegister<2>"
    assert channel.operands == ("H", "jumps")
    assert channel.origin == origin


def test_measurement_intent_is_not_a_runtime_measurement() -> None:
    _, _, MeasurementIntent, _, SourceOrigin, _, _ = _load_api()

    origin = SourceOrigin(source_id="measurement.staqex", line=7, col=9)
    intent = MeasurementIntent(
        observable="energy(H)",
        povm="z_basis",
        domain="Qubit",
        outcome="SpinOutcome",
        mode="terminal",
        origin=origin,
    )

    assert intent.observable == "energy(H)"
    assert intent.povm == "z_basis"
    assert intent.domain == "Qubit"
    assert intent.outcome == "SpinOutcome"
    assert intent.mode == "terminal"
    assert not hasattr(intent, "measurement_result")


def test_initial_condition_and_symmetry_preserve_source_order_and_provenance() -> None:
    _, InitialCondition, _, _, SourceOrigin, SymmetryNode, _ = _load_api()

    initial_origin = SourceOrigin(source_id="ising.staqex", line=4, col=1)
    symmetry_origin = SourceOrigin(source_id="ising.staqex", line=9, col=1)
    initial = InitialCondition(
        target="psi",
        domain="QubitRegister<N>",
        preparation="GroundState",
        source_order=0,
        origin=initial_origin,
    )
    symmetry = SymmetryNode(
        law_kind="conservation",
        name="Parity",
        operands=("H", "ParityOperator"),
        domain="QubitRegister<N>",
        source_order=1,
        origin=symmetry_origin,
    )

    assert initial.source_order < symmetry.source_order
    assert initial.preparation == "GroundState"
    assert symmetry.law_kind == "conservation"
    assert symmetry.operands == ("H", "ParityOperator")
    assert initial.origin.source_id == symmetry.origin.source_id


def test_verifier_rejects_missing_channel_domain_or_physical_origin() -> None:
    _, _, _, PhysicsModule, _, _, verify_physics_ir = _load_api()

    module = PhysicsModule(
        spaces=(),
        nodes=(
            {"kind": "Channel", "input_domain": None},
            {"kind": "MeasurementIntent", "origin": None},
            {"kind": "Symmetry", "domain": None},
        ),
        origins=(),
    )
    diagnostics = verify_physics_ir(module)
    codes = {diagnostic.get("code") for diagnostic in diagnostics}

    assert "PHYSICS_IR_DOMAIN_ERROR" in codes
    assert "PHYSICS_IR_PROVENANCE_ERROR" in codes


if __name__ == "__main__":
    for test in (
        test_channel_node_preserves_domains_operation_operands_and_origin,
        test_measurement_intent_is_not_a_runtime_measurement,
        test_initial_condition_and_symmetry_preserve_source_order_and_provenance,
        test_verifier_rejects_missing_channel_domain_or_physical_origin,
    ):
        test()
    print("OK — LISS-0081 Slice C Phase 1 Red")
