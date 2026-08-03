# AI work trace: H1 State Transformer H1-7 final review

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `codex/state-transformer-language-review` |
| Canonical issue | None identified; acceptance specifications are the review boundary |
| Current phase | Phase 3 — Refactor complete; final-review-ready |

## Scope

This review covers the H1-4 through H1-7 State Transformer slices:

- ordered H1 state-transform plan;
- static/dynamic control-lane classification;
- operation characteristics (`Unitary`, `Adj`, `Ctl`);
- explicit lifetime distinction between `trace_out` disposal and witnessed
  `uncompute`.

Automatic uncompute synthesis, optimizer lifetime shortening, QPU-specific
disposal, and new effect rows remain out of scope.

## Decisions and assumptions

- `trace_out` is an irreversible disposal step and never receives `Adj` or
  `Unitary` characteristics.
- `uncompute` requires the reviewed `witness` marker and records an existing
  `UncomputeObligation`; witness payload elaboration remains future work.
- Existing linear verification remains authoritative and is not replaced by
  the H1 authoring boundary.
- No canonical Issue or work-plan row was identified in the recovered
  repository artifacts; the accepted H1 specifications are the governing
  design records for this bounded slice.

## Verification

- `/usr/local/bin/python3.12 -m pytest tests/ -q` — `1187 passed`.
- `python3 tests/spec_verification/run_all.py` — `161/161`, Gate PASS.
- `python3 -m compileall -q compiler tests` — passed.
- `git diff --check` — passed.

## Changed artifacts

- `compiler/staqex/ast_nodes.py`
- `compiler/staqex/parser.py`
- `compiler/staqex/h1_authoring.py`
- `compiler/staqex/pipeline.py`
- `docs/specs/staqex-h1-4-state-transform-plan-acceptance.md`
- `docs/specs/staqex-h1-5-control-lane-classification-acceptance.md`
- `docs/specs/staqex-h1-6-operation-characteristics-acceptance.md`
- `docs/specs/staqex-h1-7-lifetime-and-disposal-acceptance.md`
- `tests/test_h1_4_state_transform_plan_red.py`
- `tests/test_h1_5_control_lane_classification_red.py`
- `tests/test_h1_6_operation_characteristics_red.py`
- `tests/test_h1_7_lifetime_and_disposal_red.py`

## Reviewer empathy summary

The implementation keeps the physicist-facing distinction visible in the
plan: disposal is not presented as reversal, and reversal is not accepted
without evidence. The provider-neutral plan and Semantic IR remain separate,
so later lowering can add execution policy without changing the language
surface.

## Next safe action

Human final review of the complete uncommitted change set, followed by an
explicit commit/PR decision. No merge or status promotion is implied by this
trace.
