"""Phase 1 Red acceptance tests for LISS-0046."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import Job, JobResult, MeasurementEnvelope  # noqa: E402
from compiler.staqex.observation import (  # noqa: E402
    CheckpointIdentity,
    ObservationReport,
    ObservationRequest,
)


def _report() -> ObservationReport:
    request = ObservationRequest(
        checkpoint=CheckpointIdentity(name="energy", stage="final"),
        observable="energy(H)",
        projection="expectation",
        target_lane="qpu",
        source_formula="expectation(H)",
    )
    return ObservationReport(
        request=request,
        job_id="job-obs-001",
        values={"expectation": -1.1},
        provenance={"shots": 1000},
    )


def test_completed_job_result_exposes_observation_reports():
    report = _report()
    result = JobResult(status="succeeded", observations=(report,))

    job = Job("job-obs-001", result)

    assert job.result().observations == (report,)
    assert job.result().observations[0].request.checkpoint.name == "energy"


def test_terminal_measurement_and_observation_report_are_separate():
    report = _report()
    measurement = MeasurementEnvelope(
        value=1,
        marginal={1: 1.0},
        vacuum=False,
        sink="stdout",
        output="1",
    )
    result = JobResult(
        status="succeeded",
        measurements=(measurement,),
        observations=(report,),
    )

    assert result.measurements == (measurement,)
    assert result.observations == (report,)


def test_result_without_observation_requests_has_no_reports():
    result = JobResult(status="succeeded")

    assert result.observations == ()


def test_observation_report_is_available_only_from_terminal_job_result():
    report = _report()
    queued = Job("job-obs-001", JobResult(status="queued", observations=(report,)))

    assert queued.status() == "queued"
    assert queued.result().status == "queued"
    assert queued.result().observations[0].job_id == queued.id


if __name__ == "__main__":
    tests = [
        test_completed_job_result_exposes_observation_reports,
        test_terminal_measurement_and_observation_report_are_separate,
        test_result_without_observation_requests_has_no_reports,
        test_observation_report_is_available_only_from_terminal_job_result,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"RED {test.__name__}: {type(error).__name__}: {error}")
    print(f"JobResult observation contract: {len(tests) - failures} passed, {failures} failed")
    raise SystemExit(1 if failures else 0)
