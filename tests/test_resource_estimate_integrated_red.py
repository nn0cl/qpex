"""AT-TDD Phase 1 Red: LISS-0091 integrated resource estimation contract.

One suite covers typed quantities, pre/post-routing stages, compositional
budgets, feasibility reports, and ADR 0100 isolation. Provider prices,
calibration, SDKs, layout/routing execution, and semantic carrier invention
are intentionally absent.
"""

from __future__ import annotations

from dataclasses import replace
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_U64_MAX = (1 << 64) - 1


def _load_api():
    from compiler.staqex.resource_estimate import (
        RESOURCE_CATEGORIES,
        CompositionalBudget,
        EstimateProvenance,
        FeasibilityReport,
        PostRoutingEstimate,
        PreRoutingEstimate,
        ResourceCategory,
        ResourceEstimateReport,
        ResourceQuantity,
        TargetProfileSnapshot,
        Unknown,
        assess_feasibility,
        estimate_resources,
        soft_resource_estimate,
        verify_resource_estimate_report,
    )

    return locals()


def _provenance(
    api,
    *,
    formula_version: str = "resource-estimate-plan-v1",
    assumptions: tuple[str, ...] = ("declared-logical-width",),
    uncertainty: str = "exact-count",
    profile_snapshot_id: str | None = "profile.sim0",
):
    return api["EstimateProvenance"](
        formula_version=formula_version,
        assumptions=assumptions,
        uncertainty=uncertainty,
        profile_snapshot_id=profile_snapshot_id,
    )


def _quantity(
    api,
    *,
    category: str = "logical",
    name: str = "logical_qubits",
    value: int | str = 4,
):
    return api["ResourceQuantity"](
        category=api["ResourceCategory"](category),
        name=name,
        value=value,
    )


def _unknown(
    api,
    *,
    name: str = "decoder_load",
    assumptions: tuple[str, ...] = ("no-decoder-model",),
):
    return api["Unknown"](name=name, assumptions=assumptions)


def _pre_routing(api, *, qubits: int = 4):
    return api["PreRoutingEstimate"](
        stage="pre_routing",
        quantities=(_quantity(api, value=qubits),),
        provenance=_provenance(api),
    )


def _post_routing(api, *, unknown: bool = True):
    if unknown:
        return api["PostRoutingEstimate"](
            stage="post_routing",
            quantities=(),
            unknowns=(
                _unknown(
                    api,
                    name="physical_qubits",
                    assumptions=("awaiting-liss-0092-routing",),
                ),
            ),
            provenance=_provenance(
                api,
                assumptions=("awaiting-liss-0092-routing",),
                uncertainty="unknown",
                profile_snapshot_id="profile.ch1",
            ),
        )
    return api["PostRoutingEstimate"](
        stage="post_routing",
        quantities=(
            _quantity(api, category="physical", name="physical_qubits", value=8),
        ),
        unknowns=(),
        provenance=_provenance(
            api,
            assumptions=("synthetic-routing",),
            uncertainty="synthetic-bound",
            profile_snapshot_id="profile.ch1",
        ),
    )


def _budget(api, *, with_assumptions: bool = True):
    return api["CompositionalBudget"](
        failure=_unknown(
            api,
            name="failure_budget",
            assumptions=("independent-faults",) if with_assumptions else (),
        ),
        decoder=_unknown(
            api,
            name="decoder_load",
            assumptions=("no-decoder-model",) if with_assumptions else (),
        ),
        link=_unknown(
            api,
            name="link_budget",
            assumptions=("single-partition",) if with_assumptions else (),
        ),
        factory=_unknown(
            api,
            name="factory_load",
            assumptions=("no-factory",) if with_assumptions else (),
        ),
        memory=_quantity(api, category="logical", name="workspace_bytes", value=1024),
        time=_unknown(
            api,
            name="wall_time",
            assumptions=("unscheduled",) if with_assumptions else (),
        ),
        power=_unknown(
            api,
            name="power",
            assumptions=("not-modeled",) if with_assumptions else (),
        ),
        cost=_unknown(
            api,
            name="cost",
            assumptions=("no-provider-price",) if with_assumptions else (),
        ),
    )


def _profile(api, profile_id: str, *, max_logical_qubits: int = 16):
    return api["TargetProfileSnapshot"](
        profile_id=profile_id,
        capabilities=(("max_logical_qubits", str(max_logical_qubits)),),
    )


def _report(api, *, qubits: int = 4, profiles=None):
    pre = _pre_routing(api, qubits=qubits)
    post = _post_routing(api)
    budget = _budget(api)
    report = api["ResourceEstimateReport"](
        report_id="estimate.integrated.0",
        pre_routing=pre,
        post_routing=post,
        budget=budget,
        feasibility=(),
        provenance=_provenance(api),
    )
    if profiles is None:
        return report
    feasibility = tuple(
        api["assess_feasibility"](report, profile) for profile in profiles
    )
    return replace(report, feasibility=feasibility)


def _codes(diagnostics) -> set[str]:
    return {diagnostic.get("code") for diagnostic in diagnostics}


def test_resource_categories_are_typed_and_exclusive() -> None:
    api = _load_api()
    assert set(api["RESOURCE_CATEGORIES"]) == {"semantic", "logical", "physical"}

    mixed = api["PreRoutingEstimate"](
        stage="pre_routing",
        quantities=(
            _quantity(api, category="logical", name="logical_qubits", value=2),
            _quantity(api, category="physical", name="physical_qubits", value=4),
        ),
        provenance=_provenance(api),
    )
    report = _report(api)
    report = replace(report, pre_routing=mixed)

    assert "RESOURCE_CATEGORY_MIXED" in _codes(
        api["verify_resource_estimate_report"](report)
    )


def test_quantities_beyond_u64_remain_exact_or_symbolic() -> None:
    api = _load_api()
    exact = _quantity(api, value=_U64_MAX + 1)
    symbolic = _quantity(api, name="expanded_ops", value="2**80")
    report = _report(api)
    pre = replace(report.pre_routing, quantities=(exact, symbolic))
    report = replace(report, pre_routing=pre)

    assert api["verify_resource_estimate_report"](report) == []
    assert report.pre_routing.quantities[0].value == _U64_MAX + 1
    assert report.pre_routing.quantities[1].value == "2**80"

    floatish = _quantity(api, value=1.5)  # type: ignore[arg-type]
    bad = replace(report, pre_routing=replace(pre, quantities=(floatish,)))
    assert "RESOURCE_QUANTITY_FLOAT_FORBIDDEN" in _codes(
        api["verify_resource_estimate_report"](bad)
    )


def test_pre_and_post_routing_stages_remain_distinct() -> None:
    api = _load_api()
    report = _report(api)

    assert report.pre_routing.stage == "pre_routing"
    assert report.post_routing.stage == "post_routing"
    assert report.pre_routing.provenance.assumptions
    assert report.pre_routing.provenance.uncertainty
    assert report.pre_routing.provenance.profile_snapshot_id
    assert report.post_routing.provenance.assumptions
    assert api["verify_resource_estimate_report"](report) == []

    swapped = replace(report, pre_routing=replace(report.pre_routing, stage="post_routing"))
    assert "RESOURCE_STAGE_MISMATCH" in _codes(
        api["verify_resource_estimate_report"](swapped)
    )


def test_post_routing_may_be_unknown_with_compositional_assumptions() -> None:
    api = _load_api()
    report = _report(api)

    assert report.post_routing.quantities == ()
    assert report.post_routing.unknowns[0].name == "physical_qubits"
    assert report.post_routing.unknowns[0].assumptions == (
        "awaiting-liss-0092-routing",
    )
    assert api["verify_resource_estimate_report"](report) == []


def test_unknown_without_assumptions_is_rejected() -> None:
    api = _load_api()
    report = _report(api)
    bare = api["Unknown"](name="physical_qubits", assumptions=())
    post = replace(report.post_routing, unknowns=(bare,))
    report = replace(report, post_routing=post)

    assert "RESOURCE_UNKNOWN_ASSUMPTIONS_REQUIRED" in _codes(
        api["verify_resource_estimate_report"](report)
    )


def test_compositional_budgets_allow_unknown_with_assumptions() -> None:
    api = _load_api()
    report = _report(api)

    assert report.budget.cost.assumptions == ("no-provider-price",)
    assert report.budget.decoder.assumptions == ("no-decoder-model",)
    assert api["verify_resource_estimate_report"](report) == []


def test_compositional_budget_missing_assumptions_is_rejected() -> None:
    api = _load_api()
    report = replace(_report(api), budget=_budget(api, with_assumptions=False))

    assert "RESOURCE_BUDGET_ASSUMPTIONS_REQUIRED" in _codes(
        api["verify_resource_estimate_report"](report)
    )


def test_estimate_resources_builds_pre_routing_from_plan_literals() -> None:
    api = _load_api()
    report = api["estimate_resources"](
        {
            "plan_id": "plan.0",
            "logical_qubits": 4,
            "ancillas": 1,
            "depth": 12,
            "operations": 40,
            "measurements": 4,
            "classical_latency": "0",
            "simulator_memory": "symbolic:sv(4)",
        }
    )

    assert report.pre_routing.stage == "pre_routing"
    names = {item.name for item in report.pre_routing.quantities}
    assert {"logical_qubits", "ancillas", "depth", "operations"}.issubset(names)
    assert all(item.category.value == "logical" for item in report.pre_routing.quantities)
    assert api["verify_resource_estimate_report"](report) == []


def test_feasibility_reports_for_synthetic_profiles() -> None:
    api = _load_api()
    profiles = (
        _profile(api, "CH1_DIGITAL_RESEARCH", max_logical_qubits=16),
        _profile(api, "NH5_REFERENCE", max_logical_qubits=10**6),
        _profile(api, "QP2_REFERENCE", max_logical_qubits=10**9),
        _profile(api, "QS2_REFERENCE", max_logical_qubits=10**12),
    )
    report = _report(api, qubits=4, profiles=profiles)

    assert len(report.feasibility) == 4
    assert all(isinstance(item, api["FeasibilityReport"]) for item in report.feasibility)
    assert all(item.status == "feasible" for item in report.feasibility)
    assert {item.profile_id for item in report.feasibility} == {
        "CH1_DIGITAL_RESEARCH",
        "NH5_REFERENCE",
        "QP2_REFERENCE",
        "QS2_REFERENCE",
    }


def test_feasibility_reject_names_exceeded_dimension_without_fallback() -> None:
    api = _load_api()
    profile = _profile(api, "CH1_DIGITAL_RESEARCH", max_logical_qubits=2)
    report = _report(api, qubits=8)
    result = api["assess_feasibility"](report, profile)

    assert result.status == "rejected"
    assert result.profile_id == "CH1_DIGITAL_RESEARCH"
    assert result.exceeded_dimensions == ("max_logical_qubits",)
    assert result.selected_alternative is None


def test_adr_0100_host_simulation_estimate_remains_isolated() -> None:
    api = _load_api()
    import compiler.staqex.resource_estimate as mod

    assert not hasattr(mod, "SimulationResourceEstimate")
    assert not hasattr(mod, "estimate_simulator_memory_bytes")
    assert set(api["RESOURCE_CATEGORIES"]) == {"semantic", "logical", "physical"}


def test_soft_estimate_from_absent_input_does_not_invent_carriers() -> None:
    api = _load_api()
    soft = api["soft_resource_estimate"](plan=None, profiles=())

    assert soft.report is None
    assert soft.diagnostics
    assert all(item.get("code", "").startswith("RES_") for item in soft.diagnostics)
    assert "RES_INPUT_ABSENT" in _codes(soft.diagnostics)


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
    print(
        f"LISS-0091 integrated Red: {len(tests) - failures} passed, {failures} failed"
    )
    raise SystemExit(1 if failures else 0)
