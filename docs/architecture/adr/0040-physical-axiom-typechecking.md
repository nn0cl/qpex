# ADR 0040 — Physical axiom typechecking (P0/P1)

- Status: Accepted
- Date: 2026-07-23
- Deciders: Language design (physical-soundness audit)

## Context

A 2026-07-23 audit showed several non-physical programs compiling successfully
(H-evolve with Length duration, independent `interfer`, `psi + expect(...)`,
dimension-swapped evolve tuples, `Length == 1.0`, `when` in ctrl, `coin` in
`evolve`). Grammar-OK is not enough; the typechecker must enforce physical axioms.

## Decision

Hard errors (see `compiler/qpex/physical_axioms.py` + `typecheck.py`):

| Code | Rule |
|------|------|
| `DIMENSION_MISMATCH_ERROR` | H-evolve `for` must be Time/ΔTime/dimensionless; evolve tuple dims match seeds; no one-sided dimless compare |
| `INTERFER_INDEPENDENT_STATE_ERROR` | `interfer` args need shared coin/ket lineage |
| `EXPECT_CLASSICAL_ONLY_ERROR` | `expect` → `Classical<Float>`; no mix into State arith |
| `NESTED_WHEN_ERROR` | Also bans `when` inside ctrl |
| `COIN_IN_EVOLVE_ERROR` | No `coin()` inside evolve bodies |

Examples: `classical_oscillator.qpex` (honest rename), `portable_bell_qpu` via
`|+>`/`cnot`/`expect`, `gauge_symmetry` via `phase`.

Verification: SV-18.

## Consequences

Pedagogical `interfer` still allowed when lineage is shared (e.g. double_slit).
Full unitarity static proofs remain Deferred beyond the MVP patterns in
ADR 0045 (`NON_UNITARY_TRANSFORM_ERROR`).
