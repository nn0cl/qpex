# WP-0095: real ℏ and dimensioned Hamiltonian dynamics

| Field | Value |
|---|---|
| Status | **open — work units 1 (Kernel primitive), 2 (`A03_h2_vqe`), and 3 (`A05_qaoa_portfolio`) complete and merged; work unit 4 (`A06_topological_edge_memory`) Phase 3 complete, not yet merged; `main` still carries the expected ADR-approved regression for the remaining 12 unmigrated examples until work unit 5+ lands** |
| Parent ADR | [ADR 0195](../architecture/adr/0195-real-hbar-hamiltonian-dynamics.md) (Accepted 2026-08-05) |
| Scope | Replace `evolve`'s hardcoded natural-units (ℏ = 1) time evolution with real, dimensioned SI-unit dynamics; migrate every example that uses `evolve` |
| Not in scope | Live QPU/pulse-level hardware timing (ADR 0193's separate concern); the unrelated `Operator G = adjoint(H)` runtime bug (tracked separately, see "Related, not blocking" below) |

## Goal

Make `evolve ψ under H for t` physically real: a physicist supplies a
Hamiltonian in real energy units (`eV`, `J`) and a duration in real time
units (`s`, `ps`, …) and gets the physically correct phase evolution,
using ℏ's real SI value — not a natural-units convention silently baked
into the simulator. Per ADR 0195, this is a real, one-time migration: the
old `U = exp(-iHt)` formula is deleted outright, not kept behind a flag.

## Decisions to preserve (from ADR 0195)

- ℏ = `1.054571817e-34` J·s (CODATA 2018 exact), one source of truth
  shared by `evolve`'s formula and the `hbar` prelude constant.
- No permanent natural-units dual-mode. An unmigrated program must fail
  closed (explicit diagnostic), never silently keep running under the old
  formula.
- Real energy/time values for each example are sourced from public
  references (NIST/CODATA, or the system's known literature values), not
  invented or auto-rescaled from the old numbers.
- Builds on the already-shipped `Energy`/`Time` Type-First dimensions
  (`compiler/staqex/dimensions.py`) — no new dimension system.

## Work units

### 1 — Kernel primitive (this Issue: LISS-0330) — **complete**

Status: **complete**, PR #376 merged (`29f2ee8`).
`HBAR_SI` lives in `stdlib/prelude.py`, not `dimensions.py` as first
sketched (that module is compile-time-only; refinement found during
Green). Two unanticipated numerical-robustness bugs in `expm_ih`/
`expm_ih_apply` were found and fixed within this Issue (both exposed only
by this Issue's own formula change). Confirmed regression, as intended:
`pytest tests/ -q` → 66 failed / 1188 passed; `spec_verification` →
132/145 (91.03%), Gate: FAIL. `main` now carries this expected,
ADR-approved regression until work unit 2+ migrates each affected
example/test. See LISS-0330 for full evidence.

1. Add `HBAR_SI` to `compiler/staqex/dimensions.py` as the single source
   of truth.
2. Change `runtime/matrix.py::expm_ih` (and the sparse-Pauli equivalent,
   `runtime/sparse_pauli.py::expm_ih_apply`) from `U = exp(-iHt)` to
   `U = exp(-iHt/hbar)`.
3. Add a fail-closed diagnostic when `H`/`t` cannot be resolved to real
   `Energy`/`Time` dimensions by the time they reach the primitive.
4. Add `hbar` to `compiler/staqex/stdlib/prelude.py`'s `PRELUDE_CONSTANTS`,
   referencing the same `HBAR_SI` value.
5. Add a hand-verified reference test case (a two-level system with a
   known real energy gap and a known real Rabi period, computed
   independently, not by running the Kernel and trusting its own output).
6. Add `ns`/`fs` time units to `dimensions.py` if the reference case or
   early migration needs them (gap confirmed during ADR 0195's design
   check: only `s`/`ms`/`us`/`ps` exist today).

No example migration in this work unit — every existing example continues
to use the old formula until this Issue lands, at which point they all
start failing closed (by design, per the "no silent old-formula survival"
decision) until migrated.

**Sequencing implication:** because work unit 1 makes every unmigrated
`evolve` fail closed, work unit 2 (first example migration) should follow
immediately — the gap between work units 1 and 2 is a period where no
`evolve`-using example runs, tracked openly rather than hidden.

### 2 — First reference migration: `A03_h2_vqe` — **complete**

Status: **complete**, PR [#381](https://github.com/nn0cl/staqex/pull/381)
merged (`510e860`),
[LISS-0332](../issues/LISS-0332-a03-h2-real-unit-migration.md). Migrated
`examples/applied/A03_h2_vqe/main_h2_vqe.sqx` to real energy/time values
derived from H₂ literature data — full derivation and provenance caveats:
[docs/research/2026-08-05-h2-two-orbital-jordan-wigner-cross-validation.md](../research/2026-08-05-h2-two-orbital-jordan-wigner-cross-validation.md).
Found and fixed an unrelated, previously-undiscovered gap during Green:
`second_quantization.py`'s Jordan-Wigner mapping never handled a scalar
coefficient on a fermionic term (only unweighted products) — no example
had ever attached one before. Confirmed: A03 no longer appears in
`test_applied_catalog_health_red.py`'s failure list; only A05/A06/A10/A11
remain (work unit 3+).

### 3 — `A05_qaoa_portfolio` — **complete**

Status: **complete**, PR [#383](https://github.com/nn0cl/staqex/pull/383)
merged (`8d36278`),
[LISS-0333](../issues/LISS-0333-a05-qaoa-arbitrary-unit-migration.md).
Unlike `A03_h2_vqe`, `A05` models an abstract QUBO portfolio-selection
cost function, not a real physical system — a Hard Stop design question
(no literature-traceable physical energy exists for QAOA cost weights)
was raised and resolved with the Adjudicator before Plan approval: give
`H_cost`/`H_mixer` real `Energy`/`Time` dimensions (`eV`/`fs`, satisfying
the Kernel's fail-closed requirement) but honestly document the
magnitudes as arbitrary problem-defined cost units, not physical
constants — see LISS-0333's "Design decision carried into this Issue"
section for the full record. Found and fixed live during design intake
(not a shipped-code bug, a design-intake finding): the mixer term's
originally-implicit coefficient `1` overflows the `hbar`-divided phase
magnitude and must also be given an explicit `Energy` value. Confirmed:
A05 no longer appears in `test_applied_catalog_health_red.py`'s failure
list; only A06/A10/A11 remain (work unit 4+).

### 4 — `A06_topological_edge_memory` — **final-review-ready**

Status: **final-review-ready** (Phase 3 complete; no PR/merge yet),
[LISS-0334](../issues/LISS-0334-a06-ssh-real-unit-migration.md). Unlike
A05, `A06` models a real physical system class (the SSH tight-binding
chain, Su-Schrieffer-Heeger 1979) — its hopping amplitudes are a genuine
`Energy` quantity, unlike A05's abstract QUBO weights, but the specific
values are not traced to a cited measurement (the README already
describes the example as "pedagogical"). Resolved with the Adjudicator
as a third honesty category, distinct from both A03 (literature-traced)
and A05 (arbitrary units): real `eV`-scale magnitudes, ratio preserved
from the original code, documented as physically plausible but not a
reproduction of a specific paper's numeric SSH parameters. Bonus,
unanticipated fix during Green: three other tests exercising A06's
legacy "example10" source also flipped from failing to passing (same
root cause). Confirmed: A06 no longer appears in
`test_applied_catalog_health_red.py`'s failure list; only A10/A11
remain (work unit 5+).

### 5+ — Remaining example migrations (one Issue each, sequenced after work unit 4)

The corrected count (a recount during this Work Plan's drafting found 15,
not ADR 0195's approximate 19 — that count included `README.md` files
alongside `.sqx` source):

1. `examples/applied/A10_mission_observatory/main_mission_observatory.sqx`
2. `examples/applied/A11_noether_forge/main_static.sqx`
3. `examples/basics/B04_evolve_not_loops/evolve_not_loops.sqx`
4. `examples/basics/B07_structure_visibility/structure_visibility.sqx`
5. `examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx`
6. `examples/basics/B16_effect_marking/effect_marking.sqx`
7. `examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx`
8. `examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx`
9. `examples/showcase/S01_quantum_disaster_response/main_fuel_search.sqx`
10. `examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx`
11. `examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx`
12. `examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx`

The five `S01_quantum_disaster_response` files are the "locked" P2-mission
showcase (`staqex-v1-showcase-mission-lock.md`) — these need extra care
and likely their own explicit lock-boundary check before migration, not
just a value substitution, given their locked status. Not reordered ahead
of schedule here; flagged so a future Issue for any of these five does not
skip that check.

Exact execution order beyond "A03 first" is not fixed here — each
remaining Issue is independently sourced and approved, not part of a
pre-committed sequence, consistent with ADR 0195's own recommendation
("each as its own Local Issue... not one giant batch").

## Related, not blocking

`Operator G = adjoint(H)` fails at runtime (`RUNTIME_ERROR: cannot compile
operator node Call`, `hamiltonian.py` has no `Call`-node handling) —
discovered during ADR 0195's design check, confirmed unrelated to ℏ or
`evolve`'s formula. Tracked as its own Local Issue under WP-0092 (found
during that Work Plan's `dag`/`adjoint` scientific-lexicon investigation),
not this Work Plan.

## Approval gates

- **Architecture approval:** ADR 0195 — complete.
- **Work-plan investigation:** this document, plus LISS-0330's own design
  intake, precede any batch-approval request. No batch approval is being
  requested — each work unit proceeds through ordinary Issue-Level Plan/
  Completion approval, one Issue at a time, matching this session's
  established pattern for every other Work Plan so far.
- **Per-Issue Plan approval:** required before each work unit's Phase 1
  Red, per CLAUDE.md's Issue-Level Autonomy.

## Verification

Each work unit's own Issue carries its own verification evidence
(`pytest`, `tests/spec_verification/run_all.py`, `git diff --check`).
Work unit 1 additionally requires a hand-computed reference value,
independent of the Kernel's own output, before it can be trusted.
