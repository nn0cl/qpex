# LISS-0218: Kernel RNG, measurement sink, and source loading are not behind ports (design)

## Metadata

- Local issue ID: LISS-0218
- Status: **complete** — 2026-08-01 (WP-0078 design; Red separate)
- Phase: phase-0-design
- Type: design
- Priority: P1
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Design ADR: [0166](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md) **Proposed**
- Related: ADR 0161 / LISS-0194 (`CredentialPort`, the pattern to follow)

## Intent

`CLAUDE.md` §External Resources Must Be Ports requires that the entropy source,
program source loading, and the measurement / diagnostic sink each be
represented as a port before a concrete implementation is used. None of the
three exists. The Kernel reaches for the concrete resource directly.

This is a standing violation of the project's own architecture contract, found
during the 2026-08-01 operations review.

## Evidence (verified 2026-08-01)

| Required port | Contract text | Actual |
|---|---|---|
| `RngPort` | "Entropy / RNG source (for `measure` sampling) via `RngPort`" | `runtime/evaluator.py` takes a raw `random.Random \| None` and constructs `random.Random(seed)` / `random.Random()` directly |
| `MeasureSinkPort` | "Measurement / diagnostic sink (stdout, stderr, or files) via `MeasureSinkPort`" | `stdlib/io_ops.write_sink` is called directly from the evaluator; `inspect_sink` is a raw `TextIO` |
| `SourcePort` | "Program source loading (file or stdin) via `SourcePort`" | `pipeline.compile_path` / `modules.load_module_graph` read the filesystem directly |

Ports that *do* exist and show the intended shape: `CredentialPort` +
`EnvCredentialAdapter` (`credentials.py`), `HostRngPort` + `HostRngAdapter`
(`host_monte_carlo.py` — Host-side Monte Carlo only, not Kernel `measure`),
`SimulatorPort`, `ObservationExecutionPort`, `PhysicalTargetPort`.

Note `HostRngPort` already exists but does not cover Kernel `measure` sampling,
so the two entropy paths are currently governed differently.

## Design questions (Architecture Path)

1. Port shape. Does `RngPort` expose raw uniforms, or measurement-level
   sampling? The seeded-determinism guarantee that every suite and every
   `--seed 0` example depends on must be preserved exactly — a reshuffle of RNG
   call order changes published outputs.
2. Should `HostRngPort` and the new `RngPort` unify, or stay separate because
   Host Monte Carlo and Kernel `measure` are different lanes?
3. `MeasureSinkPort` vs the existing `inspect_sink` `TextIO` and the Host
   `MeasurementEnvelope` / `JobResult` DTOs — is the sink a Kernel port, or is
   the Host boundary already the right seam?
4. `SourcePort` interacts with the ADR 0054 module linker. Does the port sit
   above or below `load_module_graph`?
5. Slice order — three ports is too much for one Red. Which is first?
   (Recommendation: `RngPort`, because it is the one the contract names first
   and the one with a determinism obligation worth pinning.)

## Non-goals (this Issue)

- Kernel implementation or AT-TDD Red
- Adding a datastore, network, or provider adapter (MVP boundary stands)
- Changing `measure` semantics or seeded output values

## Exit (design)

- [x] Port interfaces drafted with the determinism obligation stated
- [x] Relationship to `HostRngPort` decided
- [x] Slice order agreed
- [x] Ship ADR proposed only after the interfaces are accepted
- [x] No Kernel change in this Issue

## Resolution (WP-0078)

Accepted [ADR 0166](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md)
with locks: `RngPort` first; separate from `HostRngPort`; `MeasureSinkPort` is
a Kernel port; `SourcePort` below `load_module_graph`; bit-identical seeds.

Ship requires a **separate** Feature Path Issue before Red.
