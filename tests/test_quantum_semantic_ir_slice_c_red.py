"""AT-TDD Phase 1 Red: LISS-0082 Slice C transformation regions.

This suite fixes only the provider-neutral signatures and validity state of
Unitary, Isometry, and Channel regions.  It does not authorize execution,
matrix payloads, proof synthesis, measurement, control, lowering, or targets.
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
        ChannelRegion,
        DensityJointStateValue,
        IsometryRegion,
        PureJointStateValue,
        QuantumSemanticModule,
        RegionValidity,
        SemanticId,
        SemanticOrigin,
        UnitaryRegion,
        verify_quantum_semantic_ir,
    )

    return {
        "ActingFactor": ActingFactor,
        "ActingSpace": ActingSpace,
        "ChannelRegion": ChannelRegion,
        "DensityJointStateValue": DensityJointStateValue,
        "IsometryRegion": IsometryRegion,
        "PureJointStateValue": PureJointStateValue,
        "QuantumSemanticModule": QuantumSemanticModule,
        "RegionValidity": RegionValidity,
        "SemanticId": SemanticId,
        "SemanticOrigin": SemanticOrigin,
        "UnitaryRegion": UnitaryRegion,
        "verify": verify_quantum_semantic_ir,
    }


def _identity(api, kind: str, ordinal: int) -> object:
    return api["SemanticId"](kind=kind, scope="slice-c.module", ordinal=ordinal)


def _origin(api, transform: str = "test.slice_c.v1"):
    return api["SemanticOrigin"](
        source_id="slice-c.staqex",
        line=9,
        col=3,
        upstream_ids=("physics.module.0",),
        transform_id=transform,
    )


def _space(api, ordinal: int, dimensions: tuple[int, ...]):
    factors = tuple(
        api["ActingFactor"](
            factor_id=_identity(api, "resource", ordinal * 10 + index),
            dimension=dimension,
            label=f"f{index}",
        )
        for index, dimension in enumerate(dimensions)
    )
    total = 1
    for dimension in dimensions:
        total *= dimension
    return api["ActingSpace"](
        space_id=_identity(api, "acting_space", ordinal),
        factors=factors,
        total_dimension=total,
        origin=_origin(api),
    )


def _pure_value(api, space, ordinal: int):
    return api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", ordinal),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        producer_id=_identity(api, "producer", ordinal),
        origin=_origin(api),
    )


def _density_value(api, space, ordinal: int):
    return api["DensityJointStateValue"](
        value_id=_identity(api, "quantum_value", ordinal),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        producer_id=_identity(api, "producer", ordinal),
        origin=_origin(api),
    )


def _validity(api, kind: str, reference: str | None = None):
    return api["RegionValidity"](kind=kind, reference=reference)


def _module(api, *, spaces=(), values=(), regions=()):
    return api["QuantumSemanticModule"](
        schema_version=1,
        roots=(_identity(api, "module", 0),),
        region_roots=tuple(region.region_id for region in regions),
        origins=(_origin(api),),
        acting_spaces=tuple(spaces),
        values=tuple(values),
        regions=tuple(regions),
    )


def _codes(diagnostics) -> set[str]:
    return {diagnostic.get("code") for diagnostic in diagnostics}


def _region(api, region_type, *, ordinal, input_value, output_value,
            input_space, output_space, validity):
    return region_type(
        region_id=_identity(api, "region", ordinal),
        input_value_id=input_value.value_id,
        output_value_id=output_value.value_id,
        input_space_id=input_space.space_id,
        output_space_id=output_space.space_id,
        validity=validity,
        origin=_origin(api),
    )


def test_slice_c_api_is_importable() -> None:
    api = _load_api()
    for name in (
        "UnitaryRegion",
        "IsometryRegion",
        "ChannelRegion",
        "RegionValidity",
    ):
        assert api[name] is not None, f"Slice C must expose {name}"


def test_unitary_preserves_pure_carrier_and_acting_space() -> None:
    api = _load_api()
    space = _space(api, 0, (2, 2))
    input_value = _pure_value(api, space, 0)
    output_value = _pure_value(api, space, 1)
    region = _region(
        api,
        api["UnitaryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=space,
        output_space=space,
        validity=_validity(api, "Declared"),
    )

    diagnostics = api["verify"](
        _module(api, spaces=(space,), values=(input_value, output_value), regions=(region,))
    )

    assert "QSEM_REGION_SIGNATURE_INVALID" not in _codes(diagnostics)


def test_unitary_rejects_changed_acting_space_or_density_output() -> None:
    api = _load_api()
    input_space = _space(api, 0, (2,))
    output_space = _space(api, 1, (2, 2))
    input_value = _pure_value(api, input_space, 0)
    output_value = _density_value(api, output_space, 1)
    region = _region(
        api,
        api["UnitaryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=input_space,
        output_space=output_space,
        validity=_validity(api, "Declared"),
    )

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(input_space, output_space),
            values=(input_value, output_value),
            regions=(region,),
        )
    )

    assert "QSEM_REGION_SIGNATURE_INVALID" in _codes(diagnostics)


def test_isometry_requires_non_decreasing_finite_dimension() -> None:
    api = _load_api()
    input_space = _space(api, 0, (2, 2))
    output_space = _space(api, 1, (2,))
    input_value = _pure_value(api, input_space, 0)
    output_value = _pure_value(api, output_space, 1)
    region = _region(
        api,
        api["IsometryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=input_space,
        output_space=output_space,
        validity=_validity(api, "Required", "isometry-witness-0"),
    )

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(input_space, output_space),
            values=(input_value, output_value),
            regions=(region,),
        )
    )

    assert "QSEM_REGION_SIGNATURE_INVALID" in _codes(diagnostics)


def test_isometry_keeps_environment_obligation_explicit() -> None:
    api = _load_api()
    input_space = _space(api, 0, (2,))
    output_space = _space(api, 1, (2, 2))
    input_value = _pure_value(api, input_space, 0)
    output_value = _pure_value(api, output_space, 1)
    region = _region(
        api,
        api["IsometryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=input_space,
        output_space=output_space,
        validity=_validity(api, "Required", "ancilla-discharge-0"),
    )

    assert region.validity.kind == "Required"
    assert region.validity.reference == "ancilla-discharge-0"


def test_channel_accepts_pure_or_density_input_but_density_output() -> None:
    api = _load_api()
    space = _space(api, 0, (2,))
    pure_input = _pure_value(api, space, 0)
    density_input = _density_value(api, space, 1)
    density_output = _density_value(api, space, 2)

    for ordinal, input_value in enumerate((pure_input, density_input)):
        region = _region(
            api,
            api["ChannelRegion"],
            ordinal=ordinal,
            input_value=input_value,
            output_value=density_output,
            input_space=space,
            output_space=space,
            validity=_validity(api, "Verified", f"channel-witness-{ordinal}"),
        )
        diagnostics = api["verify"](
            _module(api, spaces=(space,), values=(input_value, density_output), regions=(region,))
        )
        assert "QSEM_REGION_SIGNATURE_INVALID" not in _codes(diagnostics)


def test_channel_rejects_pure_output_and_hidden_purification() -> None:
    api = _load_api()
    space = _space(api, 0, (2,))
    pure_input = _pure_value(api, space, 0)
    pure_output = _pure_value(api, space, 1)
    region = _region(
        api,
        api["ChannelRegion"],
        ordinal=0,
        input_value=pure_input,
        output_value=pure_output,
        input_space=space,
        output_space=space,
        validity=_validity(api, "Declared"),
    )

    diagnostics = api["verify"](
        _module(api, spaces=(space,), values=(pure_input, pure_output), regions=(region,))
    )

    assert "QSEM_REGION_SIGNATURE_INVALID" in _codes(diagnostics)


def test_validity_levels_remain_distinct() -> None:
    api = _load_api()
    declared = _validity(api, "Declared")
    verified = _validity(api, "Verified", "witness-0")
    required = _validity(api, "Required", "obligation-0")

    assert (declared.kind, declared.reference) == ("Declared", None)
    assert (verified.kind, verified.reference) == ("Verified", "witness-0")
    assert (required.kind, required.reference) == ("Required", "obligation-0")
    assert len({declared, verified, required}) == 3


def test_unverified_declaration_is_not_reported_as_verified() -> None:
    api = _load_api()
    space = _space(api, 0, (2,))
    input_value = _pure_value(api, space, 0)
    output_value = _pure_value(api, space, 1)
    region = _region(
        api,
        api["UnitaryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=space,
        output_space=space,
        validity=_validity(api, "Declared"),
    )

    diagnostics = api["verify"](
        _module(api, spaces=(space,), values=(input_value, output_value), regions=(region,))
    )

    assert all(diagnostic.get("validity") != "Verified" for diagnostic in diagnostics)


def test_region_definitions_participate_in_identity_and_provenance_checks() -> None:
    api = _load_api()
    space = _space(api, 0, (2,))
    input_value = _pure_value(api, space, 0)
    output_value = _pure_value(api, space, 1)
    first = _region(
        api,
        api["UnitaryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=space,
        output_space=space,
        validity=_validity(api, "Declared"),
    )
    duplicate = _region(
        api,
        api["UnitaryRegion"],
        ordinal=0,
        input_value=input_value,
        output_value=output_value,
        input_space=space,
        output_space=space,
        validity=_validity(api, "Declared"),
    )

    diagnostics = api["verify"](
        _module(api, spaces=(space,), values=(input_value, output_value), regions=(first, duplicate))
    )

    assert "QSEM_IDENTITY_CONFLICT" in _codes(diagnostics)


if __name__ == "__main__":
    tests = (
        test_slice_c_api_is_importable,
        test_unitary_preserves_pure_carrier_and_acting_space,
        test_unitary_rejects_changed_acting_space_or_density_output,
        test_isometry_requires_non_decreasing_finite_dimension,
        test_isometry_keeps_environment_obligation_explicit,
        test_channel_accepts_pure_or_density_input_but_density_output,
        test_channel_rejects_pure_output_and_hidden_purification,
        test_validity_levels_remain_distinct,
        test_unverified_declaration_is_not_reported_as_verified,
        test_region_definitions_participate_in_identity_and_provenance_checks,
    )

    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:  # Red may be an intentionally missing API.
            failures += 1
            print(f"FAIL {test.__name__}: {error}")
        else:
            print(f"pass {test.__name__}")

    print(f"\n{len(tests) - failures} passed, {failures} failed")
    sys.exit(1 if failures else 0)
