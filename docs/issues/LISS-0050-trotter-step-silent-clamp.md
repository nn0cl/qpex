# LISS-0050: Silent Trotter step-count clamp in QASM lowering

## Metadata

- Local issue ID: LISS-0050
- GitHub issue: none
- Status: **Complete** — Adjudicator final review approved 2026-07-25
- Phase: Architecture Path (2026-07-25, ADR 0094) → Phase 1 Red → Phase 2
  Green → Phase 3 Refactor → closed
- Type: bug / silent precision loss
- Priority: P1
- Initial planning size: S
- Current planning size: S
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: `feature/liss-0050-explicit-trotter-steps`

## Summary

`compiler/qpex/backend/qasm/trotter.py` hard-clamps the Trotter step count to
`_MAX_STEPS = 64` — silently, with no diagnostic — whenever the derived or
user-requested step count exceeds that bound. This both (a) is a hard limit
whose only stated justification is output size ("Cap slices so NISQ emit
stays bounded"), the exact pattern the Adjudicator ruled out during
[LISS-0032](LISS-0032-typed-second-quantized-operators.md) Architecture Path
review (2026-07-25): "パフォーマンスを理由とした過剰なスコープ制限や厳しい
ハードリミットの導入は不要"; and (b) silently degrades simulation accuracy
without telling the physicist, which is the same class of failure the
Adjudicator identified as the controlling constraint for
[LISS-0049](LISS-0049-qasm-function-call-lowering.md) — a user must never be
able to mistake a silently-wrong result for a correct one.

Discovered 2026-07-25 while verifying that the existing QASM/Trotter path can
receive Jordan-Wigner-mapped Hamiltonians for LISS-0032; this is an
independent, pre-existing defect, not part of LISS-0032's own scope.

## Reproduction

```qpex
package t
pub fn main() -> Unit {
    Operator H = 0.5 * I - 0.5 * Z(0)
    state psi = |+>
    state psi = evolve psi under H for 100.0
    measure psi
}
```

- Expected step count under the documented policy
  (`ceil(|t| * 8)` clamped to `[1, 64]`): `ceil(100 * 8) = 800`, clamped to
  `64`.
- `python3 -m compiler.qpex emit-qasm` exits `0` and emits exactly 64 `rz`
  gates with `dt=1.5625` — **12.5× coarser** than the `dt=0.125` a physicist
  would expect from the stated `ceil(|t|*8)` policy, with no warning on
  stdout or stderr (`// note: routed on linear-1` is the only stderr line).
- The same clamp applies even when the caller passes an explicit `steps=`
  value: `trotter_step_count(t, steps=200)` returns `64`, not `200` and not a
  diagnostic.

## Root cause

`compiler/qpex/backend/qasm/trotter.py:31-46`:

```python
# Cap slices so NISQ emit stays bounded; scale mildly with |t|.
_MAX_STEPS = 64
_MIN_STEPS = 1


def trotter_step_count(t: float, *, steps: int | None = None) -> int:
    """Fixed-N policy: explicit `steps`, else ceil(|t|*8) clamped to [1, 64]."""
    if steps is not None:
        return max(_MIN_STEPS, min(_MAX_STEPS, int(steps)))
    return max(_MIN_STEPS, min(_MAX_STEPS, math.ceil(abs(float(t)) * 8.0) or 1))
```

`min(_MAX_STEPS, ...)` silently discards any value above 64 — both the
derived value and an explicit caller-supplied `steps=` — with no code path
that surfaces a diagnostic when clamping actually occurs.

## Comparison with the project's other resource limits

| Limit | Value | Behavior on exceeding | Consistent with ADR 0088's posture? |
|---|---|---|---|
| `MVP_MAX_LOGICAL_QUBITS` (`static_hilbert.py`) | 1024 | Hard `STATIC_HILBERT_RESOURCE_ERROR` / `QFT_RESOURCE_ERROR` | Yes — rejects, does not silently truncate |
| `MAX_EXPANSION_TERMS` (`finite_binder.py`) | 1,000,000 | Hard `BINDER_RESOURCE_ERROR` | Yes — ADR 0088 explicitly forbids truncation/symbolic fallback |
| `_MAX_STEPS` (`backend/qasm/trotter.py`) | 64 | **Silent clamp, no diagnostic** | **No** — this is the one limit in the Kernel that silently changes the numerical result instead of rejecting |

## Proposed acceptance scope

**Decided 2026-07-25 (Architecture Path, [ADR 0094](../architecture/adr/0094-explicit-trotter-step-policy.md)):**
a synthesized fourth option, not any of the three originally listed below.
The Adjudicator's framing: the developer must be **in control** of the
Trotter step count, and any safety threshold on a derived value must itself
be something the developer configures — not a number the compiler bakes
in. The already-shipped `using Suzuki(...)` policy (LISS-0017/ADR 0084)
already does this correctly (explicit `steps=` preserved exactly; tolerance
mode uncapped). The decision routes everything through that one mechanism:

- [x] **Selected: require an explicit `using Suzuki(...)` policy for QASM
      emission of `evolve ... under H for t`.** A plain evolve with no
      Suzuki clause is rejected with `QASM_TROTTER_STEPS_REQUIRED`
      (actionable message: add `using Suzuki(order = 2, steps = N)` or
      `using Suzuki(order = 2, tolerance = X, error = Bound |
      EmpiricalEstimate)`). No new CLI flag or settings key. The
      first-order-only `trotter_step_count`/`trotter_gates` functions are
      removed as dead code once their only caller is retired.

Original three candidates (not selected, kept for record):

- [ ] **Option A — Reject at the existing 64 boundary.** Still an arbitrary
      compiler-chosen number; rejected because the threshold itself would
      not be under developer control.
- [ ] **Option B — Raise or remove the cap on the implicit derivation.**
      Rejected because it keeps an *implicit* default path alive at all;
      the Adjudicator's point was that the developer should decide, not
      that the compiler should decide more generously.
- [ ] **Option C — Reject-by-default with explicit opt-in above a
      threshold.** Superseded by the selected option, which removes the
      implicit default (and its threshold) entirely rather than gating it.

## Non-goals

- No change to the Trotter/Suzuki decomposition algorithm itself (LISS-0017
  covers higher-order Suzuki/error control separately).
- No performance optimization of the QASM emitter or simulator.
- No change to `MVP_MAX_LOGICAL_QUBITS` or `MAX_EXPANSION_TERMS`, which
  already behave correctly.

## Dependencies

- Parent: none
- Depends on: none
- Related: [LISS-0032](LISS-0032-typed-second-quantized-operators.md)
  (found during its Architecture Path review — independent defect, not
  blocking LISS-0032's Jordan-Wigner mapping work, since JW mapping produces
  the `Operator` value consumed by this already-existing, already-buggy
  Trotter path), [LISS-0049](LISS-0049-qasm-function-call-lowering.md)
  (same silent-wrong-output failure class; Option-selection precedent),
  ADR 0088 (finite binder lowering; same "no truncation" precedent)
- Blocks: nothing known; the silent clamp affects any `evolve ... for`
  program whose step count exceeds 64, not only second-quantized ones

## Adjudicator Decision Points

- [x] Select an option. — **Synthesized fourth option selected, 2026-07-25**
      (see Proposed acceptance scope): require an explicit `using
      Suzuki(...)` policy; reject plain `evolve ... for t` for QASM
      emission. Rationale: developer control over the step count, and over
      any threshold applied to it, was the controlling constraint — not
      resource safety or performance.
- [x] Diagnostic code and message. — `QASM_TROTTER_STEPS_REQUIRED`;
      message states the requirement and names both fix options
      (`using Suzuki(order = 2, steps = N)` / `using Suzuki(order = 2,
      tolerance = X, error = Bound | EmpiricalEstimate)`).
- [x] Approve Architecture Path design before any Phase 1 Red tests. —
      Approved 2026-07-25; Phase 1 Red explicitly authorized in the same
      exchange.

## Context

- Included: `compiler/qpex/backend/qasm/trotter.py`, existing Trotter/QASM
  regression tests, `docs/architecture/adr/0088-finite-binder-lowering.md`
  and `docs/architecture/adr/0093-jordan-wigner-numerical-mapping.md` as
  precedent for the "no silent truncation" posture.
- Omitted: CPU/SV evaluator internals (the SV `evolve` path was not probed
  for the same defect in this issue — only the QASM/Trotter lowering path
  was; worth checking as part of this issue's own investigation, not
  assumed here).
- Assumption: whichever option is chosen must not silently change a
  simulation's numerical result relative to what the stated policy
  (`ceil(|t|*8)`) promises.
- Ambiguity boundary: Option selection (A/B/C) and the specific bound/policy
  are entirely Adjudicator decisions; no option is favored by this issue.

## Verification

- Architecture review and option selection first; no Phase 1 Red before
  that.
- Once selected: a regression test asserting the reproduction program above
  either produces a diagnostic (Option A/C) or the expected uncapped/raised
  step count (Option B) — never a silent, undiagnosed clamp.
- Existing QASM/Trotter/SV regressions must remain green.

## Work Notes

- 2026-07-25: Issue opened during LISS-0032 (Jordan-Wigner mapping)
  Architecture Path work, while verifying the existing SV/QASM paths can
  receive mapped Pauli operators. Found the silent clamp while probing a
  long-duration `evolve` program. Root cause read and recorded above; no
  code changed. Split out per the Adjudicator's explicit instruction
  (2026-07-25) to keep it independent of LISS-0032's own branch/PR.
- 2026-07-25: Architecture Path review. Confirmed the SV/CPU `evolve` path
  (`runtime/matrix.py`'s `expm_ih`) does not use Trotter step counts at all
  and is unaffected — this defect is QASM/gate-lowering-only. Found that
  LISS-0017/ADR 0084's `using Suzuki(...)` policy already implements the
  correct behavior (explicit `steps=` preserved exactly; `tolerance=` mode
  uncapped) and that the MVP accepts only Suzuki order 2. Surveyed common
  quantum-computing practice (Qiskit's `LieTrotter`/`SuzukiTrotter`, explicit
  `reps` as the primary interface) — explicit step-count control is the
  practitioner norm, not automatic derivation. Probed all 9 examples using
  the plain `evolve ... for t` form: only 3
  (`quantum_ising_4.qpex`, `ising_model.qpex`, `quantum_ising.qpex`) reach
  the Trotter path at all when targeting QASM; the other 6 already fail
  earlier for unrelated reasons. Adjudicator selected a fourth, synthesized
  option (recorded above and in ADR 0094): require an explicit
  `using Suzuki(...)` policy, reject the plain form for QASM emission, and
  remove the now-dead first-order-only functions rather than patch them.
  Adjudicator explicitly authorized Phase 1 Red in the same exchange.
- 2026-07-25: Phase 1 Red. Added
  `tests/test_explicit_trotter_steps_red.py`: a plain `evolve ... for t`
  rejects with `QASM_TROTTER_STEPS_REQUIRED` naming both fixes; the SV
  simulator still runs the same plain program unaffected; an explicit
  `using Suzuki(order = 2, steps = 200)` — above the old 64 cap — is
  honored exactly. Confirmed 2 of 5 assertions failing for the expected
  reason (plain evolve still silently clamped) before any code change; the
  other 3 already passed since they exercise the already-correct Suzuki
  path (regression pins, not new Red targets).
- 2026-07-25: Phase 2 Green. `backend/qasm/lower.py`'s `_lower_evolve_under`
  now raises `TrotterError(QASM_TROTTER_STEPS_REQUIRED, ...)` when
  `ev.suzuki is None`, naming both fix options, instead of falling through
  to the silently-clamped `trotter_gates`. Removed `trotter_step_count`,
  `trotter_gates`, and `_MAX_STEPS` from `trotter.py` (dead code once their
  only caller was retired); `_MIN_STEPS` retained (`suzuki_step_count`
  still uses it).
  Migrated the 3 examples that actually reach the Trotter path when
  targeting QASM (of 9 using the plain form; the other 6 already fail
  earlier for unrelated reasons) to an explicit
  `using Suzuki(order = 2, steps = N)`, `N` matching what the old
  `ceil(|t|*8)` policy derived for that duration (5, 6, 6):
  `examples/06_statistical_physics/quantum_ising_4.qpex`, `ising_model.qpex`,
  `quantum_ising.qpex`. Updated two pre-existing tests in
  `tests/test_qasm3_codegen.py` that asserted a `"trotter"` comment
  substring to assert `"suzuki"` instead (lowering now goes through the S2
  path), and added `using Suzuki(...)` to `test_trotter_single_qubit_x`'s
  inline source. Updated the 4 Jordan-Wigner test sources in
  `test_jordan_wigner_mapping_red.py` that emit QASM to add an explicit
  Suzuki policy.
  All 5 Phase 1 Red assertions pass. Full manual regression sweep: 260 test
  functions pass (up from 255), same 5 pre-existing unrelated failures as
  `main`. Specification verification: 165/165 (100%).
- 2026-07-25: Phase 3 Refactor. Updated `trotter.py`'s module docstring
  (still said "First-order Pauli Trotter", stale since first-order lowering
  was removed in Phase 2 Green) to reflect that the module is now Suzuki S2
  only, with an explicit step policy mandatory per this Issue. No other
  cleanup opportunity found (no unused imports after the function removal;
  `_MIN_STEPS` correctly retained for `suzuki_step_count`). No behavior
  change: all 5 Phase 1 Red assertions and the 11 LISS-0032 Jordan-Wigner
  assertions still pass, full manual regression sweep still shows 260
  passing test functions with the same 5 pre-existing unrelated failures,
  and specification verification still passes 165/165.

Phase 3 complete; Adjudicator final review of the merged result is the only
remaining item.

## Closure (2026-07-25)

Adjudicator final review approved. Issue closed as **Complete**. The
silent Trotter step-count clamp is fixed; `using Suzuki(...)` is the one
required, developer-controlled mechanism for QASM Trotter step counts going
forward.
