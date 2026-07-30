#!/usr/bin/env python3
"""Check the synchronized completion evidence for one local Issue."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_COMPLETION_WORDING = (
    "merge pending",
    "merge candidate",
    "ready for PR",
    "awaits final review",
    "pending the merge",
    "final review gated",
    "ci pending",
)


def fail(message: str) -> None:
    print(f"completion packet: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    raise AssertionError("unreachable")


def issue_section(work_plan: str, issue_id: str) -> str:
    marker = f"[{issue_id}]"
    start = work_plan.find(marker)
    if start < 0:
        return ""
    next_heading = work_plan.find("\n### ", start + len(marker))
    return work_plan[start : next_heading if next_heading >= 0 else None]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Issue, work-plan, and trace completion evidence."
    )
    parser.add_argument("--issue", type=Path, required=True)
    parser.add_argument("--work-plan", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--pr", type=int, required=True)
    args = parser.parse_args()

    issue_id_match = re.search(r"LISS-\d{4}", args.issue.name)
    if issue_id_match is None:
        fail(f"issue filename has no LISS identifier: {args.issue}")
    issue_id = issue_id_match.group(0)
    pr_evidence = f"PR #{args.pr}"
    documents = {
        "issue": read(args.issue),
        "work-plan": read(args.work_plan),
        "trace": read(args.trace),
    }

    issue_status = re.search(
        r"Status/phase:\s*\*\*complete\*\*", documents["issue"], re.IGNORECASE
    )
    if issue_status is None:
        fail("Issue is not marked complete")

    for name, content in documents.items():
        if pr_evidence not in content:
            fail(f"{name} does not contain {pr_evidence}")
        for phrase in FORBIDDEN_COMPLETION_WORDING:
            if phrase.casefold() in content.casefold():
                fail(f"{name} contains pre-merge wording: {phrase!r}")

    if not re.search(r"\bcomplete\b", issue_section(documents["work-plan"], issue_id), re.IGNORECASE):
        fail(f"work-plan does not mark {issue_id} complete")

    print(
        f"completion packet: PASS: {issue_id}, {pr_evidence}, "
        "Issue/work-plan/trace synchronized"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
