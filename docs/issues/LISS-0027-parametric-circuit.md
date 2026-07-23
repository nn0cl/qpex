# LISS-0027: Parametric Circuit boundary

## Metadata

- Local issue ID: LISS-0027
- Status: Open
- Phase: Architecture Path accepted; pending Phase 1 Red approval
- Type: QPU IR / symbolic parameter semantics
- Priority: P1
- Related: ADR 0069, ADR 0070, LISS-0019, LISS-0016

## Acceptance specification

- [x] `Param<T>` is distinct from `Host<T>` and `State<T>`.
- [x] `Param<Angle>` can be used in an explicitly parameterized gate argument.
- [x] Parameters cannot control register shape, `forEach`, branching,
      measurement, or termination.
- [ ] Host binding validates all values before Job submission.
- [ ] OpenQASM/QPU IR preserves symbolic parameters without provider SDKs in
      the Kernel.
- [ ] Parameter domain, units, and invalid-value diagnostics are specified.

## Non-goals

- VQE/QAOA implementation, automatic differentiation, or optimizer selection.
- Provider SDK, credentials, retry, or Job implementation.

## Phase 1 record

- Status: **Red complete; awaiting Phase 2 Green approval**.
- Test file: `tests/test_static_parametric_dynamic_boundaries_red.py`.
- The test uses provisional `Param<Angle> theta = parameter("theta")` syntax;
  final declaration and binding syntax remain reviewable before Phase 2.

## Phase 2 record

- Status: **Green complete; awaiting Phase 3 Refactor approval**.
- `Param<T>` declarations and gate-argument acceptance are implemented at the
  type boundary; shape/control use remains rejected.
- Verification: all unit tests and SV 165/165 passed.

## Phase 3 record

- Status: **Complete for the type/diagnostic boundary; follow-up open**.
- Added physicist-oriented lane documentation and clarified that symbolic
  parameters are gate data, not state or Host runtime values.
- Remaining: concrete QPU IR parameter nodes, Host binding validation, and
  provider-neutral OpenQASM parameter emission.
