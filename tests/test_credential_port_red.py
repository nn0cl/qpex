"""AT-TDD: LISS-0194 CredentialPort + Env adapter + mock submit (ADR 0161)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.credentials import (  # noqa: E402
    CredentialGatedMockSubmit,
    CredentialSubmitError,
    EnvCredentialAdapter,
)
from compiler.staqex.qpu_submit import QpuArtifact, QpuSubmitRequest  # noqa: E402


def _request() -> QpuSubmitRequest:
    return QpuSubmitRequest(
        artifact=QpuArtifact(
            qasm="OPENQASM 3.0;",
            target_profile="mock",
            provenance={},
            content_hash="sha256:t",
        ),
        execution_settings={},
        idempotency_key="k1",
    )


def test_env_adapter_reads_injected_mapping() -> None:
    adapter = EnvCredentialAdapter({"STAQEX_QPU_TOKEN": "secret", "EMPTY": ""})
    assert adapter.get("STAQEX_QPU_TOKEN") == "secret"
    assert adapter.get("EMPTY") is None
    assert adapter.get("MISSING") is None


def test_mock_submit_fail_closed_without_credentials() -> None:
    submit = CredentialGatedMockSubmit(
        EnvCredentialAdapter({}),
        required=("STAQEX_QPU_TOKEN",),
    )
    try:
        submit.submit(_request())
        raise AssertionError("expected CredentialSubmitError")
    except CredentialSubmitError as exc:
        assert exc.diagnostic.code == "CREDENTIAL_MISSING"
        assert exc.diagnostic.missing == ("STAQEX_QPU_TOKEN",)
    assert submit.last_missing is not None


def test_mock_submit_succeeds_with_credentials() -> None:
    submit = CredentialGatedMockSubmit(
        EnvCredentialAdapter({"STAQEX_QPU_TOKEN": "tok"}),
        required=("STAQEX_QPU_TOKEN",),
    )
    job = submit.submit(_request())
    assert job.provider == "mock-local"
    assert job.opaque_id == "mock-k1"
    assert submit.last_missing is None


if __name__ == "__main__":
    test_env_adapter_reads_injected_mapping()
    print("PASS test_env_adapter_reads_injected_mapping")
    test_mock_submit_fail_closed_without_credentials()
    print("PASS test_mock_submit_fail_closed_without_credentials")
    test_mock_submit_succeeds_with_credentials()
    print("PASS test_mock_submit_succeeds_with_credentials")
