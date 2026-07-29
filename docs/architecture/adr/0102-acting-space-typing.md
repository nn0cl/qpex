# ADR 0102: Acting-space typing for operators and quantum registers

## Status

**Accepted architecture boundary** (2026-07-27). This ADR authorizes and
records the completed LISS-0058 single-register implementation. It does not
authorize provider integration or a final multi-register surface.

## Context

Staqex currently derives an operator's Hilbert-space size by scanning its syntax
for the largest Pauli site index. That is not a physical property of the
operator: an expression may contain no indexed site, may leave high qubits
unused, or may cross a function boundary. The current fallback can therefore
materialise a site-free operator as a one-qubit operator even when the
declared system is larger.

LISS-0056 introduced the minimal context-dependent mechanism required for
empty-domain identities. The remaining problem is general: acting space must
travel with the operator value or be supplied by an explicit compilation
context, rather than being rediscovered from syntax at every execution
boundary.

## Decisions

### D1 — Acting space is a first-class semantic axis

The acting space is not an ordinary runtime integer and is not inferred from
the maximum indexed site. It is a typed Hilbert-space boundary associated
with an operator value.

The intended surface family is:

```staqex
QubitRegister<4> reg = system()
Operator<QubitRegister<4>> H = ...
State<QubitRegister<4>> psi = ...
```

The exact declaration spelling remains subject to the existing
`QubitRegister<N>` surface contract. This ADR fixes the semantic relationship,
not a second register declaration grammar.

### D2 — `QubitRegister<N>` is the canonical single-register shape

For a single logical register, `QubitRegister<N>` is the authoritative
compile-time shape. The same shape must be available to type checking,
operator materialisation, simulation, QPU IR inspection, and OpenQASM
emission. No downstream component may replace a known register shape with a
syntax-derived site maximum.

### D3 — Operator values carry acting-space provenance

An operator crossing a function, method, binder, or module boundary must
retain its acting-space identity. A consumer may refine an unresolved
symbolic operator from an enclosing `QubitRegister<N>` context, but it may
not silently recompute or default the space.

The resolved representation records at least `acting_space` and the source
provenance of the operator declaration.

### D4 — Unknown acting space is an explicit unresolved state

An unparameterized or context-free operator may remain symbolic while it is
being inspected. If simulation, matrix construction, QPU IR generation, or
OpenQASM emission is requested before the space is resolved, compilation
fails with `IDENTITY_ACTING_SPACE_UNDETERMINED` for identity-specific cases
and a corresponding general acting-space diagnostic for other unresolved
operators. A one-qubit fallback is forbidden.

### D5 — Compilation context is a secondary source, not a competing type

The enclosing `QubitRegister<N>` or system declaration may supply the acting
space for a symbolic expression whose operator type is not yet fully
specialised. Once resolved, the operator carries the result. This preserves
equation-first source without creating a mutable global setting.

### D6 — Multi-register systems are a later additive extension

The semantic carrier is a register-shape identity rather than a bare integer,
so multiple registers can later be represented without changing the meaning
of single-register `QubitRegister<N>`. Multi-register naming, tensor-product
surface syntax, and cross-register indexed sites remain outside the initial
LISS-0058 slice and require a follow-up design decision.

### D7 — This is a breaking type-boundary migration

Existing operator programs that rely on syntax-derived size are not granted
an implicit compatibility alias. Concise source may remain valid when an
enclosing register or expected typed result supplies the shape, but an
execution boundary with no acting-space evidence must fail explicitly.

## Initial Phase 1 Red boundary (historical)

The first acceptance tests should cover:

1. a site-free identity in `QubitRegister<4>` materialises as a 4-qubit
   identity;
2. an identity containing only `I` does not fall back to one qubit;
3. an expression with unused high qubits retains the declared register size;
4. an operator returned through a function retains its acting-space identity;
5. a context-free execution request fails with an actionable hard diagnostic;
6. QASM and simulator paths agree on the resolved shape; and
7. a multi-register expression is rejected as unsupported rather than
   flattened into one guessed integer.

These were the original Red contracts. The single-register implementation now
fulfills them; they do not select a storage representation or authorize
provider integration or multi-register lowering.

## Consequences

- Physical system size becomes visible in the type and compilation context.
- Function boundaries no longer lose an operator's system identity.
- Syntax-derived inference cannot remain an execution fallback.
- Multi-register systems require an explicit model rather than an accidental
  approximation by one integer.
- The compiler, simulator, and QASM adapter share one shape contract.

## Deferred decisions

- Final surface spelling for named and multi-register declarations.
- Whether a specialised `Operator<QubitRegister<N>>` annotation is mandatory
  everywhere or may be inferred from an enclosing declaration.
- General acting-space diagnostic naming beyond the existing identity code.
- Provider physical-qubit mapping, routing, and post-routing resource checks.

## Related documents

- [LISS-0058](../../issues/LISS-0058-acting-space-typing.md)
- [LISS-0056](../../issues/LISS-0056-empty-domain-identity-elements.md)
- [LISS-0029](../../issues/LISS-0029-static-hilbert-kernel-surface.md)
- [ADR 0069](0069-kernel-static-hilbert-space.md)
- [ADR 0096](0096-indexed-operator-and-binder-surface.md)
