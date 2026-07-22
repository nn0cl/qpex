# Work Plan: Examples-driven Kernel brush-up

## Goal

- Turn the `examples/01`–`15` friction review into an ordered, Adjudicator-gated
  plan: Joint/classical semantics first, linker harvest second, catalog honesty
  third — without inflating toy claims.

## Scope

- In: LISS-0003…0006; ADR 0060/0061 (Proposed→Accept); collaboration catalog
  conventions; SV-09 / example cleanup after Kernel Accept.
- Out: Real cryptanalysis, metro solvers, NGS, Mars modems; OpenQASM Trotter
  (remains LISS-0002); implementing Kernel before ADR Accept.

## Issue Graph

| Issue | Status | Initial size | Current size | Planning record | Depends on | Blocks | Branch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LISS-0003 | proposed | L | L | AIP-0003-001 | - | children coordinated | docs lineage |
| LISS-0004 | proposed | M | M | AIP-0004-001 | ADR 0060 Accept | post-Grover Float DX; `times` expr | feature/joint-preserve-diffuse |
| LISS-0005 | proposed | M | M | AIP-0005-001 | ADR 0061 Accept; prefer 0004 | multi-file classical config | feature/classical-config-harvest |
| LISS-0006 | proposed | M | M | AIP-0006-001 | - (docs/SV parallel) | catalog drift | docs/examples-catalog-honesty |

## Recommended Order

1. Adjudicator reviews **ADR 0060** and **ADR 0061** (Accept / amend / reject).
2. **LISS-0006** docs/SV-09 pieces that need no Kernel (conventions already
   drafted; register missing examples; honesty for `08`) — can run in parallel
   with ADR review.
3. Feature Path Red/Green for **LISS-0004** after 0060 Accept.
4. Feature Path for **LISS-0005** after 0061 Accept (and 0004 if inspecting
   harvested Floats after Grover).
5. Close **LISS-0003** when children are done or explicitly deferred.

## Current Next Issue

- Issue: Adjudicator decision on ADR 0060 / 0061; parallel LISS-0006 docs/SV
- Reason it is unblocked: ledger and Proposed ADRs filed
- Adjudicator approval needed: yes — architecture Accept before Kernel Red

## Risks

- Shipping more dream examples (16+) before P0 lands deepens sync-comment debt.
- Candidate A classical harvest may pull scratch Floats — prefer clear surface
  at Accept (ADR 0061 B).
- Fake “QFT” under `08` without Kernel `qft` would violate honesty tables.

## Verification Plan

- Each child Acceptance Notes + full `tests/spec_verification/run_all.py`.
- Example operator comments that document the P0 holes removed only after fix.

## References

- Intake: `docs/issues/inbox/2026-07-23-examples-driven-brush-up.md`
- Conventions: `docs/collaboration/examples-catalog-conventions.md`
- Trace: `docs/collaboration/traces/2026-07-23-examples-driven-brush-up.md`
