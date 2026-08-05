# LISS-0338: rewrite A11_noether_forge as a structural-monitoring quantum magnetometer (WP-0095 work unit 6)

## Metadata

- Local issue ID: LISS-0338
- Status/phase: proposed / pre-Phase-1 (2026-08-05)
- Type: Feature Path (example content rewrite, multi-file — all 14
  files under `examples/applied/A11_noether_forge/` plus `README.md`;
  no Kernel/grammar change)
- Priority: P1
- Initial planning size: `L`
- Owner / agent: Claude Code
- Program: [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md)
  work unit 6
- Parent: [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md)
- Depends on: [LISS-0336](LISS-0336-evolve-real-unit-canonicalization-bugs.md),
  [LISS-0337](LISS-0337-spec-verification-suite-real-unit-fixtures.md)
  (both merged; this Issue's physics numbers were re-verified live under
  the fixed Kernel, since the original pre-bugfix exploration's numbers
  are no longer valid)
- Blocks: none within WP-0095
- Branch: `feature/liss-0338-a11-structural-monitoring-magnetometer`
- GitHub Issue / PR: none yet

## Design decision (already approved by the Adjudicator this session,
recorded here for the formal record)

A11's original "Noether Forge" quantum-matter-discovery theme (LISS-0120)
was rejected/deferred and formally marked "optional salvage only — not
authoritative" per `staqex-v1-showcase-mission-lock.md`. With the
Adjudicator's explicit direction to rethink A11's content while keeping
the "language review gate" spirit — and explicit freedom to freely
rewrite the existing 14-file ownership tree — this Issue rethemes A11 as
a **quantum magnetometer array for structural monitoring** (stress/
defect-induced magnetic-field distortion detection), the first of three
queued quantum-sensing themes (see memory: medical biomagnetic and
resource-exploration magnetic-anomaly detection are queued as future
candidates, not this Issue).

**Physics model:**
- NV (nitrogen-vacancy) center diamond spin qubits, a real, extensively
  published quantum-sensing platform (Doherty, M.W. et al. "The
  nitrogen-vacancy colour centre in diamond." *Physics Reports* **528**,
  1–45 (2013)). Ground-state zero-field splitting D ≈ 2.87 GHz is a
  well-established, frequently-cited real physical constant.
- **Rotating-frame simplification** (standard practice in magnetic
  resonance / ESR simulation): the D-splitting term is not itself
  simulated — it defines the qubit basis and is transformed away, so
  only the physically relevant *smaller* terms (defect-induced
  transverse coupling, inter-sensor dipolar coupling) are evolved. This
  is disclosed explicitly in the README, not hidden.
- A 3-sensor array (sites 0/1/2, site 1 "stressed", 0/2 "healthy").
  Stress/defect-induced strain shifts the stressed sensor's local
  Hamiltonian via a transverse (`X`) term (NV strain-magnetic coupling
  is real, documented physics — Barson et al. 2017 *Nano Lett.*,
  MacQuarrie et al. 2013 *PRL*). Neighboring sensors are weakly coupled
  via a real dipolar `ZZ` interaction. Magnitudes (15 MHz defect shift,
  500 kHz dipolar coupling) are physically plausible in order for real
  NV arrays but not traced to one specific cited measurement — the same
  honesty category established for A06/A10's SSH treatment.
- Noether-lineage callback (keeps the "language review gate" spirit
  alive in the *content*, not the governance sense): the defect breaks
  the array's site-permutation symmetry; that broken symmetry is the
  detection signal, read out via `physics/symmetries.sqx`.

**Re-verified live under the LISS-0336/0337-fixed Kernel** (the design's
original physics exploration predates those fixes and is no longer
trustworthy): `defect = 15 MHz`, `dip = 500 kHz`,
`Time dur = 16.7.ns` (a quarter-Rabi-period-scale duration for the
defect coupling) gives a clearly distinguishable signal — stressed site
⟨Z⟩ ≈ −0.99 (near-full flip) vs. healthy sites ⟨Z⟩ ≈ +1.13 (near
original, with a modest above-`|1|` deviation from this Kernel's
`expect(Z, …)` not performing a true partial-trace reduced-density-matrix
calculation on an entangled multi-qubit state — an existing Kernel
simplification, not something this Issue introduces or must fix;
disclosed in the README).

## Module repurposing (all 14 existing files rewired, none left as
unwired scaffolding)

- `domain/site.sqx` — `SensorRole` (Healthy/Stressed), `SiteId`,
  `SensorSite`.
- `domain/couplings.sqx` — `SensorCouplings` (real `Energy`-typed
  `defect`, `dip`).
- `domain/lattice.sqx` — `SensorArray` (3-site chain).
- `domain/experiment_config.sqx` — `ExperimentConfig` (real `Time`
  duration, seed).
- `physics/hamiltonian_builder.sqx` — `build_sensor_hamiltonian(...)`.
- `physics/model_families.sqx` — names the rotating-frame NV model
  family (documents the D-splitting simplification).
- `physics/initial_states.sqx` — baseline sensor-array state prep.
- `physics/observables.sqx` — per-site magnetization readout helpers.
- `physics/symmetries.sqx` — site-permutation symmetry-breaking check
  (Noether callback).
- `application/quench_protocol.sqx` — prepare → evolve → readout
  pipeline.
- `application/spectroscopy_protocol.sqx` — secondary readout comparing
  stressed vs. healthy signal magnitude.
- `application/phase_evidence.sqx` — assembles the detection evidence
  (signal difference, simple confidence marker).
- `application/result_contract.sqx` — small DTO for the dossier.
- `presentation/evidence_dossier.sqx` — human-readable detection
  summary.
- `main_static.sqx` — wires all of the above into the real,
  self-contained runnable entry (README's official entry point).

## Explicitly out of scope

- Medical biomagnetic and resource-exploration magnetic-anomaly themes
  (queued, not this Issue).
- Any Kernel change.
- A rigorous partial-trace fix for `expect(Z, …)` on entangled
  multi-qubit states (a pre-existing Kernel simplification, noted
  honestly in the README, not fixed here).
- Reopening the showcase mission lock — this stays `examples/applied`
  catalog content, not a showcase-track proposal.

## Acceptance reference

```gherkin
Feature: A11_noether_forge is a structural-monitoring quantum magnetometer

  Scenario: the rewritten example compiles and runs to a real terminal measurement
    Given the rewritten main_static.sqx (wiring all 14 modules)
    When it is compiled and run with a fixed seed
    Then it compiles without EVOLVE_UNRESOLVED_UNIT_ERROR or any hard diagnostic
    And it reaches a non-vacuum terminal measurement

  Scenario: the stressed sensor shows a distinguishable signal from healthy sensors
    Given the same example
    When the per-site magnetization readouts are inspected
    Then the stressed site's value differs qualitatively from the healthy sites'
```

## AI planning record (size L)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `L` — full rewrite of 14 files plus README; no Kernel change.
- Route: direct implementation by this session.
- Assumptions: physics magnitudes chosen for a clean, demonstrable
  signal within this Kernel's numerical constraints; not literature-
  pinned beyond the D≈2.87GHz citation.
- Confidence: high for syntax (live-verified under the fixed Kernel);
  medium for the exact chosen magnitudes remaining stable through the
  full multi-file wiring (verified incrementally, file by file).
- Revision links: supersedes the pre-LISS-0336 physics exploration on
  the (deleted) `feature/liss-0336-a11-structural-monitoring-magnetometer`
  branch, which was never committed.

## Exit criteria

- [ ] Phase 1 Red: new test added, fails for the documented reason
      (current `main_static.sqx` still uses the old Noether Forge
      content with a bare dimensionless duration).
- [ ] Phase 2 Green: all 14 files rewritten and wired; test passes.
- [ ] Phase 3 Refactor: README fully rewritten (theme, physics
      citations, honesty table, "Units and interpretation"); reviewer
      empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `spec_verification/run_all.py`,
      `git diff --check` — confirm A11 no longer appears in
      `test_applied_catalog_health_red.py`'s failure list.
- [ ] WP-0095 work unit 6 row updated.

## Non-goals

- Medical / resource-exploration sensing themes (queued for later).
- Any Kernel change.
- Remaining example migrations (B04/B07/B08).
