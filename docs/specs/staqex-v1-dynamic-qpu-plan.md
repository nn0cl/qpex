# Staqex v1 Dynamic QPU controller plan (LISS-0077 P0 package)

| Field | Value |
|---|---|
| Status | **complete** — P0 integrated Red/Green/Refactor; final PR/merge on branch |
| Authority | WP-0025 E1/P0-B; WP-0029 P0-B; ADR 0071 Accepted; ADR 0106 D2/D12 refine; ADR 0108–0111 non-authorizations |
| Depends on | LISS-0075/0076 **complete**; LISS-0082 **complete** (Dynamic marker handoff); LISS-0094 **complete** (fake SIM path available) |
| Blocks | LISS-0096; LISS-0097 deferred dynamic emission (E) |
| Shipping target | Python package `compiler/staqex` |
| Issue | [LISS-0077](../architecture/documentation-compression-map.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0077-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: one P0 integrated package for Dynamic QPU
  controller/feed-forward contracts — lane/type markers, finite match +
  one-merge correlation, reset/reuse capability obligations, and Fake
  simulator execution under supplied outcomes — without weakening Static
  Kernel terminal measurement.
- Specifications and files inspected: LISS-0077 Issue; WP-0025 Current next;
  WP-0029 P0-B; ADR 0071; ADR 0106 dynamic-lane refine; LISS-0082 Dynamic
  marker handoff; LISS-0028 rejection boundary; LISS-0094/0097 integrated
  package pattern; bounded packet.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  proposed compiler/staqex/dynamic_qpu.py; ControllerValue, OutcomeToken,
  MatchPlan, MergeObligation, DynamicCapabilityDemand, DynamicExecRequest,
  DynamicExecResult, FakeDynamicExecutor; read-only Semantic IR / evaluator /
  QASM by default.
- Applicable constraints: Never Leave the State for Static; Controller cannot
  escape phase, alter shape, enter Theory, or select deployment/provider;
  no silent Host emulation of unsupported dynamic features (ADR 0071);
  AT-TDD gates; no provider SDK/credentials/network.
- Decisions, assumptions, and unresolved ambiguities: A–D are internal
  dimensions (four approvals). Slice E (portable dynamic artifact / target
  metadata) is deferred follow-up that unlocks LISS-0097 dynamic emission.
  This package is contract + verifier + Fake execution first; full surface
  parser/`dynamic qpu fn` AST wiring is not required to land Red if requests
  are expressed as verified DTO fixtures (parser wire remains an explicit
  follow-up if Architecture demands it mid-Red). Timing model stays demand
  flags + reject, not a full scheduler.
- Included and omitted AI context: include Issue/WP/ADR 0071/0106 handoff,
  SIM0/CH1 profile names; omit provider SDKs, full OpenQASM dynamic grammar,
  JobResult composition redesign, live QPU submit.
- Task routing (model/assistant/tool): design synthesis by capable assistant;
  Red/Green later on Shipping Kernel Python with deterministic tests.
- Input/output evidence contract when AI output is involved: repository
  artifacts in; reviewable controller/exec contracts out; no hidden reasoning
  as runtime evidence.
- Verification plan: link/path and claim sync, prohibited-boundary search,
  git diff --check; no compiler source or tests in this intake.
```

## 1. Boundary

```text
Dynamic lane request (DTO fixture / later AST wire)
  -> lane + escape verifier (Static/Theory/shape/provider forbidden)
  -> finite match + one-merge correlation check
  -> capability obligations (reset/reuse/latency flags)
  -> FakeDynamicExecutor.execute(request, supplied_outcomes)
  -> DynamicExecResult (deterministic) | stable rejection
```

LISS-0077 P0 records **controller/feed-forward meaning and Fake execution**.
It does not:

- weaken Static Kernel terminal `measure`;
- emit OpenQASM dynamic regions (LISS-0097-E after this contract);
- select engines (LISS-0095) or mixed-state physics (LISS-0096);
- submit to live providers (LISS-0100);
- silently emulate unsupported dynamic features on the Host.

## 2. Proposed DTO / port vocabulary

Names are design candidates, not implementation authorization.

- `ControllerValue`: phase-local classical controller carrier; not `State`.
- `OutcomeToken`: finite mid-circuit outcome identity paired to one Joint
  generation / correlation id.
- `MatchPlan`: finite arms over an `OutcomeToken`; no open-ended classical
  control.
- `MergeObligation`: exactly-one-merge consumer for the correlated post-measure
  Joint/token pair.
- `DynamicCapabilityDemand`: reset/reuse/latency/feedback flags required by
  the program.
- `DynamicExecRequest`: lane marker, tokens, match/merge plans, capability
  demand, supplied outcome map, profile id (`SIM0_EXACT` / `CH1_DIGITAL_RESEARCH`).
- `DynamicExecResult`: status, consumed tokens, final classical bindings,
  diagnostics; never claims physical execution.
- `FakeDynamicExecutor`: deterministic execution under supplied outcomes only.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Static remains closed | Static-lane request with controller/token rejects; terminal-measure contract untouched (no evaluator edit) |
| Token/Joint one-merge | correlated token + merge obligation verifies; double-merge / unpaired token reject |
| Controller escape forbidden | Theory/shape/provider/deployment selection attempts reject with stable codes |
| Deterministic supplied outcomes | Fake executor returns deterministic bindings for supported SIM0 fixture |
| Unsupported capabilities | reset/reuse/latency demands beyond profile reject without fallback |
| Isolation | module text has no provider SDK / network / Semantic mutation imports |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | lane/type markers and escape diagnostics |
| B | finite match, correlation, and one-merge verifier |
| C | reset/reuse and capability obligations |
| D | Fake simulator execution under supplied outcomes |

Deferred outside this package:

| Deferred | Reason |
|---|---|
| E portable dynamic artifact / target metadata | follow-up; unlocks LISS-0097 dynamic emission |
| Full AST/`dynamic qpu fn` parser wire | optional follow-up if DTO fixtures are insufficient for Architecture |

## 5. Approval unit

1. Plan intake — this document + Issue rewrite (**this step**)
2. Architecture + Phase 1 Red (bundled; P0 package only)
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

## 6. Candidate write paths (post-Red)

- `compiler/staqex/dynamic_qpu.py`
- `tests/test_dynamic_qpu_integrated_red.py`
- Issue / plan / WP / trace status synchronization

Read-only by default:

- `quantum_semantic_ir.py`, evaluator, QASM backend (`ch0_emit.py` stays
  fail-closed for dynamic until 0097-E)

Forbidden until later approvals:

- provider SDKs / credentials / network
- Host silent emulation of unsupported dynamic features
- OpenQASM dynamic emission
- Static Kernel law changes

## 7. Explicit non-goals

- Mixed/channel dynamics (LISS-0096)
- Live QPU feed-forward (LISS-0100)
- JobResult composition redesign beyond Fake result DTOs
- Replacing ADR 0071 lane separation
