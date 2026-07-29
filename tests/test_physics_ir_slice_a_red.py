"""AT-TDD Phase 1 Red: LISS-0081 Slice A — immutable Physics IR boundary."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice A Green must provide the focused Physics IR API."""
    from compiler.staqex.physics_ir import (
        HilbertSpace,
        PhysicsModule,
        SourceOrigin,
        verify_physics_ir,
    )

    return HilbertSpace, PhysicsModule, SourceOrigin, verify_physics_ir


def test_physics_ir_dtos_are_importable() -> None:
    HilbertSpace, PhysicsModule, SourceOrigin, verify_physics_ir = _load_api()

    assert HilbertSpace is not None
    assert PhysicsModule is not None
    assert SourceOrigin is not None
    assert callable(verify_physics_ir)


def test_physics_module_is_immutable_and_has_source_provenance() -> None:
    HilbertSpace, PhysicsModule, SourceOrigin, _ = _load_api()

    origin = SourceOrigin(source_id="ising.staqex", line=4, col=9)
    space = HilbertSpace(name="QubitRegister<4>", factors=(), origin=origin)
    module = PhysicsModule(spaces=(space,), nodes=(), origins=(origin,))

    assert module.spaces[0].name == "QubitRegister<4>"
    assert module.spaces[0].origin == origin
    try:
        module.spaces = ()  # type: ignore[misc]
        mutated = True
    except (AttributeError, TypeError):
        mutated = False
    assert mutated is False, "Physics IR root must be immutable"


def test_physics_ir_verifier_rejects_node_without_source_ancestry() -> None:
    _, PhysicsModule, _, verify_physics_ir = _load_api()

    module = PhysicsModule(spaces=(), nodes=(), origins=())
    diagnostics = verify_physics_ir(module)

    assert any(
        diagnostic.get("code") == "PHYSICS_IR_PROVENANCE_ERROR"
        for diagnostic in diagnostics
    )


def test_physics_ir_does_not_require_gate_expansion_or_provider_objects() -> None:
    _, PhysicsModule, SourceOrigin, verify_physics_ir = _load_api()

    origin = SourceOrigin(source_id="formula.staqex", line=1, col=1)
    module = PhysicsModule(
        spaces=(),
        nodes=(
            {
                "kind": "Operator",
                "family": "PauliProduct",
                "operands": ("X[0]", "X[1]"),
                "origin": origin,
            },
        ),
        origins=(origin,),
    )

    assert verify_physics_ir(module) == []
    assert "gate" not in repr(module).lower()
    assert "provider" not in repr(module).lower()


if __name__ == "__main__":
    for test in (
        test_physics_ir_dtos_are_importable,
        test_physics_module_is_immutable_and_has_source_provenance,
        test_physics_ir_verifier_rejects_node_without_source_ancestry,
        test_physics_ir_does_not_require_gate_expansion_or_provider_objects,
    ):
        test()
    print("OK — LISS-0081 Slice A Phase 1 Red")
