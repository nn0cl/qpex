# LISS-0236: Kernel `MeasureSinkPort` — Red (ship ADR 0171)

## Metadata

- Local issue ID: LISS-0236
- Status: **complete**
- Phase: phase-3-refactor (no behavior change beyond Green)
- Type: feature
- Priority: P2
- Planning size: S
- Program: [WP-0083](../work-plans/WP-0083-kernel-measure-sink-port.md)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md) (**Accepted**)
- Ship ADR: [0171](../architecture/adr/0171-ship-kernel-measure-sink-port.md) (**Accepted**)
- Blocked by: [LISS-0235](LISS-0235-kernel-rng-port-red.md) (**complete**)
- Blocks: LISS-0237

## Intent

Wrap today’s `write_sink` / `inspect_sink` `TextIO` adapters behind
`MeasureSinkPort` per ADR 0166 / 0171.

## Exit

- [x] Port + TextIO / file adapters + evaluator emission
- [x] Bit-identical `--seed 0` B01 pin (`42\n`)
- [x] Custom `MeasureSinkPort` receives measure text
- [x] Full `pytest tests/` green
- [x] Host `JobResult` unchanged; no SourcePort

## Non-goals

Host `JobResult` seam changes; RngPort / SourcePort work.
