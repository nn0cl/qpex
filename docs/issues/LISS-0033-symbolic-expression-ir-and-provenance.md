# LISS-0033: Symbolic expression IR and lowering provenance

- Status: **Phase 3 reviewed** (traceable source IR boundary complete; lowering deferred)
- Depends on: LISS-0030/0031, LISS-0019, LISS-0017, LISS-0018
- Blocks: trustworthy theory-to-QPU lowering
- Acceptance draft: [`qpex-symbolic-expression-ir.md`](../specs/qpex-symbolic-expression-ir.md)
- AT-TDD Phase 1 Red: [`test_symbolic_expression_ir_red.py`](../../tests/test_symbolic_expression_ir_red.py)

## Summary

Define an expression-preserving IR between QPex source and executable QPU IR.
The IR must retain binder structure, domains, operator algebra, mappings,
discretization, approximation policy, and source provenance long enough to
support diagnostics and honest result reporting.

## Acceptance questions

- What is the stable boundary between symbolic, resolved, and executable IR?
- Which rewrites are semantics-preserving and which require an error budget?
- How are Trotter/Suzuki order, step count, mapping, and discretization
  recorded?
- Can a diagnostic point back to the original formula rather than only to a
  lowered gate?

## Non-goals

No concrete backend, QPU provider, or cloud credential policy is selected by
this LISS.

## Phase 2 Green record

- Added a provider-neutral `CompileResult.symbolic_ir` projection.
- Binder, indexed operator, operator algebra, and source `Span` structure are
  retained as inspectable nodes.
- A source provenance record links the compilation unit to the Symbolic IR.
- No Provider SDK object, backend choice, approximation, or execution effect is
  introduced.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

## Phase 3 review record

- Operator nodes receive deterministic IDs such as `operator:H`.
- The IR exposes a `ResolvedProgram` link surface with source node IDs and an
  explicit `unresolved` status.
- Provenance records include output node IDs and reserved mapping/
  approximation metadata slots.
- Empty approximation lists are explicit; no approximation is implied by the
  source projection.
- A serialized interchange format and executable lowering pass records remain
  deferred until the resolved/QPU IR design is accepted.

Phase 3 acceptance evidence: Symbolic IR tests pass, all standalone tests pass,
and specification verification passes 165/165 (100%).
