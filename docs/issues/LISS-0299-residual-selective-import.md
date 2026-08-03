# LISS-0299: Residual selective import + bare-pipe transitive link

## Metadata

- Local issue ID: LISS-0299
- Status: **complete** (2026-08-03)
- Type: Feature examples + Kernel residual (ADR 0177 / LISS-0295)
- Priority: P2
- Depends: LISS-0295 **complete**
- Branch: `feature/liss-0299-residual-selective-import`

## Summary

1. **Sample face** — convert remaining bare module imports to selective braces:
   - B09: `WalkEnvironment` + walk operators (field harvest of `n_steps` retained)
   - S01 spine: `compose_*` / `local_priority_bump` (compose free-fns made `pub`)
   - S01 morning/day2: theatre_scale constants named explicitly
   - S01 tri: `DisasterLink` system seat

2. **Kernel residual** — LISS-0295 transitive free-fn expansion only collected
   `Call` callees. Bare pipe stages (`seed |> dbl_priority`) left unary helpers
   unlinked → runtime `unknown function`. Now collect `Pipe.rhs` when it is a
   `Var`.

## Exit

- [x] Sample selective imports
- [x] Bare-pipe transitive link + unit test
- [x] seed-0 B09 + S01 spine/morning/day2/tri
