# Feature: Nested empty sum contributions are zero (LISS-0226)

## EARS

When a finite `sum` binder expands to several candidate terms and some nested
empty `sum` domains would lower to `OpIdentity(kind=sum)`, the system shall
omit those contributions from the outer sum fold (additive zero), not append an
undetermined identity operator.

When an entire outer `sum` domain is empty, the system shall continue to emit
`OpIdentity` requiring an acting space (LISS-0056).

## Gherkin

```gherkin
Scenario: where-filtered two-index sum evolves without QubitRegister
  Given Operator H = sum (i in Index<0..1>, j in Index<0..1>) where i < j { Z[i]*Z[j] }
  And two state wires
  When evolve under H
  Then run succeeds
  And IDENTITY_ACTING_SPACE_UNDETERMINED does not occur

Scenario: empty outer sum still needs acting space
  Given Operator H = sum (i in Index<3..1>) { Z[i] }
  When run without QubitRegister
  Then IDENTITY_ACTING_SPACE_UNDETERMINED is reported (LISS-0056)
```

## Out of Scope

- Changing product empty-domain identity semantics
- Requiring Host arrays

## Ambiguities

- None for MVP
