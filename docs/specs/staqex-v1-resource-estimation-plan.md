# Staqex v1 Resource estimation and feasibility plan (LISS-0091)

| Field | Value |
|---|---|
| Status | **complete** — integrated Red/Green/Refactor; final PR/merge on branch |
| Authority | WP-0025 E3; WP-0029 P1-A; ADR 0100 (separate host budget); ADR 0108–0111 Accepted non-authorizations |
| Depends on | LISS-0083 complete; LISS-0087 complete; LISS-0090 complete |
| Blocks | LISS-0092 |
| Shipping target | Python package `compiler/staqex` |
| Issue | [LISS-0091](../issues/LISS-0091-resource-estimation-feasibility.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0091-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive, immutable Algorithm Plan resource
  estimation and feasibility reporting with typed semantic/logical/physical
  categories, distinct pre/post-routing stages, exact-or-symbolic large
  quantities, and compositional Unknown budgets; no provider or routing
  execution.
- Specifications and files inspected: LISS-0091 Issue; WP-0025 Current next
  and E3 row; WP-0029 P1-A; ADR 0100 / resource_profile.py;
  algorithm_plan_ir.ResourceExpr; quantum-capacity / current-hardware
  envelopes; LISS-0087/0090 integrated-package pattern; bounded packet.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  new resource_estimate.py over immutable DTOs; Quantity / Unknown /
  EstimateProvenance / PreRoutingEstimate / PostRoutingEstimate /
  CompositionalBudget / FeasibilityReport; no file/network/provider/RNG
  adapters; no merger with SimulationResourceEstimate.
- Applicable constraints: Clean Architecture; Never Leave the State;
  AT-TDD Adjudicator gates; ADR 0110/0111 non-authorizations; LISS-0092 not
  required for DTO/post-routing Unknown contracts.
- Decisions, assumptions, and unresolved ambiguities: A–E are internal
  review dimensions of one Issue (four approvals only); soft CompileResult
  wire is in-scope for the same Issue if Red covers it; concrete formula
  constants remain versioned strings, not language maxima; no new ADR unless
  Architecture review discovers a missing decision.
- Included and omitted AI context: include Issue/spec/WP, Algorithm Plan
  ResourceExpr, ADR 0100 boundary, horizon profile names; omit provider
  SDKs, credentials, pricing tables, routing algorithms, unrelated evaluator
  internals.
- Task routing (model/assistant/tool): design synthesis by capable assistant;
  Red/Green later on Shipping Kernel Python with deterministic tests.
- Input/output evidence contract when AI output is involved: repository
  artifacts in; reviewable DTO contracts and fixtures out; no hidden
  reasoning as runtime evidence.
- Verification plan: link/path and claim sync, prohibited-boundary search,
  git diff --check; no compiler source or tests in this intake.
```

## 1. Boundary

```text
AlgorithmPlanModule (+ optional synthetic TargetProfileSnapshot)
  -> ResourceEstimateInput
  -> resource estimate / feasibility UseCase (immutable DTOs)
  -> ResourceEstimateReport / FeasibilityReport
  -> later LISS-0092 post-routing fill-in
  -> later LISS-0099 live target ports (not this Issue)
```

LISS-0091 records **estimates and feasibility evidence**. It does not:

- choose algorithms, synthesize circuits, or allocate shots
  (0088–0090);
- perform layout, SWAP insertion, or native scheduling (0092);
- load provider prices, calibration, or SDKs (0100 / live adapters);
- reinterpret Semantic IR or invent finite carriers;
- enforce host simulator binder memory budgets (ADR 0100 /
  `SimulationResourceEstimate` remains separate).

## 2. Proposed DTO vocabulary

Names are design candidates, not implementation authorization.

- `ResourceCategory`: `semantic` | `logical` | `physical` (typed; no mixed
  bag of fields without category).
- `ResourceQuantity`: exact non-negative `int`, or symbolic string; never an
  implicit float downgrade for counts beyond u64 range.
- `Unknown`: named unknown with required compositional assumptions.
- `EstimateProvenance`: formula/version id, assumptions, uncertainty note,
  and optional profile snapshot id.
- `PreRoutingEstimate`: logical/simulator-oriented quantities before topology
  mapping; stage tag `pre_routing`.
- `PostRoutingEstimate`: physical quantities after mapping; stage tag
  `post_routing`; may be entirely `Unknown` until LISS-0092 supplies
  evidence.
- `CompositionalBudget`: failure / decoder / link / factory / memory / time /
  power / cost entries; each may be quantity or Unknown with assumptions.
- `TargetProfileSnapshot`: synthetic immutable profile id and declared
  capability fields used for feasibility comparison (CH1 / NH5 / QP-2 /
  QS-2 fixtures).
- `FeasibilityReport`: per-profile pass/reject with exceeded dimensions and
  no silent alternative selection.
- `ResourceEstimateReport`: closed package of estimates, budgets, provenance,
  and optional feasibility reports.

`algorithm_plan_ir.ResourceExpr` remains the plan-side symbolic resource
expression. LISS-0091 may **consume** those strings as inputs to structured
estimates; it must not mutate Algorithm Plan modules.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Category separation | constructing mixed-category bags fails closed |
| Pre vs post routing | distinct stage tags; assumptions + uncertainty + profile snapshot present |
| Beyond u64 | exact `int` / symbolic survive round-trip; float coercion rejected |
| Compositional budgets | Unknown allowed; missing assumptions rejected |
| Feasibility | synthetic CH1/NH5/QP-2/QS-2 fixtures; reject names the exceeded dimension |
| ADR 0100 isolation | no import/alias that treats `SimulationResourceEstimate` as a plan resource |
| Soft wire (optional same Issue) | empty/absent input yields no invented carriers; soft diagnostic codes outside hard set |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | quantity / Unknown / provenance DTOs |
| B | logical + pre-routing estimate construction |
| C | physical + post-routing (Unknown-capable) |
| D | compositional FTQC/network/factory budgets |
| E | feasibility reports vs synthetic profiles |

## 5. Approval unit

1. Plan intake — this document + Issue rewrite (**this step**)
2. Architecture + Phase 1 Red (bundled)
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

No per-dimension Slice approvals. Soft compile attachment, if included, is
not a separate Slice F gate.

## 6. Candidate write paths (post-Red)

Allowed after Architecture + Red approval:

- `compiler/staqex/resource_estimate.py`
- `tests/test_resource_estimate_integrated_red.py`
- optional soft fields on `CompileResult` / `pipeline.py` within the same
  Issue packet
- Issue / plan / WP / trace status synchronization

Forbidden until later Issues authorize them:

- provider adapters, pricing, calibration fetch
- LISS-0092 routing algorithms
- changing ADR 0100 host budget semantics
- language syntax for resource limits

## 7. Explicit non-goals

- Numerical solving, gate expansion, or Jordan–Wigner execution
- Live QPU submission or capability discovery
- Treating ADR 0109–0111 envelope numbers as delivery forecasts
- Implicit remote fallback when local feasibility fails
- Replacing host `staqex.toml` simulator memory policy

## 8. Verification for this intake

- Issue, plan, WP-0025 Current next, local-issue-planning claim, and
  open-work-register row agree on integrated gates and ADR 0100 boundary.
- No `compiler/` or `tests/` mutations in the intake commit set.
- `git diff --check` clean on documentation edits.
