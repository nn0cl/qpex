"""AT-TDD Phase 1 Red: LISS-0016 provider-neutral QPU submission port."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.qpu_submit import (  # noqa: E402
    QpuArtifact,
    QpuJobPort,
    QpuSubmitPort,
    QpuSubmitRequest,
    ProviderJobId,
    ProviderJobState,
)


def test_qpu_artifact_preserves_qasm_provenance_and_hash() -> None:
    artifact = QpuArtifact(
        qasm="OPENQASM 3.0;",
        target_profile="local-fake",
        provenance={"source": "bell.qpex"},
        content_hash="sha256:artifact",
    )

    assert artifact.qasm.startswith("OPENQASM")
    assert artifact.provenance["source"] == "bell.qpex"
    assert artifact.content_hash.startswith("sha256:")


def test_submit_request_requires_host_owned_idempotency_key() -> None:
    artifact = QpuArtifact("OPENQASM 3.0;", "local-fake", {}, "sha256:a")
    request = QpuSubmitRequest(
        artifact=artifact,
        execution_settings={"shots": 100},
        idempotency_key="host-key-1",
        retry_policy="explicit-only",
    )

    assert request.idempotency_key == "host-key-1"
    assert request.retry_policy == "explicit-only"


def test_job_ports_use_fixed_states_and_opaque_provider_id() -> None:
    assert set(ProviderJobState) == {
        "queued",
        "running",
        "succeeded",
        "failed",
        "cancelled",
    }
    job_id = ProviderJobId(provider="local-fake", opaque_id="job-1")
    assert job_id.provider == "local-fake"
    assert job_id.opaque_id == "job-1"
    assert QpuSubmitPort and QpuJobPort


if __name__ == "__main__":
    for test in (
        test_qpu_artifact_preserves_qasm_provenance_and_hash,
        test_submit_request_requires_host_owned_idempotency_key,
        test_job_ports_use_fixed_states_and_opaque_provider_id,
    ):
        test()
    print("OK — qpu submit Green contract")
