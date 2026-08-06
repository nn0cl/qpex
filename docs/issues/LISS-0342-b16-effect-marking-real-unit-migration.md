# LISS-0342: migrate `B16_effect_marking` to real units (WP-0095 work unit 10)

## Metadata

- Local issue ID: LISS-0342
- Status/phase: proposed / pre-Phase-1 (2026-08-06)
- Type: Feature Path (example content only —
  `examples/basics/B16_effect_marking/effect_marking.sqx`; no Kernel
  change)
- Priority: P1
- Initial planning size: `XS`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 10 — found unmigrated during LISS-0341's honest correction
  (not exercised by any `spec_verification` suite, so absent from the
  161/161 figure)
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md),
  [LISS-0336](LISS-0336-evolve-real-unit-canonicalization-bugs.md)
- Blocks: none within WP-0095
- Branch: `feature/liss-0342-b16-effect-marking-real-unit-migration`
- GitHub Issue / PR: none yet

## Design decision

`B16_effect_marking` teaches ADR 0081 explicit effect marking (a
library `fn peek_zz(...) -> State<Float> effects { Inspect } {...}`)
using the same untyped multi-bind qubit-Pauli Hamiltonian pattern as
B08 (LISS-0341): `J, h = 1.0, 0.5`, `H = -J*(Z[0]*Z[1]) -
h*(X[0]+X[1])` (inferred), `evolve ... for 0.5` (bare duration). Same
fix as B08: `J`/`h` become explicit `Energy`-typed (ratio preserved);
`H` stays inferred; duration becomes explicit `Time`. The `peek_zz`
effect-marking teaching point is untouched.

## Intent

1. `J, h = 1.0, 0.5` → `Energy J = 1.0.eV to J` / `Energy h = 0.5.eV to
   J`.
2. `evolve (s0, s1) under H for 0.5` → `... for dur`, declaring `Time
   dur = 0.5.fs`.

## Explicitly out of scope

- Any Kernel change.
- The `peek_zz` effect-marking mechanism itself.
- Remaining example migrations (5 locked S01 files,
  `quantum_matter_discovery`).

## Acceptance reference

```gherkin
Feature: B16_effect_marking uses real physical units

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated effect_marking.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement
```

## Verification plan for this design intake (not shipped as a test)

Confirmed live: identical structure to B08 (`Energy J`/`h`, inferred
`H`, `Time dur`) plus the unchanged `peek_zz` effect-marked helper
compiles and runs to a non-vacuum measurement.

## AI planning record (size XS)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-06
- Size: `XS` — identical pattern to LISS-0341/B08.
- Route: direct implementation by this session.
- Confidence: high.

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason.
- [ ] Phase 2 Green: `.sqx` rewritten; test passes.
- [ ] Phase 3 Refactor: reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check`.
- [ ] WP-0095 work unit 10 row updated.

## Non-goals

- Kernel changes.
- Remaining example migrations (5 locked S01 files,
  `quantum_matter_discovery`).
