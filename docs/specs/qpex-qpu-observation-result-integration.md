# Staqex QPU observation/result integration specification

## Status

Accepted for LISS-0066 Phase 1 Red by ADR 0104. Provider SDKs, credentials,
network transport, and live QPU execution are out of scope.

## Acceptance scenarios

### Successful observations preserve plan order

Given a succeeded provider-neutral QPU job and an `ObservationPlan` with two
portable requests, when the Host observation projector receives a structured
result payload, then it returns a succeeded `JobResult` whose immutable
`observations` follow the plan declaration order, even if the payload entries
arrive in another order.

### Incomplete observations fail closed

Given a succeeded provider-neutral QPU job whose payload omits a requested
checkpoint, when the Host projector creates a result, then it returns a failed
`JobResult` with `QPU_OBSERVATION_INCOMPLETE` and no measurements or observation
values.

### Failed and cancelled jobs expose no partial values

Given a failed or cancelled QPU job whose provider payload contains values,
when the Host projector creates a result, then it returns the terminal
provider-neutral diagnostic and exposes neither measurements nor observations.

### Terminal measurement remains separate

Given a succeeded QPU result containing a terminal measurement and checkpoint
observations, when the Host projector creates a result, then the measurement
remains in `JobResult.measurements` and observations remain in
`JobResult.observations` without implicit conversion between them.

### Explicit attempt metadata is preserved

Given an explicit retry attempt, when its succeeded result is projected, then
the logical Job identity remains stable and the one-based attempt and opaque
provider Job identity are preserved in result metadata. Results from another
attempt are not merged.

### Simulator snapshots are rejected on the QPU lane

Given an observation request for a simulator-only state snapshot targeting a
QPU lane, when the plan is validated, then a hard provider-neutral diagnostic
is raised and no QPU result is requested.
