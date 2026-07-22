"""Spec Compliance Rate reporting."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CaseResult:
    suite: str
    case_id: str
    title: str
    passed: bool
    assertions: list[str] = field(default_factory=list)
    error_code: str | None = None
    message: str | None = None


@dataclass
class SuiteReport:
    results: list[CaseResult]

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def compliance_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return 100.0 * self.passed / self.total


def write_reports(report: SuiteReport, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "protocol": "docs/testing/qpex-spec-verification-protocol.md",
        "total": report.total,
        "passed": report.passed,
        "failed": report.failed,
        "spec_compliance_rate": round(report.compliance_rate, 4),
        "gate": "PASS" if report.failed == 0 else "FAIL",
        "cases": [asdict(r) for r in report.results],
    }
    json_path = out_dir / "latest.json"
    md_path = out_dir / "latest.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# QPex Spec Compliance Report",
        "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Spec Compliance Rate: **{payload['spec_compliance_rate']}%**",
        f"- Gate: **{payload['gate']}** ({report.passed}/{report.total} passed)",
        "",
        "| Suite | Case | Result | Assertions |",
        "|-------|------|--------|------------|",
    ]
    for r in report.results:
        mark = "PASS" if r.passed else "FAIL"
        asserts = ", ".join(r.assertions) if r.assertions else "—"
        detail = r.case_id
        if not r.passed and r.error_code:
            detail += f" (`{r.error_code}`)"
        lines.append(f"| {r.suite} | {detail} | {mark} | {asserts} |")
    lines.append("")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
