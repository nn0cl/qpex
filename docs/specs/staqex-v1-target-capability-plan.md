# Staqex v1 Target capability plan (LISS-0099)

| Field | Value |
|---|---|
| Status | **complete** — PR #165 (`ad89d15`); integrated Red/Green/Refactor |
| Authority | WP-0025 E4/E3; WP-0029 P0-B; ADR 0108–0111 Accepted non-authorizations |
| Depends on | LISS-0082 complete; LISS-0067 complete; LISS-0092 complete (consumer) |
| Blocks | LISS-0100; LISS-0102 |
| Shipping target | Python package `compiler/staqex` |
| Issue | [LISS-0099](../architecture/documentation-compression-map.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0099-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive, immutable versioned target capability
  profiles plus a provider-neutral PhysicalTargetPort with fake adapters and
  CH0/CH1/NH5 fixtures; unknown/stale facts stay explicit; no implicit
  fallback; no Semantic IR leakage.
- Specifications and files inspected: LISS-0099 Issue; WP-0025 Current next;
  WP-0029 P0-B; LISS-0092 target_routing.TargetSnapshot; LISS-0082 handoff;
  ADR 0110/0111; LISS-0087/0091/0092 integrated packages; bounded packet.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  new target_capability.py; TargetCapabilityProfile, Freshness,
  CapabilityUnknown, PhysicalTargetPort protocol, FakePhysicalTargetPort;
  optional project_to_routing_snapshot(); no network/SDK/credentials.
- Applicable constraints: Clean Architecture ports; Never Leave the State;
  AT-TDD gates; provider data adapter-owned; local insufficiency ≠ remote.
- Decisions, assumptions, and unresolved ambiguities: A–E are internal
  dimensions (four approvals); first Technology selection for a live provider
  remains LISS-0100; freshness policy uses explicit age/unknown rather than
  hidden clocks in Domain; no new ADR unless Architecture requires one.
- Included and omitted AI context: include Issue/spec/WP, 0092 snapshot DTO,
  CH0/CH1/NH5 names; omit provider SDKs, credentials, calibration blobs.
- Task routing (model/assistant/tool): design synthesis by capable assistant;
  Red/Green later on Shipping Kernel Python with deterministic tests.
- Input/output evidence contract when AI output is involved: repository
  artifacts in; reviewable DTO/port contracts out; no hidden reasoning as
  runtime evidence.
- Verification plan: link/path and claim sync, prohibited-boundary search,
  git diff --check; no compiler source or tests in this intake.
```

## 1. Boundary

```text
FakePhysicalTargetPort / (later) provider adapter
  -> TargetCapabilityProfile (versioned, immutable)
  -> verify_capability_profile / support_or_reject
  -> optional project_to_routing_snapshot
  -> LISS-0092 run_target_pipeline
```

LISS-0099 records **what a target claims to support**. It does not:

- route, schedule, or insert SWAPs (LISS-0092);
- submit jobs or authenticate (LISS-0100 / 0102);
- rewrite Semantic / Physics / Theory IR;
- invent missing calibration as defaults.

## 2. Proposed DTO / port vocabulary

Names are design candidates, not implementation authorization.

- `Freshness`: `fresh` | `stale` | `unknown` plus optional age token.
- `CapabilityUnknown`: named unknown with required reason.
- `TargetCapabilityProfile`: identity, schema version, profile id
  (CH0/CH1/NH5), native ops, connectivity, measurement/reset, timing,
  dynamic support, carrier/computation-model, capacities, deployment policy,
  resource/power/memory policies, freshness, unknowns.
- `SupportDecision`: `supported` | `rejected` with exceeded/missing dims and
  `selected_alternative is None`.
- `PhysicalTargetPort`: protocol `load_profile(profile_id) -> TargetCapabilityProfile`.
- `FakePhysicalTargetPort`: in-memory fixture map for CH0/CH1/NH5.
- `project_to_routing_snapshot(profile) -> target_routing.TargetSnapshot`:
  pure projection; may omit richer fields that routing does not consume.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Versioned distinctions | profile fields cover native/connectivity/measure/timing/dynamic/carrier/model |
| Explicit unknown/stale | stale/unknown reject or surface without inventing values |
| Adapter-owned / no fallback | Fake port only; reject sets `selected_alternative is None` |
| Shared schema fixtures | CH0/CH1/NH5 load from one schema; deterministic support evidence |
| IR isolation | module text has no physics_ir / quantum_semantic_ir imports |
| 0092 bridge | projection yields a snapshot accepted by routing for a CH1 fixture |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | identity / version / freshness / unknown |
| B | digital ops / topology / timing / dynamic |
| C | computation-model / qudit / analog flags |
| D | deployment / resource / power / consent policies |
| E | port + fake adapter + CH0/CH1/NH5 fixtures |

## 5. Approval unit

1. Plan intake — this document + Issue rewrite (**this step**)
2. Architecture + Phase 1 Red (bundled)
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

## 6. Candidate write paths (post-Red)

- `compiler/staqex/target_capability.py`
- `tests/test_target_capability_integrated_red.py`
- Issue / plan / WP / trace status synchronization

Forbidden until later Issues authorize them:

- live provider SDK / credentials / network
- Semantic IR target fields
- changing LISS-0092 routing semantics (projection-only coupling)

## 7. Explicit non-goals

- First live provider selection (LISS-0100)
- Job/session orchestration (LISS-0102)
- OpenQASM emission completion (LISS-0097)
- Treating envelope numbers as delivery forecasts

## 8. Verification for this intake

- Issue, plan, WP-0025 Current next, local-issue-planning claim, and
  open-work-register row agree on integrated gates and 0092 projection
  boundary.
- No `compiler/` or `tests/` mutations in the intake commit set.
- `git diff --check` clean on documentation edits.
