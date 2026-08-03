# LISS-0283: ADR — named struct construction (+ no mandatory struct init)

## Metadata

- Local issue ID: LISS-0283
- GitHub issue: _(none yet)_
- Status: **complete** — ADR 0181 **Accepted** + Kernel 2026-08-03
- Phase: Architecture Path (ADR draft → Accept)
- Type: Architecture ADR
- Priority: P2
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md)
- Blocks: [LISS-0284](LISS-0284-kernel-named-struct-construction.md)
- Covers re-review: P2-2 named fields; P2-5 struct without `fn init`/`this` ceremony

## Summary

Decide modern **record-style** struct construction and construction rules so
parameter packs read as named coefficients, not Java beans:

```text
Segment { length: 2.0, bc: Open }   // illustrative; final syntax in ADR
```

Structs must not require `fn init` / `this` assignment theater. `class` with
`fn init` remains valid for true physical systems.

## Decision questions

1. Exact surface (`Type { field: expr }`, `Type(field = expr)`, both?)
2. Positional `Type(a, b)` remains forever?
3. Partial / default fields?
4. Enum case construction interaction
5. Relationship to existing `val` fields and copy semantics

## Exit

- [ ] ADR drafted + Adjudicator Accept
- [ ] Explicit: class init unchanged for systems

## Policy guard

- Physics reading: named fields = named parameters on the blackboard
- Do not add mutable bean setters
