# ADR 0171: Ship Kernel `MeasureSinkPort` (second slice of ADR 0166)

## Status

**Accepted** (2026-08-02) — [WP-0083](../../work-plans/WP-0083-kernel-measure-sink-port.md)
/ [LISS-0236](../documentation-compression-map.md)
Adjudicator「はい」after WP-0082 post-review (Accept 0171).

## Context

[ADR 0166](0166-kernel-external-resource-ports.md) (**Accepted**) requires
Kernel measurement / diagnostic emission behind `MeasureSinkPort`, wrapping
today’s `write_sink` / `inspect_sink` `TextIO` adapters, after `RngPort`
(shipped ADR 0170 / WP-0082). Design ADR forbids Red without a separate ship
authorization. Host `JobResult` / `MeasurementEnvelope` remain the Host seam.

## Dependency Adoption Evidence

Not applicable. Default adapters wrap stdlib `TextIO` and filesystem paths.

## Decision

1. Authorize Feature Path AT-TDD for [LISS-0236](../documentation-compression-map.md)
   to introduce `MeasureSinkPort` + default TextIO / file adapters and route
   Kernel `measure` / `snapshot` / `inspect` emission through the port.
2. **Determinism is binding:** seeded CLI / suite stdout must stay
   **bit-identical** before/after; prove with a pinned `--seed 0` example
   string, not assertion alone.
3. Do **not** change Host `JobResult` seams in this ship.
4. Do **not** implement `SourcePort` in this ship (LISS-0237).
5. Prefer that evaluator measure/snapshot paths emit via `MeasureSinkPort`
   rather than calling `Path.write_text` or raw stdout writes inline.

## Consequences

Positive: closes the second External-Resources contract gap; measure output
becomes substitutable in tests.

Negative: emission call sites change; newline / file overwrite behavior must
match today’s `write_sink` contract.

## Enforcement

Code review should reject Host seam changes, SourcePort work, and seeded
stdout reshaping without an Adjudicator ruling.
