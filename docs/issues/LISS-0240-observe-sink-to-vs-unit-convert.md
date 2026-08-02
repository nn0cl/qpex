# LISS-0240: `measure`/`snapshot` `to <sink>` vs unit convert

## Metadata

- Local issue ID: LISS-0240
- Status: **complete**
- Type: bug
- Priority: P0
- Program: [WP-0086](../work-plans/WP-0086-spec-verification-ci.md)
- ADRs: [0029](../architecture/adr/0029-host-io-boundary-measure-sink.md),
  [0124](../architecture/adr/0124-si-scale-conversion-explicit.md)

## Intent

Statement-level `to <sink>` after `measure`/`snapshot` must not be parsed as
ADR 0124 `UnitConvert`.

## Exit

- [x] `snapshot x to stdout` parses and runs
- [x] `measure x to stdout` does not TYPE_MISMATCH as unknown unit
- [x] Ordinary `expr to unit` still parses
