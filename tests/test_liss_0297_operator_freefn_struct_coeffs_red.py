"""LISS-0297: Operator free-fn with struct field coefficients."""

from __future__ import annotations

from compiler.staqex.host import run_source


def test_operator_freefn_direct_struct_field_coeff() -> None:
    """``return k.c * Z[0]`` with object param (caller name may differ)."""
    src = """
package p
namespace D {
  pub struct Coeffs { val c: Float }
}
pub fn h_of(k: D.Coeffs) -> Operator {
  return k.c * Z[0]
}
pub fn main() -> Unit {
  D.Coeffs pack = D.Coeffs(0.5)
  Operator H = h_of(pack)
  state s = |+>
  state s = evolve s under H for 0.1
  measure s
}
"""
    r = run_source(src, settings={"seed": 0})
    assert r.status == "succeeded", r.diagnostics


def test_operator_freefn_intermediate_float_from_struct() -> None:
    src = """
package p
namespace D {
  pub struct Coeffs { val congestion: Float val fairness: Float }
}
pub fn drive_h(c: D.Coeffs) -> Operator {
  Float cong = c.congestion
  Float fair = c.fairness
  Operator H = cong * (Z[0] * Z[1]) + fair * (X[0] + X[1])
  return H
}
pub fn main() -> Unit {
  D.Coeffs coeffs = D.Coeffs(0.6, 0.5)
  Operator H = drive_h(coeffs)
  state a = |+>
  state b = |0>
  state (a, b) = evolve (a, b) under H for 0.2
  measure a tracing_out b
}
"""
    r = run_source(src, settings={"seed": 0})
    assert r.status == "succeeded", r.diagnostics


def test_operator_freefn_multi_field_direct_opattr() -> None:
    src = """
package p
namespace D {
  pub struct Coeffs { val congestion: Float val fairness: Float }
}
pub fn drive_h(c: D.Coeffs) -> Operator {
  return c.congestion * (Z[0] * Z[1]) + c.fairness * (X[0] + X[1])
}
pub fn main() -> Unit {
  D.Coeffs coeffs = D.Coeffs(0.4, 0.3)
  Operator H = drive_h(coeffs)
  state a = |+>
  state b = |0>
  state (a, b) = evolve (a, b) under H for 0.15
  measure a tracing_out b
}
"""
    r = run_source(src, settings={"seed": 0})
    assert r.status == "succeeded", r.diagnostics
