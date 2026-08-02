# LISS-0235: Kernel `RngPort` — Red (ship ADR 0170)

## Metadata

- Local issue ID: LISS-0235
- Status: **proposed**
- Phase: phase-1-red (when batch approved)
- Type: feature
- Priority: P1
- Planning size: M
- Program: [WP-0081](../work-plans/WP-0081-0165-0166-red-intake.md)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md) (**Accepted**)
- Ship ADR: [0170](../architecture/adr/0170-ship-kernel-rng-port.md) (**Proposed**)
- Depends on: ADR 0170 **Accepted** + batch approval
- Blocks: LISS-0236 / LISS-0237 (not in first batch)

## Intent

Introduce `RngPort` + default `random.Random` adapter for Kernel `measure`
sampling. Seeded outputs must remain bit-identical. Stay separate from
`HostRngPort`.

## Exit

- [ ] Port + adapter + evaluator injection
- [ ] Bit-identical `--seed 0` / suite output proof (diff)
- [ ] No `random.Random(...)` constructed inside evaluator after Green
- [ ] Full `pytest tests/` green

## Non-goals

`MeasureSinkPort`, `SourcePort`, Host RNG unification, network/datastore.
