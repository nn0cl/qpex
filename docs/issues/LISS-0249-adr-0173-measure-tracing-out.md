# LISS-0249: ADR 0173 — `measure … tracing_out …` leftover policy

## Metadata

- Local issue ID: LISS-0249
- Status: **open** (ADR **Proposed**; awaiting Accept)
- Type: Architecture Path (docs)
- Priority: P1
- Parent: pedagogy ADR batch after S01-R3
  ([scorecard](../specs/staqex-v1-s01-coverage-scorecard.md);
  [minimal dialect](../architecture/physicist-minimal-dialect.md) D2)
- Branch: `docs/adr-0173-measure-tracing-out`
- Approval: Adjudicator「承認」(2026-08-02) — draft Proposed ADR only
- ADR: [0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)

## Intent

Record and index **Proposed** ADR 0173 so leftover LINEAR wires can leave via
explicit Born partial trace at terminal `measure`, instead of ritual
`state sibling = |0>` hand-kills.

## Exit (this Issue — docs)

- [x] ADR 0173 file under `docs/architecture/adr/`
- [x] Architecture README index entry
- [x] Local issue claim in `local-issue-planning.md`
- [x] Scorecard / dialect pointers to the Proposed ADR
- [ ] Adjudicator **Accept** (or revise) of ADR 0173
- [ ] Post-Accept Feature Issue filed for Kernel Red (grammar / HIR / evaluator)

## Non-goals

- Kernel grammar, HIR, evaluator, or S01 `.sqx` edits under this Issue
- Type-First fields ADR (batch item ②)
- Failure glossary ADR (batch item ③)
- Rest-sugar `tracing_out others` / `*`

## Notes

Proposed ≠ implementation. After Accept, open a Feature Issue before Phase 1
Red; do not implement on this docs branch without a new phase/Issue approval.
