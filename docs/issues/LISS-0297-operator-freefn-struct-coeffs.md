# LISS-0297: Operator free-fn with struct field coefficients

## Metadata

- Local issue ID: LISS-0297
- Status: **complete** (2026-08-03)
- Type: Feature Kernel residual (+ S01 face)
- Priority: P1
- Depends: ADR 0114 / LISS-0121 OpAttr; LISS-0136 Operator factory scalars
- Branch: `feature/liss-0297-operator-freefn-struct-coeffs`

## Problem

```text
pub fn h_of(k: Coeffs) -> Operator { return k.c * Z[0] }
… Operator H = h_of(pack)   // pack ≠ param name
→ unbound struct for Operator coefficient `k.c`
```

`_resolve_operator_factory_call` only folded **scalar** args. OpAttr used
`self.objects` keyed by **caller** names, not free-fn **parameter** names.
Intermediate `Float c = k.field` was also skipped (`_is_closed` only saw
global objects).

## Fix

1. Bind object args under **parameter** names (`local_objects`).
2. `materialize_op_attrs` against `self.objects ∪ local_objects`.
3. Intermediate classical binds: treat Attr on free-fn object params as closed;
   eval with `local_assign`.

## S01 face

- `ConstraintDrive` class → free `constraint_hamiltonian` / `recovery_hamiltonian` / `named_coeff_sum`
- `Lattice` class → free Operator factories (`damage_hamiltonian`, …)
- Spine / day2 / lattice_four updated

## Exit

- [x] Unit tests (direct OpAttr, intermediate Float, multi-field)
- [x] seed-0 spine / day2 / lattice_four
- [x] Friction ledger §5 closed
