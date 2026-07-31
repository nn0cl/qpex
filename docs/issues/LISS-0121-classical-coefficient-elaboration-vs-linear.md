# LISS-0121: Classical coefficient elaboration vs linear quantum resources

## Metadata

- Local issue ID: LISS-0121
- GitHub issue: none
- Status: **phase-3-reviewed complete** (2026-07-31)
- Phase: Phase 3 Refactor complete
- Type: language boundary bugfix (typecheck / HIR linear / Operator elaboration)
- Priority: P0 for language honesty; also unblocks P0 example health (B08) and
  binder suites regressing on `LINEAR_IMPLICIT_DISCARD` for `J`
- Depends on: [ADR 0114](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md)
  (**Accepted**), ADR 0096, LISS-0053 acceptance intent, LISS-0075 / LISS-0114 LINEAR
- Blocks: clean B08; honest named-coefficient binders; F-02/F-05 closure
- Related: [physicist-source-friction-ledger](../architecture/physicist-source-friction-ledger.md)
  F-02, F-05

## Summary

Fix false `LINEAR_IMPLICIT_DISCARD` on Type-First / named Hamiltonian
coefficients (`Float J`, struct fields) while keeping LINEAR strict for true
quantum `state` values, under ADR 0114’s **elaboration-after-fold** invariant
(programmer must not misrecognize coefficients as classical control islands,
and folded programs must remain diagnostically honest).

## Physicist priority

Staqex is for physicists. The spelling `Float J = 1.0` then
`sum (i in Index<0..N>) { J * Z[i] * Z[next(i)] }` is normative paper form.
Programmer DX must not force literal-only Hamiltonians.

## Acceptance (draft EARS)

1. **Given** a closed Type-First coefficient `Float J = c` used only inside
   Operator / binder coefficient position, **when** the program is compiled,
   **then** no `LINEAR_IMPLICIT_DISCARD` / `LINEAR_DUPLICATE_USE` is emitted for
   `J`, and meaning matches the literal-`c` program (ADR 0114 D2.1–D2.2).
2. **Given** `state q = …` (quantum resource) left unconsumed, **when**
   compiled, **then** LINEAR diagnostics still fire (no regression).
3. **Given** a coefficient name that depends on unmeasured quantum state,
   **when** used in Operator elaboration, **then** an explicit diagnostic is
   emitted (ADR 0114 D2.4) — never silent drop.
4. **Given** attempts to use an elaboration coefficient as `when` control or
   `measure` subject, **when** compiled, **then** fail-closed with a message
   that names **coefficient vs quantum state** (ADR 0114 D3).
5. **Given** binder expansion / constant fold of coefficients, **when**
   diagnostics are collected, **then** results match the pre-fold intent
   (C-preprocessor analogy; ADR 0114 D2).

## Non-goals

- Restoring `if` / `&&`.
- Implementing showcase / reclaiming LISS-0120.
- Broad classical mid-program ALU beyond Operator elaboration.

## Implementation sketch (not authorization)

Likely touch: `typecheck.py` (Type-First quantity env kind vs State),
`hir.py` linear carrier predicate, Operator/binder elaboration + evaluator
scalar capture consistency, diagnostics copy, Red tests from LISS-0053 named
coefficient + new fold-invariant cases.

## Exit

- [x] ADR 0114 Accepted
- [x] Phase 1 Red (`tests/test_liss_0121_classical_coefficient_vs_linear_red.py`)
- [x] Phase 2 Green — Type-First elaboration coefficients are `Classical`;
  `OpAttr` in Operator DSL; `when` on coefficients →
  `COEFFICIENT_IN_QUANTUM_POSITION`; LINEAR no longer fires on `Float J`
- [x] Phase 3 Refactor — `op_attr_elaboration.py` extracted; suite still 10/10
- [x] Sync friction ledger F-02/F-05 notes (closed for named Float + field OpDSL)
- [ ] Optional P0: B08 LINEAR residuals unrelated to named coeffs
