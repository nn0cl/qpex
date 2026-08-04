# LISS-0055: Binder body as a full operator expression

## Metadata

- Local issue ID: LISS-0055
- GitHub issue: none
- Status: phase-3-reviewed (approved executable slice; follow-up acceptance remains)
- Phase: Phase 3 Refactor complete for parser/AST, inspection metadata, and the approved executable lowering slice
- Type: language surface + lowering
- Priority: P1
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none
- Implementation branch: `codex/liss-0055-resume` (merged via PR #35)

## Summary

Make a binder body a **full operator expression**, with the same grammar and
meaning as outside a binder, per
[ADR 0096](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md)
D2. One generalisation delivers every remaining expressiveness gap:

| Admitted by "body is an expression" | Model it unlocks |
|---|---|
| `+` / `-` between terms | Heisenberg, XXZ |
| **nested binders** | multi-index sums $\sum_{pq}$, $\sum_{pqrs}$ — **molecular electronic structure** |
| second-quantized atoms (`create[p]`) | Hubbard, molecular |
| `where` guards (D5) | long-range $\sum_{i<j}$ |

Multi-index sums require **no dedicated syntax**: they are nested binders,
which follow from the body being an expression. That is the design property
this issue exists to realise.

`product` lowering (ADR 0096 D10) is implemented here, since it is the same
pass and its ordering semantics are already decided.

## Scope

- Binder body accepts any operator expression: `+`, `-`, `*`, parenthesised
  subexpressions, named scalar coefficients, bare and indexed atoms.
- Nested binders in a body, with the inner binder's variable scoped to the
  inner body. Reusing a visible outer binder or Operator-scope name is
  rejected with `BINDER_VARIABLE_SHADOWING`; sibling/non-overlapping binders
  may reuse names.
- Second-quantized atoms (`create[p]`, `annihilate[q]`) in a body, composing
  with the Jordan-Wigner mapping already shipped by LISS-0032.
- Multiple binder variables in one head
  (`sum (i in D, j in D) { … }`) as **sugar for nesting**, meaning exactly
  the nested form. The normalized AST uses nested single-variable
  `OpBinder` nodes and retains `BinderOrigin` provenance for the original head.
- `where` guard (D5) filtering the expanded index tuples.
- `product` lowering: ascending order; **lexicographic by declaration order**
  for a multi-variable head; **outer-major** for nested binders (D10).

The placement and semantic boundary of `where` are fixed by
[ADR 0098](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md):
it appears before the body, is a pure static index predicate, and filters
tuples before body evaluation. It is not a quantum-state conditional.

## Acceptance notes

- [ ] Heisenberg ($\sum_i X_iX_{i+1} + Y_iY_{i+1} + Z_iZ_{i+1}$) lowers,
      runs, and emits QASM.
- [ ] A two-index sum ($\sum_{pq}$) and a four-index sum ($\sum_{pqrs}$)
      lower, with expanded term counts matching the expected products of
      domain sizes.
- [ ] A Hubbard-style body mixing second-quantized atoms and a binder lowers
      through the LISS-0032 Jordan-Wigner path and executes.
- [ ] `sum (i in D, j in D) { … }` and the equivalent nested form produce
      **identical** operator trees — the sugar is verified, not assumed.
- [ ] `sum (i in D, j in D) where i < j { … }` expands only the retained
      tuples, with the retained count asserted.
- [ ] `product` respects ascending / lexicographic / outer-major order, and
      the order is pinned by a test that would fail if reversed —
      non-commutativity makes this observable.
- [ ] Numerical equivalence against hand-written operator expressions is
      checked via measurement marginals, not internal representation.
- [ ] Any construct still not covered produces an explicit diagnostic, never
      silence (D6).

## Non-goals

- **Indexed coefficient families** (`J[i]`, `h_pq[p][q]`) — deferred as
  additive by ADR 0096; needs a classical family type.
- Empty domains and identity elements (LISS-0056).
- Notation unification (LISS-0054) — assumed already done.
- Dependent ranges (`Index<i+1..N-1>`) and their endpoint integer/overflow
  question — deferred together by ADR 0096.
- `rev()` / explicit reversed domains — deferred as additive.

## Dependencies

- Parent: none
- Depends on: **LISS-0052** (execution wiring), **LISS-0053** (composition
  and the recursive lowering pass this builds on). **LISS-0054** is strongly
  preferred first — implementing a full expression grammar in binder bodies
  while two operator grammars still exist would mean doing it twice.
- Related: ADR 0096 D2/D5/D10, LISS-0032 (Jordan-Wigner, reused for
  second-quantized bodies), ADR 0088 (the narrow body this supersedes)
- Blocks: nothing scheduled

## Adjudicator Decision Points

- [ ] Approve Phase 1 Red.
- [ ] Confirm `where` guard syntax placement (`sum (…) where cond { … }`) —
      accepted by ADR 0098; Phase 1 must cover parser and diagnostic behavior.
- [x] Confirm binder-variable shadowing: reject active-scope reuse with
      `BINDER_VARIABLE_SHADOWING`; allow sibling/non-overlapping reuse (ADR
      0098 D6).
- [x] Decide multi-variable-head AST representation and provenance: normalize
      to nested single-variable `OpBinder` nodes, preserve declaration order,
      and retain `BinderOrigin` metadata (ADR 0098 D5).
- [x] Decide pure guard predicate grammar and diagnostics: a single binary
      comparison in the MVP; use `BINDER_GUARD_UNSUPPORTED`,
      `BINDER_GUARD_TYPE_ERROR`, `BINDER_GUARD_SCOPE_ERROR`, and the existing
      `MATHEMATICAL_BINDER_EFFECT_ERROR` as applicable (ADR 0098 D2/D7).
- [x] Decide product ordering: ascending single-binder order, lexicographic
      multi-variable order, and outer-major nested order are already normative
      in ADR 0096 D10/D11.
- [x] Separate empty-domain identity semantics into LISS-0056.
- [x] Review the resource-budget boundary in
      [ADR 0100](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md): users
      configure `staqex.toml` with versioned defaults; simulator estimates are
      representation-aware; `Warn` is simulator-only and deployment lanes use
      `Abort`.

## Context

- Included: `compiler/staqex/parser.py` (binder head/body, `where`),
  `compiler/staqex/finite_binder.py` (expansion, guard filtering, ordering),
  `compiler/staqex/typecheck.py` (binder scope/shadowing, body typing),
  `compiler/staqex/second_quantization.py` (composition with JW mapping).
- Omitted: coefficient families, dependent ranges, QPU/provider lowering.
- Assumption: the expanded result remains a concrete operator tree consumed
  by the paths LISS-0052 wired — no execution path needs a binder-specific
  branch. If nested/second-quantized bodies turn out to require one, that is
  an unanticipated design decision and work stops for direction.
- Resource note: multi-index expansion grows as the product of domain sizes.
  The proposed policy is documented separately in ADR 0100: candidate and
  retained counts are distinct, `Warn`/`Abort` is explicit, and no truncation
  or symbolic fallback is allowed. Manifest implementation and benchmark
  questions remain outside this design update.

## Verification

- Phase 1 Red: Heisenberg, multi-index, Hubbard-style, `where`, and
  `product` cases each fail for their recorded reason.
- Phase 2 Green: the parser/AST and inspection-metadata acceptance slice
  passes; executable sugar/nesting equivalence and product ordering remain
  pending.
- Full regression sweep and spec verification stay green.

## Phase 2 Green Record (2026-07-26)

The approved Phase 2 implementation now provides the following bounded Green
behavior:

- Operator bodies accept `+`, `-`, and `*` expressions in the inspection
  metadata path.
- The parser accepts multiple binder bindings and normalizes them to nested
  `OpBinder` nodes in declaration order.
- A single comparison after `where` is represented as an `OpBin` guard and
  attached to the normalized inner binder.
- `product` metadata is represented as a `Product` operator tree; no implicit
  execution-order rewrite is introduced.
- Generic indexed atoms, helper calls, and nested binders are retained as
  symbolic inspection metadata. They are not silently lowered into the
  established executable Pauli path.
- Executable lowering only materializes the established finite Pauli slice.
  Unsupported executable forms are left on the original AST and therefore do
  not change existing simulator or QASM behavior.

Verification performed:

- `tests/test_binder_body_operator_expression_red.py`: 6 passed.
- `python3 -m py_compile` for the changed parser, AST, and binder modules:
  passed.
- `git diff --check`: passed.
- Full spec verification: 160/165, with the same five pre-existing example
  failures on the Phase 1 Red baseline. The failure set did not change after
  this implementation.

The remaining acceptance notes cover broader model-size examples, numerical
equivalence, and the final diagnostic matrix. They remain for Phase 3 review
and regression expansion; the execution forms listed above are no longer
deferred by this slice.

## Execution Acceptance Extension (2026-07-26)

The approved continuation completed the executable portion that can be
derived without a new architecture decision:

- `where` filters index tuples before body evaluation and records candidate
  versus retained counts in provenance.
- Nested binders recursively materialize into operator folds. Empty inner
  folds use the typed sum/product identities already fixed by ADR 0096 D9.
- `product` preserves ascending factor order during AST materialization.
- Pure second-quantized binder bodies substitute static indices and then use
  the existing whole-expression Jordan--Wigner mapping. Non-Hermitian inputs
  remain hard failures under LISS-0032.
- `BinderOrigin` preserves the original source span, declaration order, and
  whether a multi-variable head was desugared.
- Simulator and provider-neutral QASM emission consume the materialized
  operator tree without introducing a binder-specific opcode.

Additional acceptance coverage is in
`tests/test_liss0055_execution_acceptance.py`. The existing five unrelated
spec-verification failures remain unchanged from the Phase 1 Red baseline.

## Phase 3 Refactor Record (2026-07-27)

- Separated inspection metadata lowering (`_lower_metadata_expr`) from
  executable operator lowering (`_lower_executable_expr`).
- Centralized fold identity and operator selection for `sum` and `product`.
- Centralized binder-kind and guard-operator vocabularies.
- Kept the Jordan--Wigner mapping at the whole-expression boundary so
  non-Hermitian individual creation/annihilation atoms are never mapped as if
  they were complete physical operators.
- Preserved the existing fallback behavior for unsupported executable forms;
  no simulator or QASM behavior outside the accepted binder slice changed.

The refactor changed names and responsibility boundaries only. The acceptance
assertions and observed results are unchanged.

## Work Notes

- 2026-07-26: Opened from ADR 0096 D2/D5/D10. Multi-index and constrained
  sums were absent from every prior document, deferred list included, and
  were found only by deriving the surface from real Hamiltonians under
  ADR 0095.
- 2026-07-26: ADR 0098 accepted the `where` placement, static-predicate
  boundary, guard-before-body evaluation order, and separation from quantum
  `when`/`capply`. Remaining LISS-0055 decisions stay open; no Phase 1 Red
  implementation approval is implied.
- 2026-07-26: ADR 0096 D10/D11 was confirmed as the normative product and
  expansion-order contract. Empty-domain behavior remains in LISS-0056.
  Resource-budget ownership and public policy were separated into proposed
  ADR 0100; no implementation approval is implied.
- 2026-07-26: Resource profiles are user-configurable through the project
  manifest, with versioned defaults when fields are absent. Manifest schema,
  simulator estimation, and the final `Warn` continuation boundary were
  pending review in ADR 0100.
- 2026-07-26: The resource review selected `staqex.toml`,
  `schema_version = 1`, representation-aware simulator estimates, and
  simulator-only `Warn`. Remaining work is manifest implementation and
  benchmark/diagnostic refinement; no implementation approval is implied.
