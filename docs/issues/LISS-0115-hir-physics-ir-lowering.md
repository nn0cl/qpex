# LISS-0115: HIR → Physics IR lowering

## Metadata

- Local issue ID: LISS-0115
- Phase: Feature Path / Phase 3 Refactor complete
- Status: **complete** (Slices A–D; Phase 3 Refactor done)
- Type: compiler / IR
- Priority: P0
- Planning size: L
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on:
  - LISS-0081 A–D + E Phase 1 (structural DTOs / inspect / minimal builder)
  - [LISS-0116](LISS-0116-equation-unit-dto.md) for Equation/Coefficient/Unit
    consumption (Operator/Binder slices may start before 0116 merges)
- Blocks: (historical) source-backed promotion in
  [LISS-0117](LISS-0117-source-backed-physics-ir-goldens.md) — now **complete**
- Related branch: `feature/liss-0115-slice-d`
- Parallelism: Agent slot **B** —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md) **closed**
- Related: [LISS-0080](LISS-0080-phase-resolved-typed-hir.md);
  [physics-ir plan](../specs/staqex-v1-physics-ir-plan.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081. Earlier collision stubs that
claimed “Slice A Green” are **withdrawn**. Authoritative structural work is
LISS-0081 on `main`.

## Motivation — implementation gap (closed)

At Issue open, [`build_physics_ir`](../../compiler/staqex/physics_ir.py):

- built declaration-level `PhysicsNode`s and extracted Operator/Channel (and
  binders) from typed `main` statements only;
- was **not** wired into `compile_source` / the evaluator;
- did **not** preserve full equation trees, six-family recognizable structure
  from arbitrary Theory HIR, or Equation/Unit records.

**Outcome:** `physics_ir_lower.py` lowers HIR (+ optional Equation DTOs);
Slice D soft-wires `CompileResult.physics_ir`. Equation auto-extraction and
full six-family Theory lowering remain deferred (not claimed complete here).

## In scope

- Module `physics_ir_lower.py`: HIR/typed-unit → `PhysicsModule` (or
  additive nodes) preserving operator/binder/channel structure and, after
  LISS-0116, equation/coefficient structure
- Tests under `tests/test_physics_ir_lower_*.py` and A–B
  `tests/test_hir_to_physics_ir_*.py`
- Slice D: soft `compile_source` wire (`CompileResult.physics_ir`) after
  Adjudicator approval

## Exclusive write paths (Agent B)

| Path | Role |
|---|---|
| `compiler/staqex/physics_ir_lower.py` | lowering API |
| `tests/test_physics_ir_lower_*.py` | Red/Green for this Issue |
| `compiler/staqex/pipeline.py` | **Slice D only** — soft `CompileResult.physics_ir` wire |

**Read-only:** `physics_ir.py` (frozen); `physics_equation.py` after 0116
merges; golden tree (0117).

**Forbidden:** defining Equation/Unit DTOs (0116); golden fixtures/catalog
edits (0117); routine edits to `physics_ir.py`. Pre-D: `pipeline.py` was
forbidden; Slice D Adjudicator approval lifts that for the soft wire only.

## Out of scope

- Equation/Unit DTO definitions (LISS-0116)
- Source-backed golden loader / catalog promotion (LISS-0117)
- Binder finite expansion, Jordan–Wigner mapping, numerical evaluation
- Quantum Semantic IR / Algorithm Plan IR
- Provider SDK / QPU

## Acceptance (EARS)

1. When typed HIR containing an Operator (and binder where present) is lowered,
   the Physics IR shall retain recognizable operator/atom/binder structure and
   source provenance without gate expansion.
2. When LISS-0116 Equation DTOs are available and a supported equation form is
   lowered, the IR shall retain equation/coefficient/unit records
   inspectably.
3. When provenance or domain invariants required by reviewed tests fail, the
   verifier path shall emit named `PHYSICS_IR_*` diagnostics (existing or
   module-local) and shall not silently repair.
4. When Slice D is approved, `compile_source` shall expose soft
   `CompileResult.physics_ir` via the lowering API; `PHYSICS_IR_*`
   diagnostics shall not hard-fail compile. Equation nodes remain caller-
   supplied (not auto-parsed).

## Gherkin (summary)

```gherkin
Feature: HIR to Physics IR lowering

  Scenario: Operator binder structure survives lowering
    Given phase-resolved HIR with a typed Operator and binder
    When physics_ir_lower runs
    Then the PhysicsModule retains atoms binder order and SourceOrigin
    And no gate expansion occurs

  Scenario: Compile wiring exposes lowered Physics IR
    Given Slice D wiring is Adjudicator-approved
    When compile_source runs on a valid Operator program
    Then CompileResult.ok is true
    And CompileResult.physics_ir is a PhysicsModule matching explicit lower
    And PHYSICS_IR_* diagnostics do not make compile fail
```

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Lower Operator (+ binder) from typed HIR/unit into Physics IR via new module | complete; PR #127 merged |
| **B** | Channel / measurement-intent / symmetry paths already representable in 0081 DTOs | complete in the accepted A–B boundary; PR #127 merged |
| **C** | Consume LISS-0116 Equation/Coefficient/Unit in lowering | complete on `main` (PR #129) |
| **D** | `compile_source` / pipeline wire — **Adjudicator-approved** | complete |

## Parallel start rule

Slices A–B may begin Red **in parallel with LISS-0116** (files do not
overlap). Slice C required the 0116 merge, now satisfied by `origin/main`.
Do not edit `physics_equation.py`.

## Slice C completion evidence

- `compiler/staqex/physics_ir_lower.py` consumes immutable Equation DTOs and
  preserves equation order, coefficients, units, and source provenance.
- `tests/test_physics_ir_lower_c_red.py` covers valid lowering, deterministic
  ordering, nested Equation/Unit diagnostics, and rejection of generic payloads.
- Merged on `main` (PR #129).

## Slice D completion evidence

- `CompileResult.physics_ir` is populated by `lower_hir_to_physics_ir(hir,
  unit=unit)` inside `_analyze_unit` (no equations by default).
- Soft `verify_lowered_physics_ir` diagnostics are appended; `PHYSICS_IR_*`
  codes remain outside `_HARD_CODES`, so compile success is unchanged.
- Phase 3: soft wire extracted to `_soft_physics_ir`; unused lower error
  constant removed; equation-node validation simplified without behavior change.
- `tests/test_physics_ir_lower_d_red.py` and Slice C runner pass; `py_compile`
  and `git diff --check` pass.
- Evaluator / QPU paths unchanged; Equation extraction from source remains
  explicit API (not auto-parsed in the pipeline).

## Acceptance checklist

- [x] Operator/binder/channel structure via lowering API (A–B)
- [x] Equation/Coefficient/Unit consumption (C)
- [x] Soft `compile_source` wire (D)

## Adjudicator Decision Points

- [ ] Approve Issue body / plan intake (this document)
- [ ] Authorize Slice A Phase 1 Red only
- [ ] Confirm `physics_ir.py` remains frozen during normal Green
- [x] Authorize Slice C implementation after LISS-0116 merge
- [x] Approve Slice D (pipeline wire) — Adjudicator authorized via session request
