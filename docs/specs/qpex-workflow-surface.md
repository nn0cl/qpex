# Staqex declarative workflow surface

| Field | Value |
|---|---|
| Status | **Phase 4 Green; named Host update callback implemented** |
| Decision | [ADR 0073](../architecture/adr/0073-declarative-workflow-surface.md) |
| Issue | [LISS-0035](../issues/LISS-0035-hybrid-scientific-workflow.md) |

## Purpose

Provide a readable source boundary for a Host-controlled hybrid workflow while
preserving the separation between mathematical Staqex code and execution
orchestration.

## Proposed acceptance scenarios

1. A named `workflow` block can refer to an Experiment contract.
2. Parameter and observable declarations are collected independently of source
   order.
3. The resolver produces the existing immutable `WorkflowPlan` contract.
4. Workflow source cannot refer to provider SDK objects, credentials, or raw
   `Job` handles.
5. `until` is checked as a workflow termination declaration and cannot create a
   Kernel mid-program measurement or general classical loop.
6. A malformed or ambiguous workflow declaration fails before lowering.
7. Mathematical Theory/Experiment expressions remain formula-like; no builder
   chain is required.

## Deliberately unresolved

- exact parameter declaration syntax;
- canonical observable declaration syntax;
- the allowed expression language for `until`;
- richer update forms beyond a named Host callback;
- serialization format from workflow AST to `WorkflowPlan`.

No implementation is authorized by this proposal until ADR 0073 and this
specification are accepted.

Phase 1 acceptance tests are recorded in
`tests/test_workflow_surface_red.py`. They now pass: the workflow contract is
exposed by the compiler result and invalid Host/Job references are diagnosed.

Phase 3 additionally validates Experiment references, `Param<T>` parameter
types, and the restricted `until observable comparator scalar` form.

Phase 4 accepts `update = callback_name` as an opaque Host callback reference.
Inline arithmetic or Kernel expressions in `update` are rejected.
