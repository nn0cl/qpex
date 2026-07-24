# LISS-0035: Hybrid scientific workflow contract

- Status: **Phase 4 Green** (Architecture Path; named Host update callback)
- Depends on: LISS-0022, LISS-0016, LISS-0015, LISS-0034, ADR 0070/0071/0072
- Blocks: VQE/QAOA-style iterative execution language surface
- Acceptance specification: [`qpex-hybrid-workflow.md`](../specs/qpex-hybrid-workflow.md)
- Architecture decision: [ADR 0072](../architecture/adr/0072-hybrid-workflow-host-contract.md)
- Surface proposal: [ADR 0073](../architecture/adr/0073-declarative-workflow-surface.md)
- Surface specification: [`qpex-workflow-surface.md`](../specs/qpex-workflow-surface.md)
- AT-TDD Phase 1 Red: [`test_workflow_surface_red.py`](../../tests/test_workflow_surface_red.py)
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
- Unresolved: richer update forms beyond a named Host callback.

## Phase 1 Red record

- Canonical surface spelling for this slice: `experiment`, `parameter`,
  `observable`, and `until` declarations inside a named `workflow` block.
- The Red tests demonstrate the missing `CompileResult.workflow_contracts`
  boundary and provider/Kernel Job reference diagnostics.
- Verification: `python3 tests/test_workflow_surface_red.py` fails at the
  unimplemented workflow contract boundary as expected.
- Phase 2 implementation approval: granted; parser/resolver slice implemented.

## Phase 2 implementation record

- `workflow` blocks collect `experiment`, `parameter`, `observable`, and
  `until` declarations independently of source order.
- `CompileResult.workflow_contracts` exposes immutable `WorkflowContract`
  values.
- Provider/backend values and Kernel `Job`/`Task` references produce
  `WORKFLOW_SURFACE_ERROR` before lowering.
- Verification: `python3 tests/test_workflow_surface_red.py` passes.

## Phase 4 implementation record

- `update = callback_name` is retained in the immutable WorkflowContract.
- Inline arithmetic and Kernel expressions are rejected; updates remain Host
  callbacks and do not expand the Kernel into a general classical language.
- Verification: `python3 tests/test_workflow_surface_red.py` passes.

## Phase 3 implementation record

- Workflow contracts now validate that `experiment` names an Experiment scope.
- Parameter declarations retain and validate their `Param<T>` type.
- `until` must compare a declared observable with a scalar identifier or
  numeric literal.
- Invalid provider/Job references remain hard `WORKFLOW_SURFACE_ERROR`
  diagnostics before lowering.
- Verification: `python3 tests/test_workflow_surface_red.py` passes.

## Phase 3 implementation record

- `WorkflowReport` records immutable projections, final bindings, iteration
  count, and terminal status.
- `WorkflowPlan.run_iterative` calls `Job.result()` before `until` or `update`.
- Every iteration creates a new validated `JobRequest`; no previous request or
  Experiment contract is mutated.
- `until` and `update` are Host callbacks in this slice. No QPex workflow
  surface syntax or optimizer is inferred from them.
- Verification: `python3 tests/test_hybrid_workflow_red.py` passes.
