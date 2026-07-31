# ADR 0124: Explicit SI scale conversion (`expr to unit`)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0156 under WP-0038.
Companions: [ADR 0121](0121-si-base-dims-current-temperature.md); ADR 0037.

## Decisions

1. Bare unit suffixes (`.ms`, `.nm`, `.GHz`, …) keep **raw magnitude** + Dim
   (backward compatible with ADR 0121 honesty).
2. Explicit conversion uses the existing contextual keyword `to`:
   `Time t = 5.0.ms to s`.
3. MVP scale pairs (source → canonical):
   - `ms → s` (×10⁻³)
   - `nm → m` (×10⁻⁹)
   - `GHz → Hz` (×10⁹)
4. Source and target must share the same Dim; target must be a known
   `UNIT_TABLE` suffix. Mismatched Dim → `DIMENSION_MISMATCH_ERROR`.
5. Mixed-unit `+`/`-`: when both sides have known suffixes in the same
   canonical family, **promote to that canonical** then operate
   ([ADR 0155](0155-mixed-unit-canonical-promote.md)). Explicit `expr to unit`
   remains available. Incompatible families still error.

## Consequences

- AST `UnitConvert`; typecheck/evaluator apply `UNIT_SCALE` factors.
- Unsupported pairs → hard diagnostic (no silent identity).

## Deferred

°F catalog history; broader SI beyond ADR 0129/0132/0134–0136. (Implicit
mixed-unit arithmetic: **shipped** as canonical promote in ADR 0155.)
