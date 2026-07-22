"""ADR 0060 / 0061 — Joint preserve, classical phase/times, config harvest."""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.pipeline import compile_path, compile_source  # noqa: E402
from compiler.qpex.run import run_path, run_source  # noqa: E402


def test_float_survives_grover_diffuse() -> None:
    src = """
package t
public fun main() {
    Float cfg = 2.0
    state b0 = coin()
    state b1 = coin()
    state idx = b0 * 2 + b1
    state marked = phase(idx, pi, cfg)
    state amplified = grover_diffuse(marked)
    state viewed = inspect(cfg)
    measure amplified
}
"""
    buf = io.StringIO()
    r = run_source(src, seed=0, stdout=buf)
    assert r.compile_ok
    assert r.eval.measure is not None
    assert "2.0" in buf.getvalue()


def test_phase_only_from_float_scalar() -> None:
    src = """
package t
public fun main() {
    Float target = 2.0
    state b0 = coin()
    state b1 = coin()
    state idx = b0 * 2 + b1
    state marked = phase(idx, pi, target)
    state amplified = grover_diffuse(marked)
    measure amplified
}
"""
    r = run_source(src, seed=0, stdout=io.StringIO())
    assert r.compile_ok
    assert r.eval.measure is not None
    assert r.eval.measure.value == 2


def test_evolve_times_classical_float() -> None:
    src = """
package t
public fun step(c, x) {
    Operator CoinOp = 0.7071067811865476 * (X + Z)
    state c = apply(CoinOp, c)
    state x = walk_shift(c, x)
}
public fun main() {
    Float n_steps = 2.0
    State<Qubit> c = |+>
    State<Position> x = dirac(0)
    State<(Qubit, Position)> (c, x) = c *|* x
    state (c, x) = evolve (c, x) times n_steps {
        step(c, x)
    }
    measure x
}
"""
    r = run_source(src, seed=0, stdout=io.StringIO())
    assert r.compile_ok, r.diagnostics
    assert r.eval.measure is not None


def test_classical_harvest_from_pub_fun(tmp_path: Path) -> None:
    lib = tmp_path / "hints.qpex"
    lib.write_text(
        """
package demo.hints
pub fun order_hint() {
    Float r = 4.0
}
""",
        encoding="utf-8",
    )
    main = tmp_path / "main.qpex"
    main.write_text(
        """
package demo
import demo.hints
public fun main() {
    state viewed = inspect(r)
    state bit = coin()
    measure bit
}
""",
        encoding="utf-8",
    )
    compiled = compile_path(main)
    assert not any(
        d.get("code") == "CONFIG_HARVEST_COLLISION_ERROR" for d in compiled.diagnostics
    )
    buf = io.StringIO()
    r = run_path(main, seed=0, stdout=buf)
    assert r.compile_ok, r.diagnostics
    assert "4.0" in buf.getvalue()


def test_harvest_collision_diagnostic(tmp_path: Path) -> None:
    lib = tmp_path / "hints.qpex"
    lib.write_text(
        """
package demo.hints
pub fun order_hint() {
    Float r = 4.0
}
""",
        encoding="utf-8",
    )
    main = tmp_path / "main.qpex"
    main.write_text(
        """
package demo
import demo.hints
public fun main() {
    Float r = 9.0
    state v = inspect(r)
    measure v
}
""",
        encoding="utf-8",
    )
    compiled = compile_path(main)
    assert any(
        d.get("code") == "CONFIG_HARVEST_COLLISION_ERROR" for d in compiled.diagnostics
    )


def test_city_route_example_linked() -> None:
    path = _REPO / "examples/12_city_route_search/main_city_route.qpex"
    r = run_path(path, seed=0, stdout=io.StringIO())
    assert r.compile_ok
    assert r.eval.measure is not None
    assert r.eval.measure.value == 2
