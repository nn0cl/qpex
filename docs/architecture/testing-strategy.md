# Testing Strategy

Testing follows AT-TDD phase gates.

Language-axiom AT-TDD (5 meta assertions, Spec Compliance Rate):  
[`docs/testing/staqex-spec-verification-protocol.md`](../testing/staqex-spec-verification-protocol.md)  
Runner: `python3 tests/spec_verification/run_all.py`

## Test Levels

### Acceptance Tests

Purpose:

- prove Gherkin scenarios.
- drive Phase 1 Red.

Placement:

- Kernel / use-case acceptance tests live as flat files at the `tests/` root,
  named `tests/test_<topic>_red.py` for Phase 1 Red (one file per Issue or
  Slice), with `_green.py` when a Green slice needs its own file.
- Language-axiom and spec-conformance suites live in
  `tests/spec_verification/`, driven by
  `python3 tests/spec_verification/run_all.py`.
- Shared program fixtures live in `tests/fixtures/` (Kernel PoC inputs under
  `tests/fixtures/poc/`).
- Individual suites run as plain scripts, for example
  `python3 tests/test_modern_oop_and_visibility.py`. CI aggregates root suites
  with `python3 -m pytest tests/ -q` (LISS-0209 / WP-0080); pytest is installed
  only in the CI job (and optionally a local `.venv`), not as a Kernel runtime
  dependency. Spec-verification remains
  `python3 tests/spec_verification/run_all.py` and is **not** part of the
  blocking CI gate in WP-0080.
- No UI acceptance tests: the MVP has no UI (`docs/architecture/README.md`
  "Selected Technology"). Adding one is an Architecture Path decision.
- E2E tests only after a runnable shell/deployment exists.

### Domain Unit Tests

Purpose:

- prove pure domain behavior.

Rules:

- no mocks needed for pure logic.
- no framework, DB, network, file-system, or SDK imports.

### Application Use Case Tests

Purpose:

- prove orchestration through ports.

Rules:

- use fake or mock port implementations.
- assert outputs and port interactions specified by Gherkin.
- no real adapters.

### Adapter Integration Tests

Purpose:

- prove concrete provider integration.

Rules:

- must be explicitly requested or covered by an ADR.
- must be separable from normal unit tests.
- must not be required for Phase 1 Red of core behavior.

### Dependency Policy Checks

Purpose:

- catch package dependency, license, advisory, and import-boundary drift.

Rules:

- run the project's chosen dependency-policy tool(s) once configured (see
  `docs/architecture/dependency-policy.md`).
- do not treat these checks as substitutes for Clean Architecture review.

### Front-End Tests

Purpose:

- prove UI behavior and user interaction.

Rules:

- Not applicable to the MVP: there is no UI framework
  (`docs/architecture/README.md` "Selected Technology"). Selecting a UI test
  framework is a technology-selection decision and requires Architecture Path.
- The remaining rules in this section apply only once a UI exists:
- mock the shared transport/API client boundary.
- do not mock random request strings inside components.

### E2E Tests

Purpose:

- prove the assembled app flow.

Rules:

- Not applicable to the MVP: the only runnable shell is the local CLI
  (`python3 -m compiler.staqex`), and no deployment target exists. Selecting an
  E2E framework is a technology-selection decision and requires Architecture
  Path.
- do not depend on real external providers unless the test is explicitly
  marked as manual or integration.

## Phase Mapping

Phase 1 Red:

- add failing tests only.
- prefer use-case tests for core behavior.
- prefer UI tests for presentation behavior.

Phase 2 Green:

- add minimum implementation.
- do not edit reviewed tests to pass.

Phase 3 Refactor:

- improve structure.
- keep behavior and assertions stable.

## Mocking Rule

Mock ports, not concrete providers.

Examples:

- mock `QpuSubmitPort` / `QpuJobPort` (`compiler/staqex/qpu_submit.py`), not a
  provider SDK client, credentials, or HTTP endpoint.
- mock `ObservationExecutionPort`
  (`compiler/staqex/observation_execution.py`), not a concrete simulator or
  device backend.
- mock the entropy, program-source, and measurement-sink ports required by
  `docs/architecture/README.md` "Ports", not the OS RNG, the file system, or
  stdout directly.
