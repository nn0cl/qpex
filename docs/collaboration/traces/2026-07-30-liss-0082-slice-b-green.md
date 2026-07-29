# LISS-0082 Slice B Phase 2 Green and Phase 3 Refactor

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-b-red`
- Operating path: Feature Path
- Issue: LISS-0082
- Slice/phase: Slice B / Phase 2 Green + Phase 3 Refactor
- Approval: Adjudicator "Green + Refactor まで承認" after the four Slice B design
  decisions were approved and the Red unit was committed (`5e5a58a`)
- Implementation permission: **Slice B only**
- Technology selection permission: **none**
- Post-review required: Adjudicator review before Slice C

## Phase 2 Green

Extended `compiler/staqex/quantum_semantic_ir.py` additively:

- `ActingFactor` / `ActingSpace` — ordered finite tensor factors with embedded
  `SemanticOrigin`;
- `PureJointStateValue` / `DensityJointStateValue` — whole-Joint-store
  generations with an `is_pure` property and no amplitude or density-matrix
  field;
- `JointValueUse` — one consuming path, with an optional `factor_id` that only
  ever represents an invalid factor-level consumption;
- `QuantumSemanticModule` — three additive tuple fields `acting_spaces`,
  `values`, `value_uses`, all defaulted so Slice A construction is unchanged;
- verifier passes emitting `QSEM_ACTING_SPACE_INVALID` and
  `QSEM_VALUE_USE_INVALID`.

No reviewed Red assertion was modified. No Physics IR, evaluator, pipeline, QPU
adapter, or provider file was touched.

## Phase 3 Refactor

Behavior-preserving only:

1. Extracted the duplicated six-field carrier shape into a private
   `_JointStateValue` base, so purity is the single declared difference between
   the two public carriers.
2. Extracted the inline Slice A root checks into `_verify_root`, making
   `verify_quantum_semantic_ir` a four-pass dispatcher with a documented,
   reproducible pass order.
3. Ordered the verifier helpers root → acting spaces → values → uses to match
   that pass order.

No DTO field, diagnostic code, diagnostic message, or emission order changed.

## Deterministic verification

- `python3 tests/test_quantum_semantic_ir_slice_b_red.py` — passed after Green
  and again after Refactor.
- `python3 tests/test_quantum_semantic_ir_slice_a_red.py` — passed throughout.
- `python3 -m py_compile compiler/staqex/quantum_semantic_ir.py` — passed.
- Full sweep of `tests/*.py` through the direct entry point, compared against a
  baseline taken with the Green implementation stashed:
  - baseline (Red commit): 95 pass / 48 fail;
  - Green: 96 pass / 47 fail;
  - Refactor: 96 pass / 47 fail, failure set identical to Green.
  - The only difference from baseline is
    `test_quantum_semantic_ir_slice_b_red.py` moving fail → pass. The remaining
    47 failures are pre-existing and unrelated (for example
    `hir.py` `BinOp.left` and `LINEAR_IMPLICIT_DISCARD` in older suites).
- `git diff --check` — clean.
- pytest is not installed in this workspace, so the direct entry point is the
  deterministic check, matching the Slice A traces.

## Verification gaps carried forward

> **Superseded.** The Adjudicator re-review of 2026-07-30 found a fifth gap this
> list missed — `resources` is checked for arity only, never for identity and
> order against the space factors. The authoritative list is
> [the re-review record](2026-07-30-liss-0082-slice-b-review.md). This section
> is left unchanged as a historical record of what the agent reported.

Phase 2 implements only reviewed Red assertions, so these accepted contract laws
have **no** Slice B coverage yet and need their own Red before they are claimed:

1. `QSEM_IDENTITY_CONFLICT` still inspects `roots` and `region_roots` only.
   Duplicate `ActingSpace` or Joint-value identities are not reported.
2. `QSEM_PROVENANCE_INCOMPLETE` still inspects `module.origins` only. The
   `SemanticOrigin` embedded in an `ActingSpace` or a Joint value is not
   validated, even though decision 1 made embedding the accepted design.
3. Use-after-consume is detected only as fan-out. There is no ordering model in
   Slice B, so a consume-then-reuse sequence is indistinguishable from two
   parallel consumers.
4. `generation` is stored but never checked for monotonicity or uniqueness.

## Stop condition

Stop after Refactor evidence. Do not begin Slice C region kinds, Slice D
control/measurement, Slice E lowering, Slice F pipeline wiring, or any provider
work without separate approval.
