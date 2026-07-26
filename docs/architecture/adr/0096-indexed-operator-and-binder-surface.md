# ADR 0096: Indexed operator and binder surface — final form

## Status

**Proposed.** Requires Adjudicator approval before Phase 1 Red. Contains
open decision points (see the last section) that the Adjudicator must
settle; they are not decided here.

This is the first design carried out under
[ADR 0095](0095-design-horizon-ideal-form-first.md) (ideal form first). It
therefore starts from "what should a physicist be able to write", not from
the existing deferred list.

## Context

### Derivation: what physicists actually write

The surface requirements below are derived by taking the Hamiltonians a
physicist would bring to a quantum computer and asking what notation each
demands:

| Model | Formula | Demands |
|---|---|---|
| Transverse-field Ising | $-J\sum_i Z_i Z_{i+1} - h\sum_i X_i$ | sum of sums; named coefficients |
| Heisenberg / XXZ | $\sum_i (X_iX_{i+1} + Y_iY_{i+1} + \Delta Z_iZ_{i+1})$ | `+` inside a binder body |
| Periodic ring | $-J\sum_{i=0}^{N-1} Z_i Z_{(i+1)\bmod N}$ | periodic index access |
| Random-field Ising | $-\sum_i J_i Z_iZ_{i+1} - \sum_i h_i X_i$ | indexed coefficient families |
| Hubbard | $-t\sum_{\langle ij\rangle\sigma}(a^\dagger_{i\sigma}a_{j\sigma} + \text{h.c.}) + U\sum_i n_{i\uparrow}n_{i\downarrow}$ | second-quantized atoms inside binders |
| Long-range Ising | $\sum_{i<j} J_{ij} Z_iZ_j$ | multi-index sums with a constraint |
| Molecular electronic structure | $\sum_{pq}h_{pq}a^\dagger_pa_q + \tfrac12\sum_{pqrs}h_{pqrs}a^\dagger_pa^\dagger_qa_ra_s$ | multi-index sums (2 and 4 indices) |

Two of these requirements — **multi-index sums** and **constrained sums** —
do not appear anywhere in the current deferred list. They were invisible
while scoping incrementally, and they are exactly what quantum chemistry,
the flagship application, requires.

### Measured state of the current surface (2026-07-26)

| Written form | Result |
|---|---|
| `sum (i in Index<0..2>) { -1.0 * Z[i] * Z[next(i)] }` | lowers, but **not executable** — `run` and `emit-qasm` both fail: `cannot compile sparse Pauli for OpBinder` |
| `sum {...} + sum {...}` | **compiles ok, produces no lowering, emits no diagnostic** |
| `product (i in ...) { ... }` | **compiles ok, produces no lowering, emits no diagnostic** |
| `sum { X[i]*X[next(i)] + Y[i]*Y[next(i)] }` | `BINDER_DOMAIN_ERROR` — `+` rejected in body |
| `sum { J * Z[i] * Z[next(i)] }` | `BINDER_DOMAIN_ERROR` — although `J * Z(0) * Z(1)` is accepted outside a binder |
| `sum (p in ...) { sum (q in ...) { ... } }` | `BINDER_DOMAIN_ERROR` — no multi-index sums |

### The notation defect is systemic, not local

Two grammars exist — the generic expression grammar and the Operator DSL
grammar — and which one parses a given expression depends on the declared
type and the syntactic position. The result is that one concept has two
spellings, neither valid everywhere:

| Concept | Spelling A | Spelling B |
|---|---|---|
| Pauli on site *k* | `Z(k)` — valid **outside** a binder only | `Z[k]` — valid **inside** a binder only |
| Creation on orbital *p* | `create(p)` — valid in a `FermionOperator` bind | `create[p]` — valid in an `Operator` bind |

This directly violates ADR 0095 Decision 3 ("Two spellings of one concept,
or a spelling whose validity depends on syntactic context, is a defect").

## Decision

### D1 — One indexed-operator notation: `Op[index]`

Indexed operator application is spelled with brackets, everywhere an
operator expression is valid, for every operator family:

```qpex
Z[i]            X[0]            create[p]       annihilate[q]
```

Brackets are chosen over parentheses because the index is a *subscript*
($Z_i$), not a function argument, and because brackets already carry
"indexing into a family" in essentially every modern language. Bare,
unindexed atoms (`X`, `Z`, `I`) remain valid and keep their current
single-qubit/global meaning.

The parenthesised form `Z(k)` / `create(p)` is **retired, not aliased**:
it produces a hard diagnostic naming the bracket replacement. An alias
would preserve the two-spelling defect this decision exists to remove.
Shipped examples and tests using the parenthesised form are migrated in the
same change.

### D2 — A binder body is a full operator expression

The body of `sum` / `product` accepts any operator expression, with the
same grammar and the same meaning as outside a binder. Concretely this
admits, with no further special cases:

- `+` and `-` between terms (Heisenberg, XXZ);
- named classical scalar coefficients (`J`, `h`, `Delta`), resolved exactly
  as they already are outside binders;
- second-quantized atoms (`create[p]`, `annihilate[q]`), which is what
  makes Hubbard and molecular Hamiltonians expressible;
- **a nested binder** — which is how multi-index sums $\sum_{pq}$ and
  $\sum_{pqrs}$ are written, requiring no separate multi-index syntax.

### D3 — Binders are expressions

A binder is an operator expression and composes like one, so
`sum {...} + sum {...}` is an ordinary operator sum. This is what makes the
transverse-field Ising Hamiltonian — the most canonical model in the field
— writable at all.

### D4 — Boundary policy is explicit at the point of use

`next(i)` keeps its current meaning: open boundary, hard
`BINDER_INDEX_OUT_OF_BOUNDS` when it leaves the domain. Periodic access is
a distinct, explicit accessor:

```qpex
sum (i in Index<0..N-1>) { -J * Z[i] * Z[wrap(i)] }
```

Boundary policy is never inferred from the domain type or the register, and
never silently applied: a reader of the formula sees which boundary is in
use. This also keeps periodic support *additive* — it introduces no change
to existing `Index<a..b>` syntax.

### D5 — Constrained sums use a `where` guard

```qpex
sum (i in Index<0..N-1>, j in Index<0..N-1>) where i < j {
    J * Z[i] * Z[j]
}
```

A guard is required rather than optional-by-convention for cases a range
cannot express ($i \neq j$, $i < j$). Multiple binder variables in one
`sum` head are sugar for nesting (D2) and mean exactly that.

### D6 — No silent no-ops

Any binder construct this design does not cover produces an explicit
diagnostic. A construct that compiles and silently yields nothing — the
current behaviour of `sum {...} + sum {...}` and `product` — is a defect
under ADR 0095 regardless of scope, and is the first thing fixed.

### D7 — Lowering output is an executable operator, not an inspection dict

`binder_lowering`'s `operator_tree` is currently a JSON-shaped `dict` used
for inspection, while the AST bound to the operator name stays `OpBinder`,
which no execution path can consume. Lowering must instead produce a real
operator AST (`OpBin`/`OpPauli`/…) wired into the same environment a
hand-written operator uses, exactly as
[ADR 0093](0093-jordan-wigner-numerical-mapping.md) did for Jordan-Wigner.
Provenance stays as provenance; it is never the executable value.

### D8 — `state x: State<Int>` is rejected, closing the open topic

QPex already has two declaration forms: `state x = …` (inferred) and
`State<Int> x = …` (Type-First, explicit). A third, annotation-style form
would be a second spelling of explicit typing and is therefore rejected
under ADR 0095 Decision 3. The "typed surface annotations vs
inference-only" entry in `CLAUDE.md`'s open-topics list is closed by this
decision rather than left open.

## Implementation order

Per Adjudicator direction (2026-07-26), implementation proceeds after this
ADR is accepted, in this order:

1. **D6 + D7** — stop the silent no-ops and make binder lowering
   executable. This is corrective work; it needs no new surface.
2. **D1 + D2 + D3 + D4 + D5** — the surface itself, including migration of
   examples and tests off the parenthesised spelling.
3. Deferred-but-additive items below, in a later slice.

## Deferred (verified additive under ADR 0095 Decision 2)

Each of these can be added later without a breaking change, so deferral is
legitimate rather than merely convenient:

- **Indexed coefficient families** (`J[i]`, `h_pq[p][q]`) — needs a
  classical family/array type; adopting it later adds new accepted forms
  without changing existing ones.
- **Dependent ranges** (`Index<i+1..N-1>`) — an alternative spelling for
  some `where` guards; adding expression endpoints does not invalidate
  literal endpoints.
- **SI dimension extension** — `Dim` is currently a 3-vector $(L,M,T)$;
  electric current and temperature are absent, so magnetic fields, charge,
  and finite-temperature quantities cannot be dimensionally typed. Adding
  base dimensions is additive at the surface.
- Bravyi–Kitaev and other fermion mappings — the explicit
  `map(op, mapping)` surface already exists.

## Open decision points for the Adjudicator

These are genuine choices this ADR does not make:

1. **Empty domain semantics.** Mathematically $\sum_\emptyset = 0$ and
   $\prod_\emptyset = I$. LISS-0030 currently rejects empty domains, on the
   grounds that a literal empty range is almost certainly a typo. With
   computed ranges the empty case becomes legitimate. Adopt the
   mathematical identities, keep rejecting, or reject only literal-empty
   ranges?
2. **`product` over operators.** Operator products do not commute, so
   $\prod_i O_i$ needs a defined order. Ascending index order is proposed;
   confirm, or require explicit ordering.
3. **Migration cost of D1.** Retiring `Z(k)` touches shipped examples and
   tests. Confirm that a hard diagnostic (no alias, no deprecation period)
   is wanted, consistent with ADR 0095, rather than a transition window.
4. **Exact rational vs `f64` probability masses** (ADR 0076 chose `f64`).
   Adding exact arithmetic as an option is additive; *replacing* `f64`
   changes numerical results and is breaking. Whether `f64` is the
   permanent answer is a judgment about the hundred-year horizon, not a
   design detail this ADR can settle.

## Consequences

Positive:

- The canonical models — TFIM, Heisenberg, XXZ, Hubbard, and molecular
  electronic structure — become expressible, several of them for the first
  time.
- Multi-index sums fall out of "a body is an expression" (D2) rather than
  requiring dedicated syntax.
- One notation for indexed operators, valid everywhere, for every operator
  family.
- Binder lowering stops being an inspection artifact and becomes executable
  on both the SV and QASM paths.

Negative:

- D1 is a breaking change to shipped examples and tests. This is accepted
  under ADR 0095: the migration cost is paid once now, rather than by every
  program written from here on.
- The surface slice (step 2) is substantially larger than a shortest-path
  slice would have been, and touches parser, typechecker, lowering, and
  examples together.
- `where` guards and nested binders make static expansion cost harder to
  predict. Per ADR 0095 Decision 5 this is not grounds to restrict what may
  be written; the existing `BINDER_RESOURCE_ERROR` remains the honest
  rejection when expansion genuinely cannot proceed.
