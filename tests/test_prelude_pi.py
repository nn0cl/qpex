"""ADR 0062 / LISS-0007 — prelude classical constant `pi`."""

from __future__ import annotations

import io
import math
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.pipeline import compile_source  # noqa: E402
from compiler.qpex.run import run_source  # noqa: E402
from compiler.qpex.stdlib.prelude import PRELUDE_CONSTANTS, is_prelude  # noqa: E402


def test_prelude_exports_pi() -> None:
    assert is_prelude("pi")
    assert abs(PRELUDE_CONSTANTS["pi"] - math.pi) < 1e-15


def test_phase_with_pi_matches_literal() -> None:
    src_pi = """
package t
public fun main() {
    state b0 = coin()
    state b1 = coin()
    state idx = b0 * 2 + b1
    state marked = phase(idx, pi, 2)
    state amplified = grover_diffuse(marked)
    measure amplified
}
"""
    src_lit = """
package t
public fun main() {
    state b0 = coin()
    state b1 = coin()
    state idx = b0 * 2 + b1
    state marked = phase(idx, 3.141592653589793, 2)
    state amplified = grover_diffuse(marked)
    measure amplified
}
"""
    a = run_source(src_pi, seed=0, stdout=io.StringIO())
    b = run_source(src_lit, seed=0, stdout=io.StringIO())
    assert a.compile_ok and b.compile_ok
    assert a.eval.measure is not None and b.eval.measure is not None
    assert a.eval.measure.value == b.eval.measure.value == 2


def test_pi_half_in_phase() -> None:
    src = """
package t
public fun main() {
    state z = |0>
    state zp = phase(z, pi / 2.0)
    state viewed = inspect(zp)
    measure zp
}
"""
    r = run_source(src, seed=0, stdout=io.StringIO())
    assert r.compile_ok, r.diagnostics


def test_math_pi_alias_matches_pi() -> None:
    src = """
package t
public fun main() {
    state b0 = coin()
    state b1 = coin()
    state idx = b0 * 2 + b1
    state marked = phase(idx, Math.pi, 2)
    state amplified = grover_diffuse(marked)
    measure amplified
}
"""
    r = run_source(src, seed=0, stdout=io.StringIO())
    assert r.compile_ok, r.diagnostics
    assert r.eval.measure is not None
    assert r.eval.measure.value == 2


def test_state_plus_pi_type_error() -> None:
    src = """
package t
public fun main() {
    state psi = |0>
    state bad = psi + pi
    measure bad
}
"""
    compiled = compile_source(src)
    codes = {d.get("code") for d in compiled.diagnostics}
    assert "TYPE_MISMATCH" in codes or "EXPECT_CLASSICAL_ONLY_ERROR" in codes
