"""AT-TDD LISS-0228: Joint apply(qft/iqft/cqft) runtime."""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import run_source  # noqa: E402


def test_qft_iqft_roundtrip_two_wires() -> None:
    result = run_source(
        """
package t
pub fn main() -> Unit {
  QubitRegister<2> reg = system()
  Operator F = qft(reg)
  Operator Fi = iqft(reg)
  state a = |0>
  state b = |1>
  state (a, b) = apply(F, a, b)
  state (a, b) = apply(Fi, a, b)
  state a = |0>
  measure b
}
""",
        settings={"seed": 0},
        stdout=io.StringIO(),
    )
    assert result.status == "succeeded", result.diagnostics
    msgs = " ".join(str(d.get("message", "")) for d in result.diagnostics)
    assert "cannot compile operator node Call" not in msgs


def test_cqft_apply_three_wires() -> None:
    result = run_source(
        """
package t
pub fn main() -> Unit {
  QubitRegister<1> ctrl = system()
  QubitRegister<2> reg = system()
  Operator CF = cqft(ctrl, reg)
  state c = |1>
  state t0 = |0>
  state t1 = |0>
  state (c, t0, t1) = apply(CF, c, t0, t1)
  state t0 = |0>
  state t1 = |0>
  measure c
}
""",
        settings={"seed": 0},
        stdout=io.StringIO(),
    )
    assert result.status == "succeeded", result.diagnostics


if __name__ == "__main__":
    test_qft_iqft_roundtrip_two_wires()
    test_cqft_apply_three_wires()
    print("PASS LISS-0228")
