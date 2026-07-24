"""Provider-neutral Host contract for submitting emitted QPU artifacts.

This module contains only immutable DTOs and ports. Provider SDKs, secrets,
network calls, polling implementations, and retry execution belong in Host
adapters outside the compiler Kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol


class ProviderJobState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class QpuArtifact:
    qasm: str
    target_profile: str
    provenance: Mapping[str, Any]
    content_hash: str


@dataclass(frozen=True)
class QpuSubmitRequest:
    artifact: QpuArtifact
    execution_settings: Mapping[str, Any]
    idempotency_key: str
    retry_policy: str = "explicit-only"


@dataclass(frozen=True)
class ProviderJobId:
    provider: str
    opaque_id: str


class QpuSubmitPort(Protocol):
    """Submit an artifact through a Host-owned provider adapter."""

    def submit(self, request: QpuSubmitRequest) -> ProviderJobId:
        ...


class QpuJobPort(Protocol):
    """Observe or control a provider-neutral QPU job."""

    def status(self, job_id: ProviderJobId) -> ProviderJobState:
        ...

    def wait(self, job_id: ProviderJobId) -> ProviderJobState:
        ...

    def result(self, job_id: ProviderJobId) -> Mapping[str, Any]:
        ...

    def cancel(self, job_id: ProviderJobId) -> ProviderJobState:
        ...


__all__ = [
    "ProviderJobId",
    "ProviderJobState",
    "QpuArtifact",
    "QpuJobPort",
    "QpuSubmitPort",
    "QpuSubmitRequest",
]
