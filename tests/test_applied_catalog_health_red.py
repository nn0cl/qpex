"""Regression: applied catalog A01–A11 remains green after LINEAR/type changes."""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex import compile_path, run_path  # noqa: E402

_APPLIED = [
    "examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.sqx",
    "examples/applied/A02_robot_graph_planner/main_robot_graph_planner.sqx",
    "examples/applied/A03_h2_vqe/main_h2_vqe.sqx",
    "examples/applied/A04_hp_protein_folding/main_hp_protein_folding.sqx",
    "examples/applied/A05_qaoa_portfolio/main_qaoa_portfolio.sqx",
    "examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx",
    "examples/applied/A07_open_system_sensor/main_open_system_sensor.sqx",
    "examples/applied/A08_entangled_compute_ancilla/main_entangled_compute_ancilla.sqx",
    "examples/applied/A09_qkd_corridor/main_qkd_corridor.sqx",
    "examples/applied/A10_mission_observatory/main_mission_observatory.sqx",
    "examples/applied/A11_noether_forge/main_static.sqx",
]


def _hard(diags: list[dict]) -> list[dict]:
    return [
        d
        for d in diags
        if not str(d.get("code", "")).startswith("QSEM_")
        and d.get("code") != "MULTI_REGISTER_INDEX_AMBIGUOUS"
    ]


def test_applied_catalog_a01_a11_compile_and_run_green() -> None:
    failures: list[str] = []
    for rel in _APPLIED:
        path = _REPO / rel
        compiled = compile_path(str(path))
        hard_compile = _hard(compiled.diagnostics)
        if hard_compile and not compiled.ok:
            failures.append(f"{rel}: compile {[d.get('code') for d in hard_compile]}")
            continue
        result = run_path(
            str(path),
            settings={"target": "local", "seed": 0},
            stdout=io.StringIO(),
        )
        hard_run = _hard(result.diagnostics)
        if result.status != "succeeded" or hard_run:
            failures.append(
                f"{rel}: run status={result.status} "
                f"codes={[d.get('code') for d in hard_run]}"
            )
    assert not failures, "\n".join(failures)


if __name__ == "__main__":
    test_applied_catalog_a01_a11_compile_and_run_green()
    print("OK — applied catalog A01–A11 green")
