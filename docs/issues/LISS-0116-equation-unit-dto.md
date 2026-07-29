# LISS-0116: Equation / Unit DTO

## Metadata

- Local issue ID: LISS-0116
- Status: **proposed** — Issue body ready; implementation not started
- Phase: Feature Path / plan intake gated
- Type: language / IR DTO
- Priority: P0
- Planning size: M
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on: LISS-0081 A–D + E Phase 1 accepted (structural Physics IR on `main`)
- Blocks: full Equation consumption in [LISS-0115](LISS-0115-hir-physics-ir-lowering.md);
  Equation-shaped goldens in [LISS-0117](LISS-0117-source-backed-physics-ir-goldens.md)
- Related branch: `feature/liss-0116-*`
- Parallelism: Agent slot **A** —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)
- Related: [physics-ir plan](../specs/staqex-v1-physics-ir-plan.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081. **Not** LISS-0076 body-phase
residuals ([LISS-0118](LISS-0118-body-phase-typing-residuals.md), complete).

## Motivation — implementation gap

On `main`, [`compiler/staqex/physics_ir.py`](../../compiler/staqex/physics_ir.py)
has HilbertSpace, BinderNode, OperatorAtom, ChannelNode, inspection, and a
minimal `build_physics_ir`. It has **zero** `Equation` / `Coefficient` /
`Unit` / dimensional-algebra DTO types. Oscillator and symbolic-coefficient
families cannot be represented as first-class equation records.

## In scope

- Immutable DTOs: `EquationNode` (or equivalent), `Coefficient`, `Unit`, and
  dimension tags needed by Physics IR inspection
- Lightweight verifier helpers **inside the owned module** (named diagnostics;
  do not promote to compile-hard Kernel codes unless separately approved)
- Tests under `tests/test_physics_equation_*.py`

## Exclusive write paths (Agent A)

| Path | Role |
|---|---|
| `compiler/staqex/physics_equation.py` | **new** — Equation/Coefficient/Unit DTOs + module-local verify |
| `tests/test_physics_equation_*.py` | Red/Green for this Issue |

**Read-only:** `compiler/staqex/physics_ir.py` (frozen shared core).

**Forbidden:** edits to `physics_ir.py`, `pipeline.py`, golden catalog
promotion, HIR lowering modules.

## Out of scope

- HIR → Physics IR builder / `compile_source` wiring (LISS-0115)
- Source-backed golden loading (LISS-0117)
- Gate/matrix expansion, numerical solvers, SI conversion beyond `(L,M,T)` tags
  unless a later ADR says otherwise
- Provider / QPU / datastore

## Acceptance (EARS)

1. When an equation record with symbolic coefficient, unit, and source origin
   is constructed, the system shall retain those fields immutably and
   independently inspectably.
2. When a coefficient lacks required unit/dimension ancestry required by the
   reviewed tests, the module verifier shall emit a named diagnostic and shall
   not silently repair the value.
3. When parallel agents work LISS-0115/0117, this Issue shall not modify their
   exclusive paths.

## Gherkin (summary)

```gherkin
Feature: Physics equation and unit DTOs

  Scenario: Equation retains coefficient unit and provenance
    Given an immutable EquationNode with Coefficient and Unit
    And a SourceOrigin on each top-level record
    When the module verifier runs
    Then no silent repair occurs
    And provenance remains inspectable
```

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | `Coefficient`, `Unit`, dimension tags; immutability + provenance tests | pending plan approval |
| **B** | `EquationNode` sides/dynamics relation; verifier diagnostics | pending |
| **C** | Docs/catalog cross-links; optional thin re-export note for later integration | pending |

## Adjudicator Decision Points

- [ ] Approve Issue body / plan intake (this document)
- [ ] Authorize Slice A Phase 1 Red only
- [ ] Confirm units remain structured tags (not full SI conversion) for this Issue
- [ ] Confirm no edits to frozen `physics_ir.py` during normal Green
