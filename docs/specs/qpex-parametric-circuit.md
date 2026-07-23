# QPex Parametric Circuit specification

| Field | Value |
|---|---|
| Status | **Proposed acceptance specification** (2026-07-23) |
| Decision | [ADR 0070](../architecture/adr/0070-parametric-circuit.md) |
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
