# LISS-0296: Surface adoption residual (applied selective + ledger)

## Metadata

- Local issue ID: LISS-0296
- Status: **complete** (2026-08-03)
- Type: Feature examples + docs hygiene
- Priority: P2
- Depends: LISS-0291 **complete**; LISS-0295 **complete**
- Branch: `feature/liss-0296-surface-adoption-residual`

## Summary

Close remaining **sample face** debt after WP-0089 / 0290–0295:

1. Applied multi-file mains still used bare `import .pkg` (whole module) —
   convert to selective braces + short names (ADR 0177).
2. A06 pure SSH scores (`band_gap`, `topological_index`) → free fns; keep
   `SSHSystem` only for mutable clock `step()`.
3. Friction ledger §5 truth-up for nested-board demotion, free-fn closes, and
   remaining Operator free-fn residual.

## Touched samples

- A02, A04, A06, A07, A09, A10 mains
- A06 `ssh_parameters.sqx`

## Exit

- [x] Selective imports on applied multi-file mains
- [x] A06 free pure scores
- [x] Friction ledger §5 updated
- [x] seed-0 on touched applied mains
