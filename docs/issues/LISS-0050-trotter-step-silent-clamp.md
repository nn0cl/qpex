# LISS-0050: Silent Trotter step-count clamp in QASM lowering

## Metadata

- Local issue ID: LISS-0050
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design
- Type: bug / silent precision loss
- Priority: P1
- Initial planning size: S
- Current planning size: S
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

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

## Proposed acceptance scope (options for Adjudicator decision — none selected)

- [ ] **Option A — Reject.** When the derived or explicit step count exceeds
      `_MAX_STEPS`, emit a hard diagnostic (e.g.
      `QASM_TROTTER_STEP_BUDGET_EXCEEDED`) instead of clamping. Matches the
      `MVP_MAX_LOGICAL_QUBITS`/`MAX_EXPANSION_TERMS` precedent exactly.
- [ ] **Option B — Raise or remove the cap.** Revisit whether 64 is the right
      bound at all now that the project's stated posture (LISS-0032
      Architecture Path decision, 2026-07-25) is that performance/output-size
      concerns must not drive scope or limits; optimization is separate,
      future work. A materially higher (or no) default cap plus an explicit,
      documented resource policy may be more consistent than keeping 64 and
      merely making it reject instead of clamp.
- [ ] **Option C — Reject by default, allow explicit opt-in.** Reject when the
      derived count exceeds the bound, but allow an explicit `steps=` request
      above the bound to proceed (with its own, higher hard ceiling and
      resource diagnostic) since that is the physicist making an informed,
      explicit choice rather than the compiler silently deciding for them.

This issue does not select an option or a specific new bound; it is
Architecture Path design intake only, following the LISS-0049 (Option
A/B/C) precedent.

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

- [ ] Select Option A, B, or C above (or a different option not yet
      identified).
- [ ] If Option B: approve a specific new bound or an explicit resource
      policy replacing the fixed `_MAX_STEPS = 64`.
- [ ] If a new diagnostic code is introduced: approve its name and message
      text (the Adjudicator required actionable-advice wording for
      LISS-0049's `QASM_FUNCTION_CALL_UNSUPPORTED`; the same bar likely
      applies here).
- [ ] Approve Architecture Path design before any Phase 1 Red tests.

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
