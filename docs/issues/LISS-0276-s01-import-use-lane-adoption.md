# LISS-0276: S01 selective import + use Enum + lane adoption

## Metadata

- Local issue ID: LISS-0276
- GitHub issue: _(none yet)_
- Status: **complete** (2026-08-03) — spine; other chapter mains still FQN-heavy
- Phase: Feature examples (Kernel 0177/0178 already shipped)
- Type: Feature Path
- Priority: P0
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md)
- Pairs with: [LISS-0277](LISS-0277-s01-domain-struct-first.md)
- Paths: `examples/showcase/S01_quantum_disaster_response/**/*.sqx` (mains + imports)

## Summary

Adopt **shipped** selective import and `use Enum.*` across S01 so spine and
chapters stop repeating `Disaster.Domain.*` forests. Label spine with
`// staqex-lane: experiment` (and keep circuit lanes labeled). Do not change
physics narrative or constellation structure.

## Problem

ADR 0177/0178 are on main; **examples adoption = 0**. Spine has ~58 `Disaster.*`
FQNs and long reverse-DNS import lists → enterprise first screen.

## Exit

- [ ] Spine + major chapter mains use `import path.{A,B}` where multi-symbol
- [ ] `use Enum.*` at when-arm sites that currently FQN enum cases (where legal)
- [ ] Causal spine carries `// staqex-lane: experiment` (or equivalent honesty)
- [ ] Circuit samples keep `// staqex-lane: circuit`
- [ ] No new inspect museum; no identity evolve
- [ ] seed-0 / existing S01 tests still pass
- [ ] FQN count on spine first screen materially reduced (document before/after)

## Non-goals

- class→struct demotion (0277)
- Package root rename (0279)
- Relative import sugar (0287) until shipped — then 0289

## Verification

- Existing S01 pytest / seed-0 scripts
- Aesthetic: first 40 lines of `main_disaster_response.sqx`
