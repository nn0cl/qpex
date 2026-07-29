# Trace: LISS-0075 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Phase | plan intake |
| Branch | `feature/liss-0075-linear-quantum-usage` |
| Implementation | **forbidden** until Slice A plan approval → Phase 1 Red |

## [DESIGN CHECK]

- Scope: HIR-level linear-use verifier for quantum-typed bindings within a
  single `fun` scope; no-cloning / no-implicit-discard / uncomputation witness.
- Specs inspected: `WP-0025` §LISS-0075; `compiler/staqex/hir.py` (LISS-0080
  HirDecl.effects + HirModule.declarations); LISS-0080 complete.
- Component boundaries: new `HirLinearVerifier` in `compiler/staqex/hir.py`;
  touches `TypeChecker` for quantum-type identification; no evaluator rewrite
  in Slices A–B; evaluator simulator-equivalence hook in Slice C.
- Applicable constraints: LISS-0080 HIR API is the analysis surface;
  inter-procedural analysis deferred to LISS-0077; no language syntax changes
  in this Issue.
- Decisions awaiting Adjudicator confirmation (4 items — see issue doc §Design
  decisions required before Phase 1).
- Included context: `hir.py`, `WP-0025`; omitted: evaluator internals
  (not needed until Slice C).
- Task routing: Feature Path, Cursor Agent.
- Verification plan: each slice Red must fail before Green; Green must not edit
  tests; Slice D end-to-end acceptance suite runs after Refactor.

## Delivered

- `docs/issues/LISS-0075-linear-quantum-usage.md`

## Next safe action

Adjudicator reviews 4 design decisions + Slice A plan → grants Phase 1 Red approval.
