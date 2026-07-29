# Staqex Dynamic QPU lane specification

| Field | Value |
|---|---|
| Status | **Accepted rejection/capability boundary; execution follow-up remains open** (2026-07-24) |
| Decision | [ADR 0071](../architecture/adr/0071-dynamic-qpu-lane.md) |
| Issue | [LISS-0028](../issues/LISS-0028-dynamic-qpu-lane.md) |

This lane is intentionally separate from the Static Hilbert Kernel.

Required future contracts:

- explicit mid-circuit measurement semantics;
- classical feed-forward/control values;
- timing and qubit-reuse semantics;
- target capability profile and explicit unsupported-feature errors;
- simulator/QPU equivalence at the observable JobResult boundary.

No dynamic syntax or provider capability is accepted by this document yet.
