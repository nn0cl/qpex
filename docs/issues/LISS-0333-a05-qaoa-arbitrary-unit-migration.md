# LISS-0333: migrate `A05_qaoa_portfolio` to dimensioned arbitrary-cost-unit Hamiltonians (WP-0095 work unit 3)

## Metadata

- Local issue ID: LISS-0333
- Status/phase: proposed / pre-Phase-1 (2026-08-05)
- Type: Feature Path (example content only —
  `examples/applied/A05_qaoa_portfolio/main_qaoa_portfolio.sqx`,
  `README.md`; no Kernel/grammar change)
- Priority: P1
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 3 (first of the remaining 13 example migrations)
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md) (real
  ℏ, merged); [LISS-0332](LISS-0332-a03-h2-real-unit-migration.md) (first
  migration precedent, merged)
- Blocks: none within WP-0095 (each remaining migration is independent)
- Branch: `feature/liss-0333-a05-qaoa-arbitrary-unit-migration`
- GitHub Issue / PR: none yet

## Design decision carried into this Issue (resolved before Plan approval)

`A05_qaoa_portfolio` is not a physically-modeled system the way
`A03_h2_vqe` is: its `H_cost`/`H_mixer` coefficients are QUBO portfolio
cost weights, not literature-traceable physical energies. ADR 0195's
"source from public references, not invented" rule presumes a real
physical system to source from; a QAOA cost Hamiltonian has none. This
was surfaced as a Hard Stop design question and resolved with the
Adjudicator before proceeding:

- **Adopted approach**: give `H_cost`/`H_mixer` and the evolution
  durations real, dimensioned `Energy`/`Time` values (satisfying
  ADR 0195's Kernel-level fail-closed requirement, confirmed live —
  bare/implicit-`1` coefficients blow up the `hbar`-divided phase
  magnitude and are rejected), but explicitly and honestly document that
  the specific magnitudes are **arbitrary problem-defined cost units**,
  not physical constants — an extension of the same honesty pattern
  LISS-0332 used for A03's illustrative evolution duration, applied here
  to the Hamiltonian coefficients themselves.
- **Rejected**: inventing a physically-plausible hardware energy scale
  (e.g. superconducting-qubit MHz/GHz couplings) for the coefficients —
  rejected as more likely to mislead a reader into thinking the numbers
  are hardware-derived than the "arbitrary units, honestly labeled"
  approach.
- **Rejected**: treating A05 as exempt from ADR 0195 and leaving it
  dimensionless — rejected because the Kernel's fail-closed check
  (LISS-0330) has no such exemption mechanism today, and adding one
  (e.g. a `CostEnergy`/`CostTime` custom dimension family) would itself
  be a Kernel change, out of scope for this Issue. Confirmed live: a
  fully dimensionless `evolve` on this example still fails with
  `EVOLVE_UNRESOLVED_UNIT_ERROR` under the current Kernel.
- Wording guidance adopted for the README/`.sqx` comments (Adjudicator
  direction): phrase the coefficients as "relative cost weights, not
  physical energies" (avoiding "抽象的" framing that could read as
  hedging), and phrase the ADR-0195 relationship as "ADR 0195 applies to
  examples modeling real physical Hamiltonians; this example's QUBO cost
  Hamiltonian is given real Energy/Time dimensions to satisfy the
  Kernel's fail-closed requirement, but its magnitudes are arbitrary
  problem-defined units, not literature-traced physical constants."

## Intent

1. Give each of `H_cost`'s three terms and `H_mixer`'s two terms an
   explicit `Energy`-dimensioned coefficient (confirmed live: an
   implicit/bare coefficient of `1` on `H_mixer` causes
   `RUNTIME_ERROR: evolve magnitude |H*t/hbar| ~= 2**113 exceeds the
   sparse evolution step budget` — not silently wrong, but a hard
   failure, so every term needs an explicit value).
2. Replace both bare `evolve ... for 0.4` / `for 0.3` durations with real
   `Time` values (`fs`-scale, matching LISS-0332's precedent), keeping
   the same relative ratio between the mixer and cost step durations.
3. Preserve the original relative magnitudes of the QUBO weights
   (`-0.6`, `-0.4`, `0.5` for cost; `1` for both mixer terms) scaled onto
   an `eV`/`fs` magnitude that keeps `|H*t/hbar|` in a physically
   sane phase range — confirmed live below, not merely asserted.
4. Add a one-to-two-line comment in the `.sqx` source and a new "Units
   and interpretation" section in the README (contrasting explicitly
   with A03) stating the coefficients are arbitrary relative cost
   weights, not physical energies, per the wording guidance above.

## Explicitly out of scope

- Any Kernel-level custom-dimension family (`CostEnergy`/`CostTime`) for
  non-physical Hamiltonians — noted as a possible future idea in the
  design decision above, not pursued here.
- Any other example's migration (work unit 3's remaining items:
  A06/A10/A11/B04/B07/B08/B16/S01×5/quantum_matter_discovery).
- Any change to the QAOA algorithm itself (still one `p=1` layer, no
  classical optimizer loop) — unchanged, already honestly disclaimed in
  the README.

## Acceptance reference

```gherkin
Feature: A05_qaoa_portfolio uses dimensioned (arbitrary-unit) Hamiltonians

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated main_qaoa_portfolio.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement

  Scenario: the README honestly labels the coefficients as arbitrary cost units
    Given the same example
    When its README is read
    Then it states the Hamiltonian magnitudes are arbitrary problem-defined
      units, not physical constants, distinguishing this from A03
```

## Verification plan for this design intake (not shipped as a test)

Confirmed live in this session before finalizing the source:

- `Energy c0 = 0.6.eV to J` etc. as `Operator` term coefficients compile
  and run (`Operator H_cost = (-c0) * Z[0] - c1 * Z[1] + c2 * (Z[0] *
  Z[1])`).
- A bare `Operator H_mixer = X[0] + X[1]` (implicit coefficient `1`,
  whatever default unit that resolves to) fails at runtime with
  `RUNTIME_ERROR: evolve magnitude |H*t/hbar| ~= 2**113 exceeds the
  sparse evolution step budget` — confirming every term needs an
  explicit `Energy` coefficient, not just the ones that already had
  non-unity weights.
- `Operator H_mixer = m * X[0] + m * X[1]` with `Energy m = 1.0.eV to J`
  and `Time dur = 0.4.fs` / `dur2 = 0.3.fs` compiles, runs
  (`status: succeeded`), and reaches a non-vacuum measurement
  (`MeasurementEnvelope(value=1, marginal={0: 0.5, 1: 0.5}, vacuum=False)`).

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `S` — no Kernel change; one example's `.sqx` rewrite (add
  explicit Energy coefficients to existing terms, real Time durations)
  and one README section addition.
- Route: direct implementation by this session.
- Assumptions: the specific `eV`/`fs` magnitudes chosen preserve the
  original QUBO weight ratios and keep the evolution's `|H*t/hbar|`
  phase magnitude in a sane range; they carry no physical claim beyond
  that, per the design decision above.
- Confidence: high (syntax and magnitude range directly verified live).
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason
      (`EVOLVE_UNRESOLVED_UNIT_ERROR` on the current bare `for 0.4`
      duration).
- [ ] Phase 2 Green: `.sqx` rewritten with explicit `Energy`/`Time`
      values; test passes.
- [ ] Phase 3 Refactor: README "Units and interpretation" section added;
      reviewer empathy summary written.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check` — confirm A05 no longer appears in
      `test_applied_catalog_health_red.py`'s failure list and no new
      failures are introduced.
- [ ] WP-0095 work unit 3 row updated.

## Non-goals

- Kernel-level custom-dimension family for non-physical Hamiltonians.
- Remaining example migrations (A06/A10/A11/B04/B07/B08/B16/S01×5/
  quantum_matter_discovery).
- QAOA algorithm changes (classical optimizer loop, multi-layer `p>1`).
