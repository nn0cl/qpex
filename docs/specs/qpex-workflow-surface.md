# QPex declarative workflow surface

| Field | Value |
|---|---|
| Status | **Proposed; architecture review required** |
| Decision | [ADR 0073](../architecture/adr/0073-declarative-workflow-surface.md) |
| Issue | [LISS-0035](../issues/LISS-0035-hybrid-scientific-workflow.md) |

## Purpose

Provide a readable source boundary for a Host-controlled hybrid workflow while
preserving the separation between mathematical QPex code and execution
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
- whether update callbacks can be named from source or remain Host API only;
- serialization format from workflow AST to `WorkflowPlan`.

No implementation is authorized by this proposal until ADR 0073 and this
specification are accepted.
