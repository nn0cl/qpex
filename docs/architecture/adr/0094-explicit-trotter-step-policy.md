# ADR 0094: Explicit Trotter step policy required for QASM emission

## Status

Accepted (Adjudicator, 2026-07-25) for [LISS-0050](../issues/LISS-0050-trotter-step-silent-clamp.md).

## Context

`compiler/qpex/backend/qasm/trotter.py`'s `trotter_step_count` silently
clamped the Trotter step count to `_MAX_STEPS = 64` — both the value derived
from `ceil(|t|*8)` when no step count is given, and an explicit caller
`steps=` value alike — with no diagnostic. `evolve psi under H for 100.0`
silently ran at `dt=1.5625` instead of the documented policy's `dt=0.125`
(12.5× coarser), exit `0`, no warning. Full reproduction and root cause are
recorded in LISS-0050.

Two properties of the existing codebase resolved the design question during
review:

1. **The SV simulator is unaffected.** `evolve` on the CPU/SV path uses
   `runtime/matrix.py`'s `expm_ih` (scaling-and-squaring + Taylor), not
   Trotter step counts at all. This defect is confined to QASM/gate
   lowering.
2. **A correct, already-shipped mechanism already exists.** LISS-0017 /
   ADR 0084's `using Suzuki(...)` policy already does this right:
   `suzuki_step_count` (`trotter.py:140`) preserves an explicit `steps=`
   value exactly and, in tolerance mode, derives a step count from the
   ADR 0084 error bound with **no upper clamp at all**
   (`return max(_MIN_STEPS, math.ceil(estimate))`). The MVP accepts only
   Suzuki order 2 (`typecheck.py`: "the MVP supports only Suzuki order 2").

Adjudicator's framing (2026-07-25): the developer must be **in control** of
the Trotter step count — either by stating it explicitly, or by explicitly
choosing an error tolerance — rather than the compiler silently picking a
number for them in either direction (a low arbitrary clamp, or an unbounded
default nobody asked for). Any safety threshold on the *derived* step count
must itself be something the developer configures, not a value the compiler
bakes in.

A survey of common quantum-computing practice (Qiskit's
`LieTrotter`/`SuzukiTrotter` synthesis classes, which take an explicit
`reps` as the primary interface) confirmed that explicit step-count control
is the prevailing practitioner norm; automatic tolerance-derived step
selection is the less common, more theoretical convenience. Requiring an
explicit policy is not a departure from practice — it matches it.

A direct probe of every example using the plain `evolve ... under H for t`
form (no `using Suzuki(...)`) found only 3 of the 9 actually reach the
Trotter step derivation at all when targeting QASM; the other 6 already
fail earlier for unrelated, pre-existing reasons (Fock-space Hamiltonians,
an unbound Operator reference, a non-static duration) and are unaffected by
this decision.

## Decision

1. **QASM emission of a plain `evolve ... under H for t` (no `using
   Suzuki(...)` clause) is rejected.** A new diagnostic,
   `QASM_TROTTER_STEPS_REQUIRED`, is raised instead of silently deriving a
   step count. The message states the requirement and the fix: add
   `using Suzuki(order = 2, steps = N)` for an exact step count, or
   `using Suzuki(order = 2, tolerance = X, error = Bound | EmpiricalEstimate)`
   for an error-bound-derived count.
2. **No new CLI flag or settings key is introduced.** The already-shipped
   `using Suzuki(...)` surface is the complete mechanism; adding a second,
   parallel "default step budget" setting would recreate the same
   ambiguity this ADR removes.
3. **`trotter_step_count` and `trotter_gates` (the first-order,
   silently-clamped functions) are removed**, not merely bypassed. Their
   only caller was the plain-`evolve` QASM path being retired by Decision 1;
   nothing else references them, and the project's only shipped MVP Suzuki
   order is 2 (`suzuki_gates`), so no first-order fallback is needed.
   `_MIN_STEPS` is retained (`suzuki_step_count` still uses it).
4. **Existing examples that reach the Trotter path are migrated**, not
   grandfathered: `tests/fixtures/qpex/quantum_ising_4.qpex`,
   `ising_model.qpex`, and `quantum_ising.qpex` gain an explicit
   `using Suzuki(order = 2, steps = N)` clause, where `N` is the value the
   old `ceil(|t|*8)` policy would have derived for that example's duration
   (5, 6, and 6 respectively — all well under the old 64 cap, so this
   migration does not change their simulated output beyond the accuracy
   improvement inherent in moving from first-order to the already-mandatory
   second-order Suzuki product).

## Non-goals

- No change to the SV/CPU `evolve` semantics (`expm_ih`); this is a
  QASM/gate-lowering-only decision.
- No change to the Suzuki S2 algorithm, the ADR 0084 error bound, or the
  "order 2 only" MVP restriction.
- No new CLI flag, environment variable, or settings key.
- No higher-order Suzuki (S4) or adaptive step selection (tracked
  separately, deferred, per `open-work-register.md`).

## Consequences

Positive:

- No more silent accuracy loss in QASM-lowered `evolve` circuits.
- No more silent override of an explicit user-supplied step count.
- One mechanism for Trotter step control (`using Suzuki(...)`) instead of
  two divergent ones (the old implicit default and the correct explicit
  policy).
- Dead, buggy code (`trotter_step_count`, `trotter_gates`) is deleted rather
  than left unreachable.

Negative:

- Breaking change: any program using a plain `evolve ... under H for t`
  that previously reached QASM lowering must now add a `using Suzuki(...)`
  clause. Three shipped examples required this migration.
- A user who wants "just give me something reasonable" for QASM emission no
  longer has that option; they must decide `steps=` or `tolerance=`.

## Verification contract

- `emit-qasm` on a plain `evolve ... under H for t` (no Suzuki policy)
  rejects with `QASM_TROTTER_STEPS_REQUIRED` and the actionable message
  above — never a silently clamped or silently unbounded step count.
- `emit-qasm` on `evolve ... under H for t using Suzuki(order = 2, steps =
  N)` uses exactly `N` steps, for any `N` including values that would have
  exceeded the old 64 cap.
- `emit-qasm` on `evolve ... under H for t using Suzuki(order = 2, tolerance
  = X, error = Bound)` derives a step count from the ADR 0084 bound with no
  upper clamp.
- The three migrated examples still emit valid QASM.
- Existing QASM/Trotter/Suzuki regressions remain green.
