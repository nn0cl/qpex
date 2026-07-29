# LISS-0031: Operator algebra and Dirac notation

- Status: **Phase 3 reviewed** (typed algebra/domain boundary complete; Unicode sugar deferred)
- Depends on: LISS-0030, ADR 0018, ADR 0069
- Architecture decision: [ADR 0087](../architecture/adr/0087-operator-algebra-dirac-notation.md)
- Blocks: general symbolic Hamiltonians and LISS-0032/0033
- Acceptance draft: [`staqex-operator-algebra.md`](../specs/staqex-operator-algebra.md)
- AT-TDD Phase 1 Red: [`test_operator_algebra_red.py`](../../tests/test_operator_algebra_red.py)

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

## Phase 2 Green record

- Added typed validation for `adjoint`, `inner`, `outer`, `projector`,
  `commutator`, and `anticommutator`.
- Built-in Pauli operators retain an Operator contract; State/Operator
  mismatches produce `OPERATOR_ALGEBRA_TYPE_ERROR`.
- `inner` is represented as an algebraic classical scalar and does not consume
  measurement entropy; `outer` and `projector` remain Operator values.
- Early `measure` remains rejected when nested in an algebra operation.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

## Phase 3 review record

- `Operator<V>` preserves an explicit Hilbert carrier for the first typed
  domain boundary; an unparameterized `Operator` remains the compatibility
  form.
- `commutator` and `anticommutator` reject known domain mismatches.
- `adjoint` preserves its operand domain; `outer` and `projector` derive their
  operator domain from the state carrier.
- Domain/codomain pairs for non-square operators remain deferred; the current
  first slice is square-operator focused.
- Function-shaped algebra forms are normative for now. Unicode Dirac
  punctuation is deferred until lexer and grammar review.
- AST source `Span` remains the provenance boundary; serialized Symbolic IR is
  LISS-0033.

Phase 3 acceptance evidence: operator algebra tests pass, all standalone tests
pass, and specification verification passes 165/165 (100%).
