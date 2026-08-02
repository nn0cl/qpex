# LISS-0277: S01 domain struct-first demotion

## Metadata

- Local issue ID: LISS-0277
- GitHub issue: _(none yet)_
- Status: **complete** (2026-08-03)
- Phase: Feature examples
- Type: Feature Path
- Priority: P0
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md); coordinate with [LISS-0276](LISS-0276-s01-import-use-lane-adoption.md)
- Paths: `examples/showcase/S01_quantum_disaster_response/domain/**`, consumers in mains/physics/protocol

## Summary

Apply Accepted struct-first teaching (LISS-0268 / harmony): pure parameter packs
become `struct` (or free constants); retain `class` where required by physics
systems, Type-First method carriers, nested boards, or capability interfaces.

## Final inventory (2026-08-03)

### Struct (leaf packs — no nested object construction)

| Type | File |
|---|---|
| `CommandBoard` | ops.sqx (+ free `phase_tag` / `phase_bump`) |
| `FairnessReport` | comms_ops.sqx (+ free `fairness_score`) |
| `RationTicket` | rations.sqx |
| `FieldRequest` | requests.sqx |
| `HazardCell` | hazards.sqx |
| `PlanWindow` | protocol/windows.sqx (field access) |
| `PriorityPipe` | protocol/compose.sqx |
| `RouteBoard` | physics/interference.sqx (+ free tags) |
| `HonestyDossier` | provenance/honesty.sqx |
| `ConstraintCoeffs` | physics/constraint_h.sqx (pre-existing) |

### Class (keep — honest reasons)

| Type | Reason |
|---|---|
| `Quantities`, `RoadEdge`, `CorridorMap`, `ShelterSite`, `ShelterBoard`, `MorningObservation`, `RecoveryItem`, `RecoveryQueue`, `CommsCell` | Type-First fields; free-fn Call does not bind dimensioned carriers today |
| `RequestBoard`, `HazardBoard` | Nested pack construction: **struct-in-struct fails** in Kernel; class board holds struct leaves |
| `ConstraintDrive`, `Lattice` | Build `Operator` / Hamiltonian — physical systems |
| `RescueSquad`, `SupplyTruck` | Capability `interface` / `impl` receivers |

### Free constants (no class theatre)

| | |
|---|---|
| Theatre scale | free fns in theatre_scale.sqx (`mean_cell_population`, …) |

## Kernel limits recorded (not sample bugs)

1. Free function Call with Type-First field object → `unbound coordinate` on param bind  
2. Nested `struct` construction `Board(leaf, leaf)` → `unbound variable` on leaf  
3. Class board + struct leaves **works**

These may become sugar Issues under WP-0089 (e.g. named struct / call bind) later.

## Exit

- [x] Inventory with struct vs keep-class rationale  
- [x] Convert pure leaf packs to `struct`  
- [x] Keep class only with documented reasons  
- [x] Call sites updated; all S01 mains seed-0 green  
- [x] No Joint spine outcome change intended  

## Verification

```bash
for f in examples/showcase/S01_quantum_disaster_response/main_*.sqx; do
  python3 -m compiler.staqex run "$f" --seed 0
done
python3 tests/spec_verification/run_all.py
```
