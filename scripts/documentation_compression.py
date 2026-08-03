#!/usr/bin/env python3
"""Plan and apply the WP-0090 documentation source-record compaction."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_TAG = "docs/pre-canonicalization-2026-08-03"
MAP_PATH = ROOT / "docs/architecture/documentation-compression-map.md"
SOURCE_ROOTS = {
    "issue": ROOT / "docs/issues",
    "work-plan": ROOT / "docs/work-plans",
    "trace": ROOT / "docs/collaboration/traces",
}
DESTINATION = {
    "issue": "docs/architecture/open-work-register.md",
    "work-plan": "docs/architecture/open-work-register.md",
    "trace": "docs/architecture/documentation-compression-map.md",
}
UNRESOLVED_WORDS = (
    "open",
    "blocked",
    "proposed",
    "deferred",
    "awaiting",
    "investigation",
    "pending",
    "reopened",
    "residual",
    "follow-up open",
    "remains open",
)
COMPLETED_WORDS = ("complete", "completed", "closed", "merged", "superseded", "done")
PROTECTED_ISSUES = {"LISS-0075"}


@dataclass(frozen=True)
class Candidate:
    kind: str
    path: Path
    reason: str


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def all_markdown() -> list[Path]:
    return sorted((ROOT / "docs").rglob("*.md"))


def source_texts() -> dict[Path, str]:
    return {path: path.read_text(encoding="utf-8", errors="replace") for path in all_markdown()}


def identifier(path: Path) -> str:
    match = re.match(r"(LISS-\d+|WP-\d+|ADR[- ]?\d+)", path.stem, re.IGNORECASE)
    return match.group(1).upper().replace("ADR-", "ADR ") if match else ""


def explicit_status(text: str) -> str:
    match = re.search(
        r"(?im)^\s*(?:[-*]\s*)?(?:\|\s*)?status(?:/phase)?\s*(?:\|\s*)?:?\s*\*?\*?([^\n|]+)",
        text,
    )
    return match.group(1).strip().lower() if match else ""


def is_completed(text: str) -> bool:
    status = explicit_status(text)
    return bool(status and any(word in status for word in COMPLETED_WORDS))


def has_unresolved_signal(text: str) -> bool:
    sample = text[:12000].lower()
    return any(word in sample for word in UNRESOLVED_WORDS)


def is_pointer_stub(text: str) -> bool:
    return "**historical — compacted**" in text


def batch_work_plan_ids() -> set[str]:
    result: set[str] = set()
    for path in (ROOT / "docs/collaboration/reviews").glob("execution-batch-*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        work_plan_id = data.get("work_plan_id")
        if isinstance(work_plan_id, str):
            result.add(work_plan_id)
    return result


def historical_candidate(kind: str, path: Path, text: str) -> bool:
    if is_pointer_stub(text):
        return False
    if path == ROOT / "docs/work-plans/WP-0090-documentation-canonicalization.md":
        return False
    if kind == "issue":
        if identifier(path) in PROTECTED_ISSUES or not is_completed(text):
            return False
        return not has_unresolved_signal(text)
    if kind == "work-plan":
        if identifier(path) in batch_work_plan_ids() or not is_completed(text):
            return False
        return not has_unresolved_signal(text)
    if kind == "trace":
        if any(word in path.name.lower() for word in ("approval", "review", "final", "completion", "handoff", "blocked", "pending")):
            return False
        dated_old = bool(re.match(r"2026-07-", path.name))
        return (dated_old or is_completed(text)) and not has_unresolved_signal(text)
    return False


def candidates() -> list[Candidate]:
    texts = source_texts()
    result: list[Candidate] = []
    for kind, root in SOURCE_ROOTS.items():
        for path in sorted(root.glob("*.md")):
            text = texts[path]
            if historical_candidate(kind, path, text):
                result.append(Candidate(kind, path, "historical record has no unresolved obligation or current review role"))
    return result


def baseline_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{BASELINE_TAG}^{{commit}}"], cwd=ROOT, text=True
    ).strip()


def title(text: str, path: Path) -> str:
    match = re.search(r"(?m)^#\s+(.+)$", text)
    return match.group(1).strip() if match else path.stem


def relative_link(path: Path, target: str) -> str:
    return Path(target).relative_to(path.parent.relative_to(ROOT)).as_posix() if False else target


def stub(row: Candidate, source_commit: str, original: str) -> str:
    if row.kind in {"issue", "work-plan"}:
        adr_link = "../architecture/adr/0187-documentation-source-record-compaction.md"
        destination_link = "../architecture/open-work-register.md"
    else:
        adr_link = "../../architecture/adr/0187-documentation-source-record-compaction.md"
        destination_link = "../../architecture/documentation-compression-map.md"
    return "\n".join(
        [
            f"# {title(original, row.path)}",
            "",
            "| Field | Value |",
            "|---|---|",
            "| Status | **historical — compacted** |",
            f"| Canonical rule | [ADR 0187]({adr_link}) |",
            f"| Current meaning | [canonical destination]({destination_link}) |",
            f"| Original source commit | `{source_commit}` |",
            f"| Baseline tag | `{BASELINE_TAG}` |",
            f"| Original path | `{relative(row.path)}` |",
            f"| Recovery | `git show {BASELINE_TAG}:{relative(row.path)}` |",
            "",
            "This historical record remains at its stable path as a pointer. The",
            "ADR/specification and current register are the source of truth.",
            "",
        ]
    )


def inventory() -> tuple[list[str], list[Path]]:
    before = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE_TAG, "docs"], cwd=ROOT, text=True
    ).splitlines()
    after = [path for path in (ROOT / "docs").rglob("*") if path.is_file()]
    return before, after


def count(paths: list[str] | list[Path], prefix: str) -> int:
    return sum(1 for path in paths if str(path).startswith(prefix))


def previous_removed() -> list[Candidate]:
    if not MAP_PATH.exists():
        return []
    result: list[Candidate] = []
    in_removed = False
    for line in MAP_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        if line == "## Removed records":
            in_removed = True
            continue
        if in_removed and line.startswith("## "):
            break
        match = re.match(r"\| `([^`]+)` \| `[^`]+` \| `[^`]+` \| `[^`]+` \| `[^`]+` \| (.+) \|$", line)
        if not match:
            continue
        path = ROOT / match.group(1)
        if path.exists():
            continue
        kind = "issue" if "/issues/" in match.group(1) else "work-plan" if "/work-plans/" in match.group(1) else "trace"
        result.append(Candidate(kind, path, match.group(2)))
    return result


def render_map(compacted: list[Candidate], removed: list[Candidate], commit: str) -> str:
    before, after = inventory()
    lines = [
        "# Documentation compression map", "",
        "This file is generated and updated as part of WP-0090. It is the recoverability",
        "index for ADR, Issue, Work Plan, and Trace source records compacted or removed",
        "from the current tree.", "", "## Baseline", "",
        "| Field | Value |", "|---|---|", f"| Tag | `{BASELINE_TAG}` |",
        f"| Baseline commit | `{commit}` |", "| Recovery command | `git show <source_tag>:<source_path>` |", "",
        "## Inventory delta", "", "| Area | Before (baseline) | After this batch | Delta |", "|---|---:|---:|---:|",
        f"| All `docs/` files | {len(before)} | {len(after)} | {len(after) - len(before):+d} |",
        f"| Markdown files | {sum(path.endswith('.md') for path in before)} | {sum(path.suffix == '.md' for path in after)} | {sum(path.suffix == '.md' for path in after) - sum(path.endswith('.md') for path in before):+d} |",
        f"| ADRs | {count(before, 'docs/architecture/adr/')} | {count(after, str(ROOT / 'docs/architecture/adr/'))} | {count(after, str(ROOT / 'docs/architecture/adr/')) - count(before, 'docs/architecture/adr/'):+d} |",
        f"| Issues | {count(before, 'docs/issues/')} | {count(after, str(ROOT / 'docs/issues/'))} | {count(after, str(ROOT / 'docs/issues/')) - count(before, 'docs/issues/'):+d} |",
        f"| Work Plans | {count(before, 'docs/work-plans/')} | {count(after, str(ROOT / 'docs/work-plans/'))} | {count(after, str(ROOT / 'docs/work-plans/')) - count(before, 'docs/work-plans/'):+d} |",
        f"| Traces | {count(before, 'docs/collaboration/traces/')} | {count(after, str(ROOT / 'docs/collaboration/traces/'))} | {count(after, str(ROOT / 'docs/collaboration/traces/')) - count(before, 'docs/collaboration/traces/'):+d} |",
        "", "## Compacted records", "", "| source_path | source_commit | source_tag | destination | classification | reason |", "|---|---|---|---|---|---|",
    ]
    for row in compacted:
        lines.append(f"| `{relative(row.path)}` | `{commit}` | `{BASELINE_TAG}` | `{DESTINATION[row.kind]}` | `compact-pointer` | {row.reason} |")
    lines.extend(["", "## Removed records", "", "| source_path | source_commit | source_tag | destination | classification | reason |", "|---|---|---|---|---|---|"])
    for row in removed:
        lines.append(f"| `{relative(row.path)}` | `{commit}` | `{BASELINE_TAG}` | `{DESTINATION[row.kind]}` | `extract-and-remove` | {row.reason} |")
    lines.extend(["", "## Unresolved review", "", "Protected, active, or ambiguous records remain at their original paths and are not silently compacted.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write pointer stubs and the compression map")
    args = parser.parse_args()
    rows = candidates()
    commit = baseline_commit()
    print(f"baseline={BASELINE_TAG} commit={commit}")
    for row in rows:
        print(f"{row.kind}\t{relative(row.path)}\t{row.reason}")
    print(f"candidate_count={len(rows)}")
    if not args.apply:
        return 0
    removed = previous_removed()
    MAP_PATH.write_text(render_map(rows, removed, commit), encoding="utf-8")
    for row in rows:
        row.path.write_text(stub(row, commit, row.path.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
