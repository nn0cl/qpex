# LISS-0115: HIR → Physics IR lowering

## Metadata

- Local issue ID: LISS-0115
- Status: **Slice C implementation complete — review pending**
- Phase: Feature Path / Phase 2 Green
- Type: compiler / IR
- Priority: P0
- Planning size: L
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on:
  - LISS-0081 A–D + E Phase 1 (structural DTOs / inspect / minimal builder)
  - [LISS-0116](LISS-0116-equation-unit-dto.md) for Equation/Coefficient/Unit
    consumption (Operator/Binder slices may start before 0116 merges)
- Blocks: full source-backed promotion in
  [LISS-0117](LISS-0117-source-backed-physics-ir-goldens.md)
- Related branch: `feature/liss-0115-*`
- Parallelism: Agent slot **B** —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)
- Related: [LISS-0080](LISS-0080-phase-resolved-typed-hir.md);
  [physics-ir plan](../specs/staqex-v1-physics-ir-plan.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081. Earlier collision stubs that
claimed “Slice A Green” are **withdrawn**. Authoritative structural work is
LISS-0081 on `main`.

## Motivation — implementation gap

[`build_physics_ir`](../../compiler/staqex/physics_ir.py) today:

- builds declaration-level `PhysicsNode`s and extracts Operator/Channel (and
  binders) from typed `main` statements only;
- is **not** wired into `compile_source` / the evaluator;
- does **not** preserve full equation trees, six-family recognizable structure
  from arbitrary Theory HIR, or Equation/Unit records.

This Issue owns the **lowering module** that turns phase-resolved HIR into
Physics IR structures without gate expansion.

## In scope

- New module `physics_ir_lower.py`: HIR/typed-unit → `PhysicsModule` (or
  additive nodes) preserving operator/binder/channel structure and, after
  LISS-0116, equation/coefficient structure
- Tests under `tests/test_physics_ir_lower_*.py`
- Optional final Slice: `compile_source` wiring — **separate Adjudicator
  approval**; default Green does not touch `pipeline.py`

## Exclusive write paths (Agent B)

| Path | Role |
|---|---|
| `compiler/staqex/physics_ir_lower.py` | **new** — lowering API |
| `tests/test_physics_ir_lower_*.py` | Red/Green for this Issue |

**Read-only:** `physics_ir.py` (frozen); `physics_equation.py` after 0116
merges.

**Forbidden:** defining Equation/Unit DTOs (0116); golden fixtures/catalog
edits (0117); routine edits to `physics_ir.py` or `pipeline.py`.

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
4. When `compile_source` wiring is not yet approved, lowering shall remain an
   explicit API callable from tests without changing Kernel compile behavior.

## Gherkin (summary)

```gherkin
Feature: HIR to Physics IR lowering

  Scenario: Operator binder structure survives lowering
    Given phase-resolved HIR with a typed Operator and binder
    When physics_ir_lower runs
    Then the PhysicsModule retains atoms binder order and SourceOrigin
    And no gate expansion occurs

  Scenario: Compile wiring stays off until approved
    Given only Slices before the wiring Slice are implemented
    When compile_source runs on an ordinary program
    Then Physics IR lowering is not required for compile success
```

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Lower Operator (+ binder) from typed HIR/unit into Physics IR via new module | complete; PR #127 merged |
| **B** | Channel / measurement-intent / symmetry paths already representable in 0081 DTOs | complete in the accepted A–B boundary; PR #127 merged |
| **C** | Consume LISS-0116 Equation/Coefficient/Unit in lowering | implementation complete; review pending |
| **D** | Optional `compile_source` / pipeline wire — **separate approval** | gated |

## Parallel start rule

Slices A–B may begin Red **in parallel with LISS-0116** (files do not
overlap). Slice C required the 0116 merge, now satisfied by `origin/main`.
Do not edit `physics_equation.py`.

## Slice C completion evidence

- `compiler/staqex/physics_ir_lower.py` consumes immutable Equation DTOs and
  preserves equation order, coefficients, units, and source provenance.
- `tests/test_physics_ir_lower_c_red.py` covers valid lowering, deterministic
  ordering, nested Equation/Unit diagnostics, and rejection of generic payloads.
- Slice C direct runner, Physics IR A–D runners, Equation A–B runners,
  `py_compile`, and `git diff --check` pass.
- The lowering remains an explicit API; `compile_source` and the evaluator are
  unchanged.

## Slice C review boundary

- Current implementation commit: `fa87858`.
- Review required before promotion to complete.
- Slice D pipeline wiring remains separately gated.

## Adjudicator Decision Points

- [ ] Approve Issue body / plan intake (this document)
- [ ] Authorize Slice A Phase 1 Red only
- [ ] Confirm `physics_ir.py` remains frozen during normal Green
- [x] Authorize Slice C implementation after LISS-0116 merge
- [ ] Approve Slice D (pipeline wire) only after A–C Green, if desired
