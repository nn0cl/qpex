# Work Plan: Examples-driven Kernel brush-up

## Goal

- Turn the `examples/01`–`15` friction review into an ordered, Adjudicator-gated
  plan: Joint/classical semantics first, linker harvest second, catalog honesty
  third — without inflating toy claims.

## Scope

- In: [LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md)…
  [LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md); ADR 0060/0061
  (Proposed→Accept); collaboration catalog conventions; SV-09 / example cleanup
  after Kernel Accept.
- Out: Real cryptanalysis, metro solvers, NGS, Mars modems; OpenQASM Trotter
  ([LISS-0002](../issues/LISS-0002-openqasm3-codegen-backend.md)); Kernel
  implement before ADR Accept; oracle combinators / Kernel `qft` (future LISS).

## Issue Graph

| Issue | Status | Size | Planning | Depends on | Blocks | Branch |
| --- | --- | --- | --- | --- | --- | --- |
| [LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md) | **done** | L | AIP-0003-001 | — | — | `main` |
| [LISS-0004](../issues/LISS-0004-joint-preservation-classical-env.md) | **done** | M | AIP-0004-001 | ADR 0060 | — | `main` |
| [LISS-0005](../issues/LISS-0005-classical-module-config-harvest.md) | **done** | M | AIP-0005-001 | ADR 0061 | — | `main` |
| [LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md) | **done** | M | AIP-0006-001 | — | optional `pi`/rename deferred | `main` |

## Recommended Order

1. ~~Adjudicator Accept ADR 0060/0061~~ **done**
2. ~~LISS-0004 / 0005 Kernel~~ **done**
3. ~~LISS-0006 honesty / SV-09~~ **done** (optional `pi` / folder rename deferred)

## Current Next Issue

- Issue: none — plan complete (incl. LISS-0007 `pi`/`Math.pi`, `08` rename)
- Reason: P0 Kernel + catalog honesty + QoL polish shipped; SV green
- Adjudicator approval needed: only for new LISS (e.g. Kernel `qft`)

## Risks

- Shipping more dream examples (16+) before P0 lands deepens sync-comment debt.
- Candidate A classical harvest may pull scratch Floats — prefer clear surface
  at Accept (ADR 0061 B).
- Fake “QFT” under `08` without Kernel `qft` would violate honesty tables.

## Verification Plan

- Each child Acceptance Notes + full `tests/spec_verification/run_all.py`.
- Example operator comments that document the P0 holes removed only after fix.

## References

- Intake: [docs/issues/inbox/2026-07-23-examples-driven-brush-up.md](../issues/inbox/archive/2026-07-23-examples-driven-brush-up.md)
- Conventions: [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md)
- Trace: [2026-07-23-examples-driven-brush-up.md](../collaboration/traces/2026-07-23-examples-driven-brush-up.md)
- ADR: [0060](../architecture/adr/0060-joint-coordinate-preservation.md),
  [0061](../architecture/adr/0061-classical-module-config-harvest.md)
