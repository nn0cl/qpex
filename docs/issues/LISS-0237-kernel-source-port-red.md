# LISS-0237: Kernel `SourcePort` — Red (follow-on)

## Metadata

- Local issue ID: LISS-0237
- Status: **proposed** (not in WP-0081 first batch)
- Phase: phase-0-design / backlog
- Type: feature
- Priority: P2
- Planning size: S
- Program: [WP-0081](../work-plans/WP-0081-0165-0166-red-intake.md) (sequenced after LISS-0236)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md)
- Blocked by: [LISS-0236](LISS-0236-kernel-measure-sink-port-red.md)

## Intent

Place `SourcePort` below `load_module_graph` so the linker requests path
contents through the port (ADR 0166). Requires its own ship authorization /
batch.

## Non-goals

Replacing ADR 0054 module graph logic; RngPort / MeasureSinkPort work.
