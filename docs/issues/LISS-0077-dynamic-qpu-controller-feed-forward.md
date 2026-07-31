# LISS-0077: Dynamic QPU controller and feed-forward

## Metadata

- Local issue ID: LISS-0077
- GitHub issue: not created
- Initial/current planning size: XL / L (P0 package) + deferred follow-ups
- Owner/agent: unassigned
- Adjudicator decision points: integrated controller/feed-forward contract;
  Architecture + Red, Green, Refactor, and final PR/merge
- Status/phase: **complete** / `phase-3-refactor` — P0 package complete;
  final PR/merge on this branch; Slice E deferred
- Type/priority/size: language + execution contract / P0 / XL (scoped P0 first)
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: LISS-0075/0076 **complete**; LISS-0082 **complete**; LISS-0094
  **complete** (Fake SIM path available)
- Blocks: LISS-0096; dynamic portions of LISS-0097 (after deferred Slice E)
- Branch: `feature/liss-0077-dynamic-qpu`
- Implementation permission: complete pending merge evidence
- Implementation: `compiler/staqex/dynamic_qpu.py`; tests:
  `tests/test_dynamic_qpu_integrated_red.py`
- Plan: [`docs/specs/staqex-v1-dynamic-qpu-plan.md`](../specs/staqex-v1-dynamic-qpu-plan.md)
- Intake trace:
  [`docs/collaboration/traces/2026-07-31-liss-0077-integrated-plan-intake.md`](../collaboration/traces/2026-07-31-liss-0077-integrated-plan-intake.md)
- LISS-0082 handoff: consume only the closed Dynamic lane marker, correlated
  post-measurement Joint/token identity, and shape-independent control
  boundary. Controller lifetime, timing, reset/reuse, and capability behavior
  remain owned by this Issue.

## Summary

Define Dynamic-lane controller/feed-forward contracts — `Controller<T>`
meaning, finite measurement feedback, reset/reuse obligations, and Fake
deterministic execution under supplied outcomes — without weakening Static
Kernel terminal measurement.

## Acceptance scenarios (P0 package)

1. Given a Static Kernel request, dynamic tokens and post-measure controller
   operations are rejected without changing existing terminal-measure behavior.
2. Given a dynamic measurement, its finite outcome token remains paired with
   the correlated post-measurement Joint identity and is consumed by one merge.
3. Controller values cannot escape their phase, alter shape, enter Theory, or
   select deployment/provider behavior.
4. Supported supplied outcomes are deterministic on Fake SIM0; unsupported
   feedback, latency, reset, or reuse capabilities produce stable rejection.

## Integrated P0 scope and boundaries

Former slices A–D are **internal review dimensions** of one P0
implementation unit. They are not separate approval points, branches, or
phase cycles.

| Review dimension | Scope | Profile |
|---|---|---|
| A — Lane | lane/type markers and escape diagnostics | `SIM0_EXACT` |
| B — Match | finite match, correlation, and one-merge verifier | `SIM0_EXACT` |
| C — Capability | reset/reuse and capability obligations | `CH1_DIGITAL_RESEARCH` |
| D — Fake exec | simulator execution under supplied outcomes | `SIM0_EXACT` |

### Deferred (not in this approval unit)

| Slice | Scope | Gate |
|---|---|---|
| E | target metadata and portable dynamic artifact contract | follow-up; unlocks LISS-0097 dynamic emission |
| Parser wire | full `dynamic qpu fn` AST wiring | optional follow-up if DTO fixtures insufficient |

Candidate writes (after Red approval):
`compiler/staqex/dynamic_qpu.py`,
`tests/test_dynamic_qpu_integrated_red.py`, and synchronized design artifacts.

Read-only by default: `quantum_semantic_ir.py`, evaluator, QASM backend.

### Forbidden

- provider SDKs, credentials, network
- implicit measurement / silent Host emulation of unsupported dynamic features
- Static Kernel terminal-measure relaxation
- runtime-dependent Hilbert shape from controllers
- OpenQASM dynamic emission in this package

Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Approval unit

Four approvals only for the P0 package:

1. Plan intake (this document + plan spec) — **complete** (this step)
2. Integrated Architecture + Phase 1 Red
3. Phase 2 Green
4. Phase 3 Refactor + final PR/merge

Slice E, AST parser wire, or Static law changes reopen Architecture review.

## Planning

- AIP-0077-001: proposed; L for the P0 package (XL Issue with deferred
  remainder); strong controller/merge review for the **integrated** packet,
  then code assistant for deterministic Red/Green/Refactor.

## Phase 1 Red evidence

- Approval: continuing remaining Issues (Architecture + Red implied), 2026-07-31.
- Changed: `tests/test_dynamic_qpu_integrated_red.py` and status docs; no
  `compiler/staqex/dynamic_qpu.py` at Red start.
- Coverage: ten tests spanning static-lane reject, escape paths, one-merge,
  unpaired/double-merge, CH1 capability rejects, SIM0 accept, Fake
  deterministic exec, reject without fallback, Controller≠State, isolation.
- Expected Red: missing module → `0 passed, 10 failed`.

## Phase 2 Green evidence

- Approval: continuing remaining Issues, 2026-07-31.
- Changed: `compiler/staqex/dynamic_qpu.py`; Red assertions unchanged.
- Integrated Red: 10 passed / 0 failed.
- Related regressions: simulator 11, CH0 OpenQASM 10, target capability 10.

## Phase 3 Refactor evidence

- Approval: continuing remaining Issues, 2026-07-31.
- Split reject/accept result builders; behavior unchanged.
- Integrated Red: 10 passed / 0 failed after Refactor.
- Completion evidence: recorded at merge time on this branch.
