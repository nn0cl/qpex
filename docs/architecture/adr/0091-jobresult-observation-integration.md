# ADR 0091: Observation reports in the provider-neutral JobResult boundary

## Status

Accepted for [LISS-0046](../../issues/LISS-0046-jobresult-observation-integration.md) Phase 1 Red.
This acceptance authorizes contract tests only. It does not authorize
`JobResult` implementation, provider integration, or a QPex checkpoint syntax.

## Context

LISS-0044 defines explicit observation requests and reports, but its Host
contracts are not yet connected to the existing `JobResult`. The integration
must preserve the Job happens-before guarantee and keep terminal measurement,
portable observations, simulator diagnostics, and provider data distinct.

## Decision proposal

1. Extend the provider-neutral `JobResult` with an additive immutable
   `observations` collection. Existing `measurements`, `diagnostics`, and
   `metadata` retain their meanings.
2. Store `ObservationReport` values directly in that collection rather than
   hiding them in an untyped metadata dictionary.
3. Preserve source/checkpoint order in the collection. A report is available
   only after its associated Job reaches a terminal state.
4. Keep terminal `MeasurementEnvelope` values separate from checkpoint
   reports. A checkpoint does not become an implicit `measure` operation.
5. A failed or cancelled Job may return diagnostics and partial reports only
   if the result contract explicitly marks completeness; silent partial
   success is forbidden. The exact partial-result policy remains open.
6. Keep simulator-only snapshots inside an `ObservationReport` marked
   non-portable. They must not be copied into ordinary measurements or
   represented as QPU results.
7. Host adapters create and attach reports; the Kernel does not access
   `JobResult` or provider data. `WorkflowReport` continues to project its
   existing measurement contract until a separate workflow integration is
   accepted.

## Non-goals

- No provider SDK, credential, persistence, retry, or session implementation.
- No change to terminal `measure` semantics.
- No QPex `checkpoint` syntax.
- No dynamic mid-circuit measurement semantics.

## Open decisions

- Exact field name and type for `JobResult.observations`.
- Whether partial reports are allowed and how completeness is represented.
- Whether report ordering is source order, completion order, or both.
- How `WorkflowReport` exposes checkpoint reports without duplicating data.
- Whether `ObservationReport.provenance` becomes a typed value object.
