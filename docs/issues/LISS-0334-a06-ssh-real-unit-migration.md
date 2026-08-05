# LISS-0334: migrate `A06_topological_edge_memory` to real physical units (WP-0095 work unit 4)

## Metadata

- Local issue ID: LISS-0334
- Status/phase: proposed / pre-Phase-1 (2026-08-05)
- Type: Feature Path (example content only, multi-file —
  `examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx`,
  `operators/hamiltonian_builder.sqx`, `README.md`; no Kernel/grammar
  change)
- Priority: P1
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 4
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0330](LISS-0330-real-hbar-kernel-primitive.md) (real
  ℏ, merged)
- Blocks: none within WP-0095 (each remaining migration is independent)
- Branch: `feature/liss-0334-a06-ssh-real-unit-migration`
- GitHub Issue / PR: none yet

## Design decision carried into this Issue (resolved before Plan approval)

`A06_topological_edge_memory` builds an SSH (Su-Schrieffer-Heeger)
tight-binding chain — a real, published physical model class (Su,
Schrieffer, Heeger 1979, cited in the README), unlike A05's abstract
QUBO. SSH hopping amplitudes are a real physical `Energy` quantity in
real materials (e.g. polyacetylene, typical scale ~eV). However, the
existing hop coefficients (`v_intra=0.5`, `w_inter=1.5`, a 1:3 ratio) are
not tied to any specific cited measurement — the README already
describes this example as "pedagogical," not a reproduction of a
specific paper's numeric SSH parameters. This was presented to the
Adjudicator as a design choice among three options and resolved before
Plan approval:

- **Adopted approach** (mirrors LISS-0332's treatment of A03's
  illustrative evolution duration, not a fresh literature derivation):
  convert the existing hop coefficients to real `Energy` values at an
  `eV` scale, preserving their existing 1:3 ratio unchanged, and
  document them as physically plausible in magnitude for a tight-binding
  system but **not** literature-traced to a specific measurement —
  consistent with the README's existing "pedagogical" framing.
- **Rejected**: a full literature derivation of real polyacetylene
  hopping/dimerization values (the A03 treatment) — rejected as
  disproportionate additional research effort for an example the README
  already discloses as pedagogical rather than literature-reproducing.
- **Rejected**: treating the coefficients as arbitrary non-physical units
  (the A05 treatment) — rejected because the SSH model's hopping
  amplitude is a genuinely real physical `Energy` quantity in real
  materials, unlike a QUBO cost weight; labeling it "arbitrary" would
  understate what the quantity physically represents.

## Intent

1. In `operators/hamiltonian_builder.sqx`, declare `Energy v = 0.5.eV to
   J` and `Energy w = 1.5.eV to J` inside `build_ssh_hamiltonian()`,
   replacing the bare `0.5`/`1.5` literals multiplying the `hop(i, j)`
   terms (ratio unchanged, confirmed live to compile and run across the
   module boundary).
2. In `main_topological_edge_memory.sqx`, replace `evolve psi under Hssh
   for 0.5` with a real `Time` duration (`fs`-scale, matching prior
   migrations' precedent).
3. Add a short comment in `hamiltonian_builder.sqx` and a new "Units and
   interpretation" README section stating the `eV` magnitudes are
   physically plausible for a tight-binding hopping amplitude but not
   traced to a specific cited measurement (contrast with A03; different
   honesty category from A05's arbitrary units).
4. Leave `SSHParams`/`band_gap`/`topological_index` (Float-typed,
   diagnostic-only "notebook quantities," never fed into `evolve`)
   unchanged — out of scope, no fail-closed check applies to them.

## Explicitly out of scope

- A literature-grounded derivation of real polyacetylene SSH parameters
  (rejected above).
- Reconciling `SSHParams` (currently unused by `build_ssh_hamiltonian()`,
  a pre-existing structural quirk) with the Hamiltonian builder — not
  part of this migration's scope.
- Any other example's migration (A10/A11/B04/B07/B08/B16/S01×5/
  quantum_matter_discovery).

## Acceptance reference

```gherkin
Feature: A06_topological_edge_memory uses real physical units

  Scenario: the migrated example compiles and runs to a real terminal measurement
    Given the migrated main_topological_edge_memory.sqx and hamiltonian_builder.sqx
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement
```

## Verification plan for this design intake (not shipped as a test)

Confirmed live in this session before finalizing the source: a minimal
reproduction of `build_ssh_hamiltonian()` returning an `Operator` built
from `Energy`-scaled `hop(i, j)` terms, called from `main()` with a real
`Time` duration, compiles and runs to a non-vacuum measurement
(`MeasurementEnvelope(value=4, ..., vacuum=False)`).

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `S` — no Kernel change; two `.sqx` files' small edits, one
  README section addition.
- Route: direct implementation by this session.
- Assumptions: the `eV` magnitude and preserved 1:3 ratio are physically
  plausible for a tight-binding hopping amplitude; no specific literature
  measurement is claimed, per the design decision above.
- Confidence: high (syntax and cross-module behavior directly verified
  live).
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason
      (`EVOLVE_UNRESOLVED_UNIT_ERROR` on the current bare `for 0.5`
      duration).
- [ ] Phase 2 Green: `.sqx` files rewritten with explicit `Energy`/`Time`
      values; test passes.
- [ ] Phase 3 Refactor: README "Units and interpretation" section added;
      reviewer empathy summary written.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check` — confirm A06 no longer appears in
      `test_applied_catalog_health_red.py`'s failure list and no new
      failures are introduced.
- [ ] WP-0095 work unit 4 row updated.

## Non-goals

- Literature-grounded SSH/polyacetylene parameter derivation.
- Reconciling `SSHParams` with `build_ssh_hamiltonian()`.
- Remaining example migrations (A10/A11/B04/B07/B08/B16/S01×5/
  quantum_matter_discovery).
