# LISS-0075: Linear quantum usage and safe uncomputation

## Metadata

- Local issue ID: LISS-0075
- GitHub issue: not created
- Status: **in progress** — Slice A complete; Slice B Phase 1 Red
- Phase: Feature Path / Slice B
- Type: language feature / type system
- Priority: P0
- Planning size: XL
- Owner/agent: —
- Related branch: `feature/liss-0075-linear-quantum-usage`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: LISS-0071 **complete**, LISS-0080 **complete** (HIR phase + effects)
- Unlocks: LISS-0077 (full linear type system)

## Motivation

Quantum mechanics imposes hard constraints that classical types do not capture:

- **No-cloning theorem**: a quantum state cannot be duplicated.
- **No-implicit-discard**: unobserved ancilla qubits left in an entangled state
  corrupt the surrounding computation silently.
- **Uncomputation**: ancilla registers must be returned to |0⟩ (or a known
  state) before release; failing to do so leaks entanglement.

Without explicit enforcement, the compiler accepts programs that violate these
constraints. LISS-0075 introduces the minimal detection layer that makes
violations diagnosable at HIR level.

## Scope

### In scope

- HIR-level **linear-use verifier**: detect use-after-free, duplicate use, and
  implicit discard of quantum-typed bindings within a single `fun` body.
- **Uncomputation witness check**: confirm an ancilla binding re-initialized to
  its input state before scope exit (simulator-equivalence check in the
  evaluator; HIR provenance record).
- Diagnostics: named error codes `LINEAR_DUPLICATE_USE`,
  `LINEAR_IMPLICIT_DISCARD`, `UNCOMPUTE_WITNESS_MISSING`.
- Integration with existing `HirDecl.effects` (from LISS-0080) to mark
  functions that perform linear consumption.

### Out of scope (deferred to LISS-0077)

- Full borrow-checker / ownership type surface in the language syntax.
- Inter-procedural linear analysis across `fun` call boundaries.
- Dependent-type proof of uncomputation correctness.
- QPU backend linear resource scheduling.

## Acceptance criteria (Gherkin sketch)

```gherkin
Feature: Linear quantum usage enforcement

  Scenario: Duplicate use of quantum binding is rejected
    Given a fun body that applies a gate to qubit q twice without measure
    When the HIR verifier runs
    Then diagnostic LINEAR_DUPLICATE_USE is emitted for q

  Scenario: Implicit discard of ancilla is rejected
    Given a fun body that initialises ancilla a and never measures or uncomputesstaqex it
    When the HIR verifier runs
    Then diagnostic LINEAR_IMPLICIT_DISCARD is emitted for a

  Scenario: Valid uncomputation passes
    Given a fun body that initialises ancilla a, uses it, and restores a to |0>
    When the HIR verifier runs
    Then no linear diagnostic is emitted

  Scenario: Uncomputation witness is recorded in HirDecl provenance
    Given a fun that uncomputesstaqex ancilla a
    When build_hir is called
    Then HirDecl for that fun includes effect "Uncompute" in its effects set
```

## Proposed slices

| Slice | Scope | Size |
|---|---|---|
| **A** | `HirLinearVerifier` port + `LINEAR_DUPLICATE_USE` diagnostic (Red → Green → Refactor) | **complete** |
| **B** | `LINEAR_IMPLICIT_DISCARD` diagnostic; ancilla lifetime tracking within fun scope | Phase 1 Red |
| **C** | Uncomputation witness: evaluator simulator-equivalence check + `HirDecl.effects` `"Uncompute"` | L |
| **D** | Integration: wire verifier into `build_hir`; end-to-end acceptance test suite | M |

## Design decisions (Adjudicator-approved 2026-07-29)

1. **Quantum-typed binding identification**: `Ty.kind == "State"` (and later
   Density subtypes as needed). Slice A/B use `State` via HIR symbols.
2. **Scope unit**: per-`fun` / `main` body only (no inter-procedural). Confirmed.
3. **Uncomputation witness representation**: deferred to Slice C —
   `HirDecl.effects` gains `"Uncompute"` (preferred).
4. **Simulator-equivalence check**: deferred to Slice C — amplitude < 1e-12.

## Files likely touched

- `compiler/staqex/hir.py` — `HirLinearVerifier`, `HirDecl.effects` extension
- `compiler/staqex/typecheck.py` — quantum type identification helper
- `tests/test_hir_slice_*_red.py` — new test files per slice
- `docs/specs/staqex-v1-phase-resolved-hir-plan.md` — extend with linear notes

## Adjudicator Decision Points

- [x] Slice A plan approval → Phase 1 Red → Green → Refactor (**complete**)
- [x] Slice B plan approval → Phase 1 Red (this turn)
- [ ] Slice C plan approval (simulator-equivalence tolerance)
- [ ] Slice D end-to-end acceptance
- [ ] Issue completion approval
