# LISS-0137: Classical Float binding into Operator / `evolve for`

## Metadata

- Local issue ID: LISS-0137
- Status: **complete** — 2026-07-31 (PR pending)
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel residual / elaboration
- Priority: P0 (WP-0031)
- Depends on: [LISS-0136](LISS-0136-sparse-pauli-operator-return.md)
- Program: [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md);
  [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/liss-0137-0139-hamiltonian-library-surface`
- Tests: `tests/test_classical_float_operator_evolve_binding_red.py`

## Summary

Classical `Float` from factory parameters, struct fields, and method returns
are usable as Operator coefficients and as `evolve … for duration`.

## Exit

- [x] Red suite: param factory → evolve; field→Operator; method Float→`evolve for`
- [x] Green: Call args → factory scalars; `_is_closed` struct fields; scalar capture after method binds
- [x] Showcase uses `build_ising_hamiltonian(J, h)` and `evolve … for duration`
- [ ] Adjudicator PR merge review
