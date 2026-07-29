# LISS-0117: Source-backed Physics IR goldens

## Metadata

- Local issue ID: LISS-0117
- Status: **complete** — Slices A–C (Agent C, 2026-07-29)
- Phase: Feature Path / Issue completion (pending merge)
- Type: conformance / golden tests
- Priority: P1
- Planning size: M
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on:
  - LISS-0081 fixture catalog
  - [LISS-0115](LISS-0115-hir-physics-ir-lowering.md) Slice C on `main`
  - [LISS-0116](LISS-0116-equation-unit-dto.md) **complete**
- Related branch: `feature/liss-0117-slice-c`
- Parallelism: Agent slot **C** —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081 Slice E.

## Exclusive write paths (Agent C)

| Path | Role |
|---|---|
| `compiler/staqex/physics_ir_goldens.py` | golden load/compare |
| `tests/fixtures/physics_ir/**` | fixtures |
| `tests/test_physics_ir_goldens_*.py` | Red/Green |
| `docs/specs/staqex-v1-physics-ir-golden-catalog.md` | promotion / status rows |

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Fixture layout + loader | **complete** |
| **B** | Wire loader to LISS-0115 lower (≥1 family) | **complete** |
| **C** | Equation/Unit assertions + catalog evidence rows | **complete** |

### Shipped

- [`compiler/staqex/physics_ir_goldens.py`](../../compiler/staqex/physics_ir_goldens.py)
- [`tests/fixtures/physics_ir/`](../../tests/fixtures/physics_ir/)
- [`tests/test_physics_ir_goldens_slice_{a,b,c}_red.py`](../../tests/)
- Catalog: oscillator **lowered-IR evidence**; global status still
  **not a promoted runtime oracle**

## Adjudicator Decision Points

- [x] Approve Issue body / plan intake
- [x] Authorize Slice A Red / Green / ship
- [x] Continue Slice B after 0115 C on main
- [x] Approve Slice B ship
- [x] Approve Slice C (Equation/Unit + catalog evidence) — Adjudicator “承認”
- [x] Confirm full six-family public oracle remains deferred (partial promotion only)
- [x] Approve Issue completion / merge PR
