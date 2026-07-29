# LISS-0116: Equation / Unit DTO

## Metadata

- Local issue ID: LISS-0116
- Status: **complete** — Slices A–C (Agent A, 2026-07-29)
- Phase: Feature Path / Issue completion (pending merge)
- Type: language / IR DTO
- Priority: P0
- Planning size: M
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on: LISS-0081 A–D + E Phase 1 accepted (structural Physics IR on `main`)
- Blocks: full Equation consumption in [LISS-0115](LISS-0115-hir-physics-ir-lowering.md);
  Equation-shaped goldens in [LISS-0117](LISS-0117-source-backed-physics-ir-goldens.md)
- Related branch: `feature/liss-0116-slice-a`
- Parallelism: Agent slot **A** (this agent) —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)
- Related: [physics-ir plan](../specs/staqex-v1-physics-ir-plan.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081. **Not** LISS-0076 body-phase
residuals ([LISS-0118](LISS-0118-body-phase-typing-residuals.md), complete).
Agent A owns exclusive paths below; LISS-0115 A–B is a parallel agent.

## Motivation — implementation gap

On `main`, [`compiler/staqex/physics_ir.py`](../../compiler/staqex/physics_ir.py)
had **zero** `Equation` / `Coefficient` / `Unit` DTOs. This Issue adds them in
an owned module without editing the frozen core.

## In scope

- Immutable DTOs: `EquationNode`, `Coefficient`, `Unit`, `(L,M,T)` tags
- Module-local verifier (`PHYSICS_EQUATION_*`, non-compile-hard)
- Tests under `tests/test_physics_equation_*.py`
- Docs/catalog cross-links (Slice C)

## Exclusive write paths (Agent A)

| Path | Role |
|---|---|
| `compiler/staqex/physics_equation.py` | Equation/Coefficient/Unit DTOs + verify |
| `tests/test_physics_equation_*.py` | Red/Green |

**Read-only:** `compiler/staqex/physics_ir.py` (frozen).

## Out of scope

- HIR lowering / `compile_source` (LISS-0115)
- Source-backed goldens (LISS-0117)
- Re-export into `physics_ir.py` without integration approval
- Full SI conversion beyond `(L,M,T)` tags

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | `Coefficient`, `Unit`, dimension tags | **complete** |
| **B** | `EquationNode` sides/dynamics + verifier | **complete** |
| **C** | Docs/catalog cross-links | **complete** |

### Shipped

- [`compiler/staqex/physics_equation.py`](../../compiler/staqex/physics_equation.py)
- [`tests/test_physics_equation_slice_a_red.py`](../../tests/test_physics_equation_slice_a_red.py)
- [`tests/test_physics_equation_slice_b_red.py`](../../tests/test_physics_equation_slice_b_red.py)

## Adjudicator Decision Points

- [x] Approve Issue body / plan intake — “0116 を進めて”
- [x] Authorize Slice A Red / Green — “承認”
- [x] Continue Slice B (+ C closeout) — “続けて承認”
- [x] Approve Issue completion / merge PR
