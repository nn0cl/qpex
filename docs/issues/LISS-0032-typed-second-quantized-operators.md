# LISS-0032: Typed second-quantized operators

- Status: **Phase 3 reviewed** (typed/statistical provenance boundary complete; execution deferred)
- Depends on: LISS-0030, LISS-0031, LISS-0033, LISS-0019
- Blocks: quantum chemistry and many-body Hamiltonian source coverage
- Acceptance draft: [`qpex-second-quantized-operators.md`](../specs/qpex-second-quantized-operators.md)
- AT-TDD Phase 1 Red: [`test_second_quantized_operators_red.py`](../../tests/test_second_quantized_operators_red.py)

## Summary

Define distinct fermion, boson, spin, and qubit operator families. Include
creation/annihilation operators, statistics, canonical ordering, and an
explicit mapping boundary such as fermion-to-qubit lowering.

## Acceptance questions

- Are `FermionOperator`, `BosonOperator`, `SpinOperator`, and `QubitOperator`
  distinct types rather than aliases of `Operator`?
- How are canonical ordering and exchange relations represented and diagnosed?
- Which mappings are language semantics, compiler passes, or external ports?
- How are mapping choice, qubit count, and approximation provenance retained?

## Non-goals

This LISS does not select OpenFermion, Qiskit Nature, PennyLane, or a provider
SDK, and does not authorize implementation of a chemistry solver.

## Phase 2 Green record

- Added typed family boundaries for `FermionOperator`, `BosonOperator`,
  `SpinOperator`, and `QubitOperator`.
- Added symbolic `create`, `annihilate`, `spin_raise`, and `spin_lower`
  operator atoms.
- Mixed second-quantized families produce
  `SECOND_QUANTIZATION_TYPE_ERROR`.
- Mapping is explicit through the function-shaped `map(operator, mapping)`
  boundary; automatic mapping/provider selection is not performed.
- Early `measure` remains rejected in second-quantized expressions.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

## Phase 3 review record

- Symbolic IR records family statistics (`fermionic`, `bosonic`, `spin`,
  `qubit`).
- Creation/annihilation atoms receive deterministic canonical ordering.
- Fermion permutations record an exchange sign; Boson ordering does not invent
  a fermion sign.
- Explicit mapping names are recorded in the resolved-link metadata surface.
- Full exchange-law normalization, output-domain validation, and numerical
  mapping remain deferred.

Phase 3 acceptance evidence: second-quantized operator tests pass, all
standalone tests pass, and specification verification passes 165/165 (100%).
