"""AT-TDD LISS-0229: inner/outer Joint runtime Call."""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import run_source  # noqa: E402


def test_inner_identical_plus() -> None:
    result = run_source(
        """
package t
pub fn main() -> Unit {
  state a = |+>
  state b = |+>
  state ov = inner(a, b)
  state a = |0>
  state b = |0>
  measure ov
}
""",
        settings={"seed": 0},
        stdout=io.StringIO(),
    )
    assert result.status == "succeeded", result.diagnostics


def test_inner_orthogonal_zero() -> None:
    result = run_source(
        """
package t
pub fn main() -> Unit {
  state z = |0>
  state o = |1>
  state ov = inner(z, o)
  state z = |0>
  state o = |0>
  measure ov
}
""",
        settings={"seed": 0},
        stdout=io.StringIO(),
    )
    assert result.status == "succeeded", result.diagnostics


def test_outer_apply() -> None:
    result = run_source(
        """
package t
pub fn main() -> Unit {
  state a = |+>
  state b = |0>
  Operator P = outer(a, b)
  state w = |0>
  state w = apply(P, w)
  state a = |0>
  state b = |0>
  measure w
}
""",
        settings={"seed": 0},
        stdout=io.StringIO(),
    )
    assert result.status == "succeeded", result.diagnostics
    msgs = " ".join(str(d.get("message", "")) for d in result.diagnostics)
    assert "unknown function" not in msgs


if __name__ == "__main__":
    test_inner_identical_plus()
    test_inner_orthogonal_zero()
    test_outer_apply()
    print("PASS LISS-0229")
