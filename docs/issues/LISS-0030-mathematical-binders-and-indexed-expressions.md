# LISS-0030: Mathematical binders and indexed expressions

- Status: **proposed** (Architecture Path; design only)
- Depends on: ADR 0018, ADR 0069, LISS-0029
- Blocks: formula-like lattice Hamiltonians, QFT-sized indexed expressions,
  and LISS-0031/0032

## Summary

Define pure mathematical binders such as finite `sum` and `product`, indexed
operators, finite domains, and boundary conditions. These constructs must keep
the notation close to a physicist's formula without becoming a general-purpose
classical loop.

## In scope

- finite domain and index types;
- binder scope and shadowing;
- `sum` / `product` expression grammar;
- periodic/open boundary declarations;
- static expansion and resource-limit diagnostics;
- symbolic preservation before lowering.

## Out of scope

- arbitrary mutable collections or runtime classical loops;
- integrals and derivatives (LISS-0036);
- general operator algebra (LISS-0031);
- provider execution.

## Acceptance questions

- Can a binder refer to `Dimension`, `Index<N>`, and typed basis labels without
  exposing a general `Int` value in the theory expression?
- Is an empty domain an identity, an error, or a typed zero?
- How are out-of-range and boundary accesses diagnosed?
- What expansion budget and symbolic fallback are required?

## Required evidence before implementation

- formula and expanded/symbolic IR examples;
- negative tests for measurement, host values, I/O, and mutation in binders;
- deterministic tests for domain, boundary, and resource diagnostics.
