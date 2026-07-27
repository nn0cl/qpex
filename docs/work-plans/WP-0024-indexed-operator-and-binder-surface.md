# WP-0024: Indexed operator and binder surface

## Goal

Make a physicist's own Hamiltonian writable, runnable, and QASM-emittable in
QPex — the canonical many-body and quantum-chemistry models, not a
restricted subset — by realising the surface accepted in
[ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md).

This is the first work plan built under
[ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md), so
it is ordered by *path to the correct final form*, not by fastest value.

## Scope

- In: LISS-0052 … LISS-0057, and the specs/examples they migrate.
- Out: multi-register acting-space typing and provider mapping beyond LISS-0058,
  ADR 0096's deferred list (indexed coefficient families, dependent ranges,
  `rev()`, SI dimension extension, other fermion mappings),
  [ADR 0097](../architecture/adr/0097-numeric-representation-horizon.md)
  (numeric horizon — no implementation).

## What this unlocks (acceptance from the physicist's side)

| Model | Blocked by | Unblocked at |
|---|---|---|
| Any binder Hamiltonian at all (currently lowers but cannot execute) | execution wiring | **LISS-0052** |
| Transverse-field Ising $-J\sum Z_iZ_{i+1} - h\sum X_i$ | binder composition | **LISS-0053** |
| Heisenberg / XXZ | `+` in body | **LISS-0055** |
| Hubbard | second-quantized atoms in body | **LISS-0055** |
| Molecular electronic structure $\sum_{pq}, \sum_{pqrs}$ | multi-index sums | **LISS-0055** |
| Long-range $\sum_{i<j}$ | `where` guard | **LISS-0055** |
| Periodic rings | `wrap(i)` | **LISS-0057** |

## Issue graph

Statuses as of 2026-07-27. Each issue receives plan approval before Phase 1
Red and completion approval after Phase 3, per the repository's Issue-Level
Autonomy rules.

| Issue | Kind | Size | Depends on | Delivers |
|---|---|---:|---|---|
| **LISS-0052** binder lowering execution wiring | bug (spec divergence) | M | — | ADR 0096 D7; makes all later work observable — **complete** |
| **LISS-0053** composition, named coefficients, honest deferral | bug + diagnostics | M | 0052 | D3, D6, D11 — **Phase 3 complete** |
| **LISS-0054** unified `Op[index]` notation | breaking surface | L | 0052 | D1 |
| **LISS-0055** binder body as operator expression | surface | XL | 0052, 0053; 0054 strongly preferred | D2, D5, D10 — **Phase 3 reviewed for approved executable slice; follow-up acceptance remains** |
| **LISS-0056** empty-domain identity elements | semantics | L | 0052, 0053; 0055 preferred | D9, D12 (minimal) — **Phase 3 complete; two follow-up diagnostic gaps recorded** |
| **LISS-0057** periodic accessor `wrap(i)` | surface (additive) | M | 0052; 0055 preferred | D4 — **Phase 3 complete** |
| LISS-0058 acting-space typing | type system | XL | 0056 | D12 follow-up — **Phase 3 complete** |

## Order and why

1. **LISS-0052** first, unconditionally. Until lowering reaches an execution
   path, no other issue's behaviour is verifiable end-to-end — "it lowers"
   currently means "a dict was produced", which is not acceptance under
   ADR 0095 Decision 4.
2. **LISS-0053** next. Corrective, same pass, and it is what makes the
   single most canonical model (TFIM) writable. Together with 0052 this is
   ADR 0096's step 1, and per the evidence classification (ADR 0095
   Decision 6) it is **largely bug-fixing against an already-accepted spec**
   — cheaper and lower-risk than a new-surface slice.
3. **LISS-0054** before LISS-0055. Implementing a full expression grammar in
   binder bodies while two operator grammars still exist would mean doing it
   twice. Notation also accrues legacy fastest (ADR 0095 Decision 3), so it
   is settled before more programs are written.
4. **LISS-0055** — the large one, and the reason this work plan exists. The approved executable slice is now Phase 3 reviewed; broader model-size and numerical-equivalence acceptance remains a follow-up boundary.
5. **LISS-0056** and **LISS-0057** after the body grammar is final, so both
   land against the finished surface rather than an interim one. Both are now
   complete; their remaining broader acting-space concern is tracked only by
   LISS-0058.

LISS-0058 was initially left out of the sequence because it was a type-system
decision needing its own ADR. ADR 0102 now records the accepted single-register
boundary and the implementation is complete. Multi-register naming and
provider mapping remain separate follow-ups.

## Process gate

Each issue requires plan approval before Phase 1 Red and completion approval
after Phase 3 Refactor, per `CLAUDE.md`'s Claude Code Issue-Level Autonomy.
One branch per issue; the PR opens once, at completion, per
`docs/collaboration/branch-commit-pr-discipline.md`.

If an unanticipated design or architecture decision surfaces mid-issue, work
stops and the Adjudicator is asked — it is not resolved unilaterally. Two
places where this is judged likely:

- **LISS-0054**, if collapsing to a single operator-reference AST node turns
  out to require redesigning the expression grammar wholesale.
- **LISS-0055**, if nested or second-quantized bodies turn out to need a
  binder-specific branch in an execution path rather than reusing the
  ordinary operator path.

## Risks

- **LISS-0054 is deliberately breaking.** Examples, tests, and specs migrate
  in one reviewable unit; there is no alias and no deprecation window
  (ADR 0096 D1). If the migration diff proves larger than expected, the
  correct response is to review it, not to reintroduce an alias.
- **LISS-0055 is XL and touches parser, typechecker, and lowering
  together.** ADR 0095 accepts larger slices as the cost of aiming at the
  final form, but this is the issue most likely to warrant splitting after
  its own design intake.
- **Multi-index expansion grows as the product of domain sizes.** Per
  ADR 0095 Decision 5 this is not grounds to restrict what may be written;
  `BINDER_RESOURCE_ERROR` remains the honest rejection.
- **LISS-0056 depends on LISS-0058's problem being only partly solved.** The
  minimal acting-space path is sufficient for empty identities but leaves
  the general weakness in place; the boundary between them must stay clearly
  documented, or the follow-up will be forgotten.

## Verification plan

Per issue: Phase 1 Red confirmed failing for the stated reason, Phase 2
Green passing those assertions without editing a test, Phase 3 Refactor
behaviour-preserving, then the full sweep.

Repository-wide, after each issue:

- every `tests/test_*.py` function (currently 269 passing, with 5 known
  unrelated pre-existing failures);
- `python3 tests/spec_verification/run_all.py` (currently 165/165);
- for surface-affecting issues, every `examples/**/*.qpex` still runs and,
  where applicable, still emits QASM.

Numerical acceptance is by comparison against hand-written operator
equivalents via measurement marginals, not by asserting internal
representation — the pattern established by LISS-0032 and LISS-0011.

## Current next issue

- Issue: **LISS-0055** (binder body as operator expression).
- Reason: LISS-0054 unified and migrated `Op[index]`; the larger binder body
  grammar can now build on one operator-reference AST shape.
- Adjudicator approval needed: plan approval for LISS-0055 Phase 1 Red.
