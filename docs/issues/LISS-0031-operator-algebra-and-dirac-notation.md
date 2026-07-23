# LISS-0031: Operator algebra and Dirac notation

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0030, ADR 0018, ADR 0069
- Blocks: general symbolic Hamiltonians and LISS-0032/0033

## Summary

Define typed bra/ket, adjoint, inner/outer product, expectation, projector,
commutator, anticommutator, and tensor-product notation. The design must make
operator domains and codomains visible to type checking while preserving a
formula-like surface.

## In scope

- `|psi>` / `<phi|` and named state expressions;
- adjoint and operator products;
- expectation and projector forms;
- commutator and anticommutator forms;
- lowering to existing state/operator primitives where possible.

## Out of scope

- density/CPTP semantics (LISS-0011 and LISS-0037);
- fermion/boson statistics (LISS-0032);
- continuous calculus (LISS-0036).

## Acceptance questions

- Which notation is normative and which is syntax sugar?
- How are non-square operators and incompatible Hilbert spaces rejected?
- Does adjoint preserve the source provenance needed by QPU lowering?
- Which expressions are evaluable in the current Kernel and which are design
  fixtures only?
