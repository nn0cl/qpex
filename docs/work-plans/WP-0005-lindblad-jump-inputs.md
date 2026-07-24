# WP-0005: Lindblad jump input slice

## Scope

Implement LISS-0039 as a feature-unit slice on the existing density/Lindblad
branch. The work is limited to explicit numeric jump matrices and the current
CPU/simulator RK4 lane.

## Dependency order

1. LISS-0011 / ADR 0057 — completed baseline.
2. LISS-0039 Phase 0 design — completed.
3. LISS-0039 Phase 1 Red — completed and reviewed.
4. LISS-0039 Phase 2 Green — completed.
5. LISS-0039 Phase 3 Refactor — completed and reviewed.

## Omitted context

POVM effects, symbolic operator algebra, QPU backends, adaptive integration,
higher-order Suzuki methods, and provider SDKs are intentionally omitted.

## Verification target

Run the focused LISS-0039 tests, the existing density/Lindblad tests, the full
standalone test discovery, specification verification, `py_compile`, and
`git diff --check` at the applicable phase gates.
