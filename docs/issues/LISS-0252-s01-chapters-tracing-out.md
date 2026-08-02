# LISS-0252: S01 chapters/satellites migrate `|0>` → `tracing_out`

## Metadata

- Local issue ID: LISS-0252
- Status: **complete** (2026-08-02)
- Type: Feature Path (sample / pedagogy)
- Priority: P1
- Parent: [ADR 0173](../architecture/adr/0173-measure-tracing-out-leftover-policy.md);
  spine [LISS-0251](LISS-0251-s01-spine-tracing-out.md)
- Branch: `feature/liss-0250-measure-tracing-out` (PR #265)
- Approval: Adjudicator「続けて」(2026-08-02) — chapters/satellites after spine

## Intent

Replace ritual `|0>` leftover discharge on S01 constellation chapters and
satellites with `measure … tracing_out …`. Keep legitimate ket preparation
`|0>` / `|1>` / `|+>` binds.

## Exit

- [x] day2 / morning / route / lattice / tri / burst / fidelity migrated
- [x] fuel / comms already clean (no discharge block)
- [x] Each migrated main `--seed 0` green
- [x] Scorecard updated

## Non-goals

- Rest-sugar `tracing_out others`
- Kernel changes
- Demoting scorecard A+B
