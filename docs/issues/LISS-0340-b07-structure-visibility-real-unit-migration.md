# LISS-0340: migrate `B07_structure_visibility` to real units (WP-0095 work unit 8)

## Metadata

- Local issue ID: LISS-0340
- Status/phase: proposed / pre-Phase-1 (2026-08-06)
- Type: Feature Path (example content only —
  `examples/basics/B07_structure_visibility/structure_visibility.sqx`;
  no Kernel change)
- Priority: P1
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 8
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md),
  [LISS-0336](LISS-0336-evolve-real-unit-canonicalization-bugs.md)
- Blocks: none within WP-0095
- Branch: `feature/liss-0340-b07-structure-visibility-real-unit-migration`
- GitHub Issue / PR: none yet

## Design decision

`B07_structure_visibility` teaches `namespace`/`enum`/`struct`/`pub`/
module-private fields, using `Model.IsingParams { J, h, _pad }` (bare
`Float` fields) to build a qubit-Pauli Hamiltonian
(`ising_hamiltonian(p) -> Operator`, `Z[0]*Z[1]`/`X[0]+X[1]` terms) and
`evolve (s0, s1) under H for scale * 0.25` (`scale = seg.length`, a
struct-field-derived bare duration). This example's Hamiltonian goes
through the qubit-Pauli sparse path (`compile_sparse_pauli`), the same
path LISS-0336 fixed a coalescing-epsilon bug for — so, unlike B04's
non-ℏ-divided legacy path, this one genuinely needs real, appropriately-
scaled `Energy`/`Time` values (matching A05/A06's precedent), not just a
unit-satisfying wrapper.

**Adopted fix**:
- `IsingParams.J`/`.h` become `Energy`-typed (was `Float`); constructed
  with `1.0.eV to J` / `0.5.eV to J` (ratio preserved).
- `ising_hamiltonian(p: Model.IsingParams) -> Operator` — unchanged in
  shape; confirmed live this is the already-proven-safe "struct
  parameter, `Operator` return" pattern (same as A11's
  `build_sensor_hamiltonian`, LISS-0338).
- The duration's struct-field-derived computation (`scale * 0.25`) can
  no longer directly become a `Time`-typed value (the unit-suffix
  grammar only attaches to a literal, not an arbitrary expression,
  confirmed during LISS-0337/0338/0339) — replaced with an independent
  `Time dur = 0.5.fs` (matching the original numeric ratio's rough
  scale). `Float scale = seg.length` is kept as its own line (still
  demonstrates reading a `pub` struct field into a classical value, this
  example's actual teaching point), just no longer wired into the
  evolve duration.

## Intent

1. Change `Model.IsingParams.J`/`.h` from `Float` to `Energy`.
2. Construct `params` with `J: 1.0.eV to J, h: 0.5.eV to J` (ratio
   preserved from the original `1.0`/`0.5`).
3. Replace `evolve (s0, s1) under H for scale * 0.25` with `... for
   dur`, declaring `Time dur = 0.5.fs` (keep `Float scale = seg.length`
   as its own, still-meaningful demonstration line).

## Explicitly out of scope

- Any Kernel change.
- Any other example's migration (B08/B16/S01×5/quantum_matter_discovery).
- Reconnecting the geometry (`seg.length`) to the evolve duration — no
  longer directly expressible now that durations must be real
  `Time`-typed literals or variables, not derived expressions; this
  example's teaching point (namespace/enum/struct/visibility) doesn't
  depend on that connection.

## Acceptance reference

```gherkin
Feature: B07_structure_visibility uses real physical units

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated structure_visibility.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement
```

## Verification plan for this design intake (not shipped as a test)

Confirmed live: `Model.IsingParams` with `Energy`-typed `J`/`h` fields,
constructed via named kwargs (`J: 1.0.eV to J, h: 0.5.eV to J`), passed
to `ising_hamiltonian(params) -> Operator`, evolved with `Time dur =
0.5.fs`, compiles and runs to a non-vacuum measurement.

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-06
- Size: `S` — one example file, struct field retyping plus duration fix.
- Route: direct implementation by this session.
- Confidence: high (all patterns directly verified live, each already
  established by a prior WP-0095 Issue).

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason.
- [ ] Phase 2 Green: `.sqx` rewritten; test passes.
- [ ] Phase 3 Refactor: reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check`.
- [ ] WP-0095 work unit 8 row updated.

## Non-goals

- Kernel changes.
- Remaining example migrations (B08/B16/S01×5/quantum_matter_discovery).
