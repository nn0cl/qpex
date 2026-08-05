# LISS-0332: migrate `A03_h2_vqe` to real physical units (WP-0095 work unit 2)

## Metadata

- Local issue ID: LISS-0332
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — awaiting
  Plan approval before Phase 1 Red
- Type: Feature Path (Kernel — `compiler/staqex/dimensions.py` new `Ha`
  unit; example content — `examples/applied/A03_h2_vqe/main_h2_vqe.sqx`,
  `README.md`; no grammar/parser change beyond what LISS-0331 already
  shipped)
- Priority: P1
- Initial planning size: `M`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 2 (first example migration)
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md);
  physics derivation grounded in
  [docs/research/2026-08-05-h2-two-orbital-jordan-wigner-cross-validation.md](../research/2026-08-05-h2-two-orbital-jordan-wigner-cross-validation.md)
  (merged)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md) (real
  ℏ, merged); [LISS-0331](LISS-0331-second-quantized-leading-coefficient.md)
  (leading-coefficient parse fix, merged)
- Blocks: WP-0095 work unit 3+ (remaining 13 example migrations)
- Branch: `feature/liss-0332-a03-h2-real-unit-migration`
- GitHub Issue / PR: none yet

## Intent

`examples/applied/A03_h2_vqe/main_h2_vqe.sqx` currently uses a bare
fermionic hopping+interaction Hamiltonian with implicit (dimensionless)
coefficient 1 on each term, and `evolve ... for 0.5` (bare, dimensionless
duration) — both now rejected at runtime by LISS-0330's fail-closed
`EVOLVE_UNRESOLVED_UNIT_ERROR`. This Issue gives it real, dimensioned
values:

1. Add `Ha` (Hartree) to `dimensions.py`'s `Energy` unit tables —
   CODATA 2018 value `1 Ha = 4.3597447222071e-18 J` (a measured
   constant, not exact-by-definition the way `eV` is; comment this
   distinction, matching the existing `u`/`oz_t` precedent for
   CODATA-sourced, non-exact constants).
2. Extend the fermionic Hamiltonian with the two on-site energy terms it
   previously lacked (`create[0]*annihilate[0]`, `create[1]*annihilate[1]`),
   parameterized with the values derived in the research note:
   `ε0 = -1.8302 Ha` (as a positive `Energy` magnitude, negated via a
   parenthesized OpDSL coefficient per LISS-0331's documented
   parenthesized-form support — a bare unary-minus-prefixed named
   coefficient is not covered by that fix and was confirmed still
   broken during this Issue's design intake), `ε1 = -0.2738 Ha`,
   `t = 0.182 Ha`, `U = 2.2864 Ha`.
3. Add the nuclear-repulsion constant `E_nn = 0.705570 Ha` as a separate
   `Operator H = H_elec + Enn * I` term after the Jordan-Wigner mapping
   (confirmed working syntax during design intake).
4. Replace `evolve ... for 0.5` with a real `Time` duration
   (`1.0 fs`) — explicitly documented as an illustrative choice (no
   specific published Trotter-step protocol is being reproduced), unlike
   the Hamiltonian coefficients, which are literature-traced.
5. Rewrite the README's Honesty table: what is now literature-traced
   (ε0/ε1/t/U, cross-checked in the research note) vs. illustrative
   (the evolution duration) vs. still not claimed (production molecular
   integrals/basis-set computation, VQE optimizer loop — unchanged from
   today's honest "No").

## Explicitly out of scope

- Running the "Follow-up" live numerical cross-check from the research
  note (dumping Staqex's own compiled `QubitOperator` coefficients and
  diffing against the ENCCS fixture) — confirmed with the Adjudicator as
  separate, optional follow-up work, not required for this migration.
  This Issue's own manual verification (below) is a lighter, one-time
  sanity check during design intake, not a shipped automated test.
- Any other example's migration (work unit 3+).
- A general fix for bare unary-minus-prefixed leading coefficients in
  second-quantized expressions (`-e0mag * create[0]...` without
  parentheses) — confirmed still broken during this Issue's design
  intake, worked around with parentheses per LISS-0331's own documented
  boundary; not re-opening that Issue's scope here.
- Any VQE optimizer loop, parameter-shift gradients, or production
  molecular integrals — the README's existing honest "No" claims for
  these are unchanged.

## Acceptance reference

New Phase 1 scenarios (no existing spec section covers this specific
example's content — the acceptance evidence is that the migrated example
compiles, runs, and produces the intended real-unit physics):

```gherkin
Feature: A03_h2_vqe uses real physical units

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated main_h2_vqe.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement

  Scenario: hbar is used, not the retired natural-units convention
    Given the same program
    When it runs
    Then the evolution reflects the real hbar division (confirmed by the
      Hamiltonian/duration magnitudes being real Joules/seconds, not bare
      floats)
```

## Verification plan for this design intake (not shipped as a test)

Before writing the final source, the following were confirmed live in
this session, informing the exit criteria above:

- `Energy e = 1.0.eV to J` and `Time dur = 1.0.fs` both compile and carry
  a resolvable unit (`self.scalar_units`), satisfying LISS-0330's
  fail-closed check.
- `Operator H = H_elec + enn * I` (adding a constant after JW mapping)
  compiles and runs.
- `Energy e0mag = 1.8302.eV to J` (positive magnitude) as a leading
  `FermionOperator` coefficient compiles, per LISS-0331.
- A bare `-e0mag * create[0]*...` (unary minus, no parens) still fails
  with the same class of `PARSE_ERROR` LISS-0331 fixed for other forms —
  confirmed out of that fix's documented scope. `(-e0mag) * create[0]*...`
  (parenthesized) compiles correctly.

## AI planning record (size M)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `M` — one small dimension-table addition (`Ha`), one example's
  `.sqx` rewrite, one README rewrite. No new grammar/parser/evaluator
  code beyond what LISS-0330/0331 already shipped.
- Route: direct implementation by this session.
- Assumptions: the derived ε0/ε1/t/U/E_nn values (research note) are
  correct as derived; per the Adjudicator's explicit direction, no
  live numerical cross-check against Staqex's own compiled coefficients
  is required before shipping this migration (tracked as separate,
  optional follow-up work in the research note).
- Confidence: high for the syntax (directly verified live); medium for
  the specific numeric values (symbolic derivation only, per the research
  note's own stated limitations — secondary-sourced literature
  coefficients, not independently re-verified against the primary PDF).
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance test(s) for the scenarios above exist and
      fail for the documented reason (today's `.sqx` uses bare literals,
      rejected by `EVOLVE_UNRESOLVED_UNIT_ERROR`).
- [ ] Phase 2 Green: `Ha` unit added; example and README rewritten; tests
      pass without editing them.
- [ ] Phase 3 Refactor: no behavior change beyond the intended migration;
      reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q` (report the exact count — this
      migration should reduce LISS-0330's 66-failure count by however
      many tests reference `A03_h2_vqe`), `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] WP-0095 work unit 2 row updated.

## Non-goals

- The live numerical cross-check (research note Follow-up).
- Remaining example migrations (work unit 3+).
- General unary-minus-leading-coefficient parser support.
