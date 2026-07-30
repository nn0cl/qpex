# LISS-0091 integrated plan intake

## Design check

- Scope: reorganize LISS-0091 from five independently gated slices into one
  resource-estimation / feasibility implementation unit with five internal
  review dimensions; minimize Adjudicator approvals to four.
- Inspected: LISS-0091 Issue, WP-0025 E3 row and Current next, WP-0029 P1-A,
  ADR 0100 and `resource_profile.SimulationResourceEstimate`,
  `algorithm_plan_ir.ResourceExpr`, capacity/delivery envelopes, LISS-0087 /
  0090 integrated-package pattern, bounded execution packet, Definition of
  Done, and branch/PR discipline.
- Included: typed semantic/logical/physical categories, pre/post-routing
  stage separation, exact-or-symbolic large quantities, compositional
  Unknown budgets, synthetic CH1/NH5/QP-2/QS-2 feasibility fixtures, optional
  same-Issue soft CompileResult wire.
- Excluded: layout/routing (0092), provider prices/SDK/calibration, live
  target ports (0099), host simulator budget merger (ADR 0100), semantic
  reinterpretation, language maxima, implicit fallback.
- Decision: A–E are internal dimensions only. The LISS uses four approvals:
  plan intake, integrated Architecture + Red, Green, Refactor + final
  PR/merge.
- Verification: Issue, spec, WP, dependency, branch, and status terminology
  are synchronized before Phase 1 Red; no implementation or tests are
  authorized by this intake.

## Rationale

The five dimensions share one safety boundary: estimates must keep categories
and routing stages distinct, carry provenance and assumptions, and never
silently invent carriers, prices, or fallback targets. Separate Slice gates
would repeat the same quantity/budget review and invite incompatible DTO
vocabularies across pre-routing, post-routing, and feasibility reports.

## Next approval

Final PR/merge for LISS-0091. After merge, Current next advances to
LISS-0092 design intake.

## Phase 1 Red evidence

- Approval: integrated Architecture + Phase 1 Red, received 2026-07-31.
- Changed: `tests/test_resource_estimate_integrated_red.py` and Issue/status
  docs only.
- Coverage: twelve deterministic tests spanning immutable quantity/category
  contracts, pre/post routing, Unknown/budget assumptions, feasibility
  fixtures, ADR 0100 isolation, and soft absent input.
- Expected result: Red by missing `compiler.staqex.resource_estimate`; no
  implementation module was created and no assertion was weakened.
- Verification: test source compiles; direct execution reports
  `0 passed, 12 failed` with ModuleNotFoundError; `git diff --check` is clean.
- Stop condition: Phase 2 Green is not authorized by the Red approval and
  remains gated pending review of this suite.

## Phase 2 Green evidence

- Approval: integrated Phase 2 Green, received 2026-07-31.
- Changed: `compiler/staqex/resource_estimate.py`; Red suite
  `12 passed, 0 failed`.
- Fixture note: Red helper aligned Unknown assumptions for
  `physical_qubits` to the frozen assertion
  (`awaiting-liss-0092-routing`); acceptance unchanged.
- Excluded: provider SDK/prices, LISS-0092 routing, ADR 0100 merger,
  CompileResult pipeline soft wire.
- Stop condition: Refactor not authorized by Green alone.

## Phase 3 Refactor evidence

- Approval: Phase 3 Refactor + final PR/merge, received 2026-07-31.
- Changed: split verification and default builders; behavior unchanged.
- Integrated Red: 12 passed / 0 failed after Refactor.
- Related regressions remain green.

## Artifacts produced by this intake

- [LISS-0091](../../issues/LISS-0091-resource-estimation-feasibility.md)
  rewritten as integrated package
- [staqex-v1-resource-estimation-plan.md](../../specs/staqex-v1-resource-estimation-plan.md)
- WP-0025 / local-issue-planning / open-work-register synchronization
- Branch: `feature/liss-0091-resource-estimation`
