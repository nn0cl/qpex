# WP-0028: Physics IR follow-up parallelism (LISS-0115–0117)

| Field | Value |
|---|---|
| Status | **closed** — parallel follow-ups A–C complete (0115–0117) |
| Date | 2026-07-29 |
| Closed | 2026-07-29 (0115 Slice D soft wire) |
| Parent | [WP-0025](WP-0025-staqex-v1-north-star.md) LISS-0081 |
| Issues | [LISS-0116](../issues/LISS-0116-equation-unit-dto.md) **complete**,
  [LISS-0115](../issues/LISS-0115-hir-physics-ir-lowering.md) **complete**,
  [LISS-0117](../issues/LISS-0117-source-backed-physics-ir-goldens.md) **complete** |
| Shipping Kernel | Python `compiler/staqex/` |

## 1. Purpose (historical)

Separate **working copies** (one branch / worktree per agent) while keeping
**source ownership exclusive** so parallel Feature Path work did not collide
on [`physics_ir.py`](../../compiler/staqex/physics_ir.py).

LISS-0081 A–D + E Phase 1 remains the frozen structural boundary on `main`.
Follow-ups do **not** by themselves mark LISS-0081 globally complete — that
remains an Adjudicator closeout judgment.

## 2. Implementation gap (outcome)

| Gap | Outcome | Issue |
|---|---|---|
| Equation/Coefficient/Unit DTOs | shipped in `physics_equation.py` | LISS-0116 **complete** |
| HIR lowering + soft `compile_source` wire | `physics_ir_lower.py` + `CompileResult.physics_ir` | LISS-0115 **complete** |
| Source-backed golden loader | loader + oscillator lowered-IR evidence | LISS-0117 **complete** |

Remaining outside this WP: full six-family public-oracle promotion; Equation
auto-extraction in the pipeline; LISS-0081 global closeout; LISS-0082+.

## 3. Agent slots (historical exclusive writes)

| Slot | Issue | Exclusive write | Result |
|---|---|---|---|
| **A** | LISS-0116 | `physics_equation.py`, `tests/test_physics_equation_*.py` | complete |
| **B** | LISS-0115 | `physics_ir_lower.py`, `tests/test_physics_ir_lower_*.py`, Slice D `pipeline.py` soft wire | complete |
| **C** | LISS-0117 | `physics_ir_goldens.py`, fixtures, golden tests/catalog rows | complete |

**Frozen shared core:** `compiler/staqex/physics_ir.py` stayed read-only for
normal Red/Green. Soft compile wire landed via LISS-0115 Slice D without
editing DTO classes in that file.

## 4. Dependency and merge order (executed)

```text
LISS-0116 → LISS-0115 Slice C → LISS-0117 Slice B/C
LISS-0115 A–B ∥ 0116 early
LISS-0115 Slice D (soft compile wire) last for Agent B
```

## 5. ID reservation

| ID | State |
|---|---|
| LISS-0115–0117 | **complete** — do not reuse |
| LISS-0118 | complete (unrelated) |
| LISS-0119+ | next free ad-hoc |

## 6. Verification for this plan

- Exclusive paths across A/B/C did not intersect during parallel Green.
- Issue bodies / open-work-register / local-issue-planning / WP-0025 Current
  next synced on closeout of this WP.
