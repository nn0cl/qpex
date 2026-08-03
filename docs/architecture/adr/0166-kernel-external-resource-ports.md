# ADR 0166: Kernel entropy, measurement sink, and source loading behind ports

## Status

**Accepted** (2026-08-01) — WP-0078 / [LISS-0218](../documentation-compression-map.md)
Adjudicator lock. Architecture / design approval only.

This ADR **does not authorize Kernel Red or implementation**. A separate ship
ADR (or Feature Path Issue with phase approval) is required before Phase 1.

## Context

`CLAUDE.md` §External Resources Must Be Ports requires these to be represented
as ports *before* a concrete implementation is used:

> - Entropy / RNG source (for `measure` sampling) via `RngPort`.
> - Program source loading (file or stdin) via `SourcePort`.
> - Measurement / diagnostic sink (stdout, stderr, or files) via `MeasureSinkPort`.

The 2026-08-01 operations review found that none of the three exists as Kernel
ports (raw `random.Random`, direct `write_sink` / `TextIO`, direct filesystem
reads). Host already has `HostRngPort` (ADR 0163) for Monte Carlo inject only.

## Dependency Adoption Evidence

Not applicable. These ports wrap the standard library and the filesystem; no
new dependency is selected.

## Decision

1. **Determinism is binding.** Seeded outputs (`--seed 0`, SV, suites) must be
   **bit-identical** before and after port introduction. The first ship Issue
   proves this by diffing published outputs, not by assertion alone.
2. **Slice order:** `RngPort` first; then `MeasureSinkPort`; then `SourcePort`
   (separate Issues / batches).
3. **`RngPort` and `HostRngPort` stay separate.** Kernel `measure` sampling and
   Host Monte Carlo are different lanes. Shared documentation of the seed
   contract is required; unification is out of the first ship.
4. **`MeasureSinkPort` is a Kernel port** wrapping today’s `write_sink` /
   `inspect_sink` `TextIO` adapters. Host `MeasurementEnvelope` / `JobResult`
   remain the Host seam (unchanged role).
5. **`SourcePort` sits below `load_module_graph`:** the linker requests path
   contents through the port; it does not replace ADR 0054 module graph logic.
6. **No new capability:** no datastore, network, or provider adapter. MVP
   boundaries in `CLAUDE.md` stand.
7. **Draft interface sketch (ship Issue owns final signatures):**
   - `RngPort.random() -> float` (or equivalent uniform) injected into the
     evaluator; default adapter wraps `random.Random(seed)`.
   - `MeasureSinkPort.write(text: str) -> None` (and/or structured measure
     lines); default adapter writes to the configured `TextIO`.
   - `SourcePort.read_text(path: str) -> str`; default adapter is filesystem /
     stdin as today.

## Consequences

Positive:

- Closes the standing External-Resources contract gap for the Kernel lane.
- Makes `measure` entropy substitutable in tests without evaluator internals.

Negative:

- Evaluator / pipeline construction sites change on ship.
- Determinism regressions are expensive — hence constraint 1.

## Enforcement

Code review should reject:

- Port adoption that changes seeded outputs without an explicit approved
  decision to do so.
- Constructing `random.Random` inside the evaluator after `RngPort` ships.
- Kernel Red started without a separate ship authorization.
- Network / datastore / provider adapters under cover of “it is a port now”.
- Unifying `HostRngPort` and `RngPort` in the first `RngPort` ship without a
  new Adjudicator ruling.
