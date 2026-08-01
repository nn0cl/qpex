# Feature: Local Operator bindings shadow Fock atoms P/Q/N (LISS-0227)

## EARS

When an Operator-valued method or factory binds a local name `P`, `Q`, or `N`
and returns that name, the system shall return the local Operator binding, not
the ADR 0049 Fock atom of the same spelling.

When `P`, `Q`, or `N` appear unbound in an Operator polynomial, the system
shall continue to treat them as Fock number / quadrature atoms.

## Gherkin

```gherkin
Scenario: method-local product named P evolves on two wires
  Given class method returns Operator P = product (i in Index<0..1>) { Z[i] }
  And two state wires
  When evolve under the method result
  Then run succeeds
  And Fock single-bind error does not occur

Scenario: unbound P*P+Q*Q still Fock-evolves
  Given Operator H = 0.5 * (P * P + Q * Q)
  When evolve a Fock vacuum under H
  Then run succeeds
```

## Out of Scope

- Renaming Fock surface away from P/Q
- Pauli atom X/Y/Z/I shadowing (separate)

## Ambiguities

- None for MVP — lexical local binding wins over builtin atom
