# WP-0018: Symbolic Lindblad jump lowering

## Scope

Implement LISS-0040 on top of the completed LISS-0039 numeric jump slice.
Only bound one-qubit `Operator` entries inside `JumpSet` are in scope.

## Dependency order

1. LISS-0039 — completed and reviewed.
2. LISS-0040 Phase 0 design — completed.
3. LISS-0040 Phase 1 Red — completed and reviewed.
4. LISS-0040 Phase 2 Green — completed.
5. LISS-0040 Phase 3 Refactor — completed and reviewed.

## Omitted context

General operator algebra, fermionic/bosonic lowering, POVM, provider/QPU
execution, adaptive integration, and storage/dependency changes are omitted.

## Verification target

Run focused LISS-0040 tests, LISS-0039 and LISS-0011 regression tests, all
standalone tests, specification verification, `py_compile`, and
`git diff --check` at the applicable phase gates.
