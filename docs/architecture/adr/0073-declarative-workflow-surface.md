# ADR 0073: Declarative workflow surface over fluent builder syntax

## Status

Accepted for the Phase 4 surface slice. Broader workflow syntax remains
deferred.

## Context

Staqex needs a readable surface for host-controlled hybrid studies. A fluent
method chain can encode construction steps, but it makes ordering look
operational and hides the distinction between Theory, Experiment, Workflow,
and Execution. The workflow boundary already resolves declarations after
source collection and uses immutable Host DTOs.

## Decision proposal

Use a named declarative `workflow` block as the Staqex surface. Its declarations
are collected without source-order semantics and resolved into a Host
`WorkflowPlan` contract. Do not expose a mandatory fluent builder or
method-chain syntax in the Kernel lane.

Illustrative shape (not yet accepted syntax):

```staqex
workflow GroundStateSweep {
    experiment = GroundState
    parameter theta : Param<Angle>
    observe energy
    until energy <= 0.01
}
```

The block may name an Experiment, declare parameters and observables, and state
an explicit termination policy. Concrete Host values, Job handles, provider
objects, and optimizer callbacks remain outside the Kernel AST. Resolution
produces the existing provider-neutral `WorkflowPlan`/DTO boundary.

## Rules

1. Workflow declarations are order-independent; dependency direction remains
   `execution -> workflow -> experiment -> theory`.
2. Formula/operator bodies retain mathematical expression syntax and are not
   rewritten as builder calls.
3. `until` is a declarative termination constraint only. It does not introduce
   a general classical loop or mid-program measurement.
4. Provider-specific execution settings are referenced through the Execution
   contract, never embedded as SDK objects.
5. `update = callback_name` may name a Host callback. Inline arithmetic,
   Kernel expressions, and provider objects are rejected.

## Alternatives rejected for this slice

- Mandatory fluent builder chains: obscures phase boundaries and source-order
  independence.
- Job/Task methods in Staqex: violates ADR 0065 and leaks Host lifecycle into the
  Kernel.
- General classical workflow language: expands scope beyond LISS-0035.

## Review questions

- Is `until` a named constraint, a restricted expression, or Host-only metadata?
- Should `observe energy` or `observable = energy` be canonical?
- Is parameter declaration syntax shared with the Parametric Circuit lane?
- This slice accepts only a named Host callback; richer update forms remain
  deferred.
