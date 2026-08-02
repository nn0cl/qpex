# LISS-0249: ADR 0173 — `measure … tracing_out …` leftover policy

## Metadata

- Local issue ID: LISS-0249
- Status: **complete** (2026-08-02) — ADR **Accepted**
- Type: Architecture Path (docs)
- Priority: P1
- Parent: pedagogy ADR batch after S01-R3
  ([scorecard](../specs/staqex-v1-s01-coverage-scorecard.md);
  [minimal dialect](../architecture/physicist-minimal-dialect.md) D2)
- Branch: `docs/adr-0173-measure-tracing-out`
- Approval: Adjudicator「承認」(2026-08-02) — Proposed draft; second「承認」Accept
- ADR: [0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)
  (**Accepted**)
- Follow-on: [LISS-0250](LISS-0250-measure-tracing-out-red.md) (Kernel Red;
  Phase approval pending)

## Intent

Record and Accept ADR 0173 so leftover LINEAR wires can leave via explicit
Born partial trace at terminal `measure`, instead of ritual
`state sibling = |0>` hand-kills.

## Exit (this Issue — docs)

- [x] ADR 0173 file under `docs/architecture/adr/`
- [x] Architecture README index entry
- [x] Local issue claim in `local-issue-planning.md`
- [x] Scorecard / dialect pointers
- [x] Adjudicator **Accept** of ADR 0173
- [x] Post-Accept Feature Issue filed ([LISS-0250](LISS-0250-measure-tracing-out-red.md))

## Non-goals

- Kernel grammar, HIR, evaluator, or S01 `.sqx` edits under this Issue
- Type-First fields ADR (batch item ②)
- Failure glossary ADR (batch item ③)
- Rest-sugar `tracing_out others` / `*`
- Phase 1 Red (see LISS-0250)

## Notes

Accept ≠ Phase approval. Do not start Kernel Red until LISS-0250 Plan / Phase 1
is explicitly approved.
