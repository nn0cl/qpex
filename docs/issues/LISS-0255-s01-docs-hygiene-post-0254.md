# LISS-0255: S01 docs hygiene after ADR 0173/0174 and LISS-0254

## Metadata

- Local issue ID: LISS-0255
- Status: **complete** (2026-08-02)
- Type: Fast Path / docs
- Priority: P1
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Intent

Sync documentation that still claims pre-heal state after main landed:

- ADR 0173 + LISS-0250–0252 (`tracing_out`) **complete**
- ADR 0174 + LISS-0254 (Type-First field units) **complete**

Stop agents and humans from treating “0254 pending” / “LINEAR needs-ADR” as current truth.

## Exit

- [x] `docs/specs/staqex-v1-s01-coverage-scorecard.md`
  - Residuals: LISS-0254 **complete** (not Phase pending)
  - Type-First row notes reflect field unit retention shipped
  - LINEAR row remains `tracing_out` (already); remove contradictory “ritual only” if any
- [x] `docs/collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md`
  - P0 LINEAR / Type-First marked **Resolved** with ADR links
  - Follow-ups table status columns updated
- [x] `docs/issues/LISS-0245-…` status line consistent with triage + E1 + R3 + ADR heals
- [x] Redesign sketch exit checklist ticks for landed items + WP-0087 residual
- [x] No `.sqx` behavior changes

## Non-goals

- Spine causal rewrite (LISS-0256)
- New ADR content (LISS-0258)
- Scorecard row deletion

## Verification

- `git diff --check` on touched docs
- Grep residuals for “0254” / “pending” / “needs-ADR” on LINEAR/Type-First should not contradict main
