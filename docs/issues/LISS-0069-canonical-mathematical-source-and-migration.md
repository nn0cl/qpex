# LISS-0069: Canonical mathematical source and migration

## Metadata

- Local issue ID: LISS-0069
- GitHub issue: not created
- Status: **Slice B Phase 3 Refactor complete** (2026-07-28); Slice C pending plan
- Phase: phase-3-refactor complete (Slice B)
- Type: language surface / lexer / migrator
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced)
- Owner/agent: unassigned after plan approval
- Related branch: `feature/liss-0069-slice-b-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted** (v1.0 spec)

## Summary

Introduce the ADR 0106 / ADR 0095 **canonical UTF-8 NFC mathematical spelling**
for Dirac, adjoint, and tensor tokens as a **dual-accept** surface, with a
deterministic migrator contract and golden corpus. ASCII forms remain valid
until a later deprecate/remove gate. ASCII Pauli atoms are **not** removed in
this Issue’s first slice.

Companion surface contract:
[`qpex-unicode-math-source.md`](../specs/qpex-unicode-math-source.md).
Migrator contract (Slice B):
[`qpex-unicode-math-migrator.md`](../specs/qpex-unicode-math-migrator.md).

## Acceptance Notes (Issue complete when)

1. Unicode ket/bra close and open delimiters, `†`, and `⊗` parse to the same
   AST/IR nodes as the current ASCII spellings (`|…>`, `adjoint(…)`, `*|*`).
2. Pipeline `|>` never collides with ket close `⟩` (U+27E9) at the lexer.
3. Source is NFC-normalized on read for identifier and math-token comparison
   (or an equivalent documented boundary).
4. A migrator (CLI or library entry) rewrites ASCII Dirac/tensor/adjoint forms
   to canonical Unicode while preserving comments and spans in golden fixtures.
5. SV / official examples remain green under dual-accept (no forced example
   rewrite in the first Red/Green slice).
6. M-P01 Pauli ASCII removal and M-P05 `state` sugar are **out of scope** for
   the first approved slice (separate deprecate gates / Issues).

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Lexer dual-accept: `\|ψ⟩` / `⟨φ\|`, `⊗`, postfix `†`; `\|>` vs `⟩` | **complete** (Red→Green→Refactor) |
| **B** | Migrator library + `tests/fixtures/migration/` goldens for M-P02–M-P04 | **complete** (Red→Green→Refactor) |
| **C** | CLI `migrate` (name TBD) + formatter-emit preference (or defer emit to LISS-0072) | after B |

## Non-goals (Slice B)

- CLI `qpex migrate` (Slice C).
- Removing ASCII Pauli `X`/`Y`/`Z`/`I` (M-P01).
- Migrating `state` → `State<T>` sugar (M-P05).
- Force-rewriting `examples/` in the same Green.
- Bra–ket matrix-element / `inner` desugar (A.1 / LISS-0073).
- Lossless CST / full formatter (LISS-0072).

## Adjudicator Decision Points (Slice B plan)

- [x] Approve **Slice B** plan for Phase 1 Red (migrator library + goldens only).
- [x] Confirm rewrite set: R-KET, R-TENSOR, R-ADJ-SIMPLE only.
- [x] Confirm `adjoint(complex)` may remain unmigrated when unsafe to peel.
- [x] Confirm no CLI in Slice B (Slice C later).
- [x] Confirm examples tree is **not** bulk-rewritten in Slice B Green.
- [x] Implementation: Red only until Red review (default stop before Green).

## Work Notes

- 2026-07-28: Issue opened; plan proposed after LISS-0068 v1.0 promotion.
- 2026-07-28: Adjudicator **plan approved** (“承認”). PR #68 merged.
- 2026-07-28: Phase 1 Red — `tests/test_unicode_math_source_red.py`.
- 2026-07-28: Adjudicator Red **approved**; Phase 2 Green — lexer dual-accept for
  `⟩` / `⊗` / `†` / `⟨…|`; operator postfix `†` → `OpCall(adjoint, …)`.
  SV 160/160 PASS.
- 2026-07-28: Phase 3 Refactor — shared Dirac label scan + Unicode constants;
  no behavior change. Slice A complete.
- 2026-07-28: Slice A completion **approved**; Slice B plan proposed
  ([`qpex-unicode-math-migrator.md`](../specs/qpex-unicode-math-migrator.md)).
- 2026-07-28: Slice B plan **approved** (“承認”). PR #71 merged. Phase 1 Red —
  `tests/test_unicode_math_migrator_red.py` + `tests/fixtures/migration/`.
- 2026-07-28: Slice B Red **approved**; Phase 2 Green —
  `compiler/qpex/migrate_unicode_math.py`. SV 160/160 PASS.
- 2026-07-28: Slice B Phase 3 Refactor — shared ident/space helpers and slice
  copies; no behavior change. Next: Slice C plan (CLI) or stop.

## Verification

- Slice B complete through Refactor: migrator tests PASS; SV 160/160 PASS.