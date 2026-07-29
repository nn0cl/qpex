# LISS-0117: Source-backed Physics IR goldens

## Metadata

- Local issue ID: LISS-0117
- Status: **in progress** — Agent C; Slice A Green complete
- Phase: Feature Path / Slice A Phase 2 Green reviewed locally
- Type: conformance / golden tests
- Priority: P1
- Planning size: M
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
- Depends on:
  - LISS-0081 fixture catalog
    ([staqex-v1-physics-ir-golden-catalog.md](../specs/staqex-v1-physics-ir-golden-catalog.md))
  - [LISS-0115](LISS-0115-hir-physics-ir-lowering.md) for source→IR contract
    (loader Slice A may use inspect API + checked-in IR snapshots before full
    lowering)
  - [LISS-0116](LISS-0116-equation-unit-dto.md) when goldens assert Equation/Unit
    (**complete** on `main`; Slice A does not require Equation assertions yet)
- Related branch: `feature/liss-0117-slice-a`
- Parallelism: Agent slot **C** (this agent) —
  [WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)

## Claim notice

**Do not reuse this ID.** Follow-up to LISS-0081 Slice E. LISS-0081 already
ships a **fixture-only** six-family catalog; this Issue owns **source-backed**
loading and catalog promotion, not the structural DTO boundary.

## Motivation — implementation gap

The golden catalog status is “fixture evidence — not a promoted runtime
oracle.” There is no loader that:

- reads Staqex sources (or checked-in source fixtures) under
  `tests/fixtures/physics_ir/`;
- produces or compares Physics IR / inspection projections with stable golden
  IDs (`PIR-G-*`);
- records promotion criteria when HIR lowering + Equation DTOs are stable.

## In scope

- New module `physics_ir_goldens.py` (load / compare / report helpers)
- Fixture tree `tests/fixtures/physics_ir/**`
- Tests `tests/test_physics_ir_goldens_*.py`
- Updates to the **promotion** section of
  [`staqex-v1-physics-ir-golden-catalog.md`](../specs/staqex-v1-physics-ir-golden-catalog.md)
  when Adjudicator accepts promotion criteria

## Exclusive write paths (Agent C)

| Path | Role |
|---|---|
| `compiler/staqex/physics_ir_goldens.py` | **new** — golden load/compare |
| `tests/fixtures/physics_ir/**` | source and expected-projection fixtures |
| `tests/test_physics_ir_goldens_*.py` | Red/Green |
| `docs/specs/staqex-v1-physics-ir-golden-catalog.md` | promotion / status rows only |

**Read-only:** public Physics IR / equation / lower APIs.

**Forbidden:** DTO definitions, lowering implementation, `pipeline.py`,
routine `physics_ir.py` edits.

## Out of scope

- Implementing Equation DTOs (0116) or HIR lowering (0115)
- Numerical oracles, simulator execution, provider jobs
- Promoting goldens to public conformance without Adjudicator acceptance

## Acceptance (EARS)

1. When a golden ID from the six-family catalog is loaded from
   `tests/fixtures/physics_ir/`, the loader shall associate source (or explicit
   IR snapshot), expected inspection structure, and provenance requirements.
2. When an inspection record lacks required family or provenance, verification
   shall fail with a named diagnostic (existing `PHYSICS_IR_*` or documented
   golden harness code).
3. When promotion is not yet approved, the catalog shall continue to state that
   fixtures are not a public runtime oracle.

## Gherkin (summary)

```gherkin
Feature: Source-backed Physics IR goldens

  Scenario: Fixture tree loads six family golden IDs
    Given tests/fixtures/physics_ir entries for PIR-G-* families
    When the golden loader runs
    Then each family exposes required structure and provenance expectations

  Scenario: Catalog promotion stays gated
    Given promotion has not been Adjudicator-accepted
    When the golden catalog is read
    Then status remains non-oracle fixture evidence
```

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Fixture layout + loader for inspect/DTO snapshots (no new lowering) | **complete** (Green) |
| **B** | Wire loader to LISS-0115 lower output for ≥1 family | pending 0115 |
| **C** | Equation/Unit assertions (0116) + catalog promotion PR | gated |

### Slice A (shipped locally)

- Tests: [`tests/test_physics_ir_goldens_slice_a_red.py`](../../tests/test_physics_ir_goldens_slice_a_red.py)
- Loader: [`compiler/staqex/physics_ir_goldens.py`](../../compiler/staqex/physics_ir_goldens.py)
- Fixtures: [`tests/fixtures/physics_ir/`](../../tests/fixtures/physics_ir/) (`PIR-G-*.json`)

## Parallel start rule

Slice A may begin **in parallel** with 0115 using synthetic IR snapshots.
Slices B–C wait on upstream. Do not edit `physics_ir_lower.py`,
`physics_equation.py`, or `physics_ir.py`.

## Adjudicator Decision Points

- [x] Approve Issue body / plan intake — Adjudicator “LISS-0117 Slice Aを進めて”
- [x] Authorize Slice A Phase 1 Red only
- [x] Confirm fixture-only vs public-oracle promotion gate (remains gated)
- [x] Approve Slice A Red → authorize Phase 2 Green — Adjudicator “承認”
- [x] Approve Slice A Green / open Slice B when 0115 ready
- [ ] Approve catalog promotion after B/C evidence
- [x] Approve Slice A ship / merge PR
