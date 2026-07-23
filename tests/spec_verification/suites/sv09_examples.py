"""SV-09: Official physics examples — check + run regression."""

from __future__ import annotations

import io
import sys
from pathlib import Path

from harness import AssertionFailure
from harness.report import CaseResult

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.pipeline import compile_path, compile_source  # noqa: E402
from compiler.qpex.run import run_path, run_source  # noqa: E402

EXAMPLES = [
    ("01_classical_mechanics", "phase_space.qpex"),
    ("02_quantum_basics", "double_slit.qpex"),
    ("02_quantum_basics", "ket_evolve_expect.qpex"),
    ("03_quantum_information", "bell_state.qpex"),
    ("03_quantum_information", "controlled_unitary.qpex"),
    ("03_quantum_information", "toffoli.qpex"),
    ("03_quantum_information", "open_control.qpex"),
    ("03_quantum_information", "mixed_control.qpex"),
    ("03_quantum_information", "portable_bell_qpu.qpex"),
    ("04_quantum_algorithms", "grover_search.qpex"),
    ("05_harmonic_oscillator", "classical_oscillator.qpex"),
    ("05_harmonic_oscillator", "quantum_oscillator.qpex"),
    ("05_harmonic_oscillator", "xp_oscillator.qpex"),
    ("05_harmonic_oscillator", "grid_oscillator.qpex"),
    ("06_statistical_physics", "ising_model.qpex"),
    ("06_statistical_physics", "quantum_ising.qpex"),
    ("06_statistical_physics", "quantum_ising_4.qpex"),
    ("07_quantum_walk", "quantum_vs_classical_walk.qpex"),
    ("07_quantum_walk", "dtqw.qpex"),
    ("07_quantum_walk", "classical_walk.qpex"),
    ("08_gauge_symmetry", "gauge_symmetry.qpex"),
    ("09_complex_simulations", "main_quantum_walk.qpex"),
    ("10_topological_physics", "main_ssh_topological.qpex"),
    ("11_shor_rsa_toy", "main_shor_period.qpex"),
    ("12_city_route_search", "main_city_route.qpex"),
    ("13_deep_space_qkd_toy", "main_deep_space_qkd.qpex"),
    ("14_genome_motif_grover", "main_genome_motif.qpex"),
    ("15_orbital_mesh_walk", "main_orbital_mesh.qpex"),
    ("16_quantum_observatory", "main_observatory.qpex"),
    ("17_static_register_foreach", "main_static_register.qpex"),
]

HARD = {
    "FORBIDDEN_KEYWORD",
    "EARLY_COLLAPSE_ERROR",
    "NESTED_WHEN_ERROR",
    "PARSE_ERROR",
    "LEX_ERROR",
}


def run() -> list[CaseResult]:
    out: list[CaseResult] = []
    root = _REPO / "examples"

    for folder, fname in EXAMPLES:
        path = root / folder / fname
        case_id = f"sv09-{folder[:2]}-{fname.replace('.qpex', '')}"
        title = f"examples/{folder}/{fname}"
        try:
            if not path.is_file():
                raise AssertionFailure("PARSE_ERROR", f"missing {path}")
            # ADR 0054+: path-link when the entry imports other units
            source = path.read_text(encoding="utf-8")
            needs_link = "\nimport " in source or source.startswith("import ")
            if needs_link:
                compiled = compile_path(path)
                hard = [d for d in compiled.diagnostics if d.get("code") in HARD]
                if hard:
                    raise AssertionFailure(hard[0]["code"], str(hard))
                retired = [
                    d for d in compiled.diagnostics if d.get("code") == "RETIRED_KEYWORD"
                ]
                if retired:
                    raise AssertionFailure("RETIRED_KEYWORD", str(retired))
                buf = io.StringIO()
                result = run_path(path, seed=0, stdout=buf)
            else:
                compiled = compile_source(source)
                hard = [d for d in compiled.diagnostics if d.get("code") in HARD]
                if hard:
                    raise AssertionFailure(hard[0]["code"], str(hard))
                retired = [
                    d for d in compiled.diagnostics if d.get("code") == "RETIRED_KEYWORD"
                ]
                if retired:
                    raise AssertionFailure("RETIRED_KEYWORD", str(retired))
                buf = io.StringIO()
                result = run_source(source, seed=0, stdout=buf)
            if not result.compile_ok:
                raise AssertionFailure("PARSE_ERROR", str(result.diagnostics))
            if result.eval.measure is None and not result.eval.joint.is_vacuum():
                # must have terminal measure outcome (vacuum measure OK)
                raise AssertionFailure("EARLY_COLLAPSE_ERROR", "missing measure result")

            out.append(
                CaseResult(
                    "SV-09",
                    case_id,
                    title,
                    True,
                    ["qpex check", "qpex run"],
                )
            )
        except AssertionFailure as e:
            out.append(
                CaseResult(
                    "SV-09",
                    case_id,
                    title,
                    False,
                    error_code=e.code,
                    message=str(e),
                )
            )
        except Exception as e:  # noqa: BLE001 — surface kernel errors in report
            out.append(
                CaseResult(
                    "SV-09",
                    case_id,
                    title,
                    False,
                    error_code="UNEXPECTED_EXCEPTION",
                    message=str(e),
                )
            )

    # Index README exists
    try:
        if not (root / "README.md").is_file():
            raise AssertionFailure("PARSE_ERROR", "examples/README.md missing")
        for folder, _ in EXAMPLES:
            if not (root / folder / "README.md").is_file():
                raise AssertionFailure("PARSE_ERROR", f"{folder}/README.md missing")
        out.append(
            CaseResult(
                "SV-09",
                "sv09-docs",
                "examples READMEs present",
                True,
                ["docs"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-09",
                "sv09-docs",
                "examples READMEs",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    return out
