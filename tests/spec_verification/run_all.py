#!/usr/bin/env python3
"""Run all QPex Spec Verification suites and emit compliance report."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from harness.report import SuiteReport, write_reports  # noqa: E402
from suites import (  # noqa: E402
    sv01_lifting,
    sv02_when,
    sv03_failure_superposition,
    sv04_early_collapse,
    sv05_vacuum_compare,
    sv06_package_vocab,
    sv07_kernel_eval,
    sv08_ecosystem,
    sv09_examples,
    sv10_backend_targets,
    sv11_qasm_transpilation,
    sv13_physical_syntax,
    sv14_complex_phase_interference,
    sv15_type_first_dimensions,
    sv16_structured_program_syntax,
    sv17_quantum_mechanics_syntax,
    sv18_physical_axioms,
    sv19_arbitrary_hamiltonian,
    sv20_dtqw_apply,
    sv21_capply,
    sv22_typed_product,
    sv23_unitarity,
    sv24_multi_capply,
)


def main() -> int:
    results = []
    for mod in (
        sv01_lifting,
        sv02_when,
        sv03_failure_superposition,
        sv04_early_collapse,
        sv05_vacuum_compare,
        sv06_package_vocab,
        sv07_kernel_eval,
        sv08_ecosystem,
        sv09_examples,
        sv10_backend_targets,
        sv11_qasm_transpilation,
        sv13_physical_syntax,
        sv14_complex_phase_interference,
        sv15_type_first_dimensions,
        sv16_structured_program_syntax,
        sv17_quantum_mechanics_syntax,
        sv18_physical_axioms,
        sv19_arbitrary_hamiltonian,
        sv20_dtqw_apply,
        sv21_capply,
        sv22_typed_product,
        sv23_unitarity,
        sv24_multi_capply,
    ):
        results.extend(mod.run())

    report = SuiteReport(results=results)
    json_path, md_path = write_reports(report, ROOT / "reports")

    print("=== QPex Spec Verification ===")
    print(f"Protocol: docs/testing/qpex-spec-verification-protocol.md")
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        extra = f" [{r.error_code}] {r.message}" if not r.passed else ""
        print(f"  [{mark}] {r.suite}/{r.case_id}: {r.title}{extra}")
    print("---")
    print(f"Spec Compliance Rate: {report.compliance_rate:.2f}%  ({report.passed}/{report.total})")
    print(f"Gate: {'PASS' if report.failed == 0 else 'FAIL'}")
    print(f"Report: {json_path}")
    print(f"Report: {md_path}")
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
