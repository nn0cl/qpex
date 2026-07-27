# ADR 0056: Struct (value), class (reference), methods, `this`, `fn init`

## Status

**Accepted** (2026-07-23). Implemented in Kernel.

Companions: ADR 0054 (fields harvest), ADR 0055 (namespace/enum), ADR 0058 (visibility).

## Decision

### Struct (immutable value type)

- `struct S { val a: T, val b: U }` — fields always immutable.
- Construction: `S(x, y)` positional (or all-defaults).
- Copy-on-pass into methods; `s.field = …` → `IMMUTABLE_ASSIGNMENT_ERROR`.

### Class (reference + methods) — *physical system*

- Type-First fields **and** `val`/`var name: Type [= e]`.
- `ClassName()` / `ClassName(…)` — **no `new`** (Forbidden).
- `fn init(…)` is the constructor; when present, `ClassName(args)` runs `init`.
  Assigning `val` fields is allowed **only** inside `init`.
- `this.field`, `obj.method()`; non-`init` methods use an explicit terminal
  `return` value (ADR 0068).
- `this.varField = expr` only for `var` members outside `init`.

### Keywords

- Active: `fn`, `this`, `val`, `var`, `struct`, `enum`, `namespace`, `class`.
- Retired: `fun` → `fn`. Forbidden: `new`, `protected` (ADR 0058).

## Open

ADR **0057** — density matrix / Lindblad CPTP (not this ADR).

## Verification

`tests/test_modern_oop_and_visibility.py`;
`tests/test_oop_namespace_enum_struct.py`;
example `examples/applied/A06_topological_edge_memory/`.
