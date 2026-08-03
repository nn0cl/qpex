# LISS-0318: Host zone masses → finite tonight plan bridge

## Metadata

- Local issue ID: LISS-0318
- Status: **complete** (2026-08-03)
- Type: Feature Host H→E bridge (no Kernel Continuous)
- Priority: P3 expressiveness honesty (Adjudicator「1」)
- Depends: LISS-0317 field compose inject
- Branch: `feature/liss-0318-zone-feed-tonight-plan`
- Code: `host/field_compose_to_tonight_plan.py`

## Intent

Close the “next: feed zone masses…” gap: map CH-field-compose zone inject
atoms to ConstraintCoeffs-shaped floats and run a thin finite E-lane plan
sample, emitting a JSON envelope for audit.

## Honesty

- Does **not** rewrite `main_disaster_response.sqx` desk packs
- Does **not** claim full OS spine is driven by Continuous
- Shows causal map: Host compose → coeffs → evolve → `measure`

## Exit

- [x] zone → coeffs mapping
- [x] thin E-lane run + envelope JSON
- [x] docs + README causal row
- [x] runnable demo
