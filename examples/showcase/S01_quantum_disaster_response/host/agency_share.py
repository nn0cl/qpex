#!/usr/bin/env python3
"""Inter-agency inventory share gated by CredentialPort (ADR 0161)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.credentials import (
    CredentialGatedMockSubmit,
    CredentialSubmitError,
    EnvCredentialAdapter,
)
from compiler.staqex.qpu_submit import QpuArtifact, QpuSubmitRequest


def _request() -> QpuSubmitRequest:
    return QpuSubmitRequest(
        artifact=QpuArtifact(
            qasm="// static honesty lane — no live submit\nOPENQASM 3.0;\n",
            target_profile="mock-nh5ish",
            provenance={"agency": "external_depot", "live_submit": False},
            content_hash="sha256:s01-agency-share",
        ),
        execution_settings={"purpose": "external_depot_inventory"},
        idempotency_key="s01-agency-share-1",
    )


def main() -> None:
    # Fail closed without token; set STAQEX_AGENCY_TOKEN to demo success.
    env = {k: v for k, v in os.environ.items() if k.startswith("STAQEX_")}
    adapter = EnvCredentialAdapter(env)
    gate = CredentialGatedMockSubmit(
        adapter, required=("STAQEX_AGENCY_TOKEN",)
    )
    try:
        result = gate.submit(_request())
        print("agency_share_ok:", result.provider, result.opaque_id)
    except CredentialSubmitError as exc:
        print("agency_share_blocked:", exc.diagnostic.code, exc.diagnostic.missing)


if __name__ == "__main__":
    main()
