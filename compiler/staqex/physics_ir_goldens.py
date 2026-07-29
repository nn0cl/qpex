"""Physics IR golden fixture loader for LISS-0117 (Agent C).

Slice A loads checked-in inspect/DTO snapshots under a fixtures root. It does
not lower HIR, edit ``physics_ir.py``, or promote fixtures to a public oracle.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PHYSICS_IR_PROVENANCE_ERROR = "PHYSICS_IR_PROVENANCE_ERROR"
PHYSICS_IR_GOLDEN_ERROR = "PHYSICS_IR_GOLDEN_ERROR"
PhysicsGoldenDiagnostic = dict[str, str]


@dataclass(frozen=True, slots=True)
class PhysicsIrGolden:
    """One catalog-aligned golden loaded from a fixture snapshot."""

    golden_id: str
    family: str
    required_structure: tuple[str, ...]
    provenance_required: bool
    snapshot: dict[str, Any]
    oracle_promoted: bool = False


def load_physics_ir_goldens(fixtures_root: str | Path) -> tuple[PhysicsIrGolden, ...]:
    """Load every ``*.json`` golden under ``fixtures_root`` (non-recursive)."""

    root = Path(fixtures_root)
    if not root.is_dir():
        raise FileNotFoundError(f"Physics IR fixtures root not found: {root}")

    goldens: list[PhysicsIrGolden] = []
    for path in sorted(root.glob("*.json")):
        payload = json.loads(path.read_text())
        goldens.append(_golden_from_payload(payload, path))
    return tuple(goldens)


def verify_physics_ir_goldens(
    goldens: Sequence[PhysicsIrGolden] | Iterable[PhysicsIrGolden],
) -> list[PhysicsGoldenDiagnostic]:
    """Return named diagnostics; never silently repair fixture snapshots."""

    diagnostics: list[PhysicsGoldenDiagnostic] = []
    for golden in goldens:
        diagnostics.extend(_verify_one(golden))
    return diagnostics


def _golden_from_payload(payload: dict[str, Any], path: Path) -> PhysicsIrGolden:
    try:
        structure = payload["required_structure"]
        snapshot = payload["snapshot"]
        return PhysicsIrGolden(
            golden_id=str(payload["golden_id"]),
            family=str(payload["family"]),
            required_structure=tuple(str(item) for item in structure),
            provenance_required=bool(payload.get("provenance_required", True)),
            snapshot=dict(snapshot),
            oracle_promoted=bool(payload.get("oracle_promoted", False)),
        )
    except (KeyError, TypeError) as exc:
        raise ValueError(f"invalid Physics IR golden fixture: {path}") from exc


def _verify_one(golden: PhysicsIrGolden) -> list[PhysicsGoldenDiagnostic]:
    diagnostics: list[PhysicsGoldenDiagnostic] = []
    if not golden.golden_id or not golden.family:
        diagnostics.append(
            {
                "code": PHYSICS_IR_GOLDEN_ERROR,
                "message": f"golden fixture missing id/family: {golden.golden_id!r}",
            }
        )
    if golden.provenance_required:
        origin = golden.snapshot.get("source_origin")
        if origin is None:
            diagnostics.append(
                {
                    "code": PHYSICS_IR_PROVENANCE_ERROR,
                    "message": (
                        f"golden `{golden.golden_id}` snapshot lacks source ancestry"
                    ),
                }
            )
    return diagnostics
