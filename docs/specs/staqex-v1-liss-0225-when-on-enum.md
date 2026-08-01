# Feature: when on classical enum (LISS-0225)

## EARS

When a classical enum binding is used as the control of `when`, the system
shall select arms by variant name (e.g. `Open`) without KeyError, producing a
State mixture / assignment consistent with existing `when` semantics.

## Gherkin

```gherkin
Scenario: when on Open enum takes Open arm
  Given N.S s = N.S.Open
  When state w = when (s) { Open -> |1>, else -> |0>, }
  And measure w
  Then run exits 0
  And the Open arm is selected (observable via inspect/expect or measure mass)

Scenario: when on Blocked enum takes else arm
  Given N.S s = N.S.Blocked
  When state w = when (s) { Open -> |1>, else -> |0>, }
  Then run exits 0
  And the else arm is selected

Scenario: when on coin still works
  Given state bit = coin()
  When state w = when (bit) { 0 -> |0>, else -> |+>, }
  Then run exits 0
```

## External Dependencies

- None

## Out of Scope

- Pattern syntax `N.S.Open` in arms (bare variant name only, as parser today)
- Quantum enum payloads

## Ambiguities

- None for MVP
