# ADR 0186: Display-unit restore after mixed-unit promote

## Status

**Accepted** (2026-08-03) — Adjudicator residual continue after LISS-0313;
reopens [LISS-0197](../documentation-compression-map.md).
Amends [ADR 0155](0155-mixed-unit-canonical-promote.md) Decision 2 (result unit).

Feature: [LISS-0314](../documentation-compression-map.md).

## Context

ADR 0155 promotes mixed-unit `+`/`-` to the **canonical** magnitude and leaves
the result tagged with the canonical unit (e.g. `1.g + 1.kg` → `1.001` `kg`).
Physicists often want the sum expressed in the **left-hand** unit they started
with (`1001.g`), without a second `to g` rewrite. Explicit `expr to unit`
already sets display; restore is the default for mixed shared-family promote.

## Dependency Adoption Evidence

Not applicable — extends existing unit tables / promote path.

## Decision

1. When `+`/`-` (or relational prep using the same promote) has **both**
   operands with known units in the **same canonical family** and the units
   **differ**, compute in canonical space (unchanged), then **restore** the
   numeric result into the **left-hand operand's unit** and tag the result
   with that LHS unit.
2. Same-unit operands remain unchanged (no force through canonical).
3. Explicit `expr to unit` still wins for that subexpression's unit tag.
4. Affine families (C/F/R/K) use inverse affine map for restore (not scale-only).
5. Incompatible pairs remain `UNIT_MIXED_ARITHMETIC_ERROR`.
6. Typecheck result unit for mixed shared-family promote is the **LHS unit**
   (not the canonical name).

## Non-goals

- RHS-preferred restore mode
- Auto-rescale on `*`/`/` beyond Dim algebra
- New unit suffixes
- Changing canonical promote arithmetic identity (only display unit + magnitude presentation)

## Consequences

- `1.0.g + 1.0.kg` → `1001.0` with unit `g` (was `1.001` `kg`).
- `1.0.kg + 1.0.g` → `1.001` with unit `kg` (unchanged presentation).
- `0.0.C + 32.0.F` → magnitude in `C` after K-space sum (not bare `K`).
- Agents must not invent dual restore policies without a new ADR.

## Implementation permission

Architecture + residual continue authorize Feature LISS-0314 Red→Green on this
branch.
