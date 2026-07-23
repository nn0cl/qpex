# LISS-0032: Typed second-quantized operators

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0030, LISS-0031, LISS-0033, LISS-0019
- Blocks: quantum chemistry and many-body Hamiltonian source coverage

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
