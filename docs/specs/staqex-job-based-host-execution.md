# Staqex Job-based host execution contract

## Status

Accepted provider-neutral boundary specification for LISS-0022 and ADR-0065.
Provider-specific submission remains outside this contract.

## Invariants

1. Staqex source describes a program; it does not manipulate a host Job.
2. `main -> Unit` completes after its terminal `measure` effect.
3. A host Job is the unit of local, process, simulator-service, and QPU execution.
4. A Job result is opaque structured host data, not a Staqex `State<T>` or `Joint`.
5. `result()` cannot report successful completion before terminal measurement and
   result persistence have completed.

## Scenarios

### Scenario A — submit creates a Job

Given valid Staqex source and host settings

When the host calls `submit(source, settings)`

Then it receives a provider-neutral Job with an identity and lifecycle state.

### Scenario B — result waits for completion

Given a queued or running Job

When the host calls `wait()` or `result()`

Then it returns only after `main`, terminal `measure`, and result persistence
complete, or returns a structured failed/cancelled outcome.

### Scenario C — local execution uses the same contract

Given a local simulator adapter

When the host submits a program

Then it returns a completed Job through the same Job API, even if completion is
immediate.

### Scenario D — blocking run is a convenience projection

Given a valid program

When the host calls `run(source, settings)`

Then it is equivalent to submit followed by wait/result and returns JobResult.

### Scenario E — result is opaque

Given a completed Job

When the host obtains JobResult

Then the result contains structured measurement/metadata data and does not
expose AST, Joint, raw simulator state, or provider SDK objects.

### Scenario F — language boundary remains unchanged

Given a Staqex program

When it is compiled

Then no Job/Task/async/await lifecycle syntax is required or introduced.

## Out of scope

Provider SDK selection, credentials, live submission, session/batch semantics,
retry policy, and effect annotation syntax.
