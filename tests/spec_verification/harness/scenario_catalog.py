"""Parse the LISS-0071 normative conformance scenario catalog markdown."""

from __future__ import annotations

import re
from pathlib import Path

ENVELOPES = [f"E-{n:02d}" for n in range(1, 15)]
TAXONOMY = frozenset({"valid", "invalid", "semantic", "numerical", "provenance", "backend"})
STATUSES = frozenset({"covered", "gap", "deferred"})
SCENARIO_ID = re.compile(r"^E\d{2}-\d{3}$")

_DEFAULT_CATALOG = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "specs"
    / "qpex-v1-conformance-scenario-catalog.md"
)


def catalog_path() -> Path:
    return _DEFAULT_CATALOG


def normative_section(text: str) -> str:
    """Return the ## Catalog (Normative) section body (until next ##)."""
    m = re.search(
        r"^## Catalog \(Normative\)\s*\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not m:
        raise AssertionError("catalog must contain a '## Catalog (Normative)' section")
    return m.group(1)


def parse_rows(section: str) -> list[dict[str, str]]:
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        raise AssertionError("normative catalog table missing")
    header = [c.strip().strip("`") for c in lines[0].strip("|").split("|")]
    for col in ("scenario_id", "envelope", "class", "oracle", "status"):
        if col not in header:
            raise AssertionError(f"missing column {col!r} in {header}")
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(header):
            continue
        row = {header[i]: cells[i] for i in range(len(header))}
        if row.get("scenario_id", "").startswith("scenario_id"):
            continue
        rows.append(row)
    if not rows:
        raise AssertionError("normative catalog has no data rows")
    return rows


def load_normative_rows(path: Path | None = None) -> list[dict[str, str]]:
    text = (path or catalog_path()).read_text(encoding="utf-8")
    return parse_rows(normative_section(text))


def status_field(text: str) -> str:
    m = re.search(r"\|\s*Status\s*\|\s*(.*?)\s*\|", text)
    if not m:
        raise AssertionError("Status field missing")
    return m.group(1)
