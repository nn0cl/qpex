# LISS-0075: Linear quantum usage and safe uncomputation

## Metadata

- Local issue ID: LISS-0075
- GitHub issue: not created
- Status: **complete** — Slices A–D shipped; Adjudicator completion approval
  2026-07-29. Residual risks **triaged to [LISS-0114](LISS-0114-linear-verifier-hardening.md)**
  (2026-07-29); do not treat parked items as silently closed.
- Phase: Feature Path / done (A–D)
- Type: language feature / type system
- Priority: P0
- Planning size: XL
- Owner/agent: —
- Related branch: `feature/liss-0075-linear-quantum-usage`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: LISS-0071 **complete**, LISS-0080 **complete** (HIR phase + effects)
- Unlocks: [LISS-0114](LISS-0114-linear-verifier-hardening.md) (linear verifier
  hardening); LISS-0077 (Dynamic QPU) depends on this Issue for quantum-safety
  prerequisites but is **not** the linear-type successor
- Pause reason: n/a (Issue closed; residuals owned by LISS-0114).

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
- **Uncomputation witness check**: static `|0>` / `vacuum` rebind + HIR
  provenance (`Uncompute` effect). Runtime simulator-equivalence deferred to
  [LISS-0114](LISS-0114-linear-verifier-hardening.md) Slice F.
- Diagnostics: named error codes `LINEAR_DUPLICATE_USE`,
  `LINEAR_IMPLICIT_DISCARD`, `UNCOMPUTE_WITNESS_MISSING`.
- Integration with existing `HirDecl.effects` (from LISS-0080) to mark
  functions that perform linear consumption.
- `HirModule.linear_diagnostics` via `build_hir` (pipeline hard-fail → LISS-0114).

### Out of scope (deferred to [LISS-0114](LISS-0114-linear-verifier-hardening.md))

- Pipeline / CLI hard-fail for linear diagnostics.
- Full borrow-checker / ownership type surface in the language syntax.
- Inter-procedural linear analysis across `fun` call boundaries.
- Dependent-type / runtime proof of uncomputation correctness.
- Nested-block / `when` lifetime analysis; DensityState module-symbol widening.
- QPU backend linear resource scheduling.

**Note:** LISS-0077 is Dynamic QPU controller / feed-forward — **not** the home
for these linear residuals.

## Acceptance criteria (Gherkin sketch — shipped surface)

```gherkin
Feature: Linear quantum usage enforcement

  Scenario: Duplicate use via alias rebinding is rejected
    Given a fun body that binds State alias = q (same root) without measure
    When the HIR verifier runs
    Then diagnostic LINEAR_DUPLICATE_USE is emitted for the aliased root

  Scenario: Implicit discard of ancilla is rejected
    Given a fun body that initialises ancilla a and never measures or uncomputes it
    When the HIR verifier runs
    Then diagnostic LINEAR_IMPLICIT_DISCARD is emitted for a

  Scenario: Valid static uncomputation passes
    Given a fun body that initialises ancilla a and restores a to |0> or vacuum
    When the HIR verifier runs
    Then no linear diagnostic is emitted for a

  Scenario: Uncomputation witness is recorded in HirDecl provenance
    Given a fun that uncomputes ancilla a via static |0>/vacuum rebind
    When build_hir is called
    Then HirDecl for that fun includes effect "Uncompute" in its effects set
```

(Early drafts mentioned gate-twice-without-measure; that wording was drift —
see LISS-0114 R8 if further doc sync is needed.)

## Proposed slices

| Slice | Scope | Size |
|---|---|---|
| **A** | `HirLinearVerifier` port + `LINEAR_DUPLICATE_USE` diagnostic (Red → Green → Refactor) | **complete** |
| **B** | `LINEAR_IMPLICIT_DISCARD` diagnostic; ancilla lifetime tracking within fun scope | **complete** |
| **C** | Uncomputation witness: static `|0>`/vacuum + `HirDecl.effects` `"Uncompute"` (runtime amp → LISS-0114 F) | **complete** |
| **D** | Integration: wire verifier into `build_hir`; end-to-end acceptance test suite | **complete** |

## Residual risks (triaged → LISS-0114)

Triage 2026-07-29: see
[LISS-0114 disposition matrix](LISS-0114-linear-verifier-hardening.md#residual-disposition-from-liss-0075-r1r10)
and
[`2026-07-29-liss-0075-residual-triage.md`](../collaboration/traces/2026-07-29-liss-0075-residual-triage.md).

| ID | Risk | Disposition |
|---|---|---|
| **R1** | Consumption = `measure` **or** static uncompute witness | → LISS-0114 Slice B |
| **R2** | Alias = duplicate-use (`State alias = q`) | → LISS-0114 Slice C (default: keep strict) |
| **R3** | Early-collapse / terminal `measure` under-exercised | → LISS-0114 Slice B |
| **R4** | Linear type set State-centric at module symbols | → LISS-0114 Slice D |
| **R5** | Verifier on `HirModule.linear_diagnostics` only | → LISS-0114 Slice A (hard-fail) |
| **R6** | Per-block analysis only | → LISS-0114 Slice E |
| **R7** | Simulator-equivalence / evaluator coupling | → LISS-0114 Slice F |
| **R8** | Gherkin wording drift | → LISS-0114 Slice A (rebaseline; sketch above updated) |
| **R9** | Static `|0>` / `vacuum` provisional witness | MVP accepted; runtime → LISS-0114 Slice F |
| **R10** | Fun-local State missing from `TypeChecker.env` | **closed-accepted** — Type-First / in-block tracking is the shipped spec |

**Slice C provisional decisions (parked as R9 on 0114 F):** static witness only;
evaluator amplitude check deferred. `effects { Uncompute }` + same-name reset
to `|0>` / vacuum marks consumption without measure.

## Design decisions (Adjudicator-approved 2026-07-29)

1. **Quantum-typed binding identification**: `Ty.kind == "State"` (and later
   Density subtypes as needed). Slice A/B use `State` via HIR symbols.
2. **Scope unit**: per-`fun` / `main` body only (no inter-procedural). Confirmed.
3. **Uncomputation witness representation**: `HirDecl.effects` gains
   `"Uncompute"` when static `|0>` / vacuum rebind is witnessed (**Slice C**).
4. **Simulator-equivalence check**: amplitude < 1e-12 proposed — **deferred
   to LISS-0114 Slice F**; Slice C ships static `|0>` / vacuum witness only.

## Files touched

- `compiler/staqex/hir.py` — `HirLinearVerifier`, `HirDecl.effects` extension
- `compiler/staqex/typecheck.py` — `Uncompute` in known effects
- `tests/test_linear_usage_slice_*_red.py` — Red tests per slice

## Adjudicator Decision Points

- [x] Slice A plan approval → Phase 1 Red → Green → Refactor (**complete**)
- [x] Slice B plan approval → Phase 1 Red → Green → Refactor (**complete**)
- [x] **One-time** approval to proceed C/D with risks accumulate (2026-07-29)
- [x] Slice C Red → Green → Refactor (**complete**; static witness / R9)
- [x] Slice D end-to-end acceptance (**complete**; `HirModule.linear_diagnostics`)
- [x] Issue completion approval (Adjudicator 2026-07-29)
- [x] Residual triage → [LISS-0114](LISS-0114-linear-verifier-hardening.md) (2026-07-29)
