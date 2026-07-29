# ADR 0098: Binder constraints and the quantum-expression boundary

## Status

**Accepted for the LISS-0055 design boundary** (2026-07-26).

This ADR fixes the distinction between static index selection and quantum
state control. It does not approve LISS-0055 Phase 1 implementation.

## Context

Staqex binders describe finite mathematical sums and products. Their index
domains and constraints belong to compile-time operator construction, while
the expression in the binder body describes the quantum operator being
constructed.

Using a quantum conditional for an index predicate would make these worlds
look identical:

```staqex
when i < j { ... }
```

Here `i` and `j` are static indices, not quantum states. The surface must make
that distinction visible and enforce it semantically.

## Decisions

### D1 — `where` is outside the body and before `{ ... }`

The canonical constrained-binder form is:

```staqex
sum (i in Index<0..N-1>, j in Index<0..N-1>) where i < j {
    J * Z[i] * Z[j]
}
```

The structure is intentionally:

```text
domain declaration → static guard → summand expression
```

The braces contain the mathematical summand, not an imperative statement
block.

### D2 — `where` is a static, pure index predicate

For the LISS-0055 slice, a guard may reference only binder variables,
static finite-domain values, and pure comparison/boolean operations accepted
by the type checker. It must not perform or depend on:

- `measure` or any collapse operation;
- `Host<T>`, backend, shots, or runtime execution values;
- I/O, logging, mutation, or other effects;
- quantum-state control.

The first accepted comparison set is `<`, `<=`, `==`, `!=`, `>=`, and `>`;
the MVP guard grammar accepts one binary comparison. Compound boolean
operators, function calls, and other predicate forms are deferred and must
produce `BINDER_GUARD_UNSUPPORTED` rather than being partially evaluated.

### D3 — Guard filtering precedes body evaluation

Expansion evaluates a binder in this order:

1. enumerate the declared finite domain tuple;
2. evaluate the pure `where` predicate;
3. discard rejected tuples;
4. evaluate and lower the body for retained tuples;
5. apply body index-bound checks such as `next(i)`.

Consequently, a tuple excluded by `where` does not evaluate an out-of-range
access in its body. An access on a retained tuple still produces the existing
hard `BINDER_INDEX_OUT_OF_BOUNDS` diagnostic.

### D4 — Quantum branching remains a separate construct

`when`/`capply` remain the constructs for quantum-state control. A `where`
guard is not syntactic sugar for a quantum conditional, and a binder body is
not a place to introduce a classical execution branch. Unsupported control
constructs in a binder body must produce an explicit diagnostic rather than a
silent filter or implicit measurement.

### D5 — Multi-variable heads normalize to nested binders

The surface may provide a comma-separated multi-variable head:

```staqex
sum (i in D, j in D) where i < j { body }
```

The normalized AST represents this as nested single-variable `OpBinder`
nodes, preserving declaration order. The guard is attached to the innermost
binder that introduces all variables it references. The parser or normalization
pass retains `BinderOrigin` metadata containing the source span, original
variable list, and the fact that the surface form was desugared to nested
binders.

### D6 — Active binder-variable shadowing is rejected

A binder variable must not reuse a name already visible in an enclosing
binder or in the surrounding Operator scope. The inner declaration is rejected
with the hard diagnostic `BINDER_VARIABLE_SHADOWING`, pointing to the inner
declaration and identifying the hidden binding when available.

The binder variable is not visible in its own domain expression. It becomes
visible in its `where` guard and body. Reusing the same name in non-overlapping
sibling binders or separate Operator/function scopes remains valid:

```staqex
sum (i in sites) { X[i] } + sum (i in sites) { Z[i] }
```

This rule keeps mathematical dummy-index reuse concise without allowing an
inner index to silently change the meaning of an outer index or coefficient.

### D7 — `where` diagnostics identify the violated boundary

The compiler distinguishes the following cases:

| Situation | Diagnostic |
|---|---|
| malformed guard syntax | `PARSE_ERROR` |
| predicate form outside the MVP grammar | `BINDER_GUARD_UNSUPPORTED` |
| comparison does not produce a Boolean predicate | `BINDER_GUARD_TYPE_ERROR` |
| runtime/Host or out-of-scope name | `BINDER_GUARD_SCOPE_ERROR` |
| measurement, I/O, mutation, or another effect | `MATHEMATICAL_BINDER_EFFECT_ERROR` |

Diagnostics identify the guard span and, where applicable, the offending name
or operator. Unsupported guards never silently evaluate to false, disappear,
or trigger measurement.

## Consequences

- `where` has a clear mathematical-comprehension role without introducing
  classical values into the QPU state world.
- The parser needs a guard-bearing binder representation or a desugaring pass;
  the current `OpBinder` shape does not yet carry a guard.
- The type checker must distinguish static index predicates from quantum
  expressions and reject effects at the boundary.
- The finite lowering pass must filter tuples before evaluating the body.
- Multi-variable surface syntax does not require a separate lowering path; it
  is normalized before type checking and execution lowering.
- Shadowing diagnostics must be issued before lowering so a hidden index never
  reaches execution.

## Deferred decisions for LISS-0055

The following remain separate review points and are not decided by this ADR:

- `product` ordering and non-empty-domain requirements;
- the full body algebra and second-quantized substitution order;
- expansion-budget accounting for nested binders and guards;
- empty-domain identity elements, which belong to LISS-0056.

## Related documents

- [ADR 0096](0096-indexed-operator-and-binder-surface.md) D2/D5/D10
- [ADR 0088](0088-finite-binder-lowering.md)
- [LISS-0055](../../issues/LISS-0055-binder-body-as-operator-expression.md)
