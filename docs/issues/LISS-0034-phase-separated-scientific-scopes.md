# LISS-0034: Phase-separated scientific program scopes

- Status: **Phase 3 reviewed** (sealed scope contracts implemented; body-level refinement remains open)
- Depends on: ADR 0069–0071, LISS-0014/0015, LISS-0030
- Blocks: safe hybrid workflow composition (LISS-0035)
- Acceptance draft: [`qpex-scientific-scopes.md`](../specs/qpex-scientific-scopes.md)
- AT-TDD Phase 1 Red: [`test_scientific_scopes_red.py`](../../tests/test_scientific_scopes_red.py)
- AT-TDD Phase 2 Green: the same acceptance tests now pass for source-order
  independence, upward dependency rejection, and cycle rejection.
- AT-TDD Phase 3 Green: scope contracts are resolved, direction-checked, and
  exposed as immutable compile results.

## Summary

Define strict `theory`, `experiment`, `workflow`, `execution`, and result/report
boundaries. Declaration order may be deferred and resolved at the end, but
dependency direction must remain strict:

```text
execution -> workflow -> experiment -> theory
report -> execution result
```

## Acceptance questions

- Are phase-separated module kinds or named blocks the normative surface?
- Which imports and types are visible in each phase?
- What immutable contract crosses each boundary?
- Is a builder/resolver only an implementation mechanism, or user-visible
  syntax as well?
- How are backend, shots, retry, filesystem, and logging symbols rejected from
  theory expressions?

## Non-goals

This LISS does not add a general classical runtime to the static Kernel lane.

## Phase 3 implementation boundary

The current implementation recognizes top-level scientific scope blocks and
collects their declared references without interpreting their bodies as
ordinary executable code. It preserves supported Type-First declarations such
as `Operator H = …` in the scope AST. It rejects Theory references to
execution/Host symbols, validates the allowed dependency direction, detects
unknown references and cycles before lowering, and exposes sealed contracts through
`CompileResult.scope_contracts`. The contract container and each contract are
immutable. Execution assignments remain boundary metadata until their
phase-specific syntax is accepted.

### Phase 3 review record

- Scope approval: granted for LISS-0034 Architecture Path.
- Architecture approval: granted for phase-separated scopes and deferred
  source-order resolution.
- Phase approval: granted for Phase 3.
- Implementation permission: granted for sealed contract resolution.
- Verification: `python3 tests/test_scientific_scopes_red.py` passes.
- Reviewer empathy: the immutable contract boundary is complete, while the
  unresolved question of full body-level phase typing is explicitly kept out
  of this slice and remains a follow-up decision.
- Status: **Phase 3 reviewed; sealed scope contract boundary complete**.
