# LISS-0139: Operator RHS method Call parse and return

## Metadata

- Local issue ID: LISS-0139
- Status: **complete** — 2026-07-31 (PR pending)
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel residual / parser + evaluator
- Priority: P0 (WP-0031)
- Depends on: [LISS-0137](LISS-0137-classical-float-operator-evolve-binding.md)
- Program: [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md);
  [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/liss-0137-0139-hamiltonian-library-surface`
- Tests: `tests/test_operator_method_call_return_red.py`

## Summary

`Operator H = m.hamiltonian()` parses and evaluates: parser routes
`IDENT.IDENT(` to `_expression`; evaluator resolves method bodies returning
Operator with field/local Float fold.

## Exit

- [x] Red: parse + literal method return evolve
- [x] Green: field-coeff method return
- [x] Showcase `IsingDrive.hamiltonian()`
- [ ] Adjudicator PR merge review
