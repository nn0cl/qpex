# QPex mathematical binders and indexed expressions

Status: **accepted for the LISS-0030 symbolic binder boundary**.
Runtime expansion, execution, and QASM lowering remain out of scope.

## 1. Purpose

QPex needs to express finite Hamiltonian and observable formulas without
manually expanding every site. A mathematical binder must retain the formula's
structure and must not become a general-purpose classical loop.

The first supported family is finite aggregation:

```qpex
sum (i in sites) {
    coupling[i] * Z[i] * Z[next(i)]
}
```

`sum` constructs a symbolic expression. It does not sample, measure, mutate,
perform I/O, or expose a runtime classical `Int` to the theory expression.

## 2. Proposed surface

```qpex
sum (i in domain) { expression }
product (i in domain) { expression }
```

The binder variable is an index whose type is derived from `domain`. The body
is a pure expression and may refer to the binder and visible theory symbols.
The exact punctuation and domain declaration syntax remain subject to grammar
review; this specification locks the semantic boundary first.

### 2.1 Domains

The first domain forms are:

```qpex
sites              // named finite domain supplied by the theory
Index<N>            // type-level finite index family
Basis<N>            // typed basis labels, when accepted by the Hilbert model
```

`Dimension`, `ShotCount`, backend settings, and Job values are not theory
domains. A meta-level count may determine a finite domain during elaboration,
but it must not become a `State<Int>` or a mutable runtime loop variable.

Zero and empty domains are rejected in this first slice. The language does not
silently choose an identity element for an empty operator aggregation.

### 2.2 Indexed access

An indexed symbol must declare or infer an index domain:

```qpex
Z[i]
coupling[i]
Z[next(i)]
```

The checker must validate that the index expression belongs to the symbol's
domain. Boundary policy (`open`, `periodic`, or another explicitly declared
policy) is part of domain resolution, not an accidental array behavior.

## 3. Denotation

For a finite domain (D), `sum (i in D) { e(i) }` denotes the aggregation of
the resolved body expressions:

\[
\operatorname{Sum}_{i \in D} e(i).
\]

For scalar expressions this is scalar addition. For compatible operators this
is operator addition. The result type is inferred from the body and must have
a common additive identity. `product` is analogous and requires a common
multiplicative identity.

The source binder remains in Symbolic IR until domain, index, type, and resource
checks complete. A backend may expand it only after resolution.

The current provenance boundary is the AST node and its source `Span`; a
serialized Symbolic IR format is deferred to LISS-0033.

## 4. Mandatory restrictions

The binder body must reject:

- `measure` and any operation that consumes `RngPort`;
- filesystem, network, logging, or host/provider calls;
- mutation and assignment to outer bindings;
- `backend`, `shots`, `retry`, `Job`, and other execution values;
- classical short-circuit control over a measured value;
- an unbounded or runtime-sized domain in the static Kernel lane.

The binder is not a replacement for `evolve` or a dynamic QPU loop. It creates
an expression; it does not execute a sequence of effects.

## 5. Diagnostics

The accepted design must define stable diagnostics for at least:

| Condition | Required result |
|---|---|
| Domain is not finite or statically resolvable | hard compile error |
| Index belongs to another domain | typed domain mismatch |
| Index may cross an open boundary | boundary diagnostic |
| Body has incompatible additive/multiplicative types | operator/type mismatch |
| Body contains measurement or host effect | phase/effect violation |
| Expansion exceeds target budget | resource error; no silent truncation |
| Empty domain | explicitly selected identity or hard error; never implicit zero data |

## 6. Acceptance scenarios

### Scenario A — finite Ising sum

Given a finite `sites` domain and `Z[i]`, `Z[next(i)]` operator access,
`sum` resolves to a typed Hamiltonian and preserves the source binder in the
symbolic form until lowering.

### Scenario B — boundary correctness

An open chain rejects `Z[next(last)]`; a periodic chain accepts it only when the
periodic boundary is explicitly declared.

### Scenario C — no classical leakage

A binder referencing `shots`, `backend`, `measure`, or host I/O is rejected
before code generation.

### Scenario D — no hidden truncation

When the resolved expansion exceeds the target resource budget, compilation
fails with a resource diagnostic. It does not silently truncate the domain.

### Scenario E — typed aggregation

The checker accepts aggregation of compatible scalar/operator terms and rejects
mixing a host count, a state carrier, and an operator merely because their
implementation representation could be an integer or floating-point value.

## 7. Follow-up boundary

This specification intentionally does not define bra-ket notation, adjoints,
commutators, fermionic statistics, continuous integrals, or provider lowering.
Those remain LISS-0031, LISS-0032, LISS-0036, and LISS-0019 concerns. Once this
specification is accepted, LISS-0031 may use its resolved indexed operator
model as a prerequisite.
