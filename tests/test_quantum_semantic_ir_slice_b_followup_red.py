"""AT-TDD Phase 1 Red: LISS-0082 Slice B follow-up 1 (gaps 1, 2, 5).

The Adjudicator re-review of 2026-07-30 left five Slice B contract laws
unverified. This suite covers the three that need no new vocabulary:

- gap 1: duplicate **definition** identities among acting spaces, factors, and
  Joint values, reported as `QSEM_IDENTITY_CONFLICT`. An identity appearing as a
  reference is not a definition and must never be counted as a duplicate.
- gap 2: `SemanticOrigin` embedded in an `ActingSpace` or a Joint value,
  reported as `QSEM_PROVENANCE_INCOMPLETE`.
- gap 5: `value.resources` must match the acting-space factor identities
  exactly and in order, reported as `QSEM_ACTING_SPACE_INVALID`.

Gaps 1 and 2 extend Slice A's identity and provenance diagnostics to Slice B
definition sites. Gap 5 uses the Slice B shape code `QSEM_ACTING_SPACE_INVALID`,
strengthening its resource check from arity to ordered identity.

Gap 3 separately removes the redundant integer field while preserving the
whole-Joint-state generation semantics fixed here. Gap 4 adds no ordering
field; cycle detection is delegated to the Slice C region graph. Region kinds,
measurement, control lanes, lowering, pipeline, and provider work remain
unauthorized.
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
        "JointValueUse": JointValueUse,
        "PureJointStateValue": PureJointStateValue,
        "QuantumSemanticModule": QuantumSemanticModule,
        "SemanticId": SemanticId,
        "SemanticOrigin": SemanticOrigin,
        "verify": verify_quantum_semantic_ir,
    }


def _identity(api, kind: str, ordinal: int):
    return api["SemanticId"](kind=kind, scope="module.main", ordinal=ordinal)


def _origin(api):
    """A complete origin, so no provenance diagnostic comes from the root."""
    return api["SemanticOrigin"](
        source_id="slice-b-followup.staqex",
        line=11,
        col=5,
        upstream_ids=("physics.module.0",),
        transform_id="test.slice_b_followup.v1",
    )


def _space(api, *, space_id, factor_ordinals=(0, 1), dimensions=(2, 2), origin=None):
    factors = tuple(
        api["ActingFactor"](
            factor_id=_identity(api, "resource", ordinal),
            dimension=dimension,
            label=f"q{ordinal}",
        )
        for ordinal, dimension in zip(factor_ordinals, dimensions)
    )
    total = 1
    for dimension in dimensions:
        total *= dimension
    return api["ActingSpace"](
        space_id=space_id,
        factors=factors,
        total_dimension=total,
        origin=origin if origin is not None else _origin(api),
    )


def _value(api, space, *, value_id, resources=None, origin=None):
    return api["PureJointStateValue"](
        value_id=value_id,
        space_id=space.space_id,
        resources=(
            resources
            if resources is not None
            else tuple(factor.factor_id for factor in space.factors)
        ),
        producer_id=_identity(api, "producer", 0),
        origin=origin if origin is not None else _origin(api),
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


# --- Gap 1: duplicate definition identities -------------------------------


def test_duplicate_acting_space_definitions_conflict() -> None:
    api = _load_api()
    shared = _identity(api, "acting_space", 0)
    first = _space(api, space_id=shared, factor_ordinals=(0,), dimensions=(2,))
    second = _space(api, space_id=shared, factor_ordinals=(1,), dimensions=(2,))

    codes = _codes(api["verify"](_module(api, acting_spaces=(first, second))))

    assert "QSEM_IDENTITY_CONFLICT" in codes


def test_duplicate_factor_definitions_conflict_within_and_across_spaces() -> None:
    api = _load_api()

    within = _space(
        api,
        space_id=_identity(api, "acting_space", 0),
        factor_ordinals=(0, 0),
        dimensions=(2, 2),
    )
    codes_within = _codes(api["verify"](_module(api, acting_spaces=(within,))))
    assert "QSEM_IDENTITY_CONFLICT" in codes_within, (
        "a factor identity must be defined once inside a space"
    )

    first = _space(
        api,
        space_id=_identity(api, "acting_space", 0),
        factor_ordinals=(0,),
        dimensions=(2,),
    )
    second = _space(
        api,
        space_id=_identity(api, "acting_space", 1),
        factor_ordinals=(0,),
        dimensions=(2,),
    )
    codes_across = _codes(api["verify"](_module(api, acting_spaces=(first, second))))
    assert "QSEM_IDENTITY_CONFLICT" in codes_across, (
        "a factor identity must not be defined by two spaces"
    )


def test_duplicate_joint_value_definitions_conflict() -> None:
    api = _load_api()
    space = _space(api, space_id=_identity(api, "acting_space", 0))
    shared = _identity(api, "quantum_value", 0)
    first = _value(api, space, value_id=shared)
    second = _value(api, space, value_id=shared)

    codes = _codes(
        api["verify"](_module(api, acting_spaces=(space,), values=(first, second)))
    )

    assert "QSEM_IDENTITY_CONFLICT" in codes


def test_definition_conflict_is_detected_across_categories() -> None:
    """One identity may be defined by exactly one object, whatever its kind."""
    api = _load_api()
    shared = _identity(api, "entity", 0)
    space = _space(api, space_id=shared)
    value = _value(api, space, value_id=shared)

    codes = _codes(
        api["verify"](_module(api, acting_spaces=(space,), values=(value,)))
    )

    assert "QSEM_IDENTITY_CONFLICT" in codes


def test_referenced_identities_are_not_counted_as_duplicate_definitions() -> None:
    """`space_id`, `resources`, `producer_id`, and use targets are references."""
    api = _load_api()
    space = _space(api, space_id=_identity(api, "acting_space", 0))
    value = _value(api, space, value_id=_identity(api, "quantum_value", 0))
    use = api["JointValueUse"](
        value_id=value.value_id,
        consumer_id=_identity(api, "consumer", 0),
        factor_id=None,
    )

    diagnostics = api["verify"](
        _module(api, acting_spaces=(space,), values=(value,), value_uses=(use,))
    )

    assert diagnostics == [], (
        f"references must not be reported as redefinitions: {diagnostics}"
    )


# --- Gap 2: provenance embedded in Slice B definitions --------------------


def test_incomplete_acting_space_origin_is_reported() -> None:
    api = _load_api()
    space = _space(
        api,
        space_id=_identity(api, "acting_space", 0),
        origin=api["SemanticOrigin"](
            source_id="slice-b-followup.staqex",
            line=11,
            col=5,
            upstream_ids=(),
            transform_id="",
        ),
    )

    codes = _codes(api["verify"](_module(api, acting_spaces=(space,))))

    assert "QSEM_PROVENANCE_INCOMPLETE" in codes


def test_incomplete_joint_value_origin_is_reported() -> None:
    api = _load_api()
    space = _space(api, space_id=_identity(api, "acting_space", 0))
    value = _value(
        api,
        space,
        value_id=_identity(api, "quantum_value", 0),
        origin=api["SemanticOrigin"](
            source_id="",
            line=0,
            col=0,
            upstream_ids=(),
            transform_id="test.slice_b_followup.v1",
        ),
    )

    codes = _codes(
        api["verify"](_module(api, acting_spaces=(space,), values=(value,)))
    )

    assert "QSEM_PROVENANCE_INCOMPLETE" in codes


# --- Gap 5: resource identities must match the factor order ---------------


def test_resources_out_of_factor_order_are_reported() -> None:
    api = _load_api()
    space = _space(
        api,
        space_id=_identity(api, "acting_space", 0),
        factor_ordinals=(0, 1),
        dimensions=(2, 3),
    )
    reversed_resources = tuple(reversed([f.factor_id for f in space.factors]))
    value = _value(
        api,
        space,
        value_id=_identity(api, "quantum_value", 0),
        resources=reversed_resources,
    )

    codes = _codes(
        api["verify"](_module(api, acting_spaces=(space,), values=(value,)))
    )

    assert "QSEM_ACTING_SPACE_INVALID" in codes, (
        "resource order must follow the ordered tensor factors"
    )


def test_resources_naming_unknown_factors_are_reported() -> None:
    api = _load_api()
    space = _space(api, space_id=_identity(api, "acting_space", 0))
    value = _value(
        api,
        space,
        value_id=_identity(api, "quantum_value", 0),
        resources=(
            _identity(api, "resource", 90),
            _identity(api, "resource", 91),
        ),
    )

    codes = _codes(
        api["verify"](_module(api, acting_spaces=(space,), values=(value,)))
    )

    assert "QSEM_ACTING_SPACE_INVALID" in codes, (
        "resources must name the factors of their own acting space"
    )


def test_resources_in_factor_order_are_accepted() -> None:
    api = _load_api()
    space = _space(
        api,
        space_id=_identity(api, "acting_space", 0),
        factor_ordinals=(0, 1),
        dimensions=(2, 3),
    )
    value = _value(api, space, value_id=_identity(api, "quantum_value", 0))

    diagnostics = api["verify"](
        _module(api, acting_spaces=(space,), values=(value,))
    )

    assert diagnostics == [], f"exact factor order must verify: {diagnostics}"


if __name__ == "__main__":
    tests = (
        test_duplicate_acting_space_definitions_conflict,
        test_duplicate_factor_definitions_conflict_within_and_across_spaces,
        test_duplicate_joint_value_definitions_conflict,
        test_definition_conflict_is_detected_across_categories,
        test_referenced_identities_are_not_counted_as_duplicate_definitions,
        test_incomplete_acting_space_origin_is_reported,
        test_incomplete_joint_value_origin_is_reported,
        test_resources_out_of_factor_order_are_reported,
        test_resources_naming_unknown_factors_are_reported,
        test_resources_in_factor_order_are_accepted,
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
