# LISS-0075: Linear quantum usage and safe uncomputation

## Metadata

- Local issue ID: LISS-0075
- GitHub issue: not created
- Status: **paused** — Slices A–B complete; Slice C blocked pending Adjudicator
  risk review of current source (2026-07-29)
- Phase: Feature Path / pause before Slice C
- Type: language feature / type system
- Priority: P0
- Planning size: XL
- Owner/agent: —
- Related branch: `feature/liss-0075-linear-quantum-usage`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: LISS-0071 **complete**, LISS-0080 **complete** (HIR phase + effects)
- Unlocks: LISS-0077 (full linear type system)
- Pause reason: Adjudicator will re-read A/B implementation with fresh eyes
  before approving Slice C (uncomputation / evaluator coupling).

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
    Given a fun body that initialises ancilla a and never measures or uncomputes it
    When the HIR verifier runs
    Then diagnostic LINEAR_IMPLICIT_DISCARD is emitted for a

  Scenario: Valid uncomputation passes
    Given a fun body that initialises ancilla a, uses it, and restores a to |0>
    When the HIR verifier runs
    Then no linear diagnostic is emitted

  Scenario: Uncomputation witness is recorded in HirDecl provenance
    Given a fun that uncomputes ancilla a
    When build_hir is called
    Then HirDecl for that fun includes effect "Uncompute" in its effects set
```

## Proposed slices

| Slice | Scope | Size |
|---|---|---|
| **A** | `HirLinearVerifier` port + `LINEAR_DUPLICATE_USE` diagnostic (Red → Green → Refactor) | **complete** |
| **B** | `LINEAR_IMPLICIT_DISCARD` diagnostic; ancilla lifetime tracking within fun scope | **complete** |
| **C** | Uncomputation witness: evaluator simulator-equivalence check + `HirDecl.effects` `"Uncompute"` | **blocked** — risk review |
| **D** | Integration: wire verifier into `build_hir`; end-to-end acceptance test suite | **blocked** — after C |

## Open risks (parked — review before Slice C)

Adjudicator pause 2026-07-29: re-read source with fresh eyes before Slice C.
Primary implementation: `compiler/staqex/hir.py` (`HirLinearVerifier`).
Tests: `tests/test_linear_usage_slice_a_red.py`,
`tests/test_linear_usage_slice_b_red.py`.

| ID | Risk | Why it matters | Suggested review focus |
|---|---|---|---|
| **R1** | “Consumption” is **`measure` only** | Discard message already says “or uncomputation”, but no uncompute path exists yet. Slice C would invent semantics if rushed. | Decide what counts as a linear consume before evaluator coupling. |
| **R2** | Alias = duplicate-use (`State alias = q`) | May be stricter than intended; some styles use temporary names without cloning. | Confirm no-cloning surface vs. allowed renaming. |
| **R3** | Early-collapse / terminal `measure` | Duplicate `measure` paths are hard to express in Valid programs; Slice A’s measure-reuse arm is under-exercised. | Keep, drop, or replace with non-terminal consume ops. |
| **R4** | Linear type set is `Ty.kind == "State"` only | `DensityState` / register carriers may need the same rules later. | Whether Slice C widens the type set or stays State-only. |
| **R5** | Verifier is **opt-in** (`HirLinearVerifier().verify`) | Not wired into `build_hir` / pipeline (Slice D). Easy to forget in tooling. | Ship D with C, or accept advisory-only until then. |
| **R6** | Per-block analysis only | Nested blocks / `when` arms / `foreach` not modeled; false negatives possible. | Accept for MVP or expand before uncompute. |
| **R7** | Slice C couples HIR + evaluator | Simulator-equivalence (1e-12) is a policy choice with numeric risk. | Confirm tolerance and whether witness is static vs. runtime. |
| **R8** | Diagnostic / Gherkin wording drift | Early Gherkin mentioned gate-twice-without-measure; A/B ship alias + discard. | Rebaseline Then-clauses before C Red. |

**Do not start Slice C until** this table is reviewed (accept / defer / split to follow-up LISS).

## Design decisions (Adjudicator-approved 2026-07-29)

1. **Quantum-typed binding identification**: `Ty.kind == "State"` (and later
   Density subtypes as needed). Slice A/B use `State` via HIR symbols.
2. **Scope unit**: per-`fun` / `main` body only (no inter-procedural). Confirmed.
3. **Uncomputation witness representation**: deferred to Slice C —
   `HirDecl.effects` gains `"Uncompute"` (preferred). **Blocked on risk review.**
4. **Simulator-equivalence check**: deferred to Slice C — amplitude < 1e-12.
   **Blocked on risk review (R7).**

## Files likely touched

- `compiler/staqex/hir.py` — `HirLinearVerifier`, `HirDecl.effects` extension
- `compiler/staqex/typecheck.py` — quantum type identification helper
- `tests/test_linear_usage_slice_*_red.py` — Red tests per slice
- `docs/specs/staqex-v1-phase-resolved-hir-plan.md` — extend with linear notes

## Adjudicator Decision Points

- [x] Slice A plan approval → Phase 1 Red → Green → Refactor (**complete**)
- [x] Slice B plan approval → Phase 1 Red → Green → Refactor (**complete**)
- [ ] **Risk review** of R1–R8 (source read) before Slice C
- [ ] Slice C plan approval (simulator-equivalence tolerance)
- [ ] Slice D end-to-end acceptance
- [ ] Issue completion approval
