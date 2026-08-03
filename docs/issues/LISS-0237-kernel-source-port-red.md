# LISS-0237: Kernel `SourcePort` — Red (ship ADR 0172)

## Metadata

- Local issue ID: LISS-0237
- Status: **complete**
- Phase: phase-3-refactor (no behavior change beyond Green)
- Type: feature
- Priority: P2
- Planning size: S
- Program: [WP-0084](../work-plans/WP-0084-kernel-source-port.md)
- Design ADR: [0166](../architecture/adr/0166-kernel-external-resource-ports.md) (**Accepted**)
- Ship ADR: [0172](../architecture/adr/0172-ship-kernel-source-port.md) (**Accepted**)
- Blocked by: [LISS-0236](LISS-0236-kernel-measure-sink-port-red.md) (**complete**)

## Intent

Place `SourcePort` below `load_module_graph` so the linker requests path
contents through the port (ADR 0166 / 0172).

## Exit

- [x] Port + filesystem adapter + `load_module_graph` / `compile_path` injection
- [x] `module-info.sqx` reads used by the linker go through the port
- [x] Custom SourcePort can override disk bytes for an existing path
- [x] Bit-identical `--seed 0` B01 pin (`42\n`)
- [x] Full `pytest tests/` green
- [x] ADR 0054 merge / visibility logic unchanged

## Non-goals

Replacing ADR 0054 module graph logic; RngPort / MeasureSinkPort work;
CLI migrate `Path.read_text` helpers outside the linker path.
