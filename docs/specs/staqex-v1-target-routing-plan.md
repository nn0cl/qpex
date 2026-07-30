# Staqex v1 Target routing plan (LISS-0092)

| Field | Value |
|---|---|
| Status | **complete** — PR #163 merged (`afdbfa9`) |
| Authority | WP-0025 E3; WP-0029 P1-A; ADR 0108–0111 Accepted non-authorizations |
| Depends on | LISS-0089 complete; LISS-0091 complete; LISS-0099 deferred (synthetic snapshots) |
| Shipping target | Python package `compiler/staqex` |
| Issue | [LISS-0092](../issues/LISS-0092-layout-routing-native-scheduling.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0092-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive, immutable target-planning pipeline
  with ordered layout → routing → native translation → schedule stages,
  provenance, logical identity survival, and explicit infeasibility; no
  provider or Theory mutation.
- Specifications and files inspected: LISS-0092 Issue; WP-0025 Current next;
  WP-0029 P1-A; LISS-0099 Issue (port deferred); LISS-0091 resource estimate
  post-routing Unknown pattern; LISS-0087/0090/0091 integrated packages;
  bounded packet; capacity/delivery envelopes.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  new target_routing.py over immutable DTOs; TargetSnapshot (synthetic),
  LayoutResult, RoutingResult, NativeTranslation, ScheduleResult,
  TargetPipelineResult; no file/network/provider/RNG adapters; no Semantic
  IR mutation.
- Applicable constraints: Clean Architecture; Never Leave the State;
  AT-TDD Adjudicator gates; ADR 0110/0111 non-authorizations; target
  constraints never flow into Theory/Physics/Semantic.
- Decisions, assumptions, and unresolved ambiguities: A–E are internal
  review dimensions (four approvals); LISS-0099 live port deferred — synthetic
  TargetSnapshot fixtures authorize Red/Green without Technology selection;
  deterministic routing policy is explicit and versioned; no new ADR unless
  Architecture review requires one.
- Included and omitted AI context: include Issue/spec/WP, 0091/0099
  boundaries, CH1/NH5 profile names; omit provider SDKs, credentials,
  calibration tables, heuristic search catalogs.
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
Logical plan fragment (+ synthetic TargetSnapshot)
  -> layout
  -> routing / SWAP records
  -> native translation
  -> schedule / barriers
  -> TargetPipelineResult (+ post-routing evidence for LISS-0091)
```

LISS-0092 records **target-stage planning evidence**. It does not:

- rewrite Theory, Physics IR, or Semantic IR;
- fetch live capability or calibration (LISS-0099 / adapters);
- choose providers or submit jobs (LISS-0100 / 0102);
- invent semantic carriers or finite Hilbert facts.

## 2. Proposed DTO vocabulary

Names are design candidates, not implementation authorization.

- `TargetSnapshot`: versioned immutable connectivity, native ops, timing,
  measurement/reset, and concurrency facts (synthetic fixtures for this Issue).
- `LogicalResourceId`: stable identity that must survive all stages.
- `LayoutResult`: logical→physical map + topology validation provenance.
- `InsertedOperation`: SWAP or other insertion with justification ids.
- `RoutingResult`: ordered insertions + surviving logical identities.
- `NativeTranslation`: logical/native op pairs + reject reasons.
- `ScheduleResult`: timing/barrier records + concurrency assumptions.
- `TargetPipelineResult`: ordered stage outputs, overall status
  (`verified` | `infeasible`), diagnostics, and provenance chain.
- Diagnostic codes: `TARGET_*` hard rejects; soft codes if any stay outside
  the compile hard set.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Ordered stages | pipeline exposes layout → routing → native → schedule with provenance |
| Snapshot-only constraints | missing/invalid snapshot rejects; no hidden defaults |
| Logical identity | resource ids equal before/after routing validation |
| Explicit infeasibility | disconnected topology / over-capacity → `infeasible` + codes |
| Theory isolation | module does not import/mutate Physics/Semantic IR modules |
| CH1/NH5 fixtures | synthetic snapshots exercise both profiles deterministically |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | stage/result DTOs |
| B | layout / topology validation |
| C | deterministic routing / SWAP records |
| D | native translation + post-route verifier |
| E | timing/barrier schedule + CH1/NH5 fixtures |

## 5. Approval unit

1. Plan intake — this document + Issue rewrite (**this step**)
2. Architecture + Phase 1 Red (bundled)
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

## 6. Candidate write paths (post-Red)

- `compiler/staqex/target_routing.py`
- `tests/test_target_routing_integrated_red.py`
- Issue / plan / WP / trace status synchronization

Forbidden until later Issues authorize them:

- LISS-0099 live ports and provider adapters
- calibration fetch, credentials, network
- Theory/Physics/Semantic mutation
- non-deterministic heuristic search without a reviewed policy ADR

## 7. Explicit non-goals

- Live QPU submission
- Error mitigation (LISS-0093)
- Host simulator memory budgets (ADR 0100)
- Treating envelope numbers as delivery forecasts

## 8. Verification for this intake

- Issue, plan, WP-0025 Current next, local-issue-planning claim, and
  open-work-register row agree on integrated gates and 0099 deferral.
- No `compiler/` or `tests/` mutations in the intake commit set.
- `git diff --check` clean on documentation edits.
