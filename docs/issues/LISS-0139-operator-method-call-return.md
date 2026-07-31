# LISS-0139: Operator RHS method Call parse and return

## Metadata

- Local issue ID: LISS-0139
- Status: **ready** — filed under WP-0031; not started
- Phase: Feature Path (awaiting Plan; **after** LISS-0137)
- Type: Kernel residual / parser + evaluator
- Priority: P0 (WP-0031)
- Depends on: [LISS-0137](LISS-0137-classical-float-operator-evolve-binding.md) for field/param coeffs;
  [LISS-0136](LISS-0136-sparse-pauli-operator-return.md) for Operator return fold
- Program: [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md);
  [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md)
- Implementation permission: **none** until Adjudicator Plan/Phase approve
- Branch: TBD (`feature/liss-0139-…`)

## Summary

Physicist reading of a physical **system**:

```text
Operator H = model.hamiltonian()
```

fails today with `PARSE_ERROR: empty tuple`. Cause: Type-First `Operator`
binds use `_op_expression` unless the RHS looks like a bare `ident(` factory.
`recv.method(` is not covered, so OpDSL mis-parses the `(`.

Even after parse, evaluator must resolve `Call(Attr(recv, name), args)` as an
Operator-returning method (reuse 0136/0137 scalar materialization).

## Target forms (Red)

```text
pub class Model {
  // …
  pub fn hamiltonian() -> Operator {
    Operator H = -1.0 * (Z[0] * Z[1]) - 0.5 * (X[0] + X[1])
    return H
  }
}
Operator H = m.hamiltonian()
// then evolve …
```

Follow-on in same Issue or 0137 reuse: `this.J` / field coeffs inside the method.

## Exit

- [ ] Red: `Operator H = m.hamiltonian()` parses
- [ ] Green: literal-coeff method return evolves on SV
- [ ] Green: field/named coeffs in method body (via 0137 machinery)
- [ ] Parser: `_type_first_bind` routes `IDENT DOT IDENT LPAREN` to `_expression`
- [ ] Showcase optional `hamiltonian()` on discovery model
- [ ] Docs / friction updated

## Non-goals

- Inheritance / `protected`
- Non-Operator method Call redesign outside Operator bind RHS
- LISS-0138
