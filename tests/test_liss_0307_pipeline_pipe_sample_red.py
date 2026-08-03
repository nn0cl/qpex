"""LISS-0307: B17 pipeline pipe sample."""

from __future__ import annotations

from pathlib import Path

from compiler.staqex.host import run_path


def test_b17_pipeline_pipe_seed0() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "examples/basics/B17_pipeline_pipe/pipeline_pipe.sqx"
    )
    r = run_path(str(path), settings={"seed": 0})
    assert r.status == "succeeded", r.diagnostics
    # 3 |> bump |> dbl → 8
    assert r.measurements[-1].value == 8.0
