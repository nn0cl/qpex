# LISS-0114: Linear verifier hardening and residual risks

## Metadata

- Local issue ID: LISS-0114
- GitHub issue: not created
- Status: **complete** — Slices A–F shipped (2026-07-29); Adjudicator Slice F
  approval「F 承認」. ADR 0107 remains **Proposed**.
- Phase: Feature Path / done (A–F)
- Type: language feature / type system / pipeline
- Priority: P0
- Planning size: L (sliced A–F; first Red = Slice A only after plan approval)
- Owner/agent: —
- Related branch: `feature/liss-0114-slice-a`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: [LISS-0075](LISS-0075-linear-quantum-usage.md) **complete**
- Related: [LISS-0080](LISS-0080-phase-resolved-typed-hir.md) (HIR);
  does **not** fold into [LISS-0077](../work-plans/WP-0025-staqex-v1-north-star.md)
  (Dynamic QPU — different track)
- Unlocks: safer CLI/pipeline linear enforcement; runtime uncompute path (Slice F)

## Motivation

[LISS-0075](LISS-0075-linear-quantum-usage.md) shipped an HIR-level linear-use
MVP (`LINEAR_DUPLICATE_USE`, `LINEAR_IMPLICIT_DISCARD`, static Uncompute
witness, `HirModule.linear_diagnostics`). Parked risks R1–R10 remain. Early
docs incorrectly pointed residual work at LISS-0077; that Issue is **Dynamic
QPU controller**, not a linear-type successor. This Issue owns the hardening
and residual disposition.

## Scope

### In scope

- Pipeline / CLI hard-fail for linear diagnostics (R5).
- Gherkin / acceptance rebaseline to shipped surface (R8).
- Documented consume-set policy and R3 test stance (R1, R3).
- Alias rename design gate (R2); default remains strict alias = duplicate.
- DensityState linear set widening (R4).
- Nested / `when` lifetime analysis (R6).
- Runtime simulator-equivalence uncompute witness + tolerance policy (R7, R9).

### Out of scope

- Full borrow-checker / ownership syntax (still future; not LISS-0077).
- Inter-procedural analysis across `fun` call boundaries (may stay deferred).
- Dynamic QPU / `Controller<T>` (LISS-0077).
- Quantum Semantic IR (LISS-0082).
- Changing LISS-0075 shipped assertions without Adjudicator approval.

## Residual disposition (from LISS-0075 R1–R10)

| ID | Disposition | Slice |
|---|---|---|
| **R5** | Fix — fold linear diags into `compile_source` / CLI as **errors** (hard-fail) | **A** |
| **R8** | Fix — rebaseline Gherkin / acceptance to alias + discard + static uncompute | **A** |
| **R10** | **Closed-accepted** on LISS-0075 — Type-First / in-block tracking is spec; HIR local symbols = future polish only | — |
| **R1** | Design → implement — consume = `measure` ∪ static uncompute; gate apply is non-consume unless scenarios expand | **B** |
| **R3** | Absorb into B — add Red for measure-reuse path or mark explicitly out of MVP | **B** |
| **R2** | **Closed-accepted: strict alias** (`State alias = q` → `LINEAR_DUPLICATE_USE`); rename not authorized | **C** |
| **R4** | **Shipped** — `LINEAR_CARRIER_KINDS` + `is_linear_carrier_ty` (State ∪ DensityState Object) | **D** |
| **R6** | **Shipped** — `forEach`/`dynamic qpu` nested blocks; `when` scrutinee/arms; `inspect` uses | **E** |
| **R7+R9** | **Shipped** — runtime ≈|0⟩ check + `LINEAR_UNCOMPUTE_AMPLITUDE_TOL`; ADR 0107 Proposed | **F** |
| **R9 static** | **Accepted with runtime guard** — static HIR witness + evaluator verify (F) | **F** |

## Consume-set policy (Slice B / R1 — shipped)

Authoritative export: `compiler.staqex.hir.LINEAR_CONSUME_KINDS`

| Kind | Counts as consume? |
|---|---|
| `measure` | **yes** |
| same-name `|0>` / `vacuum` rebind (`static_uncompute_zero_reset`) | **yes** |
| `hadamard` / `apply` / other gate rebinds | **no** (still need measure or uncompute) |

R3: a second `measure` on a consumed root emits `LINEAR_DUPLICATE_USE` (may
co-occur with `EARLY_COLLAPSE_ERROR` when measure is non-terminal).

## Alias policy (Slice C / R2 — locked)

Authoritative export: `compiler.staqex.hir.LINEAR_ALIAS_POLICY == "strict"`.

- `State alias = q` remains `LINEAR_DUPLICATE_USE` (no silent rename / move).
- Adjudicator「承認」2026-07-29 confirmed the default; rename would need a
  future explicit override Issue.

## Carrier set (Slice D / R4 — shipped)

Authoritative exports:

- `LINEAR_CARRIER_KINDS` = `{State, DensityState}`
- `is_linear_carrier_ty(ty)` — `Ty.kind == "State"` **or**
  `Ty(kind="Object", payload="DensityState")` (Kernel env encoding)

Module-symbol lookup and Type-First heads share this predicate.

## Control-flow lifetime (Slice E / R6 — shipped)

- Nested `forEach` / `dynamic qpu` bodies are analyzed; inner discards surface.
- `when (ctrl) { … }` consumes linear `ctrl` and Vars used in arm expressions.
- `inspect(x)` counts as a linear use of `x` (non-destructive view).
- Gate/`hadamard` Call args remain non-consume (Slice B).

## Runtime uncompute (Slice F / R7·R9 — shipped)

- Export: `LINEAR_UNCOMPUTE_AMPLITUDE_TOL` (= physical `1e-12`, ADR 0076 class)
- Helpers: `runtime.uncompute.is_computational_basis_zero` /
  `require_computational_basis_zero`
- Evaluator: verify after `|0>` / `vacuum` rebind; verify returns of
  `effects { Uncompute }` functions
- ADR candidate: [0107](../architecture/adr/0107-linear-uncompute-amplitude-tolerance.md)
  (**Proposed**)

## Acceptance criteria (sketch; Slice A first)

```gherkin
Feature: Linear verifier pipeline hard-fail

  Scenario: Implicit discard fails compile_source
    Given a program with an unconsumed State binding
    When compile_source runs with HIR build
    Then CompileResult.ok is false
    And diagnostics include LINEAR_IMPLICIT_DISCARD

  Scenario: Acceptance text matches shipped surface
    Given the LISS-0075 / 0114 Gherkin for duplicate use
    Then the scenario describes alias rebinding (not gate-twice-without-measure)
```

## Proposed slices

| Slice | Scope | Size | Status |
|---|---|---|---|
| **A** | `compile_source` / CLI hard-fail for `HirModule.linear_diagnostics` (R5) + Gherkin rebaseline (R8) | S | **complete** |
| **B** | Consume-set documentation + R3 measure-reuse Red (R1, R3) | S–M | **complete** |
| **C** | Alias rename policy design gate (R2) — **strict locked**; no rename impl | design / S | **complete** |
| **D** | Module-symbol linear set includes `DensityState` (R4) | M | **complete** |
| **E** | Nested block / `when` lifetime analysis (R6) | L | **complete** |
| **F** | Runtime uncompute witness + numeric tolerance ADR candidate (R7, R9) | L–XL | **complete** |

**Default R5 policy:** hard-fail (errors), not advisory. Advisory would need an
explicit ADR or flag.

**Default R2 policy:** keep strict alias = `LINEAR_DUPLICATE_USE`.

## Files likely touched (when Feature Path starts)

- `compiler/staqex/pipeline.py` — merge linear diagnostics into `CompileResult`
- `compiler/staqex/hir.py` — consume-set / control-flow / DensityState (later slices)
- `tests/test_linear_usage_slice_*` or new `tests/test_linear_hardening_slice_a_red.py`
- Docs: this Issue, LISS-0075 cross-links, open-work-register, WP-0025

## Adjudicator Decision Points

- [x] Approve Issue ID **LISS-0114**, disposition matrix, and slices A–F
      (Adjudicator「承認」2026-07-29)
- [x] Confirm Slice A first Red after plan intake (hard-fail + Gherkin)
- [x] Confirm R5 hard-fail default (or override to advisory)
- [x] Confirm R2 strict-alias default (or authorize rename)
- [x] Slice A Red → Green → Refactor (**complete** 2026-07-29)
- [x] Authorize Slice B plan gate (R1 consume-set + R3; Adjudicator「承認」)
- [x] Slice B Red → Green → Refactor (**complete** 2026-07-29)
- [x] Authorize Slice C design gate — **strict alias locked** (Adjudicator「承認」)
- [x] Slice C design lock + policy export (**complete** 2026-07-29)
- [x] Authorize Slice D plan gate (R4 DensityState; Adjudicator「Dへ。承認」)
- [x] Slice D Red → Green → Refactor (**complete** 2026-07-29)
- [x] Authorize Slice E plan gate (R6; Adjudicator「E 承認」)
- [x] Slice E Red → Green → Refactor (**complete** 2026-07-29)
- [x] Authorize Slice F plan gate (R7/R9; Adjudicator「F 承認」)
- [x] Slice F Red → Green → Refactor (**complete** 2026-07-29)
- [x] Issue completion (Slices A–F) — ADR 0107 remains Proposed pending architecture accept