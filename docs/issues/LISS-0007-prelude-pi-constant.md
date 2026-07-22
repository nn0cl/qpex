# LISS-0007: Prelude classical constant `pi`

## Metadata

- Local issue ID: LISS-0007
- GitHub issue: none
- Status: **done** (2026-07-23)
- Phase: Feature Path — Green
- Type: feature + DX
- Priority: P2 (QoL; follow-on to LISS-0006 deferred item)
- Initial planning size: S
- Current planning size: S
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Register prelude classical `pi` (ADR 0062) and replace magic float literals in
official examples / related fixtures.

## Acceptance Notes

- [x] `PRELUDE_CONSTANTS["pi"]` in `stdlib/prelude.py`
- [x] Evaluator + typechecker + unitarity seed `pi`
- [x] `Math.pi` Attr alias of the same classical constant
- [x] `State ⊕ pi` → static reject (`TYPE_MISMATCH` / `EXPECT_CLASSICAL_ONLY_ERROR`)
- [x] `phase(..., pi)` / `pi / 2.0` / `Math.pi` work
- [x] Examples + SV fixtures replaced
- [x] `tests/test_prelude_pi.py`
- [x] SV suite green

## Dependencies

- Parent: [LISS-0006](LISS-0006-examples-catalog-honesty.md) (deferred QoL)
- Related: ADR 0031, [ADR 0062](../architecture/adr/0062-prelude-pi-constant.md)

## Verification

- Unit + `python3 tests/spec_verification/run_all.py`
