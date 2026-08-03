# LISS-0207: Residual regression cluster (3 suites, distinct causes)

## Metadata

- Local issue ID: LISS-0207
- Status: **complete** — 2026-08-01 (WP-0075)
- Phase: phase-0-design
- Type: bug
- Priority: P2
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Intent

The three failing suites that do not belong to any other cluster. Each has its
own cause; they are grouped only so the sweep's 50 failures are fully accounted
for, and may be split once triaged.

## Evidence (reproduced 2026-08-01)

| Suite | Failure |
|---|---|
| `tests/test_operator_algebra_red.py` | `OPERATOR_DOMAIN_ERROR: commutator operands require the same Hilbert-space domain` on a program the suite asserts must compile |
| `tests/test_evolve_until_runtime_red.py` | `assert with_until == "succeeded"` — the bounded `evolve … until` run does not reach a succeeded Job status |
| `tests/test_kernel_classical_boundary_red.py` | `assert len(re.findall(r"(?m)^h q\[.*forEach", qasm)) == 3` — QASM `forEach` unrolling emits the wrong gate count |

The `evolve … until` and `forEach` cases both touch the QPU/QASM lane, where
[`staqex-v1-qpu-capability-honesty.md`](../specs/staqex-v1-qpu-capability-honesty.md)
already records `evolve … until` as not lowerable as a runtime loop. Whether
these suites are asserting across that documented boundary needs checking
before any code change.

## Adjudicator decision points

1. `test_operator_algebra_red`: is the commutator domain check newly
   over-strict, or was the suite relying on implicit domain widening that
   ADR 0058 acting-space typing removed?
2. The two QPU-lane suites: are they asserting behavior the capability-honesty
   spec says is out of scope? If so the suites are wrong, not the Kernel.
3. Whether to split this Issue into three once (1) and (2) are answered.

## Exit

- [x] Each of the three triaged to a named root cause
- [x] Suites green, or retired with a recorded reason if they assert across a
      documented capability boundary
- [x] Split decision recorded

## Non-goals

The five other regression clusters; test-harness defects
([LISS-0208](../architecture/documentation-compression-map.md)); enabling CI
([LISS-0209](LISS-0209-ci-runs-test-suite.md)).

## Resolution (WP-0075)

Triaged without split:

1. `test_operator_algebra_red`: `Operator A = adjoint(X)` must parse as
   expression `Call` (`_ALGEBRA_EXPR_CALLEES`), not OpDSL `OpCall`; inner/outer
   suite uncomputes live args (LISS-0229 pattern).
2. `test_evolve_until_runtime_red`: unused `coin()` noise failed LINEAR after
   HARD_CODES unification — removed (test compares Job status only).
3. `test_kernel_classical_boundary_red`: QASM unrolling emits `h q[i];` without
   a `forEach` comment — regex matches `^h q\[` ×3.
