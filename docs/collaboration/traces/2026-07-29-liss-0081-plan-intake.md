# Trace: LISS-0081 Phase 0 design intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0081 |
| Path | Feature Path — Phase 0 design intake (historical through Slice E) |
| Phase | **Superseded by Issue body** — A–D + E Phase 1 accepted on `main` (PR #124) |
| Branch | `feature/liss-0081-plan-intake` (merged) |
| Working copy | `/private/tmp/qpex-liss-0081` |

> **Status note (2026-07-29 docs sync):** Intermediate “Slice C pending” /
> mid-slice headers below are historical diary entries. Authoritative status is
> [LISS-0081](../../architecture/documentation-compression-map.md)
> and [physics-ir plan](../../specs/staqex-v1-physics-ir-plan.md).

## [DESIGN CHECK]

- Scope and expected behavior: define a provider-neutral Physics IR that
  preserves equations, operator algebra, binders, units, statistics,
  symmetries, channels, observables, and source provenance without gate
  expansion; acceptance scenarios are in the Issue.
- Specifications and files inspected: WP-0025 LISS-0081 section; LISS-0073,
  LISS-0074, LISS-0080; ADR 0106; compiler blueprint §3–§4.2; v1 north-star;
  `compiler/staqex/hir.py`; `compiler/staqex/symbolic_ir.py`.
- Component boundaries, ports/adapters, and VO/DTO candidates: immutable
  domain DTOs in a focused `physics_ir.py` candidate; HIR builder/verifier
  boundary; no external ports or adapters in the core transformation.
- Applicable constraints: Python Shipping Kernel is authoritative; additive
  extraction only; no second language semantics; no provider SDK, QPU,
  datastore, gate expansion, numerical evaluation, or Quantum Semantic IR.
- Decisions, assumptions, and unresolved ambiguities: proposed DTO vocabulary
  and slices A–E are not accepted until Adjudicator review; units, non-square
  codomains, fermion canonical ordering, continuous basis descriptors, and the
  symbolic IR bridge remain open.
- Included and omitted AI context: included only the listed issue/spec/ADR,
  HIR/symbolic-IR locations, and minimal north-star examples; omitted unrelated
  runtime, provider, Rust, private, and generated content.
- Task routing: human Adjudicator for scope/architecture; deterministic tools
  for tests and checks; code assistant only after Phase 1 Red approval.
- Input/output evidence contract when AI output is involved: no AI-generated
  runtime data; any future fixture must pair source, expected IR shape,
  provenance evidence, and verification status.
- Verification plan: review docs in Phase 0; after approval, add Slice A
  failing tests only, then stop for Red review.

## Current result

Slice A Red, Green, and Refactor are complete and accepted on the isolated
branch. Slice B Red, Green, and Refactor are complete; both reviewed test files
remain unchanged. Slice C remains out of scope; its plan intake is the next
safe action.

### Reviewer empathy summary

- The implementation is intentionally small and isolated in
  `compiler/staqex/physics_ir.py`; it does not rewire HIR, evaluation, or
  provider boundaries.
- The verifier currently covers only the Slice A provenance invariant. Domain,
  unit, statistics, and equation invariants are deliberately deferred to later
  approved slices.
- The direct test runner passes. pytest could not run because pytest is not
  installed in the environment.

### Slice B reviewer empathy summary

- The refactor isolates dictionary-fixture diagnostics in `_node_diagnostics`
  and gives diagnostic codes stable names.
- Existing Slice A operator fixtures without a `statistics` field remain valid;
  only an explicit `statistics: None` is diagnosed.
- Binder expansion, Jordan–Wigner mapping, evaluator wiring, and unit handling
  remain deferred to separately approved slices.

## Slice B design check

- Scope: preserve binder structure and second-quantized statistics/order in
  Physics IR; no expansion or mapping.
- Included context: `finite_binder.py`, `second_quantization.py`,
  `symbolic_ir.py`, existing binder/second-quantized tests, and Slice A DTOs.
- Omitted context: runtime/provider/QPU implementations and unrelated frontend
  slices.
- Next phase: Slice C Phase 1 Red only after Adjudicator approval.
- Open decisions: source order plus canonical metadata policy, and confirmation
  that expansion/mapping remain deferred.

## Slice C completion evidence

Slice C Red, Green, and Refactor are complete. The reviewed test file was not
modified. Direct runners for Slices A, B, and C all pass; pytest is unavailable
in the environment.

### Reviewer empathy summary

- Channel, measurement intent, initial condition, and symmetry are immutable
  structure-only DTOs; no runtime measurement or numerical validation was
  introduced.
- Shared verifier helpers preserve the exact named diagnostics while reducing
  duplicated construction logic.
- Slice D (formula-family golden inspection) remains out of scope.

## Review result

Slice C Phase 3 was accepted. Slice D plan intake is the next safe action;
Slice D implementation remains out of scope.

## Slice C design check

- Scope: preserve channels, POVM/observable measurement intent, initial
  conditions, Lindblad references, and symmetries/conservation laws.
- Included context: `mixed_state.py`, `measurement.py`, observation contracts,
  Lindblad source/runtime boundaries, and the v1 north-star examples.
- Omitted context: numerical integrators, provider adapters, simulator engines,
  and QPU target plans.
- Candidate DTOs: `ChannelNode`, `MeasurementIntent`, `InitialCondition`, and
  `SymmetryNode`, all requiring source origin and domain references.
- Next phase: Slice C Phase 1 Red only after plan approval.
- Open decisions: exact terminal/dynamic measurement intent representation and
  whether symmetry operands use typed references or opaque expression nodes.

## Slice D design check

- Scope: deterministic inspection of Ising, Heisenberg, Hubbard, molecular
  electronic, oscillator, and Lindblad Physics IR structure.
- Included context: Slices A–C DTOs, `symbolic_ir.py`, north-star §§6/8/9/10,
  existing binder/second-quantized/mixed-state contracts, and inspection ADRs.
- Omitted context: new parser syntax, numerical solvers, discretization/mapping
  passes, provider adapters, and simulator execution.
- Candidate API: immutable `InspectionRecord`/`PhysicsInspection` and a
  read-only `inspect_physics_ir` projection.
- Next phase: Slice D Phase 1 Red only after plan approval.
- Open decisions: golden fixture representation and stable node identity policy.

## Slice D completion evidence

Slice D Red, Green, and Refactor are complete. The reviewed Red test was not
modified. Direct runners for Slices A–D all pass; pytest remains unavailable.

### Reviewer empathy summary

- Inspection remains a deterministic read-only projection over immutable
  Physics IR and does not perform execution or lowering.
- Formula-family and provenance diagnostics use small shared helpers; the six
  family set remains explicit and reviewable.
- No new parser, numeric solver, mapping pass, or provider dependency was
  introduced.

## Slice E design check

- Scope: docs-only golden/diagnostic catalog synchronization and explicit
  remaining-work closeout for the current DTO/inspection boundary.
- Included context: promoted diagnostic catalog, conformance oracle rule,
  Issue/plan/work-plan status, and Slice A–D direct test evidence.
- Omitted context: HIR lowering, Equation/Unit DTO implementation, runtime,
  numeric solvers, parser, providers, and QPU backends.
- Candidate artifacts: stable six-family golden catalog and four verifier
  diagnostic entries.
- Next phase: Slice E Phase 1 documentation/fixture preparation after approval.
- Open decisions: fixture-only versus public-oracle promotion, and whether the
  active work-plan row should be updated in this Issue.

## Slice E completion evidence

Slice E Phase 1 documentation/fixture preparation is complete. Added the
fixture-only six-family golden catalog and synchronized four non-compile-hard
Physics IR verifier diagnostics. HIR lowering, Equation/Unit DTOs, and
source-backed golden loading remain explicitly open.

No compiler or test files were changed in this docs-only phase. Next safe action
is Adjudicator review of the catalog and the remaining-work boundary.

## Slice E review result

Slice E Phase 1 was accepted. The current DTO/inspection boundary is reviewed,
but LISS-0081 remains open for separately authorized HIR lowering,
Equation/Unit DTOs, and source-backed golden loading.

Follow-up Issue intake recorded: LISS-0115, LISS-0116, and LISS-0117. No new
ADR is required unless the accepted ownership, unit policy, source boundary,
or public-oracle semantics change.
