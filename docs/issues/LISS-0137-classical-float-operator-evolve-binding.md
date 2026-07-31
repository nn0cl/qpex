# LISS-0137: Classical Float binding into Operator / `evolve for`

## Metadata

- Local issue ID: LISS-0137
- Status: **ready** — expanded under WP-0031; not started
- Phase: Feature Path (awaiting Plan / batch authorize)
- Type: Kernel residual / elaboration
- Priority: P0 (WP-0031)
- Depends on: [LISS-0136](LISS-0136-sparse-pauli-operator-return.md) (local Float factory fold);
  related to [ADR 0114](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md) / LISS-0121
- Program: [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md);
  [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md)
- Discovered by: [LISS-0134](LISS-0134-showcase-s1-thin-slice.md); expanded for \(H(J,h)\)
- Implementation permission: **none** until Adjudicator Plan/Phase approve
- Branch: TBD (`feature/liss-0137-…`)
- Blocks: [LISS-0139](LISS-0139-operator-method-call-return.md) field-coeff path; showcase param factory

## Summary

Classical `Float` values that come from:

1. **Factory parameters** — `pub fn tfim(J: Float, h: Float) -> Operator`
2. struct field reads (`c.J` bound to `Float J = c.J` or OpAttr),
3. class method returns (`schedule.t()` → `Float duration`),

must remain usable as Operator coefficients and as `evolve … for duration`.

LISS-0136 folds **factory-local** `Float` binds into returned Operators.
Parametrized factories still fail with `unbound Operator / scalar …` because
call arguments are not entered into the factory scalar environment before
`materialize_op_scalar_vars`.

Literals and inspect-only classical tags work. S1 still uses literal duration.

## Target forms (Red)

```text
pub fn tfim(J: Float, h: Float) -> Operator {
  Operator H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
  return H
}
Operator H = tfim(1.0, 0.5)
// …
Float t = schedule.t()
state (s0, s1) = evolve (s0, s1) under H for t …
```

Also: field / OpAttr coefficients without forcing literals.

## Exit

- [ ] Red suite: param factory → evolve; field→Operator; method Float→`evolve for`
- [ ] Green: `_resolve_operator_expr` binds Call args to FunDecl params as scalars
- [ ] Green: evolve duration / Operator paths use consistent classical scalar env
- [ ] Showcase can call `build_ising_hamiltonian(J, h)` / `tfim(J, h)` (follow-up OK)
- [ ] Docs / friction F-11 updated; ADR note only if elaboration policy changes

## Non-goals

- `Operator H = m.hamiltonian()` parse/eval ([LISS-0139](LISS-0139-operator-method-call-return.md))
- `when` ket arms (LISS-0138)
- Live QPU duration binding
- Changing LINEAR consume rules for true quantum resources
