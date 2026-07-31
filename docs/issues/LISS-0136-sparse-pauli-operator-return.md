# LISS-0136: Sparse Pauli Operator return from helper `fn`

## Metadata

- Local issue ID: LISS-0136
- Status: **complete** — 2026-07-31 (awaiting PR merge review)
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel residual / language
- Priority: P1
- Depends on: discovered by [LISS-0134](LISS-0134-showcase-s1-thin-slice.md)
- Implementation permission: **yes** (Adjudicator 「承認」 after #179 merge)
- Branch: `feature/liss-0136-sparse-pauli-operator-return`
- Tests: `tests/test_sparse_pauli_operator_return_red.py`

## Summary

Returning a sparse-Pauli `Operator` built with named `Float` coefficients from
a helper `fn` failed at evolve time with `unbound Operator / scalar …`
because `_resolve_operator_expr` copied the factory AST without folding
factory-local scalars into `OpLit`.

Literal-coeff and `hop` factories already worked; named-Float factories did
not.

## Fix

- `materialize_op_scalar_vars` in `runtime/op_attr_elaboration.py`
- Factory evaluation in `_resolve_operator_expr` captures closed classical
  binds, then substitutes before publishing the Operator to the caller
- Showcase physics module now returns Ising `H` from `build_ising_hamiltonian()`

## Exit

- [x] Failing Red suite locked to the Repro
- [x] Green: returned sparse Pauli with named Floats usable under `evolve`
- [x] Showcase physics helper uses named-Float factory
- [x] Docs / friction ledger updated
- [ ] Adjudicator PR merge review

## Non-goals

- Live QPU / OpenQASM lowering of returned Operators
- LISS-0137 (method/field Float → `evolve for` / Operator outside factories)
- LISS-0138 (`when` ket arms)
