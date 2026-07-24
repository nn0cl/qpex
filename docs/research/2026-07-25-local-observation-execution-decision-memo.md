# LISS-0047 local observation execution: decision memo

## Purpose

This memo records the remaining architecture decisions before Phase 1 Red.
It does not authorize implementation. The design must remain pleasant for a
physicist reading an observation plan and clean for an engineer maintaining
the Host/Kernel boundary.

## Recommendation summary

| Decision | Recommended direction | Why it matters |
|---|---|---|
| Port input | `ObservationExecutionPort.execute(plan, execution)` where `execution` is a Host-owned opaque execution context | Keeps source/AST/evaluator objects out of the adapter API while allowing a simulator to use a compiled experiment |
| Deterministic values | Local fake adapter uses an injected `ObservationValueSource` seeded by the Host execution policy | Tests reproducibility without pretending that a fake value is a physical simulator result |
| Adapter name | `LocalObservationAdapter` | Describes the lane, not a provider or an implementation trick |
| Separate Job | Phase 1 records requested cost only; it does not create child Jobs | Avoids inventing lifecycle semantics before Job ordering and partial-result policy are accepted |
| Unsupported projection | `OBSERVATION_PROJECTION_UNSUPPORTED` as a hard provider-neutral diagnostic | Makes unsupported capability visible and prevents fabricated reports |

## 1. Port input boundary

### Preferred shape

```text
ObservationExecutionPort
  execute(plan: ObservationPlan, execution: HostExecutionContext)
    -> ObservationExecutionResult
```

`HostExecutionContext` should identify the program/Job, target lane, seed
policy, and already validated execution metadata. It must not expose `Joint`,
AST, provider SDK objects, or raw simulator buffers.

The port should not accept raw source because parsing and compilation belong to
the existing Host submission path. It should not accept `CompilationUnit`
because that would leak compiler internals into an adapter contract.

### Decision required

Whether to introduce `HostExecutionContext` now or use a smaller existing
`JobRequest`/`JobResult` composition. This is an architecture boundary choice,
not merely a class name choice.

## 2. Deterministic value source

The local adapter needs a deterministic source for portable observation values.
It should not fabricate values silently and label them as physical simulation.

Recommended MVP:

- inject an `ObservationValueSource` port;
- use a deterministic fake implementation in contract tests;
- require an explicit seed in the execution context;
- attach `source = fake` or `source = simulator` provenance to the report.

An actual evaluator-backed expectation calculation is a later slice because it
requires deciding how a checkpoint refers to an intermediate state without
violating terminal measurement semantics.

### Decision required

Whether Phase 2 should implement only a fake value source or also connect the
existing simulator evaluator. The former is safer and smaller; the latter is
more useful but introduces a new execution-state boundary.

## 3. Separate Job semantics

`ObservationRequest.separate_job` currently records an explicit resource
request. It must not silently cause a child `Job` in the first local slice.

Recommended MVP behavior:

- preserve `separate_job` and `additional_shots` in the execution result;
- return one completed parent JobResult;
- defer child Job identity, ordering, cancellation, and partial failures.

This is consistent with the existing Job happens-before contract and avoids
pretending that a local adapter has cloud-like queue semantics.

### Decision required

Whether the first local slice is allowed to return one parent report only, or
must model child Job identities immediately.

## 4. Unsupported projection diagnostic

Unsupported projections must be hard diagnostics. The adapter must not return
an empty or guessed report.

Recommended code:

```text
OBSERVATION_PROJECTION_UNSUPPORTED
```

The diagnostic should include projection, target lane, checkpoint identity, and
whether the request was portable or simulator-only.

## Phase gate

Phase 1 Red can start after the four decisions above are accepted. Until then,
the repository has a complete Phase 0 design intake but no authoritative
contract for the execution port or its value source.
