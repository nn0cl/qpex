# Staqex continuous operator and discretization contract

| Field | Value |
|---|---|
| Status | **Phase 3 Green; explicit Theory-to-Kernel Bridge implemented** |
| Decision | [ADR 0074](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) |
| Issue | [LISS-0036](../issues/LISS-0036-continuous-operator-and-discretization-boundary.md) |

## Invariants

1. A continuous-domain lowering has an explicit discretization contract.
2. The contract records domain, basis, finite resolution, boundary condition,
   approximation method, and provenance.
3. No backend may silently invent a resolution, boundary condition, or
   approximation order.
4. A discretized operator is distinguishable from its continuous source and
   retains approximation metadata in Symbolic IR.
5. QPU execution consumes only the finite representation; it does not claim
   infinite-dimensional execution.

Phase 2 implements declaration parsing, required-field validation, MVP
domain/basis validation, and the missing-contract diagnostic. It does not yet
connect a continuous operator to a named contract or lower it to a finite
Kernel representation.

Phase 3 adds the explicit Bridge form
`use Contract for Theory.Operator as alias`. The compiler validates both ends
and records the contract/source relationship in Symbolic IR. It does not yet
perform numerical discretization or QPU lowering.

## MVP semantic vocabulary

First-class domains are `Position`, `Momentum`, and `PhaseAngle`. First-class
bases are `UniformGrid`, `FourierBasis`/`PlaneWave`, and `DVR`. These names
carry physical meaning and are not generic integer containers.

`resolution` and approximation order are contract fields available to static
validation. A power-of-two resolution may establish a
`QubitRegister<k>` relation when the basis representation supports it. Other
resolutions require an explicit finite representation and cannot be silently
rounded or padded.

Approximation provenance records either an analytical bound, an
`Empirical(tol = …)` target, or explicit `Unbounded` status.

## Proposed acceptance scenarios

1. A discretization declaration resolves independently of source order.
2. A continuous operator references a named discretization contract.
3. Missing resolution, basis, or boundary produces a hard diagnostic.
4. Conflicting domain or basis choices produce a hard diagnostic.
5. Symbolic IR records the discretization and approximation provenance.
6. A backend cannot lower a continuous operator when its contract is absent.
7. Existing finite-dimensional operators remain valid without a continuous
   discretization declaration.
8. A continuous operator with `error_bound = Unbounded` remains compilable but
   carries that fact into provenance; it is not treated as a guaranteed error
   bound.

## Deferred

- integral and derivative surface notation;
- concrete finite-difference/spectral element implementations;
- numerical error-bound algorithms;
- infinite-dimensional semantics;
- provider-specific hardware mapping.
- final syntax for `kernel` and `use … for … as …` bridge statements.
