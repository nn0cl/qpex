# LISS-0069: Canonical mathematical source and migration

## Metadata

- Local issue ID: LISS-0069
- GitHub issue: not created
- Status: **Slice C Phase 2 Green** (2026-07-28); Slice A/B complete
- Phase: phase-2-green (Slice C)
- Type: language surface / lexer / migrator
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced)
- Owner/agent: unassigned after Green review
- Related branch: `feature/liss-0069-slice-c-green`
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
CLI contract (Slice C):
[`qpex-unicode-math-migrate-cli.md`](../specs/qpex-unicode-math-migrate-cli.md).

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
| **C** | CLI `migrate` + stdout / `--write` / `--check` (formatter emit → LISS-0072) | **Phase 2 Green** |

## Non-goals (Slice C)

- Recursive / multi-file batch migrate.
- Formatter / CST pretty-print (LISS-0072).
- Changing Slice B rewrite rules.
- Bulk rewrite of `examples/` in the same Green.
- Pauli / `state` migrations (M-P01 / M-P05).
- Bra–ket matrix-element / `inner` desugar (A.1 / LISS-0073).

## Adjudicator Decision Points (Slice C plan)

- [x] Approve **Slice C** plan for Phase 1 Red (CLI wiring only).
- [x] Confirm subcommand name **`migrate`**.
- [x] Confirm default = stdout preview; `-w` / `--write` for in-place; `--check`
      for CI drift.
- [x] Confirm formatter emit stays out of Slice C (LISS-0072).
- [x] Confirm no recursive directory walk in Slice C.
- [x] Implementation: Red only until Red review (default stop before Green).

## Adjudicator Decision Points (Slice C Red)

- [x] Approve Phase 1 Red assertions (`tests/test_unicode_math_migrate_cli_red.py`).
- [x] Authorize Phase 2 Green (`cmd_migrate` + subparser; no rewrite-rule change).

## Adjudicator Decision Points (Slice C Green)

- [ ] Approve Phase 2 Green (`cmd_migrate` wiring).
- [ ] Authorize Phase 3 Refactor (readability only; no behavior change).

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
  copies; no behavior change. Slice B complete.
- 2026-07-28: Slice C plan proposed
  ([`qpex-unicode-math-migrate-cli.md`](../specs/qpex-unicode-math-migrate-cli.md)).
- 2026-07-28: Slice C plan **approved** (“承認”). PR #74 merged. Phase 1 Red —
  `tests/test_unicode_math_migrate_cli_red.py`.
- 2026-07-28: Slice C Red **approved**; Phase 2 Green — `cmd_migrate` in
  `compiler/qpex/cli.py`. CLI + migrator tests PASS; SV 160/160 PASS.

## Verification

- Slice A/B complete through Refactor: Unicode + migrator tests PASS; SV 160/160 PASS.
- Slice C Green: migrate CLI tests PASS; SV 160/160 PASS.
