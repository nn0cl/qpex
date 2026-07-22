# Agent sync addendum: language spec / Kotlin DX / packages

Date: 2026-07-23. Append to `agent-sync-qpex-baseline.md` read order.

## Canonical

`docs/architecture/qpex-language-spec.md` + ADR **0024**.

## Surface lock (new)

| Role | Spelling |
|------|----------|
| Mixture | `when` (not `span` in new text) |
| Model capsule | `class Foo : System` (not keyword `system`) |
| Capability | `interface` (preferred) / `System` |
| Modules | `package` / `import` = subsystem borders |
| Construct | `Foo(args)` — no `new` |
| Functions | `fun` only (`fn` abolished, ADR 0026) |

## Unchanged laws

Never Leave the State; universal `State<T>` lift; terminal `measure`;
correlation; Trace-Out at block exit; ADR 0021 stdlib names.

## Hold

No parser / typechecker / package resolver implementation until unseal.
