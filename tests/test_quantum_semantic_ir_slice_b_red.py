"""AT-TDD Phase 1 Red: LISS-0082 Slice B — acting spaces and Joint state values.

Slice B fixes only the finite acting-space contract, the pure/density
whole-Joint-state carriers, and the generation-based one-producer /
one-consuming-path verifier laws.

It deliberately does NOT authorize region kinds (Slice C), control or
measurement lanes (Slice D), Physics lowering (Slice E), pipeline wiring
(Slice F), amplitudes, density matrices, encodings, or qubit allocation.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice B Green must provide this narrow additive API."""
    from compiler.staqex.quantum_semantic_ir import (
        ActingFactor,
        ActingSpace,
        DensityJointStateValue,
        JointValueUse,
        PureJointStateValue,
        QuantumSemanticModule,
        SemanticId,
        SemanticOrigin,
        verify_quantum_semantic_ir,
    )

    return {
        "ActingFactor": ActingFactor,
        "ActingSpace": ActingSpace,
        "DensityJointStateValue": DensityJointStateValue,
        "JointValueUse": JointValueUse,
        "PureJointStateValue": PureJointStateValue,
        "QuantumSemanticModule": QuantumSemanticModule,
        "SemanticId": SemanticId,
        "SemanticOrigin": SemanticOrigin,
        "verify": verify_quantum_semantic_ir,
    }


def _origin(api, transform: str = "test.slice_b.v1"):
    return api["SemanticOrigin"](
        source_id="slice-b.staqex",
        line=7,
        col=3,
        upstream_ids=("physics.module.0",),
        transform_id=transform,
    )


def _identity(api, kind: str, ordinal: int):
    return api["SemanticId"](kind=kind, scope="module.main", ordinal=ordinal)


def _two_qubit_space(api):
    """An ordered finite space of two dimension-2 factors."""
    return api["ActingSpace"](
        space_id=_identity(api, "acting_space", 0),
        factors=(
            api["ActingFactor"](
                factor_id=_identity(api, "resource", 0), dimension=2, label="q0"
            ),
            api["ActingFactor"](
                factor_id=_identity(api, "resource", 1), dimension=2, label="q1"
            ),
        ),
        total_dimension=4,
        origin=_origin(api),
    )


def _pure_value(api, space, generation: int = 0, producer_ordinal: int = 0):
    return api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", generation),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        generation=generation,
        producer_id=_identity(api, "producer", producer_ordinal),
        origin=_origin(api),
    )


def _module(api, *, acting_spaces=(), values=(), value_uses=()):
    return api["QuantumSemanticModule"](
        schema_version=1,
        roots=(_identity(api, "module", 0),),
        region_roots=(),
        origins=(_origin(api),),
        acting_spaces=acting_spaces,
        values=values,
        value_uses=value_uses,
    )


def _codes(diagnostics) -> set[str]:
    return {diagnostic.get("code") for diagnostic in diagnostics}


# --- Acceptance scenario 1: ordered finite acting space -------------------


def test_slice_b_api_is_importable() -> None:
    api = _load_api()

    for name in (
        "ActingFactor",
        "ActingSpace",
        "PureJointStateValue",
        "DensityJointStateValue",
        "JointValueUse",
    ):
        assert api[name] is not None, f"Slice B must expose {name}"


def test_acting_space_is_ordered_finite_and_immutable() -> None:
    api = _load_api()
    space = _two_qubit_space(api)

    assert isinstance(space.factors, tuple), "factor order must be canonical"
    assert [factor.dimension for factor in space.factors] == [2, 2]
    assert space.total_dimension == 4

    try:
        space.total_dimension = 8  # type: ignore[misc]
        mutated = True
    except (AttributeError, TypeError):
        mutated = False
    assert mutated is False, "ActingSpace must be immutable"

    assert "0x" not in repr(space), "identity must not depend on object address"
    assert "provider" not in repr(space).lower()


def test_verifier_rejects_non_positive_and_inconsistent_dimensions() -> None:
    api = _load_api()
    origin = _origin(api)

    zero_dimension = api["ActingSpace"](
        space_id=_identity(api, "acting_space", 0),
        factors=(
            api["ActingFactor"](
                factor_id=_identity(api, "resource", 0), dimension=0, label="bad"
            ),
        ),
        total_dimension=0,
        origin=origin,
    )
    inconsistent_total = api["ActingSpace"](
        space_id=_identity(api, "acting_space", 1),
        factors=(
            api["ActingFactor"](
                factor_id=_identity(api, "resource", 1), dimension=2, label="q0"
            ),
            api["ActingFactor"](
                factor_id=_identity(api, "resource", 2), dimension=3, label="q1"
            ),
        ),
        total_dimension=5,
        origin=origin,
    )
    empty_space = api["ActingSpace"](
        space_id=_identity(api, "acting_space", 2),
        factors=(),
        total_dimension=1,
        origin=origin,
    )

    for space in (zero_dimension, inconsistent_total, empty_space):
        diagnostics = api["verify"](_module(api, acting_spaces=(space,)))
        assert "QSEM_ACTING_SPACE_INVALID" in _codes(diagnostics), (
            f"space {space.space_id.ordinal} must be rejected"
        )


# --- Acceptance scenario 2: whole-Joint-state carriers --------------------


def test_joint_values_declare_purity_explicitly() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    pure = _pure_value(api, space)
    density = api["DensityJointStateValue"](
        value_id=_identity(api, "quantum_value", 1),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        generation=1,
        producer_id=_identity(api, "producer", 1),
        origin=_origin(api),
    )

    assert pure.is_pure is True
    assert density.is_pure is False
    assert type(pure) is not type(density), "purity must be a carrier category"


def test_joint_values_carry_no_amplitudes_or_matrices() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    common = {
        "value_id": _identity(api, "quantum_value", 0),
        "space_id": space.space_id,
        "resources": tuple(factor.factor_id for factor in space.factors),
        "generation": 0,
        "producer_id": _identity(api, "producer", 0),
        "origin": _origin(api),
    }

    try:
        api["PureJointStateValue"](amplitudes=(1.0, 0.0, 0.0, 0.0), **common)
        accepted_amplitudes = True
    except TypeError:
        accepted_amplitudes = False
    assert accepted_amplitudes is False, "Semantic IR must carry no amplitudes"

    try:
        api["DensityJointStateValue"](density_matrix=((1.0,),), **common)
        accepted_matrix = True
    except TypeError:
        accepted_matrix = False
    assert accepted_matrix is False, "Semantic IR must carry no density matrix"


def test_verifier_rejects_unknown_space_and_resource_arity_mismatch() -> None:
    api = _load_api()
    space = _two_qubit_space(api)

    dangling = api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", 0),
        space_id=_identity(api, "acting_space", 99),
        resources=(_identity(api, "resource", 0),),
        generation=0,
        producer_id=_identity(api, "producer", 0),
        origin=_origin(api),
    )
    arity_mismatch = api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", 1),
        space_id=space.space_id,
        resources=(_identity(api, "resource", 0),),
        generation=1,
        producer_id=_identity(api, "producer", 1),
        origin=_origin(api),
    )

    for value in (dangling, arity_mismatch):
        diagnostics = api["verify"](
            _module(api, acting_spaces=(space,), values=(value,))
        )
        assert "QSEM_ACTING_SPACE_INVALID" in _codes(diagnostics), (
            f"value {value.value_id.ordinal} must be rejected"
        )


# --- Acceptance scenario 2: one producer, one consuming path --------------


def test_verifier_accepts_single_producer_and_single_consumer() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    value = _pure_value(api, space)
    use = api["JointValueUse"](
        value_id=value.value_id,
        consumer_id=_identity(api, "consumer", 0),
        factor_id=None,
    )

    diagnostics = api["verify"](
        _module(api, acting_spaces=(space,), values=(value,), value_uses=(use,))
    )

    assert diagnostics == [], f"well-formed Slice B module must verify: {diagnostics}"


def test_verifier_rejects_missing_producer() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    orphan = api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", 0),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        generation=0,
        producer_id=None,
        origin=_origin(api),
    )

    diagnostics = api["verify"](
        _module(api, acting_spaces=(space,), values=(orphan,))
    )

    assert "QSEM_VALUE_USE_INVALID" in _codes(diagnostics)


def test_verifier_rejects_fan_out_of_one_generation() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    value = _pure_value(api, space)
    uses = (
        api["JointValueUse"](
            value_id=value.value_id,
            consumer_id=_identity(api, "consumer", 0),
            factor_id=None,
        ),
        api["JointValueUse"](
            value_id=value.value_id,
            consumer_id=_identity(api, "consumer", 1),
            factor_id=None,
        ),
    )

    diagnostics = api["verify"](
        _module(api, acting_spaces=(space,), values=(value,), value_uses=uses)
    )

    assert "QSEM_VALUE_USE_INVALID" in _codes(diagnostics), (
        "a Joint generation must have at most one consuming path"
    )


def test_verifier_rejects_use_of_unknown_value() -> None:
    api = _load_api()
    space = _two_qubit_space(api)
    value = _pure_value(api, space)
    dangling_use = api["JointValueUse"](
        value_id=_identity(api, "quantum_value", 99),
        consumer_id=_identity(api, "consumer", 0),
        factor_id=None,
    )

    diagnostics = api["verify"](
        _module(
            api,
            acting_spaces=(space,),
            values=(value,),
            value_uses=(dangling_use,),
        )
    )

    assert "QSEM_VALUE_USE_INVALID" in _codes(diagnostics)


def test_verifier_rejects_independent_factor_use() -> None:
    """Factor IDs are coordinates inside one Joint value, not separable states."""
    api = _load_api()
    space = _two_qubit_space(api)
    value = _pure_value(api, space)
    factor_use = api["JointValueUse"](
        value_id=value.value_id,
        consumer_id=_identity(api, "consumer", 0),
        factor_id=space.factors[0].factor_id,
    )

    diagnostics = api["verify"](
        _module(
            api,
            acting_spaces=(space,),
            values=(value,),
            value_uses=(factor_use,),
        )
    )

    assert "QSEM_VALUE_USE_INVALID" in _codes(diagnostics), (
        "a factor must not be consumed as an independent state value"
    )


# --- Slice A root contract must survive the additive extension ------------


def test_slice_a_root_diagnostics_are_unchanged() -> None:
    api = _load_api()
    module = api["QuantumSemanticModule"](
        schema_version=999,
        roots=(_identity(api, "module", 0), _identity(api, "module", 0)),
        region_roots=(),
        origins=(_origin(api),),
    )

    codes = _codes(api["verify"](module))

    assert "QSEM_IDENTITY_CONFLICT" in codes
    assert "QSEM_SCHEMA_VERSION_UNSUPPORTED" in codes


if __name__ == "__main__":
    for test in (
        test_slice_b_api_is_importable,
        test_acting_space_is_ordered_finite_and_immutable,
        test_verifier_rejects_non_positive_and_inconsistent_dimensions,
        test_joint_values_declare_purity_explicitly,
        test_joint_values_carry_no_amplitudes_or_matrices,
        test_verifier_rejects_unknown_space_and_resource_arity_mismatch,
        test_verifier_accepts_single_producer_and_single_consumer,
        test_verifier_rejects_missing_producer,
        test_verifier_rejects_fan_out_of_one_generation,
        test_verifier_rejects_use_of_unknown_value,
        test_verifier_rejects_independent_factor_use,
        test_slice_a_root_diagnostics_are_unchanged,
    ):
        test()
    print("OK — LISS-0082 Slice B Phase 1 Red")
