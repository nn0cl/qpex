"""AT-TDD Phase 1 Red: LISS-0087 integrated verified pass manager.

One suite covers pass identity, pre/post safety, exactness and obligation
propagation, deterministic composition, provenance, and CH0/NH5 evidence.
Provider SDKs, backend fallbacks, mutable registries, and pass-specific policy
are intentionally absent.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.verified_pass import (
        PassConfiguration,
        PassDefinition,
        PassInput,
        PassOutput,
        PassPipeline,
        PassProvenance,
        run_verified_pipeline,
        verify_pass_result,
    )

    return locals()


def _provenance(api, *, complete=True):
    return api["PassProvenance"](
        source_id="noether-forge.staqex",
        upstream_ids=("plan.node.0",) if complete else (),
        transform_id="pass.red.v1" if complete else "",
    )


def _configuration(api, pass_id="pass.identity"):
    return api["PassConfiguration"](
        pass_id=pass_id,
        version="1",
        parameters=(("mode", "deterministic"),),
    )


def _input(api, *, verified=True, exactness="exact", obligations=()):
    return api["PassInput"](
        value={"plan": "compact"},
        verified=verified,
        provenance=_provenance(api),
        exactness=exactness,
        obligations=obligations,
    )


def _output(api, *, exactness="exact", obligations=(), complete=True):
    return api["PassOutput"](
        value={"plan": "compact"},
        provenance=_provenance(api, complete=complete),
        exactness=exactness,
        obligations=obligations,
    )


def _pass(api, *, pass_id="pass.identity", execute=None, precondition=True, postcondition=True):
    return api["PassDefinition"](
        pass_id=pass_id,
        configuration=_configuration(api, pass_id),
        execute=execute if execute is not None else lambda item: _output(api),
        precondition=precondition,
        postcondition=postcondition,
    )


def _run(api, passes, input_value=None):
    pipeline = api["PassPipeline"](passes=tuple(passes))
    return api["run_verified_pipeline"](
        input_value if input_value is not None else _input(api),
        pipeline,
    )


def test_immutable_pass_configuration_and_result_are_exposed() -> None:
    api = _load_api()
    configuration = _configuration(api)
    result = _run(api, (_pass(api),))

    assert configuration.pass_id == "pass.identity"
    assert result.status == "verified"
    assert api["verify_pass_result"](result) == []


def test_failed_precondition_hard_stops_before_execution() -> None:
    api = _load_api()
    calls = []

    def execute(item):
        calls.append("execute")
        return _output(api)

    result = _run(api, (_pass(api, execute=execute, precondition=False),))

    assert calls == []
    assert result.status == "failed"
    assert "PASS_PRECONDITION_FAILED" in {
        item.get("code") for item in result.diagnostics
    }


def test_failed_postcondition_rejects_output() -> None:
    api = _load_api()
    result = _run(api, (_pass(api, postcondition=False),))

    assert result.status == "failed"
    assert "PASS_POSTCONDITION_FAILED" in {
        item.get("code") for item in result.diagnostics
    }


def test_failed_pass_does_not_call_later_pass() -> None:
    api = _load_api()
    calls = []

    def later(item):
        calls.append("later")
        return _output(api)

    result = _run(
        api,
        (
            _pass(api, pass_id="pass.failed", postcondition=False),
            _pass(api, pass_id="pass.later", execute=later),
        ),
    )

    assert result.status == "failed"
    assert calls == []


def test_unverified_input_cannot_enter_a_pass() -> None:
    api = _load_api()
    result = _run(api, (_pass(api),), input_value=_input(api, verified=False))

    assert result.status == "failed"
    assert "PASS_INPUT_UNVERIFIED" in {
        item.get("code") for item in result.diagnostics
    }


def test_approximation_obligations_are_preserved() -> None:
    api = _load_api()
    obligations = ("obligation.energy-bound",)

    def approximate(item):
        return _output(api, exactness="approximate", obligations=obligations)

    result = _run(
        api,
        (_pass(api, execute=approximate),),
        input_value=_input(api, exactness="approximate", obligations=obligations),
    )

    assert result.status == "verified"
    assert result.output.obligations == obligations
    assert result.output.exactness == "approximate"


def test_output_provenance_must_remain_complete() -> None:
    api = _load_api()
    result = _run(
        api,
        (_pass(api, execute=lambda item: _output(api, complete=False)),),
    )

    assert result.status == "failed"
    assert "PASS_PROVENANCE_INCOMPLETE" in {
        item.get("code") for item in result.diagnostics
    }


def test_pipeline_order_and_diagnostics_are_deterministic() -> None:
    api = _load_api()
    first = _run(api, (_pass(api, pass_id="pass.a"), _pass(api, pass_id="pass.b")))
    second = _run(api, (_pass(api, pass_id="pass.a"), _pass(api, pass_id="pass.b")))

    assert first == second
    assert first.status == "verified"


def test_ch0_and_nh5_evidence_use_the_same_pass_contract() -> None:
    api = _load_api()
    ch0 = _run(api, (_pass(api, pass_id="CH0_COMMON_PHYSICAL"),))
    nh5 = _run(api, (_pass(api, pass_id="NH5"),))

    assert ch0.status == nh5.status == "verified"
    assert api["verify_pass_result"](ch0) == []
    assert api["verify_pass_result"](nh5) == []


def test_provider_fallback_and_nondeterministic_configuration_are_rejected() -> None:
    api = _load_api()
    provider_pass = _pass(api, pass_id="provider.sdk.fallback")
    result = _run(api, (provider_pass,))

    assert result.status == "failed"
    assert "PASS_POLICY_INVALID" in {
        item.get("code") for item in result.diagnostics
    }


if __name__ == "__main__":
    tests = (
        test_immutable_pass_configuration_and_result_are_exposed,
        test_failed_precondition_hard_stops_before_execution,
        test_failed_postcondition_rejects_output,
        test_failed_pass_does_not_call_later_pass,
        test_unverified_input_cannot_enter_a_pass,
        test_approximation_obligations_are_preserved,
        test_output_provenance_must_remain_complete,
        test_pipeline_order_and_diagnostics_are_deterministic,
        test_ch0_and_nh5_evidence_use_the_same_pass_contract,
        test_provider_fallback_and_nondeterministic_configuration_are_rejected,
    )

    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
        else:
            print(f"pass {test.__name__}")

    print(f"\n{len(tests) - failures} passed, {failures} failed")
    sys.exit(1 if failures else 0)
