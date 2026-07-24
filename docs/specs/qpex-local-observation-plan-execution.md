# QPex local observation plan execution

## Status

Proposed for LISS-0047 Phase 0 review. No implementation is authorized by this
specification.

## Acceptance scenarios

### Local portable observations

Given a valid local `ObservationPlan` containing expectation, probability, or
counts requests, when the local observation port executes it, then a completed
JobResult contains reports in request order with the correct checkpoint and
Job identity.

### Explicit resources

Given requests with `extra_shots` or `separate_job`, when a plan is executed,
then the resulting Job metadata records those requested resources. No hidden
requests or measurements are inserted.

### Deterministic fake execution

Given the same source, plan, and explicit seed, when the local adapter runs
twice, then the portable report values and provenance are reproducible.

### Unsupported projection

Given a projection outside expectation, probability, or counts, when execution
is requested, then the adapter returns a stable provider-neutral diagnostic and
does not fabricate a report.

### Provider isolation

Given a local execution, when the adapter returns, then no provider SDK,
network, credential, evaluator Joint, AST, or raw simulator buffer crosses the
Host result boundary.

## Out of scope

QPU submission, provider adapters, snapshot execution, dynamic measurement,
partial-report semantics, persistence, and WorkflowReport integration.
