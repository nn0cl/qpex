# WP-0095: real ℏ and dimensioned Hamiltonian dynamics

| Field | Value |
|---|---|
| Status | **open — work unit 1 (Kernel primitive) in design intake** |
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

### 1 — Kernel primitive (this Issue: LISS-0330) — **final-review-ready**

Status: **final-review-ready** (Phase 3 complete; no PR/merge yet).
`HBAR_SI` lives in `stdlib/prelude.py`, not `dimensions.py` as first
sketched (that module is compile-time-only; refinement found during
Green). Two unanticipated numerical-robustness bugs in `expm_ih`/
`expm_ih_apply` were found and fixed within this Issue (both exposed only
by this Issue's own formula change). Confirmed regression, as intended:
`pytest tests/ -q` → 66 failed / 1188 passed; `spec_verification` →
132/145 (91.03%), Gate: FAIL. See LISS-0330 for full evidence.

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

### 2 — First reference migration: `A03_h2_vqe`

Migrate `examples/applied/A03_h2_vqe/main_h2_vqe.sqx` to real energy/time
values sourced from H₂ molecule literature data (e.g. NIST or a cited
quantum-chemistry reference for the relevant electronic energy gap).
Chosen first because it already targets a real molecule, making its real
energy scale the least speculative to source (per ADR 0195's own
recommendation).

### 3+ — Remaining example migrations (one Issue each, sequenced after work unit 2)

The corrected count (a recount during this Work Plan's drafting found 15,
not ADR 0195's approximate 19 — that count included `README.md` files
alongside `.sqx` source):

1. `examples/applied/A05_qaoa_portfolio/main_qaoa_portfolio.sqx`
2. `examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx`
3. `examples/applied/A10_mission_observatory/main_mission_observatory.sqx`
4. `examples/applied/A11_noether_forge/main_static.sqx`
5. `examples/basics/B04_evolve_not_loops/evolve_not_loops.sqx`
6. `examples/basics/B07_structure_visibility/structure_visibility.sqx`
7. `examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx`
8. `examples/basics/B16_effect_marking/effect_marking.sqx`
9. `examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx`
10. `examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx`
11. `examples/showcase/S01_quantum_disaster_response/main_fuel_search.sqx`
12. `examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx`
13. `examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx`
14. `examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx`

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
