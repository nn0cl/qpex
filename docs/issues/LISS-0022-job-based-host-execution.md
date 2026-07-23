# LISS-0022: Job-based host execution and result contract

## Metadata

- Local issue ID: LISS-0022
- Status: Phase 3 complete; provider adapter follow-up remains open
- Phase: Architecture Path, then Feature Path
- Type: host boundary contract
- Priority: P0
- Initial planning size: XL
- Related: ADR-0027, ADR-0029, ADR-0032, ADR-0036, ADR-0064, ADR-0065,
  LISS-0015, LISS-0016, LISS-0019

## Summary

Define the provider-neutral host contract that executes a QPex program as a
`Job`, waits for completion, and returns an opaque structured result. The
contract must work for a local simulator and future cloud/QPU adapters without
leaking `Joint`, AST, or provider SDK types into the Kernel.

## Acceptance criteria

- [ ] `submit(program, settings) -> Job` is specified as the primary async-capable host operation.
- [ ] `Job.status()`, `Job.wait()`, `Job.result()`, and `Job.cancel()` semantics are specified.
- [ ] `run(program, settings) -> JobResult` is specified as a blocking convenience operation.
- [ ] `JobResult` and `MeasurementEnvelope` fields and opacity rules are specified.
- [ ] Result availability guarantees completion of `main`, terminal measurement, and sink/provider persistence.
- [x] Local fake adapter contract tests exist and do not require a provider or network.
- [x] CLI/Python embedding migration boundaries are documented.
- [ ] No QPex language syntax for Job/Task lifecycle is introduced.
- [ ] No provider SDK, credential, or network dependency enters the Kernel.

## Explicit non-goals

- Selecting IBM, AWS, Azure, Braket, or another provider.
- Implementing real cloud/QPU submission.
- Defining hybrid session/batch orchestration.
- Exposing raw `T`, `Joint`, AST, or simulator buffers to host callers.

## Design questions

- Canonical public name: `Job` or `Task` (with aliases only if necessary).
- State set: `queued`, `running`, `succeeded`, `failed`, `cancelled`.
- Whether cancellation is best-effort or guaranteed at each state.
- Stable serialization for measurement values and counts.
- Mapping provider errors and retry metadata into the neutral result.

## Dependencies

- ADR-0065 architecture acceptance.
- LISS-0021 / ADR-0064 for explicit `main -> Unit`.
- LISS-0015 for future effect vocabulary.
- LISS-0016 for provider-specific submission after the neutral contract.

## AT-TDD sequence

1. Phase 1 Red: fake-Job contract tests only.
2. Phase 2 Green: minimum local Job port/adapter and host DTOs.
3. Phase 3 Refactor: CLI/embedding boundary cleanup and reviewer empathy pass.

## Current implementation evidence

- `compiler/qpex/host.py` provides the minimum local Job boundary.
- `tests/test_job_host_contract_red.py` passes 5/5.
- Full spec verification remains 164/164.
- Phase 3 local CLI/embedding work is complete; provider-specific work remains
  outside this Issue's implementation boundary.

## Phase 3 completion

- CLI `run` and REPL now use the provider-neutral host result boundary.
- Linked source files are supported by `submit_path()` and `run_path()`.
- OpenQASM emission and QPU submit reservation remain unchanged.
- Provider SDK submission, retries, cancellation guarantees, and sessions are
  deferred to LISS-0016 and future follow-up issues.
