# Feature: `inner` / `outer` Joint runtime Call (LISS-0229)

## EARS

When the program evaluates `inner(phi, psi)` as a State bind, the system shall
compute the Joint amplitude inner product of the two named wires' computational
marginals and bind a Classical Float (as a State payload) equal to the real part
when the imaginary part is negligible.

When the program binds `Operator P = outer(psi, phi)`, the system shall
materialize the dense outer product |ψ⟩⟨φ| for later `apply(P, w)` on one wire
(MVP: single-wire states).

## Gherkin

```gherkin
Scenario: inner of identical |+> is one
  Given state a = |+>, b = |+>
  When state ov = inner(a, b)
  Then ov inspects near 1.0 and run succeeds

Scenario: inner of orthogonal kets is zero
  Given state z = |0>, o = |1>
  When state ov = inner(z, o)
  Then ov is near 0.0

Scenario: outer can be applied
  Given Operator P = outer(a, b) for single-wire states
  When apply(P, w)
  Then run succeeds without unknown function
```

## Out of Scope

- Paper sugar ⟨φ|ψ⟩ (LISS-0217)
- Multi-wire outer / partial traces

## Ambiguities (locked)

- Inner uses computational marginals on named wires
- Outer MVP is 1-qubit dense matrix Operator
