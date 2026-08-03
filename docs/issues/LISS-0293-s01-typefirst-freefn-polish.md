# LISS-0293: S01 Type-First free-fn polish (post LISS-0292)

## Metadata

- Local issue ID: LISS-0293
- Status: **complete** (2026-08-03)
- Type: Feature examples
- Priority: P1
- Depends: LISS-0292 **complete**

## Summary

Use LISS-0292 so S01 domain packs that only convert Type-First fields are
**struct + free functions**, not class methods:

- `Quantities` → struct + `window_ms` / `water_plus_payload_g` / …
- `CommsCell` → struct + `priority_headroom`

Spine / day2 call sites updated; named struct construction preferred.

## Exit

- [x] Quantities free-fn conversions
- [x] CommsCell free-fn headroom
- [x] seed-0 spine + day2
