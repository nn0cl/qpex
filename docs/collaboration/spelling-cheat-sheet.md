# QPex spelling cheat sheet (old → new)

Status: **Normative migration aid** (2026-07-23). ADR 0021–0035.
Canonical umbrella: `docs/architecture/qpex-language-spec.md`.

Use the **New** column in all new docs, examples, and agent output.
Lexer/Parser: `docs/architecture/qpex-token-specification.md` (ADR 0035).

## Surface keywords & stdlib

| Old / retired | New | Notes |
|---------------|-----|-------|
| `observe` | `measure` | Collapse only; not PPL condition |
| `span` | `when` | Same §Span denotation; `else` = wildcard |
| `fn` | `fun` | `fun` retired (ADR 0066) |
| keyword `system` | `class … : System` | Capsule laws unchanged |
| `trait` (preferred DX) | `interface` | AST may still say TraitDef |
| `filter` / `given` / `where` / `restrict` | `project` | Proj. + renormalize |
| `fold` / `combine` | `interfer` | Pure state combine |
| `QSystem` / `Evolvable` | `System` | Capability name |
| `try` / `catch` / `throw` | *(forbidden)* | Use `Result` + `when` / `project` |
| `Thread` / `async` / `await` | *(forbidden)* | Use `when` / joint product (ADR 0028) |
| Promise / Future / async VM | *(not for compute)* | DAG + data-parallel (ADR 0032) |
| In-place `this.field =` / setters | *(forbidden)* | Return new `class` (ADR 0033) |
| `synchronized` / domain locks | *(forbidden)* | Immutability (ADR 0033) |
| `null` / `None` | basis labels / `Error` / `Vacuum` | No bottom escape |

## Types & failure

| Concept | Spelling |
|---------|----------|
| Superposition value | `State<T>` |
| Fallible carrier | `Result<T, E>` |
| Success / failure arms | `Success(…)` / `Error(…)` inside `when` |
| Null projection ($Z=0$) | → **`Vacuum`** (not exception; ADR 0026) |

## Modules

| Concept | Spelling |
|---------|----------|
| Subsystem border | `package com.example.optics;` |
| Bring into scope | `import com.example.core.System;` |
| Construct | `Foo(args)` — no `new` |

## Semantics section names (unchanged math titles)

| Surface | Formal section |
|---------|----------------|
| `when` | §Span |
| `project` | §Project |
| `interfer` | §Interfer |
| `measure` | §Measure (terminal) |

## Quick example

```qpex
package com.example.demo;

import com.physics.core.System;

pub class Demo : System {
    fn step(self) -> Demo { self }

    fn main() -> Unit {
        state r = when (coin()) {
            0 -> Success(dirac(1))
            else -> Error("fail")
        };
        state ok = r.project(x -> x is Success); // Z=0 → Vacuum (ADR 0026)
        measure ok;
    }
}
```
