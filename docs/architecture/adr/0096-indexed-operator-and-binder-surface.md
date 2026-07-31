# ADR 0096: Indexed operator and binder surface — final form

## Status

**Accepted** (2026-07-26), following an independent design review that
resolved the four open decision points this ADR originally carried, and
Adjudicator direction to apply that review's conclusions.

One decision (D12, action-space determination) is accepted only in the
minimal form D9 requires; replacing the current qubit-count inference in
general is recorded as a required follow-up, not as part of this ADR.

Numeric representation, originally open point 4 here, is **split out** to
[ADR 0097](0097-numeric-representation-horizon.md) and is not decided by
this ADR.

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

### Pre-LISS-0054 measured surface (2026-07-26)

Classified per [ADR 0095](0095-design-horizon-ideal-form-first.md)
Decision 6 — a failing program is a bug, a documented deferral, or a genuine
design gap, and the three call for different responses. This table originally
omitted the classification; it is included here because it changes both the
argument and the implementation plan.

| Written form | Result | Kind |
|---|---|---|
| `sum (i in Index<0..2>) { -1.0 * Z[i] * Z[next(i)] }` | lowers, but **not executable** — `run` and `emit-qasm` both fail: `cannot compile sparse Pauli for OpBinder` | **Bug** — ADR 0088 Decision 3 already promises an executable operator tree |
| `sum {...} + sum {...}` | **compiles ok, no lowering, no diagnostic** | **Bug** — named nowhere, not even as deferred; the pass inspects only a top-level binder |
| `sum { J * Z[i] * Z[next(i)] }` | `BINDER_DOMAIN_ERROR` | **Bug** — ADR 0088 Decision 3 does not restrict *coefficient* to a literal, and `J * Z(0) * Z(1)` works outside a binder |
| `Z[k]` outside a binder | `RUNTIME_ERROR` | **Bug** — `compile_sparse_pauli` has no `OpIndexed` handler |
| `product (i in ...) { ... }` | **compiles ok, no lowering, no diagnostic** | **Documented deferral**, defectively expressed — silence instead of a diagnostic |
| `sum { X[i]*X[next(i)] + Y[i]*Y[next(i)] }` | `BINDER_DOMAIN_ERROR` — `+` rejected in body | **Documented deferral** (ADR 0088 restricts the body to a Pauli nearest-neighbour term) whose accepted scope is too narrow for canonical models |
| `sum (p in ...) { sum (q in ...) { ... } }` | `BINDER_DOMAIN_ERROR` | **Genuine design gap** — multi-index sums appear in no document, deferred or otherwise |
| which of `Z(k)` / `Z[k]` is canonical | undecided | **Genuine design gap** |

Consequence for planning: the corrective step (D6/D7) is largely
bug-fixing against an already-accepted spec, so it is cheaper and lower-risk
than a new-surface slice. The design work proper is the notation decision,
the body-as-expression generalisation, and multi-index/constrained sums.

### The notation defect is systemic, not local

Two grammars exist — the generic expression grammar and the Operator DSL
grammar — and which one parses a given expression depends on the declared
type and the syntactic position. The result is that one concept has two
spellings, neither valid everywhere:

| Concept | Spelling A | Spelling B |
|---|---|---|
| Pauli on site *k* | `Z(k)` — valid **outside** a binder only | `Z[k]` — valid **inside** a binder only |
| Creation on orbital *p* | `create(p)` — valid in a `FermionOperator` bind | `create[p]` — valid in an `Operator` bind |

This pre-migration state directly violated ADR 0095 Decision 3 ("Two spellings of one concept,
or a spelling whose validity depends on syntactic context, is a defect").

## Decision

### D1 — One indexed-operator notation: `Op[index]`

Indexed operator application is spelled with brackets, everywhere an
operator expression is valid, for every operator family:

```staqex
Z[i]            X[0]            create[p]       annihilate[q]
```

Brackets are chosen over parentheses because the index is a *subscript*
($Z_i$), not a function argument, and because brackets already carry
"indexing into a family" in essentially every modern language. Bare,
unindexed atoms (`X`, `Z`, `I`) remain valid and keep their current
single-qubit/global meaning.

The parenthesised form is **retired, not aliased** — an alias would preserve
the two-spelling defect this decision exists to remove. Two constraints on
how it is retired:

- **The diagnostic is name-resolution aware.** `f(x)` in general must keep
  working; a legitimate user-defined callable that happens to be named `Z`
  must not be rejected on the strength of its name. The diagnostic fires
  from name resolution, or from the context in which the retired operator
  syntax was previously valid — never from the identifier alone.
- **The dual grammar is collapsed, not merely re-spelled.** Replacing the
  spelling while leaving two grammars selected by declared type and
  syntactic position would let the same class of divergence reappear in
  semantic analysis. At minimum, an operator reference must be a **single
  AST node** after this change, regardless of which surface position it
  was written in.

Shipped examples, tests, and specs are migrated in the same change.

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

```staqex
sum (i in Index<0..N-1>) { -J * Z[i] * Z[wrap(i)] }
```

Boundary policy is never inferred from the domain type or the register, and
never silently applied: a reader of the formula sees which boundary is in
use. This also keeps periodic support *additive* — it introduces no change
to existing `Index<a..b>` syntax.

### D5 — Constrained sums use a `where` guard

```staqex
sum (i in Index<0..N-1>, j in Index<0..N-1>) where i < j {
    J * Z[i] * Z[j]
}
```

A guard is required rather than optional-by-convention for cases a range
cannot express ($i \neq j$, $i < j$). Multiple binder variables in one
`sum` head are sugar for nesting (D2) and mean exactly that.

A guard that excludes **every** element yields the same identity element as
a syntactically empty domain (D9). Constraint-emptied and range-emptied
binders are one case, not two.

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

Staqex already has two declaration forms: `state x = …` (inferred) and
`State<Int> x = …` (Type-First, explicit). A third, annotation-style form
would be a second spelling of explicit typing and is therefore rejected
under ADR 0095 Decision 3. The "typed surface annotations vs
inference-only" entry in `CLAUDE.md`'s open-topics list is closed by this
decision rather than left open.

### D9 — Empty domains yield identity elements, materialised late

`Index<a..b>` with $a > b$ denotes an **empty domain**. It is never
interpreted as reverse iteration.

- An empty `sum` yields the **additive identity** of its body's type; an
  empty `product` yields the **multiplicative identity**.
- The identity is produced as a **typed symbolic** `Zero` / `Identity`. It
  is **not** immediately materialised into a concrete matrix, and in
  particular is never materialised at one qubit by default.
- It materialises when the acting space is determined — from the expected
  type, or from the surrounding system/register declaration.
- If it reaches matrix construction, simulation, or OpenQASM emission with
  the acting space still undetermined, that is a **hard diagnostic**.
  Falling back to a single qubit is forbidden.
- A statically detectable $a > b$ range emits a **non-hard lint
  diagnostic** (likely typo), not a compile error. The existing hard
  `BINDER_DOMAIN_ERROR` is retained for genuinely malformed ranges, not for
  well-formed empty ones.
- The body is name-resolved and type-checked **even when the domain is
  empty**, so that a later change to a constant cannot suddenly surface a
  latent error in a body that was never checked.

Rationale: `sum` and `product` are monoid folds, and defining the empty
fold as the identity makes the composition law total — which matters not
only for future computed ranges but for any transformation, optimisation,
or `where` filter that removes all terms. Deferring *materialisation*
rather than deferring *meaning* is what makes this safe: an identity is
well-defined once its algebra is fixed, and only its concrete matrix
dimension needs the acting space.

### D10 — `product` is ascending, with lexicographic multi-binder order

```staqex
product (i in Index<0..N>) { O[i] }   ==   O[0] * O[1] * … * O[N]
```

- Single binder: ascending index order.
- Multiple binder variables in one head: **lexicographic order by
  declaration order** of the binder variables.
- Nested binders: **outer binder is the major order**, inner the minor —
  which is the same thing, consistent with D2/D5 treating a multi-variable
  head as sugar for nesting.

Operator products do not commute, so this order is normative semantics, not
an implementation detail. Note that applying $O_0O_1O_2$ to a ket applies
$O_2$ first; that is inherent to operator notation and is not in tension
with ascending construction order. A genuine need for enumeration order to
match time-ordering of application exists, but it is served by a future
explicit reversed domain, not by changing this rule. `rev()` is deferred
(additive, D-list below).

### D11 — Expansion and aggregation order is normative

`f64` addition is not associative, so the order in which binder terms are
expanded and combined is observable in results. Expansion is **ascending**
(matching D10) and aggregation is **left-to-right**, for `sum` as well as
`product`. This is fixed as semantics so that results are reproducible; it
is not left to the backend, and it is not an optimisation target that may
be reordered silently.

### D12 — Acting space is determined by context, minimally (with follow-up)

D9 requires a way for context to determine the space an operator acts on.
This ADR accepts the minimal form: the expected type or the surrounding
system/register declaration determines the acting space at materialisation,
and failure to determine it is a hard diagnostic.

The broader problem is recorded as a **required follow-up, not decided
here**: the current implementation infers qubit count by scanning an
expression for the maximum Pauli site index. The empty-identity case is one
symptom; the same weakness affects expressions containing only identity
operators, systems with unused qubits, and systems with several registers.
The long-term correction is for the operator's type or the compilation
context to carry which system it acts on. That is a type-system change
beyond this ADR's scope and needs its own design.

## Accepted additive follow-up (LISS-0143 / LISS-0144, 2026-07-31)

**Indexed coefficient families** (Kernel literals) are accepted at any rank:

```staqex
Float[N] J = [a0, /* … */, a_{N-1}];
Operator H = sum (i in Index<0..N-2>) { J[i] * Z[i] * Z[next(i)] }

Float[N][M] h = [ /* nested lists */ ];
Operator G = sum (p in Index<0..N-1>, q in Index<0..M-1>) {
    h[p][q] * Z[p] * Z[q]
}
```

- `Float[N0][N1]…[Nk-1]` is a classical fixed-shape float tensor; nested
  list literal shape must match. Element count `∏ Ni` must not exceed the
  Kernel resource budget (`1_000_000`).
- Inside binder / Operator lowering, a **full-rank** chain
  `a[i0][i1]…[i_{k-1}]` with static indices substitutes an `OpLit`.
- Partial indexing (fewer indices than rank) as a **classical** remaining-shape
  bind is Accepted under [ADR 0118](0118-basis-binder-and-partial-float.md)
  (LISS-0149). Scalar binder coefficients still require a full-rank chain.
- Host/Param tensor inject remain deferred.
- Unbound indexed coefficients remain
  `BINDER_LOWERING_UNSUPPORTED` (LISS-0140 honesty).

## Deferred (verified additive under ADR 0095 Decision 2)

Each of these can be added later without a breaking change, so deferral is
legitimate rather than merely convenient:

- **Host-bound / Param coefficient tensors** — in-memory Host inject is
  Accepted under [ADR 0119](0119-host-coefficient-tensor-inject.md)
  (LISS-0150). File adapters and geometry remain deferred.
- **`EnergyLevel` / `Bit` / `SpinProjection` binder domains** — `Basis<N>`
  expansion is Accepted under [ADR 0118](0118-basis-binder-and-partial-float.md)
  (LISS-0148); other carriers remain honesty-only.
- **SI dimension extension** — base dims $I$, $\Theta$ Accepted under
  [ADR 0121](0121-si-base-dims-current-temperature.md). **Scale conversion**
  remains deferred (and was reopened for design under permanent-out reopen).
- Bravyi–Kitaev and other fermion mappings — the explicit
  `map(op, mapping)` surface already exists.

Dependent ranges and `rev()` are **Accepted** under
[ADR 0117](0117-binder-index-endpoints-and-rev.md) (LISS-0146 / LISS-0147).
`Basis<N>` binder expansion and classical partial Float indexing are
**Accepted** under [ADR 0118](0118-basis-binder-and-partial-float.md).


## Implementation order

Per Adjudicator direction (2026-07-26), implementation proceeds in this
order:

1. **D6 + D7** — stop the silent no-ops and make binder lowering
   executable. Corrective work; needs no new surface.
2. **D1–D5, D9–D12** — the surface itself, including migration of examples,
   tests, and specs off the parenthesised spelling.
3. Deferred-but-additive items above, in a later slice.

## Resolution of this ADR's original open points

Recorded for traceability; all four were settled by the independent review.

| Original open point | Resolution |
|---|---|
| 1. Empty domain semantics | Identity elements, symbolic until the acting space is known, hard diagnostic if never known, lint (not error) for literal empty ranges → **D9** |
| 2. `product` ordering | Ascending, plus lexicographic multi-binder and outer-major nesting order, which the original framing had left undefined → **D10** |
| 3. D1 migration without a deprecation window | Confirmed, with two added constraints: name-resolution-aware diagnostic, and collapse the dual grammar rather than only re-spelling → **D1** |
| 4. Exact rational vs `f64` | Split out of this ADR entirely → **[ADR 0097](0097-numeric-representation-horizon.md)** |

The review also identified requirements that neither the original ADR nor
the reviewed positions had raised: normative expansion/aggregation order
(**D11**), type-checking an empty binder's body (**D9**), applying the
identity rule to `where`-emptied binders (**D5**), the acting-space typing
weakness (**D12**), and the endpoint integer/overflow question that travels
with dependent ranges (Deferred list).

## Consequences

Positive:

- The canonical models — TFIM, Heisenberg, XXZ, Hubbard, and molecular
  electronic structure — become expressible, several of them for the first
  time.
- Multi-index sums fall out of "a body is an expression" (D2) rather than
  requiring dedicated syntax.
- One notation for indexed operators, valid everywhere, for every operator
  family, backed by a single AST node.
- Binder lowering stops being an inspection artifact and becomes executable
  on both the SV and QASM paths.
- Algebraic composition is total: empty and fully-filtered binders have
  defined meaning instead of being errors or silent nothings.

Negative:

- D1 is a breaking change to shipped examples and tests. This is accepted
  under ADR 0095: the migration cost is paid once now, rather than by every
  program written from here on.
- The surface slice (step 2) is substantially larger than a shortest-path
  slice would have been, and touches parser, typechecker, lowering,
  examples, and specs together.
- D9 introduces a symbolic identity value whose materialisation is
  context-dependent — genuinely more machinery than an error would have
  been, and dependent on D12's minimal acting-space determination.
- D11 fixes evaluation order as semantics, which forecloses some
  reassociation optimisations. Per ADR 0095 Decision 5 that is the correct
  trade: reproducibility is surface behaviour, speed is later work.
- `where` guards and nested binders make static expansion cost harder to
  predict. Per ADR 0095 Decision 5 this is not grounds to restrict what may
  be written; the existing `BINDER_RESOURCE_ERROR` remains the honest
  rejection when expansion genuinely cannot proceed.
