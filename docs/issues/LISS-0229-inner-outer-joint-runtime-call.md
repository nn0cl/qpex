# LISS-0229: `inner` / `outer` Joint runtime Call

## Metadata

- Local issue ID: LISS-0229
- Status: **complete**
- Phase: Phase 3 complete
- Type: feature
- Priority: P1
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)
- Spec: [staqex-v1-liss-0229-inner-outer-joint-runtime-call.md](../specs/staqex-v1-liss-0229-inner-outer-joint-runtime-call.md)

## Acceptance Notes

- [x] Spec + Red + Green
- [x] S01 fidelity main runnable
- [x] Scorecard Honesty updated at ship

## Verification

- `python3 tests/test_liss_0229_inner_outer_joint_runtime_call_red.py`
- `python3 -m compiler.staqex run …/main_fidelity_inner_check.sqx --seed 0`
