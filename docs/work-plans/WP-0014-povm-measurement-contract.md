# WP-0014: Terminal POVM and measurement contract

## Scope

Define and implement the first LISS-0037 slice: terminal computational-basis
measurement for the existing one-qubit pure and mixed lanes, with an explicit
typed POVM boundary reserved for later effect-list support.

## Dependency order

1. LISS-0011 / ADR 0057 — completed baseline.
2. LISS-0028 / ADR 0071 — dynamic lane boundary.
3. ADR-0075 / LISS-0037 Phase 0 — completed.
4. LISS-0037 Phase 1 Red — completed and reviewed.
5. LISS-0037 Phase 2 Green — completed.
6. LISS-0037 Phase 3 Refactor — completed and reviewed.

## Omitted context

General POVM effect matrices, arbitrary outcome carriers, provider shots,
mid-circuit measurement, feed-forward, and QPU execution are omitted from the
first slice.

## Verification target

Focused LISS-0037 tests, existing pure/mixed measurement tests, all standalone
tests, Spec Verification, `py_compile`, and `git diff --check`.
