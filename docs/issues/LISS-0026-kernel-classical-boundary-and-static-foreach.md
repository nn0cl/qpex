# LISS-0026: Kernel classical boundary and static `forEach` (historical slice)

## Metadata

- Local issue ID: LISS-0026
- Status: Complete (historical bounded `register(N)` static-elaboration slice;
  superseded final surface is `QubitRegister<N>` in LISS-0029)
- Phase: Feature Path → Phase 3 Refactor reviewed and accepted
- Type: language semantics / QPU boundary / compile-time elaboration
- Priority: P0
- Related: ADR 0065, ADR 0069, LISS-0016, LISS-0019, LISS-0022

## Problem

The QPU lane should not look like a classical host program. Raw `Int`, `Float`,
and runtime loop control currently have no explicit boundary in the language
design. A user needs a concise way to apply the same operation to a known set
of wires without seeing bookkeeping indices or accidentally introducing
measurement-dependent control.

## Acceptance specification

- [x] QPU-lane Kernel values are limited to the accepted quantum/state surface
      and explicitly permitted parameter forms.
- [x] `Host<T>` is documented as a Host API boundary type, not a Kernel runtime
      value and not a provider SDK type.
- [x] `forEach` over a statically known register/wire collection is specified
      as deterministic pre-submission elaboration.
- [x] The bound `forEach` element is opaque to user arithmetic and can be used
      as a gate/operator target.
- [x] Measurement-dependent, unbounded, or dynamically sized iteration is
      rejected in the QPU lane with a stable diagnostic category.
- [x] Host code may choose static inputs and submit a Job, but no provider
      scheduling or polling syntax enters QPex source.
- [ ] Expansion order and resource-limit behavior are specified before codegen
      implementation.
- [x] CPU simulation and existing Kernel semantics remain one language
      semantics; no hidden host fallback is introduced.

## Non-goals

- Provider SDK, credentials, authentication, retry, session, or cloud Job
  implementation.
- Dynamic circuits or measurement-dependent classical feed-forward.
- A general-purpose classical collection library inside the QPU lane.
- Choosing the final register declaration syntax or QPU IR representation.

## Dependencies

- ADR 0065 / LISS-0022: Job-oriented Host execution boundary.
- LISS-0016: host-side provider submission.
- LISS-0019: concrete QPU IR.
- Existing `measure` terminal-collapse rule and OpenQASM emission.

## Review questions

1. Is the opaque element handle sufficient for all first-wave gate and
   Hamiltonian examples?
2. Should static shape be a register declaration, a type parameter, or a host
   submission setting?
3. What expansion limit and diagnostic should protect users from accidental
   circuit blow-up?
4. Are parameterized gates a separate `Host<T>` boundary or a QPU parameter
   surface with its own type?

## Verification direction

Phase 1: `tests/test_kernel_classical_boundary_red.py` contains parser,
typechecker, elaboration, and codegen contract tests in Red only. The fixture
uses `register(3)` as a deliberately visible provisional spelling; the
register declaration surface remains a review question and may change before
Phase 2.

## Phase 1 record

- Status: **Red complete**.
- Four tests fail as intended against the current Kernel.
- No production implementation or existing test was changed.
- Deterministic verification: manual test invocation confirmed 4/4 expected
  failures; `git diff --check` passed.

## Phase 2 record

- Status: **Green complete**.
- Added `forEach` AST/parser support with `register(N)` static-bound checking.
- Added opaque wire-handle checking and Kernel `Host<T>` rejection.
- Added deterministic expansion to the Python evaluator and OpenQASM lowering.
- Verification: all `tests/test_*.py`, SV 164/164, QASM codegen, a direct
  `run_source` static-register execution, and `git diff --check` passed.

## Phase 3 record

- Status: **Complete for the bounded `register(N)` static-elaboration slice**.
- Refactored QASM lowering into named static-register and body-extraction
  helpers.
- Added official teaching example 17 and registered it in SV-09; total SV is
  now 165/165.
- Updated the language/type-system and examples documentation with the
  Host/QPU boundary and opaque wire-handle explanation.
- Deferred follow-up remains: final register declaration syntax, expansion
  resource limits, parameterized QPU values, and dynamic-circuit support.

## Final review record

- Adjudicator approval: Phase 3 Refactor accepted (2026-07-23).
- Implementation permission was limited to the bounded `register(N)` slice;
  no provider SDK, credentials, or dynamic-circuit behavior was added.
- Follow-up architecture questions remain open under ADR 0069 and do not
  invalidate this bounded-slice completion.

Phase 2: static elaboration and diagnostics with no provider dependency.

Phase 3: examples and teaching documentation, followed by full unit/SV/QASM
verification.
