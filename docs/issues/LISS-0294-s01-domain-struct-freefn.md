# LISS-0294: S01 domain packs as struct + free-fn scores

## Metadata

- Local issue ID: LISS-0294
- Status: **complete** (2026-08-03)
- Type: Feature examples + Kernel residual (nested classical free-fn)
- Priority: P1
- Depends: LISS-0292 **complete**, LISS-0293 **complete**
- Branch: `feature/liss-0294-s01-domain-struct-freefn`
- Parents: WP-0089 residual demotion (roads / shelters / morning / recovery /
  requests / hazards)

## Summary

Demote remaining pure S01 domain packs from `class` methods to **struct +
free-fn scores**, reusing LISS-0292 classical free-fn object args.

Kept as `class` (true systems / drive): `RescueSquad`, `SupplyTruck`,
`Lattice`, `ConstraintDrive`, and similar.

## Kernel residual (same branch)

Nested classical free-fn evaluation and free-fn param shadowing of outer
object names were incomplete after LISS-0292:

1. Thread caller `assign` into nested classical free-fn arg bind.
2. Prefer free-fn local objects over `self.objects` for Attr field reads.

Sibling free-fn calls across selective import were a residual of ADR 0177
linkage; LISS-0294 initially inlined leaf math. **Fixed by LISS-0295**
(transitive free-fn link under selective import); domain scores may nest
sibling free-fns again.

## Domain demotions

| Pack | Shape |
|---|---|
| `roads` | `RoadEdge` / `CorridorMap` struct; `corridor_open_score`, `blockage_pressure` |
| `shelters` | `ShelterSite` / `ShelterBoard` struct; `total_remaining`, `shelter_pressure_tag`, … |
| `morning` | `MorningObservation` struct; `readiness_for_day2`, `morning_tag` |
| `recovery` | `RecoveryItem` / `RecoveryQueue` struct; `queue_pressure`, … |
| `requests` | `FieldRequest` / `RequestBoard` struct; `total_people`, `fairness_proxy` |
| `hazards` | `HazardCell` / `HazardBoard` struct; `secondary_pressure`, … |

Spine / morning / day2 mains call free-fns and import score names.

## Exit

- [x] Domain packs demoted
- [x] Mains updated
- [x] Nested free-fn Kernel residual + unit tests
- [x] seed-0: `main_disaster_response`, `main_morning_collect`,
  `main_day2_recovery` (+ other S01 mains smoke)
