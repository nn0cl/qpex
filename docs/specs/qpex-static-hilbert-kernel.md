# Staqex Static Hilbert Kernel specification

| Field | Value |
|---|---|
| Status | **Accepted MVP specification; target-profile follow-up remains open** (2026-07-24) |
| Decision | [ADR 0069](../architecture/adr/0069-kernel-static-hilbert-space.md) |
| Issue | [LISS-0029](../issues/LISS-0029-static-hilbert-kernel-surface.md) |

## Normative direction

- `QubitRegister<N>` describes a compile-time logical tensor-product shape.
- `N` is not a runtime `Int` and cannot be measured, incremented, or used as
  Kernel control state.
- `State<T>` is the pre-measurement state over the system; `measure` remains
  the terminal observation boundary.
- `forEach` expands over logical register factors before backend emission.
- The element handle is opaque and cannot be converted to a classical index.
- Resource overflow is an explicit compile/lowering error; truncation is
  forbidden.
- The dependency-free MVP compiler safety budget is 1024 logical qubits,
  shared by type checking, local simulation, and QASM lowering. Target
  profile limits are not inferred from this value and remain backend work.

## Example direction

```staqex
QubitRegister<3> reg

forEach q in reg {
    apply(H, q)
}

measure reg
```

Declaration initialization, measurement result shape, and exact diagnostic
codes remain LISS-0029 review items. This example is not yet a conformance
fixture.
