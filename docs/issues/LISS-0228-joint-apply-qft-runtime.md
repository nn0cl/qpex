# LISS-0228: Joint `apply(qft/iqft/cqft, …)` runtime

## Metadata

- Local issue ID: LISS-0228
- GitHub issue: (none yet)
- Status: **complete**
- Phase: Phase 3 complete
- Type: feature
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: Cursor agent
- Related branch: `batch/wp-0072-s01-coverage-residuals`
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

Dense exact QFT/IQFT/CQFT matrices for Joint `apply(F, w…)`. In-place multi-wire
`state (a,b) = apply(F,a,b)` LINEAR revive + runtime multi-bind.

## Acceptance Notes

- [x] Spec (EARS/Gherkin)
- [x] Red: qft∘iqft + cqft apply
- [x] Green dense factory + apply path
- [x] S01 `main_burst_spectrum.sqx` uses apply
- [x] Scorecard Honesty updated at ship

## Dependencies

- Spec: [staqex-v1-liss-0228-joint-apply-qft-runtime.md](../specs/staqex-v1-liss-0228-joint-apply-qft-runtime.md)

## Verification

- `python3 tests/test_liss_0228_joint_apply_qft_runtime_red.py`
- `python3 -m compiler.staqex run …/main_burst_spectrum.sqx --seed 0`
