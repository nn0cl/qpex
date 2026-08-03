# Adjudicator review — LISS-0290 (ADR 0180 residual)

## Approval type requested

- Plan approval → Phase 1 Red (Feature Path)
- Architecture: **no new ADR** (conformance to Accepted 0180 Decision §3)

## Approved scope (proposed)

Kernel typecheck fills omitted `StateBind.ty` for unique elaborations;
tests for Operator QASM + classical Call Float + bare struct; B08 chalk
restore after Green.

## Current phase

Intake / proposed — **not** Red until「承認」.

## Implementation permission

Denied until Phase 1 Red approved.

## Post-review requirement

Yes — after Phase 3, Adjudicator completion / merge.

## Decision points

1. Proceed Red without ADR amendment?
2. Include B08 face restore in same Issue?
3. Any residual to defer (e.g. bare `s0 = |+>` without `state`)?
