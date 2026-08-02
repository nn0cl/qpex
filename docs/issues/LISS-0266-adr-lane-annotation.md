# LISS-0266: ADR — lane annotation (experiment / circuit / host)

## Metadata

- Local issue ID: LISS-0266
- Status: **open**
- Type: Architecture Path (ADR)
- Priority: P1
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Parents: vision §3.1 outer vs Kernel vs lanes; minimal dialect D4

## Intent

Make E / circuit / open / host **visible in source** so multi-lane products do
not look like one enterprise soup and so `forEach` vs bare `for` is teachable.

Candidates:

```text
@lane(experiment)
// or file header: staqex-lane: circuit
// or: experiment fn main()
```

Meaning: **annotation / checking / diagnostics**, not new physics.

## Exit

- [ ] ADR **Proposed** (syntax + diagnostics when lanes mix unmarked)
- [ ] Official sample policy: spines labeled experiment; burst labeled circuit
- [ ] Accept / reject
- [ ] Kernel follow-up via 0269 if Accepted

## Non-goals

- Changing evolve/measure semantics
- Banning multi-lane repos (only require labels)
