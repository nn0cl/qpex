"""AT-TDD Phase 1 Red: LISS-0082 Slice D semantic lanes and obligations.

Slice D separates coherent control, terminal Static measurement, and Dynamic
feedback structurally. It also fixes parameter shape independence and explicit
ancilla/uncompute obligations. Execution, sampling, lowering, and providers
remain outside this suite.
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
        AncillaDischarge,
        AncillaScope,
        CoherentControlRegion,
        DynamicControlRegion,
        DynamicMeasurementRegion,
        OutcomeIntent,
        ParameterSymbol,
        PureJointStateValue,
        QuantumSemanticModule,
        RegionValidity,
        SemanticId,
        SemanticLane,
        SemanticOrigin,
        TerminalMeasurementRegion,
        UncomputeObligation,
        UnitaryRegion,
        verify_quantum_semantic_ir,
    )

    return {
        "ActingFactor": ActingFactor,
        "ActingSpace": ActingSpace,
        "AncillaDischarge": AncillaDischarge,
        "AncillaScope": AncillaScope,
        "CoherentControlRegion": CoherentControlRegion,
        "DynamicControlRegion": DynamicControlRegion,
        "DynamicMeasurementRegion": DynamicMeasurementRegion,
        "OutcomeIntent": OutcomeIntent,
        "ParameterSymbol": ParameterSymbol,
        "PureJointStateValue": PureJointStateValue,
        "QuantumSemanticModule": QuantumSemanticModule,
        "RegionValidity": RegionValidity,
        "SemanticId": SemanticId,
        "SemanticLane": SemanticLane,
        "SemanticOrigin": SemanticOrigin,
        "TerminalMeasurementRegion": TerminalMeasurementRegion,
        "UncomputeObligation": UncomputeObligation,
        "UnitaryRegion": UnitaryRegion,
        "verify": verify_quantum_semantic_ir,
    }


def _identity(api, kind: str, ordinal: int):
    return api["SemanticId"](kind=kind, scope="slice-d.module", ordinal=ordinal)


def _origin(api, *, complete: bool = True):
    return api["SemanticOrigin"](
        source_id="slice-d.staqex" if complete else "",
        line=11 if complete else 0,
        col=5 if complete else 0,
        upstream_ids=("semantic.region.0",),
        transform_id="test.slice_d.v1" if complete else "",
    )


def _space(api):
    factors = (
        api["ActingFactor"](
            factor_id=_identity(api, "resource", 0), dimension=2, label="control"
        ),
        api["ActingFactor"](
            factor_id=_identity(api, "resource", 1), dimension=2, label="target"
        ),
        api["ActingFactor"](
            factor_id=_identity(api, "resource", 2), dimension=2, label="ancilla"
        ),
    )
    return api["ActingSpace"](
        space_id=_identity(api, "acting_space", 0),
        factors=factors,
        total_dimension=8,
        origin=_origin(api),
    )


def _value(api, space, ordinal: int, producer_ordinal: int | None = None):
    producer = ordinal if producer_ordinal is None else producer_ordinal
    return api["PureJointStateValue"](
        value_id=_identity(api, "quantum_value", ordinal),
        space_id=space.space_id,
        resources=tuple(factor.factor_id for factor in space.factors),
        producer_id=_identity(api, "region", producer),
        origin=_origin(api),
    )


def _unitary(api, space, input_value, output_value, ordinal: int):
    return api["UnitaryRegion"](
        region_id=_identity(api, "region", ordinal),
        input_value_id=input_value.value_id,
        output_value_id=output_value.value_id,
        input_space_id=space.space_id,
        output_space_id=space.space_id,
        validity=api["RegionValidity"](kind="Declared"),
        origin=_origin(api),
    )


def _coherent(
    api,
    space,
    input_value,
    output_value,
    *,
    controls,
    targets,
    ordinal: int = 0,
):
    return api["CoherentControlRegion"](
        region_id=_identity(api, "region", ordinal),
        input_value_id=input_value.value_id,
        output_value_id=output_value.value_id,
        input_space_id=space.space_id,
        output_space_id=space.space_id,
        validity=api["RegionValidity"](kind="Declared"),
        control_factor_ids=tuple(controls),
        target_factor_ids=tuple(targets),
        origin=_origin(api),
    )


def _outcome(api):
    return api["OutcomeIntent"](
        intent_id=_identity(api, "outcome_intent", 0),
        measured_factor_ids=(_identity(api, "resource", 1),),
        outcome_domain=("0", "1"),
        origin=_origin(api),
    )


def _terminal_measurement(api, space, input_value):
    outcome = _outcome(api)
    region = api["TerminalMeasurementRegion"](
        region_id=_identity(api, "region", 10),
        input_value_id=input_value.value_id,
        input_space_id=space.space_id,
        outcome_intent_id=outcome.intent_id,
        origin=_origin(api),
    )
    return outcome, region


def _dynamic_pair(api, space, input_value, post_measure_value, merged_value):
    measurement = api["DynamicMeasurementRegion"](
        region_id=_identity(api, "region", 20),
        input_value_id=input_value.value_id,
        post_measure_value_id=post_measure_value.value_id,
        input_space_id=space.space_id,
        output_space_id=space.space_id,
        token_id=_identity(api, "dynamic_token", 0),
        outcome_domain=("0", "1"),
        branch_region_ids=(
            _identity(api, "region", 21),
            _identity(api, "region", 22),
        ),
        required_capability="DynamicMeasurementFeedback",
        origin=_origin(api),
    )
    control = api["DynamicControlRegion"](
        region_id=_identity(api, "region", 23),
        measurement_region_id=measurement.region_id,
        post_measure_value_id=post_measure_value.value_id,
        token_id=measurement.token_id,
        branch_region_ids=measurement.branch_region_ids,
        merge_region_id=_identity(api, "region", 24),
        output_value_id=merged_value.value_id,
        origin=_origin(api),
    )
    return measurement, control


def _module(
    api,
    *,
    lane="StaticKernel",
    spaces=(),
    values=(),
    regions=(),
    outcome_intents=(),
    parameters=(),
    ancilla_scopes=(),
    uncompute_obligations=(),
):
    return api["QuantumSemanticModule"](
        schema_version=1,
        lane=api["SemanticLane"](kind=lane),
        roots=(_identity(api, "module", 0),),
        region_roots=tuple(region.region_id for region in regions),
        origins=(_origin(api),),
        acting_spaces=tuple(spaces),
        values=tuple(values),
        regions=tuple(regions),
        outcome_intents=tuple(outcome_intents),
        parameters=tuple(parameters),
        ancilla_scopes=tuple(ancilla_scopes),
        uncompute_obligations=tuple(uncompute_obligations),
    )


def _codes(diagnostics) -> set[str]:
    return {diagnostic.get("code") for diagnostic in diagnostics}


# D1 — lane and control-domain separation


def test_slice_d_api_is_importable_and_lanes_are_closed() -> None:
    api = _load_api()

    assert api["SemanticLane"](kind="StaticKernel").kind == "StaticKernel"
    assert (
        api["SemanticLane"](kind="DynamicQpuContract").kind
        == "DynamicQpuContract"
    )
    try:
        api["SemanticLane"](kind="AmbiguousControl")
        accepted = True
    except ValueError:
        accepted = False
    assert accepted is False


def test_coherent_control_uses_factor_selectors_on_one_joint_state() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    output_value = _value(api, space, 1)
    region = _coherent(
        api,
        space,
        input_value,
        output_value,
        controls=(space.factors[0].factor_id,),
        targets=(space.factors[1].factor_id,),
    )

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(space,),
            values=(input_value, output_value),
            regions=(region,),
        )
    )

    assert "QSEM_CONTROL_LANE_INVALID" not in _codes(diagnostics)


def test_coherent_control_rejects_overlapping_selectors() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    output_value = _value(api, space, 1)
    factor = space.factors[0].factor_id
    region = _coherent(
        api,
        space,
        input_value,
        output_value,
        controls=(factor,),
        targets=(factor,),
    )

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(space,),
            values=(input_value, output_value),
            regions=(region,),
        )
    )

    assert "QSEM_CONTROL_LANE_INVALID" in _codes(diagnostics)


def test_coherent_control_rejects_unknown_factor_selector() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    output_value = _value(api, space, 1)
    region = _coherent(
        api,
        space,
        input_value,
        output_value,
        controls=(_identity(api, "resource", 99),),
        targets=(space.factors[1].factor_id,),
    )

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(space,),
            values=(input_value, output_value),
            regions=(region,),
        )
    )

    assert "QSEM_CONTROL_LANE_INVALID" in _codes(diagnostics)


def test_compile_time_selection_has_no_semantic_region_api() -> None:
    import compiler.staqex.quantum_semantic_ir as semantic_ir

    assert not hasattr(semantic_ir, "StaticSelectionRegion")
    assert not hasattr(semantic_ir, "GenericControlRegion")


def test_dynamic_marker_is_rejected_from_static_kernel() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    post_measure = _value(api, space, 1)
    merged = _value(api, space, 2)
    measurement, control = _dynamic_pair(
        api, space, input_value, post_measure, merged
    )

    diagnostics = api["verify"](
        _module(
            api,
            lane="StaticKernel",
            spaces=(space,),
            values=(input_value, post_measure, merged),
            regions=(measurement, control),
        )
    )

    assert "QSEM_CONTROL_LANE_INVALID" in _codes(diagnostics)


# D2 — terminal and dynamic measurement boundaries


def test_terminal_measurement_has_no_reusable_output_value() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    outcome, region = _terminal_measurement(api, space, input_value)

    assert not hasattr(region, "output_value_id")
    assert not hasattr(region, "classical_value_id")
    assert outcome.outcome_domain == ("0", "1")


def test_post_terminal_measurement_quantum_use_is_rejected() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    reused_output = _value(api, space, 1)
    outcome, measurement = _terminal_measurement(api, space, input_value)
    illegal_successor = _unitary(api, space, input_value, reused_output, 11)

    diagnostics = api["verify"](
        _module(
            api,
            spaces=(space,),
            values=(input_value, reused_output),
            regions=(measurement, illegal_successor),
            outcome_intents=(outcome,),
        )
    )

    assert "QSEM_MEASUREMENT_BOUNDARY_INVALID" in _codes(diagnostics)


def test_dynamic_pair_is_valid_only_in_dynamic_lane() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    post_measure = _value(api, space, 1)
    merged = _value(api, space, 2)
    measurement, control = _dynamic_pair(
        api, space, input_value, post_measure, merged
    )

    diagnostics = api["verify"](
        _module(
            api,
            lane="DynamicQpuContract",
            spaces=(space,),
            values=(input_value, post_measure, merged),
            regions=(measurement, control),
        )
    )

    assert "QSEM_CONTROL_LANE_INVALID" not in _codes(diagnostics)
    assert "QSEM_DYNAMIC_CORRELATION_INVALID" not in _codes(diagnostics)


def test_dynamic_token_state_or_merge_mismatch_is_rejected() -> None:
    api = _load_api()
    space = _space(api)
    input_value = _value(api, space, 0)
    post_measure = _value(api, space, 1)
    merged = _value(api, space, 2)
    measurement, control = _dynamic_pair(
        api, space, input_value, post_measure, merged
    )
    mismatched = api["DynamicControlRegion"](
        region_id=control.region_id,
        measurement_region_id=measurement.region_id,
        post_measure_value_id=post_measure.value_id,
        token_id=_identity(api, "dynamic_token", 99),
        branch_region_ids=measurement.branch_region_ids,
        merge_region_id=None,
        output_value_id=merged.value_id,
        origin=_origin(api),
    )

    diagnostics = api["verify"](
        _module(
            api,
            lane="DynamicQpuContract",
            spaces=(space,),
            values=(input_value, post_measure, merged),
            regions=(measurement, mismatched),
        )
    )

    assert "QSEM_DYNAMIC_CORRELATION_INVALID" in _codes(diagnostics)


# D3 — parameters and resource obligations


def test_runtime_parameter_shape_dependence_is_rejected() -> None:
    api = _load_api()
    parameter = api["ParameterSymbol"](
        parameter_id=_identity(api, "parameter", 0),
        scalar_type="Real",
        unit="rad",
        binding_phase="Runtime",
        shape_defining=True,
        origin=_origin(api),
    )

    diagnostics = api["verify"](_module(api, parameters=(parameter,)))

    assert "QSEM_PARAMETER_SHAPE_DEPENDENCE" in _codes(diagnostics)


def test_parameter_symbol_records_domain_unit_phase_and_provenance() -> None:
    api = _load_api()
    parameter = api["ParameterSymbol"](
        parameter_id=_identity(api, "parameter", 0),
        scalar_type="Real",
        unit="rad",
        binding_phase="CompileTime",
        shape_defining=True,
        origin=_origin(api),
    )

    diagnostics = api["verify"](_module(api, parameters=(parameter,)))

    assert "QSEM_PARAMETER_SHAPE_DEPENDENCE" not in _codes(diagnostics)
    assert "provider" not in repr(parameter).lower()
    assert "target" not in repr(parameter).lower()


def test_ancilla_discharge_variants_are_closed_and_explicit() -> None:
    api = _load_api()
    accepted = (
        "ReturnedZero",
        "AbsorbedByIsometry",
        "TracedByChannel",
        "TerminalMeasurement",
    )

    for ordinal, kind in enumerate(accepted):
        discharge = api["AncillaDischarge"](
            kind=kind,
            reference=f"evidence-{ordinal}",
        )
        scope = api["AncillaScope"](
            scope_id=_identity(api, "ancilla_scope", ordinal),
            resource_id=_identity(api, "resource", 2),
            acquire_precondition="Zero",
            discharge=discharge,
            origin=_origin(api),
        )
        diagnostics = api["verify"](_module(api, ancilla_scopes=(scope,)))
        assert "QSEM_RESOURCE_DISCHARGE_MISSING" not in _codes(diagnostics)


def test_missing_ancilla_discharge_is_rejected() -> None:
    api = _load_api()
    scope = api["AncillaScope"](
        scope_id=_identity(api, "ancilla_scope", 0),
        resource_id=_identity(api, "resource", 2),
        acquire_precondition="Zero",
        discharge=None,
        origin=_origin(api),
    )

    diagnostics = api["verify"](_module(api, ancilla_scopes=(scope,)))

    assert "QSEM_RESOURCE_DISCHARGE_MISSING" in _codes(diagnostics)


def test_uncompute_obligation_records_evidence_without_synthesis_policy() -> None:
    api = _load_api()
    obligation = api["UncomputeObligation"](
        obligation_id=_identity(api, "uncompute_obligation", 0),
        resource_id=_identity(api, "resource", 2),
        witness_ref="upstream.uncompute.0",
        origin=_origin(api),
    )

    assert obligation.witness_ref == "upstream.uncompute.0"
    assert not hasattr(obligation, "inverse_operations")
    assert not hasattr(obligation, "tolerance")
    assert not hasattr(obligation, "synthesize")


def test_slice_d_definitions_join_identity_and_provenance_checks() -> None:
    api = _load_api()
    duplicated_id = _identity(api, "parameter", 0)
    first = api["ParameterSymbol"](
        parameter_id=duplicated_id,
        scalar_type="Real",
        unit=None,
        binding_phase="CompileTime",
        shape_defining=False,
        origin=_origin(api),
    )
    duplicate_incomplete = api["ParameterSymbol"](
        parameter_id=duplicated_id,
        scalar_type="Real",
        unit=None,
        binding_phase="CompileTime",
        shape_defining=False,
        origin=_origin(api, complete=False),
    )

    diagnostics = api["verify"](
        _module(api, parameters=(first, duplicate_incomplete))
    )

    assert "QSEM_IDENTITY_CONFLICT" in _codes(diagnostics)
    assert "QSEM_PROVENANCE_INCOMPLETE" in _codes(diagnostics)


if __name__ == "__main__":
    tests = (
        test_slice_d_api_is_importable_and_lanes_are_closed,
        test_coherent_control_uses_factor_selectors_on_one_joint_state,
        test_coherent_control_rejects_overlapping_selectors,
        test_coherent_control_rejects_unknown_factor_selector,
        test_compile_time_selection_has_no_semantic_region_api,
        test_dynamic_marker_is_rejected_from_static_kernel,
        test_terminal_measurement_has_no_reusable_output_value,
        test_post_terminal_measurement_quantum_use_is_rejected,
        test_dynamic_pair_is_valid_only_in_dynamic_lane,
        test_dynamic_token_state_or_merge_mismatch_is_rejected,
        test_runtime_parameter_shape_dependence_is_rejected,
        test_parameter_symbol_records_domain_unit_phase_and_provenance,
        test_ancilla_discharge_variants_are_closed_and_explicit,
        test_missing_ancilla_discharge_is_rejected,
        test_uncompute_obligation_records_evidence_without_synthesis_policy,
        test_slice_d_definitions_join_identity_and_provenance_checks,
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
