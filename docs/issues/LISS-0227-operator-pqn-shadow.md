# LISS-0227: Local Operator `P`/`Q`/`N` must shadow Fock atoms

## Metadata

- Local issue ID: LISS-0227
- GitHub issue: (none yet)
- Status: **complete**
- Phase: Phase 3 complete (Adjudicator authorized re-check residual)
- Type: bug
- Priority: P0
- Initial planning size: S
- Current planning size: S
- Owner/agent: Cursor agent
- Related branch: `feature/wp-0071-binder-when-enum-gaps`
- Program: [WP-0071](../work-plans/WP-0071-s01-kernel-gaps-from-review.md) residual

## Summary

Inside an Operator method:

```staqex
pub fn corridor() -> Operator {
  Operator P = product (i in Index<0..1>) { Z[i] }
  return P
}
```

`return P` historically parsed as momentum quadrature `OpQuadrature(kind=P)`
(ADR 0049 atom), not the local binding. Evolve then took the Fock path and
failed with `Fock Hamiltonian evolve requires a single bind name` on multi-wire
Pauli product Hamiltonians.

Bare `P`/`Q`/`N` in polynomials with **no** local binding must keep Fock
meaning (`Operator H = 0.5 * (P * P + Q * Q)`).

## Acceptance Notes

- [x] Red: method-local `Operator P = product …; return P` evolves on two wires
- [x] Red: same for `Q` and `N` local names returning Pauli products
- [x] Green: unbound `P*P+Q*Q` Fock HO still evolves (ADR 0049 / SV-27)
- [x] S01 `corridor_product` can evolve under method return (rename optional)

## Dependencies

- Related: ADR 0049, LISS-0224, LISS-0051
- Spec: [staqex-v1-liss-0227-operator-pqn-shadow.md](../specs/staqex-v1-liss-0227-operator-pqn-shadow.md)

## Verification

- `python3 tests/test_liss_0227_operator_pqn_shadow_red.py`
- XP / Fock examples still green
