# LISS-0246: S01-R2 spine dialect pass (inspect / identity evolve / fuel until)

## Metadata

- Local issue ID: LISS-0246
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: P1
- Parent redesign: [S01 redesign sketch](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md) slice **S01-R2**
- Dialect: [physicist-minimal-dialect.md](../architecture/physicist-minimal-dialect.md) (**Accepted**)
- Prior: [LISS-0244](LISS-0244-s01-r1-dialect-honesty-readme-scorecard.md) (R1), [LISS-0245](LISS-0245-s01-expressiveness-review-scenario-expansion.md) (E0 intake; R2 authorized by Adjudicator 2026-08-02「承認」)
- Branch: `feature/liss-0246-s01-r2-spine-dialect`
- Implementation approval: **yes** (Adjudicator「承認」)

## Intent

Make tonight spine pass the dialect scoring rule for the fatal anti-patterns:

1. Remove `inspect` / `viewed_*` flood from `main_disaster_response.sqx`
2. Remove identity `evolve times 2 { (plan0, plan1) }`
3. Move soft-only `evolve … until` fuel demo off the spine into a labeled
   Non-placeable satellite (keep scorecard evidence path)
4. Keep sparse `expect` + terminal `measure plan0`; retain LINEAR discharge
   only as documented residual until `tracing_out` ADR
5. Preserve Host ticket non-vacuum (LISS-0243) under seed 0

## Exit criteria

- [x] Spine has **zero** `inspect(`
- [x] Spine has no identity `evolve times`
- [x] `evolve … until` evidence on a Non-placeable satellite (or chapter)
- [x] `run_path` / ticket export seed 0: non-vacuum or fail-closed
- [x] Scorecard / README updated; no A+B row deleted without demotion note
- [x] pytest for export / spine still green

## Non-goals

- Full dialect-length spine (domain Float theater shrink = R3)
- `tracing_out` language surface
- Morning/day2 inspect strip (separate; scorecard still indexes them)
