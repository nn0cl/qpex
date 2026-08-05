# LISS-0341: migrate `B08_operators_hamiltonians` to real units (WP-0095 work unit 9)

## Metadata

- Local issue ID: LISS-0341
- Status/phase: proposed / pre-Phase-1 (2026-08-06)
- Type: Feature Path (example content only —
  `examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx`;
  no Kernel change)
- Priority: P1
- Initial planning size: `XS`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 9 — the last `examples/basics`/`examples/applied` entry;
  after this, only the 5 locked S01 files and `quantum_matter_discovery`
  remain
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md),
  [LISS-0336](LISS-0336-evolve-real-unit-canonicalization-bugs.md)
- Blocks: none within WP-0095
- Branch: `feature/liss-0341-b08-operators-hamiltonians-real-unit-migration`
- GitHub Issue / PR: none yet

## Design decision

`B08_operators_hamiltonians` teaches ADR 0176's **minimal dialect face**
(`// staqex-profile: experiment`-style, no `package`/`main`, no ritual
uncompute) with ADR 0180 Operator type-inference and ADR 0184 classical
multi-bind: `J, h = 1.0, 0.5` (untyped multi-bind), `H_chain = -J *
(Z[0]*Z[1]) - h*(X[0]+X[1])` (inferred `Operator`), `evolve ... for 0.7`
(bare duration). This is the same qubit-Pauli sparse-path pattern as
B07 (LISS-0340) — genuinely needs real, appropriately-scaled `Energy`/
`Time` values, not just a unit-satisfying wrapper.

**Adopted fix**: `J`/`h` become explicit `Energy`-typed declarations
(breaking pure type-inference for just these two, since a bare
multi-bind literal cannot carry unit information — confirmed no other
way to attach a unit to an inferred classical multi-bind); `H_chain`
stays inferred (no `Operator` keyword needed — confirmed live: ADR
0180's ty-fill still works with `Energy`-typed operands); the duration
becomes an explicit `Time dur = 0.7.fs`. This preserves the "minimal
dialect" teaching point (no `package`/`main`, `H_chain`/`s0,s1` stay
inferred) while satisfying ADR 0195's real-unit requirement for the two
values that must carry dimensions.

## Intent

1. `J, h = 1.0, 0.5` → `Energy J = 1.0.eV to J` / `Energy h = 0.5.eV to
   J` (ratio preserved).
2. `H_chain = ...` — unchanged (still inferred).
3. `evolve (s0, s1) under H_chain for 0.7` → `... for dur`, declaring
   `Time dur = 0.7.fs` (ratio/magnitude preserved from the original).

## Explicitly out of scope

- Any Kernel change.
- Changing `H_chain`/`s0, s1`'s inferred-type style (still demonstrates
  ADR 0180/0176).
- Remaining example migrations (the 5 locked S01 files,
  `quantum_matter_discovery`).

## Acceptance reference

```gherkin
Feature: B08_operators_hamiltonians uses real physical units

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated operators_hamiltonians.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement
```

## Verification plan for this design intake (not shipped as a test)

Confirmed live: `Energy J = 1.0.eV to J`, `Energy h = 0.5.eV to J`,
`H_chain = -J * (Z[0]*Z[1]) - h*(X[0]+X[1])` (still inferred, no
`Operator` keyword), `Time dur = 0.7.fs`, `evolve (s0, s1) under
H_chain for dur` compiles and runs to a non-vacuum measurement.

## AI planning record (size XS)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-06
- Size: `XS` — one example file, minimal targeted retyping.
- Route: direct implementation by this session.
- Confidence: high (identical pattern to B07/LISS-0340, plus a live
  confirmation that ADR 0180 inference still works with Energy operands).

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason.
- [ ] Phase 2 Green: `.sqx` rewritten; test passes.
- [ ] Phase 3 Refactor: reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check`.
- [ ] WP-0095 work unit 9 row updated.

## Non-goals

- Kernel changes.
- Remaining example migrations (5 locked S01 files,
  `quantum_matter_discovery`).
