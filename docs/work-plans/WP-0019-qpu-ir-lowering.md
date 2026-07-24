# WP-0019: Provider-neutral QPU IR lowering

## Scope

Implement LISS-0041's first in-memory QPU IR lowering slice. The work is
limited to the accepted gate/parameter/measurement vocabulary and must not
introduce provider or serialization concerns.

## Dependency order

1. LISS-0019 / ADR 0077 — inspection boundary accepted.
2. ADR 0085 / LISS-0041 Phase 0 — opcode and lowering contract accepted.
3. LISS-0041 Phase 1 Red — acceptance tests (complete).
4. LISS-0041 Phase 2 Green — immutable IR and pure lowering (complete).
5. LISS-0041 Phase 3 Refactor — review and provenance audit (complete).

## Verification target

Focused LISS-0041 tests, existing QPU IR/OpenQASM tests, Spec Verification,
`compileall`, and `git diff --check`.
