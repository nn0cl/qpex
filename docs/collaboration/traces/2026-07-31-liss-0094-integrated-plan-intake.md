# LISS-0094 integrated plan intake

## Design check

- Scope: reorganize LISS-0094 from five independently gated slices into one
  simulator-port / capability-profile implementation unit with five internal
  review dimensions; minimize Adjudicator approvals to four.
- Inspected: LISS-0094 Issue, WP-0025 Current next and E4 row, WP-0029 P0-B,
  delivery envelope SIM0/SIM1, compiler blueprint §6.1 SimulatorPort,
  LISS-0082/0083 handoff, LISS-0095 engine non-authorization, LISS-0091/
  0092/0099 integrated-package pattern, `target_capability.py` placement,
  bounded packet, Definition of Done, and branch/PR discipline.
- Included: capability/request/result/rejection VOs, SimulatorPort + fake
  adapter, seed/budget/observation contracts, SIM0_EXACT/SIM1_MIXED
  fixtures, pre-allocation rejection, simulation-labelled results.
- Excluded: engine Technology selection (0095), dynamic/mixed semantics
  beyond flags (0096), OpenQASM (0097), provider SDKs, Semantic IR mutation,
  replacing the live Kernel SV evaluator in this Issue.
- Decision: A–E are internal dimensions only. The LISS uses four approvals:
  plan intake, integrated Architecture + Red, Green, Refactor + final
  PR/merge. Preferred write path is `compiler/staqex/simulator_port.py`.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  are synchronized before Phase 1 Red; no implementation or tests are
  authorized by this intake.

## Rationale

Capability negotiation, budgets, seeds, observation refs, and result
labelling share one safety boundary: unsupported or over-budget work must
fail closed before allocation, and simulation evidence must never be
mislabelled as physical. Separate Slice gates would repeat the same
isolation review across fixtures and port shapes.

## Also synchronized in this intake

- LISS-0099 completion wording: PR #165 merge tip `ad89d15` (was still
  “pending merge” in some docs).

## Next approval

None for LISS-0094 after merge. Current next advances to LISS-0097
design intake (OpenQASM static CH0 subset).

## Artifacts produced by this intake

- [LISS-0094](../../issues/LISS-0094-simulator-port-capability-profiles.md)
  rewritten as integrated package
- [staqex-v1-simulator-port-plan.md](../../specs/staqex-v1-simulator-port-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0094-simulator-port`

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_simulator_port_integrated_red.py` and Issue/status
  docs only.
- Coverage: eleven deterministic tests spanning capability VOs, fake port
  fixtures, validate/execute contracts, budgets, observation refs, SIM0/SIM1,
  isolation, and fail-closed unknowns.
- Expected result: Red by missing `compiler.staqex.simulator_port`;
  `0 passed, 11 failed` with ModuleNotFoundError.
- Stop condition: Phase 2 Green is not authorized by the Red approval.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/simulator_port.py`; Red suite
  `11 passed, 0 failed`.
- Excluded: engine packages, credentials, network.
- Stop condition: Refactor not authorized by Green alone.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Changed: split fixture helpers and validation helpers; behavior unchanged.
- Integrated Red: 11 passed / 0 failed after Refactor.
