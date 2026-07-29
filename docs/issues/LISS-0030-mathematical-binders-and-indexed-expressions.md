# LISS-0030: Mathematical binders and indexed expressions

Executable finite-range lowering is tracked separately in
[LISS-0043](LISS-0043-finite-binder-lowering.md); this issue remains the
symbolic binder boundary.

- Status: **Phase 3 reviewed** (symbolic binder boundary complete; lowering deferred)
- Depends on: ADR 0018, ADR 0069, LISS-0029, LISS-0038
- Blocks: formula-like lattice Hamiltonians, QFT-sized indexed expressions,
  and LISS-0031/0032
- Acceptance draft: [`staqex-mathematical-binders.md`](../specs/staqex-mathematical-binders.md)
- AT-TDD Phase 1 Red: [`test_mathematical_binders_red.py`](../../tests/test_mathematical_binders_red.py)

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

## Current phase

The acceptance specification is drafted, but its carrier prerequisite is now
explicit: LISS-0038 must be accepted before `Index<N>` or indexed access is
implemented. After that review, the Adjudicator must authorize the AT-TDD
Phase 1 Red slice.

## Phase 2 Green record

- Added `OpBinder`, `OpIndexed`, and pure symbolic `OpCall` AST nodes.
- Parsed `sum (i in domain) { expression }` and
  `product (i in domain) { expression }` inside `Operator` expressions.
- Added typed validation for finite semantic domains, binder variables,
  indexed access, effectful calls, execution-phase values, and expansion
  resource limits.
- Binder trees are retained; no runtime expansion, measurement, or QASM
  lowering was added.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

## Phase 3 review record

- The normative first surface is `sum (i in domain) { expression }` and
  `product (i in domain) { expression }`.
- `Index<N>` and named `Dimension` domains require a positive finite shape.
  Empty/zero domains are rejected; no implicit additive or multiplicative
  identity is selected for this first slice.
- Boundary wrapping is not implicit. `next(i)` remains symbolic, and periodic
  boundary syntax is deferred until the domain/lowering design is accepted.
- Source provenance is retained through the AST node and its `Span`; a stable
  serialized Symbolic IR format is deferred to LISS-0033.
- Resource budgets reject oversized elaboration; there is no silent truncation.
- Runtime expansion, simulator execution, and QASM lowering remain deferred to
  the next implementation slice.

Phase 3 acceptance evidence: binder tests pass, all standalone tests pass, and
specification verification passes 165/165 (100%).
