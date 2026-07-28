#!/usr/bin/env python3
"""Run all QPex Spec Verification suites and emit compliance report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from harness.report import SuiteReport  # noqa: E402
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
    sv25_open_control,
    sv26_mixed_control,
    sv27_fock_quadrature,
    sv28_sparse_pauli,
    sv29_position_grid_ho,
    sv30_extended_unitarity,
    sv31_module_linker,
)

_SUITE_MODULES = (
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
    sv25_open_control,
    sv26_mixed_control,
    sv27_fock_quadrature,
    sv28_sparse_pauli,
    sv29_position_grid_ho,
    sv30_extended_unitarity,
    sv31_module_linker,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="QPex Spec Verification runner")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="write tests/spec_verification/reports/latest.{json,md}",
    )
    return parser.parse_args(argv)


def emit_reports_if_requested(
    report: SuiteReport,
    root: Path,
    *,
    write: bool,
) -> tuple[Path, Path] | None:
    """Write compliance reports only when explicitly requested (CI / --write-report)."""
    if not write:
        return None
    # Prefer the package module path if already loaded (tests may patch it);
    # fall back to the script-local `harness.report` import used by run_all.py.
    report_mod = sys.modules.get("tests.spec_verification.harness.report")
    if report_mod is None:
        report_mod = sys.modules.get("harness.report")
    if report_mod is None:
        try:
            from tests.spec_verification.harness import report as report_mod
        except ImportError:
            from harness import report as report_mod
    return report_mod.write_reports(report, root / "reports")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    results = []
    for mod in _SUITE_MODULES:
        results.extend(mod.run())

    report = SuiteReport(results=results)
    paths = emit_reports_if_requested(report, ROOT, write=args.write_report)

    print("=== QPex Spec Verification ===")
    print("Protocol: docs/testing/qpex-spec-verification-protocol.md")
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        extra = f" [{r.error_code}] {r.message}" if not r.passed else ""
        print(f"  [{mark}] {r.suite}/{r.case_id}: {r.title}{extra}")
    print("---")
    print(f"Spec Compliance Rate: {report.compliance_rate:.2f}%  ({report.passed}/{report.total})")
    print(f"Gate: {'PASS' if report.failed == 0 else 'FAIL'}")
    if paths is None:
        print("Report: (not written; pass --write-report to emit latest.json/md)")
    else:
        json_path, md_path = paths
        print(f"Report: {json_path}")
        print(f"Report: {md_path}")
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
