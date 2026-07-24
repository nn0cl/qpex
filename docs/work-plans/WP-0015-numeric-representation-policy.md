# WP-0015: Numeric representation and precision policy

## Scope

Resolve LISS-0018 as an architecture/documentation slice: MVP floating
representation, contract-specific tolerance classes, literal policy, and the
Kernel boundary for continuous distributions.

## Dependency order

1. ADR 0014/0018/0037 — existing numeric and type baselines.
2. LISS-0011 / LISS-0037 — physical tolerance consumers.
3. ADR-0076 / LISS-0018 Phase 0 — current.
4. LISS-0018 Phase 1 Red — completed and reviewed.
5. LISS-0018 Phase 2 Green — completed.
6. LISS-0018 Phase 3 Refactor — completed and reviewed.
7. Any broader implementation follow-on — separate Issue and phase approval.

## Omitted context

Arbitrary precision, continuous PDF runtime, Monte Carlo ports, sparse or
accelerated matrix storage, and provider execution are omitted.
