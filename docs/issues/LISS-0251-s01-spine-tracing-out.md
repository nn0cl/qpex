# LISS-0251: S01 spine migrate `|0>` discharge → `tracing_out`

## Metadata

- Local issue ID: LISS-0251
- Status: **complete** (2026-08-02)
- Type: Feature Path (sample / pedagogy)
- Priority: P1
- Parent: [ADR 0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md)
  (**Accepted**); Kernel [LISS-0250](LISS-0250-measure-tracing-out-red.md)
- Branch: `feature/liss-0250-measure-tracing-out` (stacked on Kernel Green; PR #265)
- Approval: Adjudicator「spine 移行」(2026-08-02)

## Intent

Replace ritual `state sibling = |0>` hand-kills on the tonight spine
[`main_disaster_response.sqx`](../../examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx)
with terminal `measure … tracing_out …` (ADR 0173).

## Exit

- [x] Spine measure uses `tracing_out` for live leftover State carriers
- [x] No ritual `|0>` discharge block before measure on the spine
- [x] `python3 -m compiler.staqex run …/main_disaster_response.sqx --seed 0` green
- [x] Scorecard / README / dialect pointers updated
- [x] Non-spine chapters / satellites **not** required in this Issue

## Non-goals

- Migrating morning / day2 / satellites (optional follow-on)
- Rest-sugar `tracing_out others`
- Demoting scorecard A+B rows
- Kernel changes (already LISS-0250)
