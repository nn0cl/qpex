# LISS-0053: Binder composition, named coefficients, and honest deferral

## Metadata

- Local issue ID: LISS-0053
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design complete (ADR 0096 D3/D6/D11 accepted); awaiting Phase 1 Red approval
- Type: bug + diagnostic honesty
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Three defects in finite-binder lowering, grouped because they share one
cause — the lowering pass inspects only a top-level `OpBinder` with a
narrowly-matched body — and one fix location:

1. **`sum {...} + sum {...}` silently produces no lowering and no
   diagnostic.** This is a bug: composition of binders is named nowhere,
   not in ADR 0088's decisions and not in its deferred list. It is also why
   the transverse-field Ising Hamiltonian cannot be written.
2. **A named scalar coefficient (`J * Z[i] * Z[next(i)]`) is rejected** with
   `BINDER_DOMAIN_ERROR`, although ADR 0088 Decision 3 writes
   `coefficient * Pauli[i] * Pauli[next(i)]` without restricting
   *coefficient* to a literal, and `J * Z(0) * Z(1)` is accepted outside a
   binder. Also a bug.
3. **`product` silently produces no lowering and no diagnostic.** Here the
   *deferral is legitimate* — `product` is explicitly named in ADR 0088's
   deferred list — but its expression is not: silence violates ADR 0096 D6.

This issue does **not** implement `product`; it makes the deferral honest.
`product` semantics are decided (ADR 0096 D10) and implemented in
LISS-0055.

## Reproduction

```qpex
QubitRegister<4> register = system()
Float J = 1.0

// 1. silently no lowering, no diagnostic
Operator tfim = sum (i in Index<0..2>) { -1.0 * Z[i] * Z[next(i)] }
              + sum (i in Index<0..3>) { -1.0 * X[i] }

// 2. BINDER_DOMAIN_ERROR, though `J * Z(0) * Z(1)` is fine outside a binder
Operator named = sum (i in Index<0..2>) { J * Z[i] * Z[next(i)] }

// 3. silently no lowering, no diagnostic
Operator parity = product (i in Index<0..3>) { Z[i] }
```

## Acceptance notes

- [ ] A binder composes as an ordinary operator expression: `sum {...} +
      sum {...}`, `-sum {...}`, and `c * sum {...}` all lower, per ADR 0096
      D3.
- [ ] The transverse-field Ising Hamiltonian
      ($-J\sum Z_iZ_{i+1} - h\sum X_i$) lowers, runs, and emits QASM.
- [ ] A named classical scalar in a binder body resolves exactly as it does
      outside a binder, including prelude constants.
- [ ] `product` produces an **explicit, actionable diagnostic** naming it as
      not yet lowered — never silence. (Actionable-message bar per
      LISS-0049.)
- [ ] Any other binder construct not covered by this issue also produces an
      explicit diagnostic rather than silently yielding nothing.
- [ ] **Expansion and aggregation order is pinned by test** (ADR 0096 D11):
      ascending expansion, left-to-right aggregation. `f64` addition is not
      associative, so this is observable semantics and must be locked, not
      left to the backend.

## Non-goals

- Implementing `product` lowering (LISS-0055).
- `+`/`-` *inside* a single binder body, nested binders, second-quantized
  atoms (LISS-0055).
- Empty domains and `where` (LISS-0056).
- Notation unification (LISS-0054).

## Dependencies

- Parent: none
- Depends on: **LISS-0052** — until lowering reaches an execution path,
  "it lowers" cannot be verified end-to-end
- Related: ADR 0096 D3/D6/D11, ADR 0088 (deferred list), LISS-0049 and
  LISS-0050 (the established "no silent degradation" posture and the
  actionable-diagnostic bar)
- Blocks: nothing directly; LISS-0055 builds on the same pass

## Adjudicator Decision Points

- [ ] Approve Phase 1 Red.
- [ ] Confirm the diagnostic code names for the deferral cases (proposal:
      `BINDER_LOWERING_UNSUPPORTED`, with a message naming the specific
      construct and that it is not yet lowered).

## Context

- Included: `compiler/qpex/finite_binder.py` (`_operator_metadata`,
  `_lower_expr`), `compiler/qpex/pipeline.py` (diagnostic registration),
  and the scalar-resolution path already used outside binders
  (`runtime/hamiltonian.py`'s `scalars`).
- Omitted: parser (no new syntax), QASM emitter internals.
- Assumption: "compose as an operator expression" means the lowering pass
  recurses through ordinary operator nodes to find binders, rather than
  binders being special-cased at the top level only.

## Verification

- Phase 1 Red: the three reproduction cases behave as recorded above.
- Phase 2 Green: TFIM lowers/runs/emits; named coefficients resolve;
  `product` and any uncovered construct emit an explicit diagnostic;
  expansion/aggregation order matches the pinned expectation.
- Full regression sweep and spec verification stay green.

## Work Notes

- 2026-07-26: Opened from ADR 0096's implementation order. Grouped per the
  ADR 0095 Decision 6 classification: items 1 and 2 are bugs, item 3 is a
  legitimate deferral whose silence is the defect.
