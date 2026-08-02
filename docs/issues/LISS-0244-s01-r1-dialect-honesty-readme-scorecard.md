# LISS-0244: S01-R1 dialect honesty (README + scorecard constellation)

## Metadata

- Local issue ID: LISS-0244
- Status: **complete** (2026-08-02)
- Type: docs / Fast Path
- Priority: P1
- Parent redesign: [staqex-v1-s01-redesign-toward-minimal-dialect.md](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md) slice **S01-R1**
- Dialect: [physicist-minimal-dialect.md](../architecture/physicist-minimal-dialect.md) (**Accepted**)
- Cuts policy: [staqex-destructive-simplification-sketch.md](../architecture/staqex-destructive-simplification-sketch.md) (**Accepted**)
- Branch: `docs/physicist-minimal-dialect-and-s01-redesign`
- Implementation approval: **yes** for docs-only R1 (Adjudicator 2026-08-02:「１，２，３」)
- Out of scope: spine `.sqx` strip (R2+), Kernel / `tracing_out` ADR

## Intent

Rewrite S01 README and coverage scorecard so they match Accepted teaching law:

- Ops-inspired **language experiment**, not a city-scale OS claim.
- Scorecard = **constellation index** (path → surface), not proof that one
  `main` is an OS.
- Point at E vs H lanes and residual Class E debt (inspect flood, LINEAR kill,
  identity evolve) without pretending the spine already passes the dialect test.

## Exit criteria

- [x] README honesty aligns with minimal dialect + redesign sketch §4
- [x] Scorecard states constellation policy; flags spine Class E residuals
- [x] Links to Accepted dialect / redesign / this Issue
- [x] No `.sqx` behavior changes in R1

## Non-goals

- Stripping inspect / identity evolve from `main_disaster_response.sqx` (R2)
- Host ticket export (LISS-0243, separate branch)
- Language surface changes
