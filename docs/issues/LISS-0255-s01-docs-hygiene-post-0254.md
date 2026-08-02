# LISS-0255: S01 docs hygiene after ADR 0173/0174 and LISS-0254

## Metadata

- Local issue ID: LISS-0255
- Status: **open**
- Type: Fast Path / docs
- Priority: P1
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Branch (suggested): `docs/liss-0255-s01-docs-hygiene` or batch WP-0087

## Intent

Sync documentation that still claims pre-heal state after main landed:

- ADR 0173 + LISS-0250–0252 (`tracing_out`) **complete**
- ADR 0174 + LISS-0254 (Type-First field units) **complete**

Stop agents and humans from treating “0254 pending” / “LINEAR needs-ADR” as current truth.

## Exit

- [ ] `docs/specs/staqex-v1-s01-coverage-scorecard.md`
  - Residuals: LISS-0254 **complete** (not Phase pending)
  - Type-First row notes reflect field unit retention shipped
  - LINEAR row remains `tracing_out` (already); remove contradictory “ritual only” if any
- [ ] `docs/collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md`
  - P0 LINEAR / Type-First marked **Resolved** with ADR links
  - Inventory Action counts updated if still historical
- [ ] `docs/issues/LISS-0245-…` status line consistent with triage + E1 complete
- [ ] Optional: redesign sketch exit checklist ticks for landed items
- [ ] No `.sqx` behavior changes

## Non-goals

- Spine causal rewrite (LISS-0256)
- New ADR content (LISS-0258)
- Scorecard row deletion

## Verification

- `git diff --check` on touched docs
- Grep residuals for “0254” / “pending” / “needs-ADR” on LINEAR/Type-First should not contradict main
