# Research: Quantum execution boundaries and result flow

## Status

Research note for QPex architecture review. This note is informative; it does
not itself authorize implementation or accept ADR-0064.

## Question

Should QPex model execution as a synchronous call chain, an OS-process fork,
or a job/handle workflow when the long-term target includes simulators, QPUs,
remote providers, and hybrid quantum-classical execution?

## Sources reviewed

- IBM Quantum Runtime documents describe `run()` returning a `RuntimeJobV2`
  with status, result, and cancellation operations, and distinguish job,
  session, and batch execution modes:
  [IBM Runtime API](https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/runtime-service),
  [execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes).
- Amazon Braket documents describe `device.run()` creating a queued quantum
  task, storing results in S3, and `task.result()` polling until completion:
  [Braket task submission](https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html),
  [task tracking](https://docs.aws.amazon.com/braket/latest/developerguide/braket-monitor-tasks-sdk.html).
- Azure Quantum documents describe jobs with IDs, provider/target metadata,
  queued and executing states, final succeeded/failed states, and output
  storage:
  [Azure Quantum jobs](https://learn.microsoft.com/en-us/azure/quantum/how-to-work-with-jobs).
- Q# documents show a contrasting language-level model: callables have
  explicit return types, `Result` represents a measurement result, and `Unit`
  represents no value:
  [Q# overview](https://learn.microsoft.com/en-us/azure/quantum/qsharp-overview),
  [returns and termination](https://learn.microsoft.com/en-us/azure/quantum/user-guide/language/expressions/returnsandtermination).
- QIR-EE research describes a cross-platform execution engine with extension
  points for runtimes and hardware environments:
  [A Cross-Platform Execution Engine for QIR](https://arxiv.org/abs/2404.14299).

## Observed industry/research pattern

### 1. Language callables have explicit result contracts

Q# is a clear example: operations and functions declare result types; a
measurement operation can return a `Result`, and no-result operations use
`Unit`. This supports compositional source-level reasoning.

### 2. Physical execution is usually a job, not a process fork

IBM Runtime, Amazon Braket, and Azure Quantum all expose job/task identity,
status, result retrieval, and (where supported) cancellation. Queueing and
provider availability make a blocking call an implementation convenience, not
the universal execution model.

### 3. Synchronous APIs are convenience projections over asynchronous backends

SDKs commonly offer a blocking `result()` / equivalent wait operation over a
job handle. Local simulators can complete immediately; QPUs and remote
services cannot be assumed to do so.

### 4. Results cross a host boundary as structured data

Results are returned as primitive results, measurement arrays/counts,
probabilities, metadata, or files/object storage. The caller does not receive
the simulator's internal state vector or the provider's internal execution
state as the normal application result.

### 5. Hybrid execution needs more than one lifecycle

IBM's job/session/batch modes and QIR execution-engine work show that one
submission may contain multiple quantum invocations, classical preprocessing,
or dependent/independent sub-jobs. A single `fork` abstraction is too low-level
and a single synchronous call is too restrictive.

## QPex architectural recommendation

Use two layers with different semantics, using the industry-facing `Job`
vocabulary at the host boundary:

```text
QPex language:
    main -> Unit
    pure function/method call chain
    terminal measure boundary

Host Runtime API:
    run(program) -> JobResult                    # blocking convenience
    submit(program) -> Job                       # async-capable
    job.wait() / job.result() -> JobResult
    job.status() / job.cancel()
```

`JobResult` must be a host DTO/ABI result, not a QPex value and not an
exposed `Joint`/AST. A typed measurement may be represented as a serialized
`MeasurementEnvelope` containing the payload schema, value/counts, target,
shots, status, and provenance metadata.

The happens-before contract is:

```text
JobResult available
  => QPex main completed
  => terminal measurement completed
  => result sink/job persistence completed
```

For a local CPU run, `run()` can implement this synchronously. For a process,
simulator service, or QPU, the host adapter implements `submit()` and
`wait()` using a process handle or provider job handle. Fork semantics must not
become QPex language semantics.

## Consequences for existing QPex decisions

- `main -> Unit` remains a language-level lifecycle result; it does not need to
  return the sampled `T`.
- `measure` is a terminal language effect. The sampled value crosses the
  Runtime/Host port boundary as an envelope or sink event.
- The CLI is a host entry point that invokes QPex `main`; it is not a second
  QPex `main` and must not inspect QPex internals.
- `compiler/qpex.run_path()` currently exposes `EvalResult` containing internal
  state; this should become an internal/debug API once the host ABI is defined.
- Direct stdout/file writes inside `_measure()` are adapter policy. The core
  should emit through `MeasureSinkPort`; file/network/provider policy belongs
  outside the language domain.
- LISS-0016 (host-side QPU submit), LISS-0015 (effects), and ADR-0064
  (explicit `main -> Unit`) are related boundaries. They should converge on
  the provider-neutral `Job` / `JobResult` contract rather than invent
  provider-specific language semantics.

## Rejected architectural extremes

### QPex-level fork

Rejected as language semantics. It exposes OS scheduling and wait behavior,
does not model remote QPU queues, and complicates state/result ownership.
Process handles remain a host adapter implementation.

### Always-blocking QPex call

Rejected as the only host API. It is suitable for local CPU and CLI ergonomics
but cannot represent queueing, cancellation, retries, sessions, or delayed
provider results without blocking the caller.

### Returning raw `T` or `Joint` from QPex `main`

Rejected for the MVP boundary. A raw `T` would make observation a normal
object-language return and a raw `Joint` would leak implementation state. A
host-side typed result envelope preserves opacity and provider portability.

## Proposed next work

1. Accept or revise ADR-0064's explicit `main -> Unit` contract.
2. Create a dedicated host execution/result LISS that defines `Job`,
   `JobResult`, `MeasurementEnvelope`, lifecycle states, cancellation,
   persistence, and error mapping.
3. Refactor the CLI and Python embedding API behind that host contract.
4. Implement QPU submit only in a host adapter, after the contract is accepted.

## Confidence and gaps

Confidence is high for the broad lifecycle pattern because the IBM, AWS, and
Azure APIs independently expose job identity/status/result retrieval. Exact
QPex envelope fields, serialization, cancellation guarantees, and whether a
future hybrid loop needs in-session callbacks remain design questions and need
their own acceptance specification.
