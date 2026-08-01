# Feature: Method-returned finite binder under evolve (LISS-0224)

## EARS

When a class method (or free `fn`) returns an `Operator` whose body is an
accepted finite `sum`/`product` binder, the system shall lower that binder to
an executable Pauli operator tree before `evolve` / sparse-Pauli compilation.

If the same binder is bound at top level in `main`, the system shall continue
to behave as LISS-0052 (no regression).

## Gherkin

```gherkin
Scenario: Method-returned sum binder drives evolve
  Given a class method that returns Operator H = sum (i in Index<0..2>) { Z[i] }
  And a caller binds Operator H = instance.method()
  When the program evolves three qubits under H with Suzuki
  Then run exits 0
  And the failure "cannot compile sparse Pauli for OpBinder" does not occur

Scenario: Top-level binder still runs
  Given Operator H = sum (i in Index<0..2>) { Z[i] } in main
  When the program evolves under H
  Then run exits 0
```

## External Dependencies

- None (Kernel Joint / finite_binder only)

## Out of Scope

- New binder kinds beyond the accepted finite slice
- Requiring Host arrays inside method-returned binders

## Ambiguities

- None for MVP
