# Work Plan: Pre–north-star Kernel bump (v0.2 closure)

- Status: **complete** (2026-07-27)
- Branch: `docs/wp-0027-pre-north-star-kernel-bump`
- SV gate: **160/160**

## Goal

Close the reviewed **deferred execution slices** and the remaining **Basics
examples (B13–B15)** before opening [LISS-0068](../issues/LISS-0068-staqex-v1-normative-rebaseline.md)
/ [WP-0025](WP-0025-staqex-v1-north-star.md) Architecture Path. This batch
raises the shipping Python Kernel from the post–examples-v2 baseline without
starting a second language semantics or CST/formatter rebaseline.

## Scope

### In

- Parent: [LISS-0110](../issues/LISS-0110-pre-north-star-kernel-bump.md)
- Runtime follow-ups:
  - [LISS-0012](../issues/LISS-0012-evolve-until.md) — bounded `evolve … until`
    repetition in the Joint evaluator
  - [LISS-0027](../issues/LISS-0027-parametric-circuit.md) — QPU IR symbolic
    parameters, OpenQASM preservation, Host binding validation
  - [LISS-0036](../issues/LISS-0036-continuous-operator-and-discretization-boundary.md)
    — numerical lowering MVP (see [LISS-0111](../issues/LISS-0111-continuous-discretization-numerical-lowering-mvp.md))
- Examples closure:
  - B13 `B13_host_job_api`, B14 `B14_resource_profile`, B15 `B15_multi_register`
    per [staqex-examples-catalog-v2.md](../specs/staqex-examples-catalog-v2.md)
- Documentation: this work plan, follow-up Issue records, `open-work-register`
  status sync, and a collaboration trace when CI requires it.

### Out

- [LISS-0068](../issues/LISS-0068-staqex-v1-normative-rebaseline.md) / WP-0025
  normative rebaseline, CST, formatter, or source-version migration.
- **Provider physical routing** and coupling-map placement (ADR 0105 D6; Host
  adapter scope — not Kernel).
- Provider SDK, credentials, network submit, live QPU execution.
- Full continuous PDE / spectral catalog beyond the LISS-0111 MVP slice.
- VQE/QAOA optimizer loops, automatic differentiation, or new scientific
  surface syntax unrelated to the listed Issues.

## Issue graph

| Issue | Status (entry) | Size | Depends on | Delivers |
| --- | --- | --- | --- | --- |
| [LISS-0110](../issues/LISS-0110-pre-north-star-kernel-bump.md) | **complete** | XL | WP-0026 done | batch parent + exit gate |
| LISS-0012 runtime | **complete** | L | ADR 0079 | Joint `until` loop, max-step diagnostic |
| LISS-0027 QPU IR + binding | **complete** | L | ADR 0070, LISS-0041 | symbolic params in IR/QASM; Host validation |
| [LISS-0111](../issues/LISS-0111-continuous-discretization-numerical-lowering-mvp.md) | **complete** | XL | LISS-0036, ADR 0074 | Bridge → finite operator (MVP domain) |
| LISS-0108 B13–B15 | **done** | S–M | 0012/0027 optional | Basics examples + SV registration |
| LISS-0067 provider routing | **gated / out** | — | post-MVP Host | not in this batch |

## Recommended order

### Wave 1 — language runtime gaps (P1)

1. **LISS-0012 runtime** — evaluator repetition; QPU lane keeps
   `E_QPU_UNSUPPORTED_CAPABILITY`.
2. **LISS-0027 QPU IR + binding** — parameter nodes through OpenQASM; Host
   validates bindings before submit; no provider SDK.

### Wave 2 — Examples + Host wiring (P2) — **complete**

3. ~~**B14**~~ — `staqex.toml` + `run_with_profile.py`.
4. ~~**B13**~~ — `run_as_job.py` + `submit_source` / `JobResult`.
5. ~~**B15**~~ — `RegisterSet` Basics entry.

### Wave 3 — continuous lowering MVP (P1, largest) — **complete**

6. ~~**LISS-0111**~~ — one explicit MVP path, e.g. `Position` + `UniformGrid` +
   1D finite-difference Hamiltonian from a named Bridge. Target parity with
   pedagogical intent of `tests/fixtures/staqex/grid_oscillator.staqex`, but via the
   ADR 0074 contract rather than silent grid inference.

### Exit gate (before LISS-0068)

- All Wave 1–3 slices: Phase 3 reviewed.
- B13–B15 registered in SV-09; examples README paths current.
- `python3 tests/spec_verification/run_all.py` — 100% gate.
- Full `tests/test_*.py` sweep documented in trace.
- `open-work-register.md` deferred rows updated for 0012, 0027, 0036/0111.
- **No** provider physical routing claimed as complete.

## LISS-0036 vs LISS-0111 (clarification)

| Layer | LISS-0036 (done) | LISS-0111 (this batch) |
| --- | --- | --- |
| Question | *How do we record grid/basis/boundary choices honestly?* | *How does a bridged continuous operator become a finite matrix/evolve step?* |
| Surface | `discretization { … }`, `use Grid for Theory.H as H_fd` | same contracts; adds lowering to executable `Operator` |
| IR | Symbolic provenance only | finite Kernel representation + metadata |
| Non-goals | silent grids, infinite-dimensional QPU | full PDE zoo, adaptive meshes |

## LISS-0067 boundary (clarification)

LISS-0067 **Kernel/QPU-IR work is reviewed complete** (named registers,
`RegisterSet`, qualified sites, logical/flat QPU identity). What remains is:

1. **B15** — Basics pedagogy (not new semantics).
2. **Provider physical routing** — maps logical qubits to device topology;
   explicitly **Host/provider** per ADR 0105 D6; gated post-MVP.

This batch includes (1) and **excludes (2)** to avoid scope creep and a second
semantics fork before LISS-0068.

## Approval model

1. **Plan approval** — this work plan + LISS-0110 scope (Adjudicator).
2. Per slice: **Phase 1 Red** before implementation (LISS-0111 MVP spec fixed
   at Red review).
3. Waves may run Red → Green → Refactor without per-phase check-in unless a
   new architecture decision surfaces (then stop and split Issue).

## Verification

- Per Issue: targeted Red tests, then full unit sweep, then SV.
- Wave exit: `git diff --check`, trace under `docs/collaboration/traces/` when
  collaboration docs change.
- Batch exit: checklist in [LISS-0110](../issues/LISS-0110-pre-north-star-kernel-bump.md).

## Wave 1 progress

- LISS-0012 runtime: **complete** (2026-07-27).
- LISS-0027 QPU IR + binding: **complete** (2026-07-27).

## Wave 2 progress

- B13–B15 Basics: **complete** (2026-07-27); SV **160/160**.

## Wave 3 progress

- LISS-0111 continuous lowering MVP: **complete** (2026-07-27); SV **160/160**.

## Batch status

**WP-0027 exit gate met** — ready for LISS-0068 Architecture Path entry. Provider
physical routing remains explicitly out of scope.
