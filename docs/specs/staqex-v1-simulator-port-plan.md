# Staqex v1 Simulator port plan (LISS-0094)

| Field | Value |
|---|---|
| Status | **complete** — PR #166 (`b6d2dda`); integrated Red/Green/Refactor |
| Authority | WP-0025 E4; WP-0029 P0-B; ADR 0108–0111 Accepted non-authorizations |
| Depends on | LISS-0082 **complete**; LISS-0083 **complete** |
| Blocks | LISS-0095; LISS-0096; LISS-0104 |
| Shipping target | Python package `compiler/staqex` |
| Issue | [LISS-0094](../issues/LISS-0094-simulator-port-capability-profiles.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0094-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive, provider-neutral SimulatorPort with
  capability negotiation, explicit budgets/RNG/observation inputs, fake
  adapters, and SIM0_EXACT / SIM1_MIXED fixtures; reject over-budget or
  unsupported plans before allocation; results labelled simulation, never
  physical.
- Specifications and files inspected: LISS-0094 Issue; WP-0025 Current next /
  E4; WP-0029 P0-B; delivery envelope SIM* profiles; compiler blueprint §6.1;
  LISS-0082/0083 handoff; LISS-0095 engine non-authorization; LISS-0091/0092/
  0099 integrated packages; target_capability.py placement precedent;
  bounded packet; Definition of Done.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  proposed compiler/staqex/simulator_port.py; SimulatorCapabilityProfile,
  SimulationRequest, SimulationBudget, ObservationPlanRef, ValidationReport,
  SimulationResult, SimulatorPort protocol, FakeSimulatorPort; no engine
  packages, no provider SDKs, no Semantic IR mutation.
- Applicable constraints: Clean Architecture ports; Never Leave the State;
  AT-TDD gates; deterministic seed contract; fail-closed rejection without
  fallback; simulation ≠ physical evidence (ADR 0111 / envelope §6).
- Decisions, assumptions, and unresolved ambiguities: A–E are internal
  dimensions (four approvals); placement prefers Kernel module over a new
  ports/ tree to match 0091/0092/0099; LISS-0095 remains the only engine
  Technology selection; FakeSimulatorPort may return canned deterministic
  oracle payloads without importing the live SV evaluator; observation plan
  shape is a minimal ref/DTO, not a reimplementation of LISS-0044–0047.
- Included and omitted AI context: include Issue/spec/WP, SIM0/SIM1 bounds,
  blueprint SimulatorPort shape; omit engine shortlists, licenses,
  credentials, provider APIs, full Algorithm Plan IR dumps.
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
verified Algorithm Plan / Semantic projection (caller-owned)
  -> SimulatorPort.validate(plan, budget, capability)
  -> SimulatorPort.execute(plan, inputs, observation_plan, seed)  [only if valid]
  -> SimulationResult (execution_kind = "simulation")
```

LISS-0094 records **how a simulator backend is asked and answered**. It does
not:

- select or import a concrete engine (LISS-0095);
- implement dynamic/mixed physics beyond fixture capability flags (LISS-0096);
- submit jobs to physical targets (LISS-0099 / 0100 / 0102);
- rewrite Semantic / Physics / Theory / Algorithm Plan IR meaning;
- label simulation results as physical execution.

## 2. Proposed DTO / port vocabulary

Names are design candidates, not implementation authorization.

- `SimulatorCapabilityProfile`: profile id (`SIM0_EXACT` / `SIM1_MIXED`),
  schema version, supported carriers/ops, max qubits (fixture bounds),
  memory/budget limits, observation modes, dynamic support flag, exact vs
  mixed oracle class.
- `SimulationBudget`: qubit/memory/time/shot ceilings and optional tolerance;
  missing required fields remain explicit unknowns, not silent defaults that
  enlarge capacity.
- `ObservationPlanRef`: opaque/minimal reference to requested non-collapsing
  or terminal observations; unsupported modes reject before execute.
- `SimulationRequest`: plan handle/payload ref, profile id, budget, seed,
  observation plan, and provenance token.
- `ValidationReport`: `accepted` | `rejected` with exceeded/missing
  dimensions; `selected_alternative is None` (no implicit engine fallback).
- `SimulationResult`: `execution_kind="simulation"`, seed used, profile id,
  deterministic payload fields for the fake oracle, diagnostics.
- `SimulatorPort` (Protocol), aligned with blueprint §6.1:
  - `capabilities(profile_id) -> SimulatorCapabilityProfile`
  - `validate(request) -> ValidationReport`
  - `execute(request) -> SimulationResult` (must fail closed if validate
    would reject)
- `FakeSimulatorPort`: in-memory SIM0/SIM1 fixtures; deterministic seed
  echo; canned exact-oracle answers for bounded cases; reject over-budget.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Fake port submission | FakeSimulatorPort accepts a minimal verified-plan fixture; no engine type in Domain/module imports |
| Capability negotiation | unsupported carrier/op/memory/observation/dynamic rejects before execute |
| Explicit RNG / budgets / labels | seed propagates; budgets required; `execution_kind == "simulation"` |
| SIM0_EXACT oracle + over-budget | bounded fixture succeeds; over-budget rejects deterministically pre-allocation |
| SIM1_MIXED fixture | profile loads; mixed/dynamic beyond flags reject without fallback |
| IR / engine isolation | module text has no quantum_semantic_ir / physics_ir / provider / qiskit / cirq / pennylane imports |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | capability / request / result / rejection VOs |
| B | port + fake adapter + deterministic seed contract |
| C | observation plan ref and exact-oracle result contract |
| D | budget estimator / pre-allocation rejection |
| E | `SIM0_EXACT` / `SIM1_MIXED` fixtures |

## 5. Approval unit

1. Plan intake — complete
2. Architecture + Phase 1 Red — complete
3. Phase 2 Green — complete
4. Phase 3 Refactor + final PR/merge — complete (this step)

## 6. Candidate write paths (post-Red)

- `compiler/staqex/simulator_port.py` (preferred; matches 0091/0092/0099)
- `tests/test_simulator_port_integrated_red.py`
- Issue / plan / WP / trace status synchronization

Forbidden until later Issues authorize them:

- concrete engine packages or Technology selection (LISS-0095)
- live provider / QPU adapters
- Semantic IR simulator fields
- unbounded allocation or silent clamp of budgets

## 7. Explicit non-goals

- Engine shortlist, license, or performance bake-off (LISS-0095)
- Density/channel/dynamic execution semantics beyond capability flags
  (LISS-0096)
- OpenQASM emission (LISS-0097)
- Physical target profiles (LISS-0099 — already complete)
- Replacing the existing Shipping Kernel SV evaluator in this Issue; the port
  is the replaceable boundary those engines will later sit behind

## 8. Placement note

The Issue originally listed `ports/simulator.py`. Shipping Kernel peers place
port contracts beside their DTOs under `compiler/staqex/` (see
`target_capability.py`). This plan selects that precedent unless Architecture
review requires a separate `ports/` package.
