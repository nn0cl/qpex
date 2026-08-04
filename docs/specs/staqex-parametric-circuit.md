# Staqex Parametric Circuit specification

| Field | Value |
|---|---|
| Status | **Accepted boundary specification; QPU binding follow-up remains open** (2026-07-24) |
| Decision | [ADR 0070](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) |
| Issue | [LISS-0027](../issues/LISS-0027-parametric-circuit.md) |

`Param<T>` is a symbolic circuit parameter. It is not a Host value and not a
`State<T>` coordinate.

Normative direction:

- `Param<Angle>` may be passed to parameterized unitary gates.
- Parameter expressions cannot control register shape, `forEach`, branching,
  measurement, or termination.
- Host submission binds concrete values before Job submission.
- Binding and unit/domain validation occur outside the Kernel semantics and
  before provider execution.
