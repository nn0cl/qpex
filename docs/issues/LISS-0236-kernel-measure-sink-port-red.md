# LISS-0236: Kernel `MeasureSinkPort` — Red (follow-on)

## Metadata

- Local issue ID: LISS-0236
- Status: **proposed** (not in WP-0081 first batch)
- Phase: phase-0-design / backlog
- Type: feature
- Priority: P2
- Planning size: S
- Program: [WP-0081](../work-plans/WP-0081-0165-0166-red-intake.md) (sequenced after LISS-0235)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md)
- Blocked by: [LISS-0235](LISS-0235-kernel-rng-port-red.md)

## Intent

Wrap today’s `write_sink` / `inspect_sink` `TextIO` adapters behind
`MeasureSinkPort` per ADR 0166. Requires its own ship authorization / batch.

## Non-goals

Host `JobResult` seam changes; RngPort / SourcePort work.
