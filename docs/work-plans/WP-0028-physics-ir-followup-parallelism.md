# WP-0028: Physics IR follow-up parallelism (LISS-0115–0117)

| Field | Value |
|---|---|
| Status | **active** — docs coordination for parallel agents |
| Date | 2026-07-29 |
| Parent | [WP-0025](WP-0025-staqex-v1-north-star.md) LISS-0081 |
| Issues | [LISS-0116](../issues/LISS-0116-equation-unit-dto.md),
  [LISS-0115](../issues/LISS-0115-hir-physics-ir-lowering.md),
  [LISS-0117](../issues/LISS-0117-source-backed-physics-ir-goldens.md) |
| Shipping Kernel | Python `compiler/staqex/` |

## 1. Purpose

Separate **working copies** (one branch / worktree per agent) while keeping
**source ownership exclusive** so parallel Feature Path work does not collide
on [`physics_ir.py`](../../compiler/staqex/physics_ir.py).

LISS-0081 A–D + E Phase 1 remains the frozen structural boundary on `main`.
Follow-ups do not mark LISS-0081 globally complete.

## 2. Implementation gap (locked)

| Gap | Evidence on `main` | Issue |
|---|---|---|
| No Equation/Coefficient/Unit DTOs | zero matching classes in `physics_ir.py` | LISS-0116 |
| Incomplete HIR lowering; no `compile_source` wire | minimal `build_physics_ir` only | LISS-0115 |
| No source-backed golden loader | catalog is fixture-only | LISS-0117 |

## 3. Agent slots and exclusive writes

| Slot | Issue | Branch pattern | Exclusive write | Forbidden |
|---|---|---|---|---|
| **A** | LISS-0116 | `feature/liss-0116-*` | `physics_equation.py`, `tests/test_physics_equation_*.py` | `physics_ir.py`, pipeline, goldens |
| **B** | LISS-0115 | `feature/liss-0115-*` | `physics_ir_lower.py`, `tests/test_physics_ir_lower_*.py` | equation DTO defs, golden tree, routine `physics_ir.py` / `pipeline.py` |
| **C** | LISS-0117 | `feature/liss-0117-*` | `physics_ir_goldens.py`, `tests/fixtures/physics_ir/**`, `tests/test_physics_ir_goldens_*.py`, golden catalog promotion rows | DTO/lower implementation |

**Frozen shared core:** `compiler/staqex/physics_ir.py` — read-only for A/B/C
during normal Red/Green. Re-exports or `compile_source` wiring require a
single-agent integration Slice with explicit Adjudicator approval (prefer
LISS-0115 Slice D).

## 4. Dependency and merge order

```text
LISS-0116 (Equation DTOs)
    |
    +--> LISS-0115 Slice C (consume equations)
    |
LISS-0115 Slices A–B (Operator/Binder/Channel)  } may start Red in parallel with 0116
    |
    +--> LISS-0117 Slice B (source→lower)
LISS-0117 Slice A (fixture snapshots)           } may start Red in parallel
```

**Recommended merge order:** 0116 → 0115 → 0117.

## 5. Stop conditions (hand back to Adjudicator)

- Any agent needs to edit another slot’s exclusive path.
- Shared `physics_ir.py` must change for a Green to pass.
- New ADR-level choice (unit vector model, public-oracle semantics, pass order).
- Claim ID collision or branch ownership unclear.

## 6. ID reservation

| ID | State |
|---|---|
| LISS-0115–0117 | reserved follow-ups; bodies in `docs/issues/` |
| LISS-0118 | complete (unrelated) |
| LISS-0119+ | next free ad-hoc |

Do not invent work under WP-0025 reserved numbers `0070`, `0077`–`0079`,
`0081`–`0105` except as already defined roadmap rows.

## 7. Verification for this plan

- Exclusive paths across A/B/C do not intersect.
- Issue bodies cite this WP for parallelism.
- open-work-register / local-issue-planning / WP-0025 Current next stay in sync.
