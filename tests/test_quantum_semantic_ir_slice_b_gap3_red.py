"""AT-TDD Phase 1 Red: LISS-0082 Slice B gap 3.

A quantum value identity is one immutable whole-Joint-state generation.
Pure and density carriers therefore expose neither a separate `generation`
constructor keyword nor a `.generation` attribute.

This phase changes tests only. Region ordering, lineage, lowering, pipeline,
and provider behavior remain out of scope.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.quantum_semantic_ir import (
        ActingFactor,
        ActingSpace,
        DensityJointStateValue,
        PureJointStateValue,
        SemanticId,
        SemanticOrigin,
    )

    return {
        "ActingFactor": ActingFactor,
        "ActingSpace": ActingSpace,
        "DensityJointStateValue": DensityJointStateValue,
        "PureJointStateValue": PureJointStateValue,
        "SemanticId": SemanticId,
        "SemanticOrigin": SemanticOrigin,
    }


def _identity(api, kind: str, ordinal: int):
    return api["SemanticId"](kind=kind, scope="module.main", ordinal=ordinal)


def _origin(api):
    return api["SemanticOrigin"](
        source_id="slice-b-gap3.staqex",
        line=5,
        col=3,
        upstream_ids=("physics.module.0",),
        transform_id="test.slice_b_gap3.v1",
    )


def _carrier_kwargs(api):
    factor = api["ActingFactor"](
        factor_id=_identity(api, "resource", 0),
        dimension=2,
        label="q0",
    )
    space = api["ActingSpace"](
        space_id=_identity(api, "acting_space", 0),
        factors=(factor,),
        total_dimension=2,
        origin=_origin(api),
    )
    return {
        "value_id": _identity(api, "quantum_value", 0),
        "space_id": space.space_id,
        "resources": (factor.factor_id,),
        "producer_id": _identity(api, "producer", 0),
        "origin": _origin(api),
    }


def _construct_without_generation(api, carrier_name: str):
    try:
        return api[carrier_name](**_carrier_kwargs(api))
    except TypeError as error:
        assert False, (
            f"{carrier_name} must not require a separate generation field: {error}"
        )


def _assert_generation_keyword_is_rejected(api, carrier_name: str) -> None:
    try:
        api[carrier_name](generation=0, **_carrier_kwargs(api))
        accepted = True
    except TypeError:
        accepted = False

    assert accepted is False, (
        f"{carrier_name} must reject the redundant generation keyword"
    )


def test_pure_carrier_has_no_generation_attribute() -> None:
    api = _load_api()
    value = _construct_without_generation(api, "PureJointStateValue")

    assert not hasattr(value, "generation"), (
        "PureJointStateValue identity is the generation; no attribute is stored"
    )


def test_density_carrier_has_no_generation_attribute() -> None:
    api = _load_api()
    value = _construct_without_generation(api, "DensityJointStateValue")

    assert not hasattr(value, "generation"), (
        "DensityJointStateValue identity is the generation; no attribute is stored"
    )


def test_pure_carrier_rejects_generation_keyword() -> None:
    _assert_generation_keyword_is_rejected(_load_api(), "PureJointStateValue")


def test_density_carrier_rejects_generation_keyword() -> None:
    _assert_generation_keyword_is_rejected(_load_api(), "DensityJointStateValue")


if __name__ == "__main__":
    tests = (
        test_pure_carrier_has_no_generation_attribute,
        test_density_carrier_has_no_generation_attribute,
        test_pure_carrier_rejects_generation_keyword,
        test_density_carrier_rejects_generation_keyword,
    )

    failures = 0
    for test in tests:
        try:
            test()
        except AssertionError as error:
            failures += 1
            print(f"FAIL {test.__name__}: {error}")
        else:
            print(f"pass {test.__name__}")

    print(f"\n{len(tests) - failures} passed, {failures} failed")
    sys.exit(1 if failures else 0)
