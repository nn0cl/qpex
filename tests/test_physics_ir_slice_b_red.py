"""AT-TDD Phase 1 Red: LISS-0081 Slice B — binders and statistics."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice B Green must extend the focused Physics IR API."""
    from compiler.staqex.physics_ir import (
        BinderNode,
        OperatorAtom,
        PhysicsModule,
        SourceOrigin,
        Statistics,
        verify_physics_ir,
    )

    return (
        BinderNode,
        OperatorAtom,
        PhysicsModule,
        SourceOrigin,
        Statistics,
        verify_physics_ir,
    )


def test_binder_node_preserves_domain_constraints_body_and_origin() -> None:
    BinderNode, _, _, SourceOrigin, _, _ = _load_api()

    origin = SourceOrigin(source_id="ising.staqex", line=6, col=5)
    binder = BinderNode(
        kind="sum",
        variables=("i",),
        domain="Index<0..N-1>",
        constraints=("i < N",),
        body={"kind": "OperatorProduct", "operands": ("Z[i]", "Z[next(i)]")},
        origin=origin,
    )

    assert binder.kind == "sum"
    assert binder.variables == ("i",)
    assert binder.domain == "Index<0..N-1>"
    assert binder.constraints == ("i < N",)
    assert binder.body["kind"] == "OperatorProduct"
    assert binder.origin == origin


def test_nested_binders_preserve_nesting_and_source_order_without_expansion() -> None:
    BinderNode, _, _, SourceOrigin, _, _ = _load_api()

    outer_origin = SourceOrigin(source_id="hubbard.staqex", line=3, col=1)
    inner_origin = SourceOrigin(source_id="hubbard.staqex", line=4, col=5)
    inner = BinderNode(
        kind="sum",
        variables=("orbital",),
        domain="Orbitals",
        constraints=(),
        body={"kind": "FermionAtom", "symbol": "create"},
        origin=inner_origin,
    )
    outer = BinderNode(
        kind="sum",
        variables=("site",),
        domain="Sites",
        constraints=(),
        body=inner,
        origin=outer_origin,
    )

    assert outer.body is inner
    assert outer.origin.line < inner.origin.line
    assert not hasattr(outer, "expanded_terms")


def test_operator_atom_retains_statistics_and_source_order() -> None:
    _, OperatorAtom, _, SourceOrigin, Statistics, _ = _load_api()

    origin = SourceOrigin(source_id="fermion.staqex", line=8, col=20)
    statistics = Statistics(family="fermionic", policy="anticommuting")
    atoms = (
        OperatorAtom(symbol="create", index=1, source_order=0, origin=origin),
        OperatorAtom(symbol="annihilate", index=0, source_order=1, origin=origin),
    )

    assert statistics.family == "fermionic"
    assert statistics.policy == "anticommuting"
    assert [atom.index for atom in atoms] == [1, 0]
    assert [atom.source_order for atom in atoms] == [0, 1]
    assert all(atom.origin == origin for atom in atoms)


def test_verifier_rejects_missing_binder_domain_or_statistics_reference() -> None:
    _, _, PhysicsModule, _, _, verify_physics_ir = _load_api()

    module = PhysicsModule(
        spaces=(),
        nodes=(
            {"kind": "Binder", "domain": None},
            {"kind": "Operator", "statistics": None},
        ),
        origins=(),
    )
    diagnostics = verify_physics_ir(module)
    codes = {diagnostic.get("code") for diagnostic in diagnostics}

    assert "PHYSICS_IR_DOMAIN_ERROR" in codes
    assert "PHYSICS_IR_STATISTICS_ERROR" in codes


if __name__ == "__main__":
    for test in (
        test_binder_node_preserves_domain_constraints_body_and_origin,
        test_nested_binders_preserve_nesting_and_source_order_without_expansion,
        test_operator_atom_retains_statistics_and_source_order,
        test_verifier_rejects_missing_binder_domain_or_statistics_reference,
    ):
        test()
    print("OK — LISS-0081 Slice B Phase 1 Red")
