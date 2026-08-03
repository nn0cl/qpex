# ADR 0116: Classical Type-First quantities with State arithmetic

## Status

**Accepted** (2026-07-31) — architecture for [LISS-0133](../documentation-compression-map.md).

Extends [ADR 0114](0114-classical-coefficient-elaboration-vs-linear.md) and
[ADR 0037](0037-type-first-dimensions-structured-units.md).

## Decision

1. Type-First quantity heads (`Mass`, `Time`, `Delta<Time>`, … already listed in
   `ELABORATION_COEFFICIENT_HEADS`, plus `Delta<…>`) are **Classical** carriers:
   not linear Joint coordinates.
2. Unit literals may initialize those Classical heads when dimensions match.
3. Classical quantities may scale `State` values via `*` / `/` with dimensional
   algebra; the result remains `State` (Never Leave the State).
4. Explicit `State<Qty>` remains the linear form when the quantity itself is a
   mid-program quantum coordinate.

## Verification

`tests/test_expression_residuals_red.py`.
