# LISS-0235: Kernel `RngPort` — Red (ship ADR 0170)

## Metadata

- Local issue ID: LISS-0235
- Status: **complete**
- Phase: phase-3-refactor (no behavior change beyond Green)
- Type: feature
- Priority: P1
- Planning size: M
- Program: [WP-0082](../work-plans/WP-0082-kernel-rng-port.md)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md) (**Accepted**)
- Ship ADR: [0170](../architecture/adr/0170-ship-kernel-rng-port.md) (**Accepted**)
- Depends on: WP-0082 execution batch
- Blocks: LISS-0236 / LISS-0237

## Intent

Introduce `RngPort` + default `random.Random` adapter for Kernel `measure`
sampling. Seeded outputs must remain bit-identical. Stay separate from
`HostRngPort`.

## Exit

- [x] Port + adapter + evaluator injection
- [x] Bit-identical `--seed 0` / suite output proof (diff)
- [x] No `random.Random(...)` constructed inside evaluator after Green
- [x] Full `pytest tests/` green (1073 passed)

## Non-goals

`MeasureSinkPort`, `SourcePort`, Host RNG unification, network/datastore.
