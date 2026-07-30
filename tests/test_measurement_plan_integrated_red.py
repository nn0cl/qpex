"""AT-TDD Phase 1 Red: LISS-0090 integrated measurement-plan contract.

One suite covers observable mapping, compatibility/grouping, statistical
targets, allocation, and raw/derived provenance. It uses provider-neutral
records and deterministic literals only. Physical sampling, calibration,
provider SDKs, mitigation, and result publication are intentionally absent.
"""

from __future__ import annotations

from dataclasses import replace
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.measurement_plan import (
        CompatibilityWitness,
        ConfidenceTarget,
        CovarianceAssumption,
        MeasurementGroup,
        MeasurementPlan,
        ObservableSpec,
        ShotAllocation,
        allocate_shots,
        reconstruct_observable,
        verify_measurement_plan,
    )

    return locals()


def _observable(api, observable_id: str, *, origin_id: str = "source.obs.0"):
    return api["ObservableSpec"](
        observable_id=observable_id,
        terms=(f"{observable_id}:Z0",),
        origin_id=origin_id,
    )


def _witness(api, group_id: str, *, compatible: bool = True):
    return api["CompatibilityWitness"](
        group_id=group_id,
        relation="commutes" if compatible else "incompatible",
        evidence_ids=("source.obs.0", "source.obs.1"),
    )


def _group(api, group_id: str = "group.0", observable_ids=("obs.0",)):
    return api["MeasurementGroup"](
        group_id=group_id,
        observable_ids=tuple(observable_ids),
        witness=_witness(api, group_id),
        basis="computational-z",
    )


def _target(api, *, confidence="0.95", interval="two-sided"):
    return api["ConfidenceTarget"](
        confidence=confidence,
        interval=interval,
        estimator="bounded-mean",
    )


def _covariance(api, *, kind="independent", evidence="declared"):
    return api["CovarianceAssumption"](kind=kind, evidence=evidence)


def _allocation(api, group_id="group.0", shots="100"):
    return api["ShotAllocation"](
        group_id=group_id,
        shots=shots,
        lower_bound="1",
        rounding="largest-remainder",
    )


def _plan(api, *, profile="SIM0_EXACT", total_shots="100"):
    return api["MeasurementPlan"](
        plan_id=f"measurement.{profile.lower()}",
        profile=profile,
        observables=(_observable(api, "obs.0"),),
        groups=(_group(api),),
        confidence_target=_target(api),
        covariance=_covariance(api),
        allocations=(_allocation(api),),
        total_shots=total_shots,
        provenance=("plan.node.measurement", "source.obs.0"),
    )


def _codes(diagnostics) -> set[str]:
    return {diagnostic.get("code") for diagnostic in diagnostics}


def test_immutable_plan_maps_observables_to_reconstructable_raw_groups() -> None:
    api = _load_api()
    plan = _plan(api)

    assert api["verify_measurement_plan"](plan) == []
    assert api["reconstruct_observable"](plan, "obs.0").group_id == "group.0"
    assert plan.total_shots == "100"


def test_compatible_terms_require_and_preserve_a_witness() -> None:
    api = _load_api()
    observables = (_observable(api, "obs.0"), _observable(api, "obs.1"))
    group = _group(api, observable_ids=("obs.0", "obs.1"))
    plan = _plan(api)
    plan = replace(plan, observables=observables, groups=(group,))

    assert api["verify_measurement_plan"](plan) == []
    assert plan.groups[0].witness.relation == "commutes"


def test_incompatible_grouping_is_rejected() -> None:
    api = _load_api()
    group = api["MeasurementGroup"](
        group_id="group.bad",
        observable_ids=("obs.0", "obs.1"),
        witness=_witness(api, "group.bad", compatible=False),
        basis="computational-z",
    )
    plan = _plan(api)
    plan = replace(
        plan,
        observables=(_observable(api, "obs.0"), _observable(api, "obs.1")),
        groups=(group,),
    )

    assert "MEASUREMENT_GROUP_INCOMPATIBLE" in _codes(
        api["verify_measurement_plan"](plan)
    )


def test_duplicate_or_missing_observable_identity_is_rejected() -> None:
    api = _load_api()
    duplicate = _observable(api, "obs.0", origin_id="source.obs.duplicate")
    plan = _plan(api)
    duplicate_plan = replace(plan, observables=(plan.observables[0], duplicate))
    missing_plan = replace(
        plan, groups=(_group(api, observable_ids=("obs.unknown",)),)
    )

    assert "MEASUREMENT_OBSERVABLE_ID_CONFLICT" in _codes(
        api["verify_measurement_plan"](duplicate_plan)
    )
    assert "MEASUREMENT_MAPPING_INCOMPLETE" in _codes(
        api["verify_measurement_plan"](missing_plan)
    )


def test_confidence_and_covariance_policy_must_be_explicit() -> None:
    api = _load_api()
    plan = _plan(api)
    invalid_target = api["ConfidenceTarget"](
        confidence="", interval="", estimator=""
    )
    invalid_covariance = api["CovarianceAssumption"](kind="", evidence="")
    invalid_plan = replace(
        plan, confidence_target=invalid_target, covariance=invalid_covariance
    )

    codes = _codes(api["verify_measurement_plan"](invalid_plan))
    assert "MEASUREMENT_STATISTICAL_TARGET_INVALID" in codes
    assert "MEASUREMENT_COVARIANCE_INVALID" in codes


def test_allocation_conserves_exact_total_budget_and_rounding_policy() -> None:
    api = _load_api()
    allocations = api["allocate_shots"](
        (_group(api, "group.0"), _group(api, "group.1")),
        _target(api),
        _covariance(api),
        total_shots="101",
    )

    assert tuple(item.group_id for item in allocations) == ("group.0", "group.1")
    assert sum(int(item.shots) for item in allocations) == 101
    assert all(item.rounding == "largest-remainder" for item in allocations)


def test_covariance_aware_allocation_keeps_assumptions_and_is_deterministic() -> None:
    api = _load_api()
    covariance = _covariance(api, kind="declared-covariance", evidence="cov.0")
    first = api["allocate_shots"](
        (_group(api, "group.0"), _group(api, "group.1")),
        _target(api),
        covariance,
        total_shots="101",
    )
    second = api["allocate_shots"](
        (_group(api, "group.0"), _group(api, "group.1")),
        _target(api),
        covariance,
        total_shots="101",
    )

    assert first == second
    assert covariance.evidence == "cov.0"


def test_allocation_rejects_negative_or_non_deterministic_budget() -> None:
    api = _load_api()
    try:
        api["allocate_shots"](
            (_group(api),), _target(api), _covariance(api), total_shots="-1"
        )
    except ValueError as error:
        assert "MEASUREMENT_ALLOCATION_INVALID" in str(error)
    else:
        raise AssertionError("negative shot budgets must be rejected")


def test_raw_and_derived_provenance_remain_continuous() -> None:
    api = _load_api()
    plan = _plan(api)

    assert plan.provenance == ("plan.node.measurement", "source.obs.0")
    assert plan.observables[0].origin_id in plan.provenance
    assert api["verify_measurement_plan"](plan) == []


def test_current_and_research_profiles_use_one_provider_neutral_schema() -> None:
    api = _load_api()
    sim = _plan(api, profile="SIM0_EXACT")
    research = _plan(api, profile="CH1_DIGITAL_RESEARCH")

    assert api["verify_measurement_plan"](sim) == []
    assert api["verify_measurement_plan"](research) == []
    assert sim.observables == research.observables
    assert sim.groups == research.groups


def test_provider_and_implicit_sampling_fields_are_not_domain_inputs() -> None:
    api = _load_api()
    try:
        plan = _plan(api)
        api["MeasurementPlan"](
            plan_id=plan.plan_id,
            profile=plan.profile,
            observables=plan.observables,
            groups=plan.groups,
            confidence_target=plan.confidence_target,
            covariance=plan.covariance,
            allocations=plan.allocations,
            total_shots=plan.total_shots,
            provenance=plan.provenance,
            provider_name="provider.sdk",
            random_seed=7,
        )
    except TypeError:
        return
    raise AssertionError("provider and sampling fields must stay outside the plan")


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
    print(f"LISS-0090 integrated Red: {len(tests) - failures} passed, {failures} failed")
    raise SystemExit(1 if failures else 0)
