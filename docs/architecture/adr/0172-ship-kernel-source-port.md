# ADR 0172: Ship Kernel `SourcePort` (third slice of ADR 0166)

## Status

**Accepted** (2026-08-02) — [WP-0084](../../work-plans/WP-0084-kernel-source-port.md)
/ [LISS-0237](../documentation-compression-map.md)
Adjudicator「はい」after WP-0083 post-review (Accept 0172).

## Context

[ADR 0166](0166-kernel-external-resource-ports.md) (**Accepted**) requires
program source loading behind `SourcePort`, sitting **below**
`load_module_graph` so the linker requests path contents through the port
without replacing ADR 0054 module graph logic. `RngPort` (0170) and
`MeasureSinkPort` (0171) already shipped.

## Dependency Adoption Evidence

Not applicable. Default adapter wraps filesystem UTF-8 reads.

## Decision

1. Authorize Feature Path AT-TDD for [LISS-0237](../documentation-compression-map.md)
   to introduce `SourcePort` + default filesystem adapter and inject it into
   `load_module_graph` / `_parse_file` (and `module-info.sqx` reads used by
   the linker).
2. **Do not** replace ADR 0054 import resolution, merge, or visibility rules.
3. Path existence / `rglob` discovery may remain filesystem probes in this
   ship; content reads go through the port.
4. **Determinism is binding** for seeded run outputs that load via
   `compile_path` / CLI file entry (`--seed 0` pin).
5. CLI migrate helpers and unrelated `Path.read_text` call sites outside the
   module linker remain out of scope unless they are on the
   `load_module_graph` path.

## Consequences

Positive: closes the third External-Resources contract gap; source text
becomes substitutable under the linker.

Negative: linker construction sites gain an optional port parameter.

## Enforcement

Code review should reject ADR 0054 logic rewrites, datastore/network adapters,
and seeded stdout reshaping without an Adjudicator ruling.
