# Feature: Joint `apply(qft/iqft/cqft, …)` runtime (LISS-0228)

## EARS

When the program binds `Operator F = qft(reg)` (or `iqft` / `cqft` /
`ciqft`) and later executes `apply(F, w0, …, w_{n-1})` with one state wire per
logical qubit of the operator's acting space, the system shall apply the exact
dense Fourier unitary on those Joint wires.

When `apply` wire count mismatches the register arity encoded in the QFT Call,
the system shall reject with a clear KernelError.

`apply(F, reg)` register sugar remains out of MVP (registers have no runtime
coordinates).

## Gherkin

```gherkin
Scenario: qft then iqft restores computational basis on two wires
  Given QubitRegister<2> reg and Operator F = qft(reg), Fi = iqft(reg)
  And state a = |0>, b = |1>
  When apply(F, a, b) then apply(Fi, a, b)
  Then a computational witness restores |01> (seed 0 green run)

Scenario: cqft applies under filled control
  Given QubitRegister<1> ctrl, QubitRegister<2> reg
  And Operator CF = cqft(ctrl, reg)
  When apply(CF, c, t0, t1) with c in |1>
  Then run succeeds without Call compile error
```

## Out of Scope

- `apply(F, reg)` sugar
- Approximate QFT
- Live QPU submit

## Ambiguities (locked for WP-0072)

- Wire order: MSB = first apply wire (matches `apply_unitary_on_wires`)
- Dense matrix factory (ADR 0120 optional) is the Joint path
