"""Provider-neutral Host credential port (ADR 0161 / LISS-0194).

Credentials never enter Kernel syntax. Host adapters read secrets from an
injected environment mapping (tests) or OS env (production). No cloud SDK.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Protocol

from .qpu_submit import ProviderJobId, QpuSubmitRequest


class CredentialPort(Protocol):
    """Lookup a named credential; missing → None (never invent values)."""

    def get(self, name: str) -> str | None:
        ...


class EnvCredentialAdapter:
    """Read credentials from an env mapping (default: os.environ)."""

    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        self._env: Mapping[str, str] = env if env is not None else os.environ

    def get(self, name: str) -> str | None:
        value = self._env.get(name)
        if value is None or value == "":
            return None
        return value


@dataclass(frozen=True)
class CredentialMissing:
    """Fail-closed diagnostic when required credentials are absent."""

    code: str
    missing: tuple[str, ...]
    message: str


class CredentialGatedMockSubmit:
    """Mock QpuSubmitPort that refuses submit when credentials are missing.

    Does not call any cloud SDK. On success returns a local opaque job id.
    """

    def __init__(
        self,
        credentials: CredentialPort,
        *,
        required: tuple[str, ...] = ("STAQEX_QPU_TOKEN",),
        provider: str = "mock-local",
    ) -> None:
        self._credentials = credentials
        self._required = required
        self._provider = provider
        self.last_missing: CredentialMissing | None = None

    def submit(self, request: QpuSubmitRequest) -> ProviderJobId:
        missing = tuple(
            name for name in self._required if self._credentials.get(name) is None
        )
        if missing:
            self.last_missing = CredentialMissing(
                code="CREDENTIAL_MISSING",
                missing=missing,
                message=(
                    "QPU submit refused: missing Host credentials "
                    + ", ".join(missing)
                ),
            )
            raise CredentialSubmitError(self.last_missing)
        self.last_missing = None
        return ProviderJobId(
            provider=self._provider,
            opaque_id=f"mock-{request.idempotency_key}",
        )


class CredentialSubmitError(Exception):
    """Raised by CredentialGatedMockSubmit when credentials are missing."""

    def __init__(self, diagnostic: CredentialMissing) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


__all__ = [
    "CredentialGatedMockSubmit",
    "CredentialMissing",
    "CredentialPort",
    "CredentialSubmitError",
    "EnvCredentialAdapter",
]
