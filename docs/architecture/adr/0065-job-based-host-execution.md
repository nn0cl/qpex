# ADR 0065: Job-based host execution boundary

## Status

**Accepted** (2026-08-01) — WP-0077 / LISS-0213. Shipped slice matches
[LISS-0022](../../issues/LISS-0022-job-based-host-execution.md) (local Job /
JobResult, linked-file APIs, CLI, REPL). Provider submission, retries, and
sessions remain deferred and are **not** authorized by this acceptance.


## Context

Local simulation is naturally synchronous, but real QPU and cloud execution is
queued and externally observed through a job or task. IBM Runtime, Amazon
Braket, and Azure Quantum independently expose identity, lifecycle state, and
result retrieval at this boundary. Modeling Staqex as an OS process or as an
always-blocking call would not match that operational model.

The language must nevertheless preserve its own semantic boundary: `main` is a
Staqex program with `-> Unit`, and terminal `measure` is the only observation
effect. The language must not acquire provider-specific scheduling or polling
syntax.

## Decision proposal

1. The public Host API is Job-oriented:

   ```text
   submit(program, settings) -> Job
   job.status()                  -> JobStatus
   job.wait()                    -> JobResult
   job.result()                  -> JobResult   # only after completion
   job.cancel()                  -> CancelOutcome
   run(program, settings)        -> JobResult   # blocking convenience
   ```

2. `Job` is a provider-neutral handle. A local simulator, subprocess adapter,
   simulator service, and remote QPU adapter all satisfy the same lifecycle
   contract.
3. `JobResult` is a host DTO/ABI. It may contain `MeasurementEnvelope`, status,
   target, shots, provenance, diagnostics, and provider references. It must not
   expose Staqex AST, `Joint`, or simulator state as the normal result.
4. `ExecutionHandle` and `ExecutionResult` remain possible internal names, but
   they are not the primary student/researcher-facing vocabulary.
5. `Handler` is adapter terminology only. Staqex source does not submit, poll,
   cancel, or await a Job.
6. The happens-before guarantee is:

   ```text
   job.result() available
     => main completed
     => terminal measure completed
     => result sink / provider persistence completed
   ```

7. CLI `staqex run` may hide submit/wait for local ergonomics while documenting
   the same Job lifecycle. A local completed Job is not a separate semantic
   model.

## Consequences

Positive:

- The mental model matches real quantum hardware and cloud SDKs.
- Students can start with blocking `run`, then learn `Job` when using a QPU.
- Provider queueing, delayed results, cancellation, and metadata have a stable
  home outside the language kernel.
- `main -> Unit` and measurement opacity remain intact.

Negative:

- A provider-neutral result schema and lifecycle state machine must be defined.
- CLI and Python embedding APIs need an adapter migration.
- Cancellation, retry, persistence, and session/batch semantics require later
  policy decisions.

## Boundaries and non-goals

- No provider SDK or credentials in `compiler/staqex/`.
- No Staqex-level `async`, `await`, `Job`, or `Task` syntax.
- No live cloud test in the Kernel conformance suite.
- Provider-specific job semantics remain in LISS-0016 after this contract.

## Verification proposal

- Phase 1: contract tests for Job lifecycle, blocking `run`, result opacity, and
  completion ordering using a fake adapter.
- Phase 2: minimal local Job implementation behind a Host port.
- Phase 3: refactor CLI and embedding API without changing contract assertions.
- Full SV, QASM, and existing language conformance remain green.
