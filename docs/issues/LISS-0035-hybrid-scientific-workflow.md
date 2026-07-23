# LISS-0035: Hybrid scientific workflow contract

- Status: **Phase 3 Green / Phase 4 Design Proposed** (Architecture Path)
- Depends on: LISS-0022, LISS-0016, LISS-0015, LISS-0034, ADR 0070/0071/0072
- Blocks: VQE/QAOA-style iterative execution language surface
- Acceptance specification: [`qpex-hybrid-workflow.md`](../specs/qpex-hybrid-workflow.md)
- Architecture decision: [ADR 0072](../architecture/adr/0072-hybrid-workflow-host-contract.md)
- Surface proposal: [ADR 0073](../architecture/adr/0073-declarative-workflow-surface.md)
- Surface specification: [`qpex-workflow-surface.md`](../specs/qpex-workflow-surface.md)
- AT-TDD Phase 2: [`test_hybrid_workflow_red.py`](../../tests/test_hybrid_workflow_red.py)
- AT-TDD Phase 3: the same test suite covers completed-result feedback,
  immutable iteration history, and `until` termination.

## Summary

Define an explicit host/workflow layer for VQE/QAOA-like loops around a closed
experiment specification. The layer may bind parameters, submit Jobs, consume
typed measurement results, update a classical optimizer, and schedule another
run, while keeping provider policy outside the Kernel.

## Acceptance questions

- What are the parameter-binding, measurement-result, convergence, and
  cancellation DTOs?
- How are shots, seeds, retries, and reproducibility reported?
- Which feedback is host workflow, and which is Dynamic QPU feed-forward?
- How does a workflow compose Job/Task handles without exposing provider SDKs?

## Non-goals

No provider SDK, credentials, cloud submission, or optimizer implementation is
authorized by this design issue.

## Phase 1 design record

- Scope approval: granted for LISS-0035 Architecture Path.
- Architecture proposal: provider-neutral immutable Workflow/Job DTO boundary.
- Implementation permission: granted for the local provider-neutral DTO slice.
- Unresolved boundaries: workflow surface syntax, update expression model,
  convergence/`until`, and cancellation/retry ownership.

## Phase 2 implementation record

- `ParamBinding`, `ExecutionPolicy`, `JobRequest`, and
  `MeasurementProjection` are immutable provider-neutral DTOs.
- `WorkflowPlan` validates declared parameter and observable names.
- `run_once` obtains the result only through the existing `Job.result()`
  boundary and projects measurement data without exposing AST or simulator
  state.
- No provider SDK, credentials, optimizer, retry, session, or workflow surface
  syntax was added.
- Verification: `python3 tests/test_hybrid_workflow_red.py` passes.

## Phase 4 design record

- Proposal: declarative named `workflow` blocks, resolved independently of
  source order.
- Fluent builder chains are not the normative QPex surface.
- Architecture approval: required before parser implementation.
- Unresolved: parameter/observable spelling, `until` expression restrictions,
  and source-level update callbacks.

## Phase 3 implementation record

- `WorkflowReport` records immutable projections, final bindings, iteration
  count, and terminal status.
- `WorkflowPlan.run_iterative` calls `Job.result()` before `until` or `update`.
- Every iteration creates a new validated `JobRequest`; no previous request or
  Experiment contract is mutated.
- `until` and `update` are Host callbacks in this slice. No QPex workflow
  surface syntax or optimizer is inferred from them.
- Verification: `python3 tests/test_hybrid_workflow_red.py` passes.
