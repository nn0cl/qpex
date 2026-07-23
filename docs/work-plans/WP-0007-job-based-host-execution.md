# WP-0007: Job-based host execution

## Design status

Architecture approved; Phase 3 completed for the local CLI and Python host
boundary. Provider submission, retry policy, and session/batch migration remain
future work.

## [DESIGN CHECK]

- Scope and expected behavior: establish a provider-neutral Job/JobResult host boundary for local and future remote execution.
- Specifications and files inspected: ADR-0027/0029/0032/0064, ADR-0065 proposal, QPex language specification, runtime execution model, LISS-0015/0016, research note.
- Component boundaries, ports/adapters, and VO/DTO candidates: `JobPort`, `Job`, `JobStatus`, `JobResult`, `MeasurementEnvelope`; provider adapters implement the port; Kernel remains provider-free.
- Applicable constraints: no language-level Job API; no raw Joint/AST leakage; no provider dependency; AT-TDD phase gates.
- Decisions, assumptions, unresolved ambiguities: `Job` is the public vocabulary; exact state and envelope serialization remain open design questions.
- Included and omitted AI context: included only relevant contracts and research; omitted provider SDK code, credentials, unrelated language features, and generated reports.
- Task routing: strong reasoning for ADR/contract review; deterministic tools for tests and search; code assistant only after Green approval.
- Input/output evidence contract when AI output is involved: any generated contract must map to the reviewed scenarios; deterministic tests are the acceptance evidence.
- Verification plan: Phase 1 Red fake-adapter tests; later full SV/QASM and CLI regression.

## Sequence

1. Accept/revise ADR-0065 and the LISS-0022 specification.
2. Phase 1 Red tests.
3. Phase 2 Green minimum host DTO/port/adapter.
4. Phase 3 refactor and CLI/embedding migration.

## Phase 2 Green evidence

- Added `compiler/qpex/host.py` with local `Job`, `JobResult`, and
  `MeasurementEnvelope` DTOs.
- Added `submit_source()` and blocking `run_source()` host APIs.
- Provider-neutral result does not expose `Joint` or AST.
- `tests/test_job_host_contract_red.py`: 5/5 passed after implementation.
- Full spec verification: 164/164 passed.
- OpenQASM 3 codegen tests passed.
- Existing LISS-0021 `main -> Unit` Red test remains pending and was not altered.

## Phase 3 evidence

- Added linked-file `submit_path()` / `run_path()` host entry points.
- CLI `run` and REPL execution now consume `JobResult` through the Host
  boundary while preserving existing exit-code behavior.
- QPU mode remains OpenQASM emission only; no provider SDK was introduced.
- Repeated Job contract, capstone, SV, QASM, CLI, and whitespace checks pass.
- Reviewer empathy: the source language remains synchronous and measurement
  terminal; only the host-facing execution vocabulary changes to Job/Result.
