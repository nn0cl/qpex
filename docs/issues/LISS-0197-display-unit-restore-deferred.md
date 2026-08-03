# LISS-0197: Display-unit restore after canonical promote (deferred)

## Metadata

- Local issue ID: LISS-0197
- Status: **superseded complete** (2026-08-03) — ship [ADR 0186](../architecture/adr/0186-display-unit-restore.md) / [LISS-0314](LISS-0314-display-unit-restore.md)
- Related: [ADR 0155](../architecture/adr/0155-mixed-unit-canonical-promote.md);
  [ADR 0156](../architecture/adr/0156-atomic-mass-and-ton-alias.md) (when merged)

## Intent

After mixed-unit `+`/`-` promote to canonical magnitudes, optionally restore
display units toward the left-hand operand's unit. Deliberately **out of** the
WP-0062…0066 ship batch.

## Non-goals

Kernel work until a dedicated ship ADR + Feature Path approval.
