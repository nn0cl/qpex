# LISS-0034: Phase-separated scientific program scopes

- Status: **proposed** (Architecture Path; design only)
- Depends on: ADR 0069–0071, LISS-0014/0015, LISS-0030
- Blocks: safe hybrid workflow composition (LISS-0035)

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
