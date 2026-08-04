# WP-0094 Tensor hardening — Phase 1 Red handoff

## Current State

- Current phase: Phase 1 Red complete; Phase 2 Green pending approval.
- User request: continue the remaining ASCII quantum notation implementation.
- Scope: Tensor alias parity, binary arity, left association, factor order, and
  tensor/arithmetic grouping.
- Out of scope: Unicode source policy, ket/bra lexing, quantum semantics, QPU
  adapters, and formatter presentation.

## Completed

- Added `tests/test_ascii_tensor_parity_red.py` from the accepted WP-0094
  acceptance scenarios.
- Confirmed four expected failures against the current implementation:
  alias AST parity, compile-time alias arity, arithmetic grouping, and
  classical-constructor separation. The left-association/factor-order parser
  assertion already passes.
- Commit: `7a0cdc2` on `codex/wp0094-tensor-hardening`.

## Next Safe Action

After Phase 2 approval, implement the minimum Parser/Typechecker/Runtime
changes without modifying the reviewed Red assertions, then run the focused
suite and full deterministic checks.

## Open Decisions

- Use stable diagnostics `TENSOR_ARITY_ERROR` and `TENSOR_GROUPING_ERROR` as
  specified by the new acceptance tests unless an existing diagnostic catalog
  requires a documented name.
- Update WP-0094 / ADR 0191 status only after Green and final verification.
