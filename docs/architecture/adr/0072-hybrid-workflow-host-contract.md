# ADR 0072: Provider-neutral hybrid workflow contract

## Status

Accepted (2026-07-24). This ADR records the LISS-0035 architecture boundary;
it does not select a provider, credential system, or optimizer implementation.

## Context

VQE/QAOA-like studies repeat a closed experiment with host-bound parameters,
submit a Job, consume an opaque JobResult, and decide whether to submit again.
That feedback loop is not QPU Kernel logic. It must not introduce `Job`,
`Task`, `async`, `await`, provider SDK objects, or mutable classical values into
the Theory scope.

## Decision proposal

1. A Workflow is a provider-neutral host orchestration contract over an
   immutable Experiment contract.
2. A workflow may declare parameter bindings, a Job submission policy, a typed
   result projection, a host update step, and a termination policy.
3. The workflow exchanges only immutable boundary DTOs:
   `ExperimentSpec`, `ParamBinding`, `JobRequest`, `JobResult`, and
   `WorkflowReport`.
4. Provider SDK objects, credentials, retries, sessions, and optimizer
   implementations remain adapters or later LISS work.
5. A workflow cannot mutate the Theory or Experiment AST. Each iteration
   creates a new parameter binding and a new Job request.
6. Completion ordering is inherited from ADR 0065: a result is consumable only
   after `main`, terminal `measure`, and result persistence complete.
7. A workflow surface, if accepted, is declarative and source-order
   independent. The resolver builds a dependency graph; it is not an
   imperative method chain.

## Boundary model

```text
Theory -> Experiment -> Workflow contract -> Host Job adapter
                                      ^             |
                                      |             v
                                  update <- opaque JobResult
```

`Workflow` may read a result projection and produce the next `ParamBinding`,
but it may not read backend SDK state or reach into Kernel state.

## Non-goals

- provider SDK selection or credentials;
- retry/session/batch policy;
- optimizer implementation or convergence mathematics;
- dynamic mid-circuit feed-forward;
- Job lifecycle syntax inside the Kernel lane.

## Consequences

The design matches real hardware/cloud execution while keeping the Kernel
semantics closed and measurement-terminal. It requires an explicit DTO schema
and a later host adapter implementation. The first implementation slice can
validate and serialize a local workflow plan without submitting to a provider.
