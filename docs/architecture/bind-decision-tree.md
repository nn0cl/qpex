# Bind decision tree (experiment face)

| Field | Value |
|---|---|
| Status | **Teaching law** (LISS-0303) — not a new axiom; not Kernel authorization |
| Parents | [minimal dialect](physicist-minimal-dialect.md), ADR 0180 inference, ADR 0115 typed state, [re-review](2026-08-03-language-design-rereview.md) P0-2 |

When writing Staqex experiment source, choose a bind form by **what the RHS is**,
not by habit.

## Decision tree

```text
Is the value mid-program quantum / State-forming?
├─ yes → use `state name = …`  (or `state name: State<T> = …` when teaching types)
│         Prefer `state` so Never Leave the State stays visible.
└─ no  → classical / Operator / pack
         ├─ Unit / dimension matters (Mass, Length, Time, …)?
         │  └─ yes → Type-First head: `Mass m = …`, `Length L = …`
         │           (field units ADR 0174; SI `to` as needed)
         └─ no  → experiment profile: bare `name = …` is fine
                  (ADR 0180 local inference; B01/B08 face)
                  Multi-file library: prefer typed head or clear name.
```

## Examples (official face)

| Form | Use |
|---|---|
| `answer = dirac(42)` | B01 classical→state via dirac; bare bind under experiment profile |
| `J = 1.0` / `H = -J * …` | B08 chalk coefficients + Operator |
| `J, h = 1.0, 0.5` | Classical multi-bind (ADR 0184 / LISS-0305) |
| `s0, s1 = \|+>, \|+>` | State multi-ket multi-bind (LISS-0309) |
| `state s0 = \|+>` | Explicit State wire |
| `Mass water_g = water_plus_payload_g(qty)` | Type-First free-fn result |
| `CommandBoard board = CommandBoard { … }` | Named struct pack (classical desk) |

## Anti-patterns

| Avoid | Prefer |
|---|---|
| `Float s = expect(Z, psi)` mid-program as “measurement” | `state z = expect(…)` then Host after terminal `measure` |
| Inspect flood of every classical Float | Host logs; ≤1 notebook `inspect` |
| Typed `Float` on every chalk coeff in experiment profile | bare bind when unitless |

## Multi-file note

Selective `import .pkg.{Name}` does not change this tree. Library modules may
keep explicit types for export clarity; experiment entry files should still
prefer the tree above for **new** locals.

## Related honesty

- Soft `QSEM_*` on green runs: see [QUICKSTART](../../QUICKSTART.md) §1.
- Closed-enum `when` without `else` must list every variant
  (`WHEN_NONEXHAUSTIVE`, LISS-0304); incomplete arms no longer sample vacuum.
