# LISS-0003: Examples-driven Kernel brush-up (parent)

## Metadata

- Local issue ID: LISS-0003
- GitHub issue: none (local-only)
- Status: **done** (2026-07-23) — children closed; QoL follow-ons (LISS-0006/0007) also done
- Phase: Architecture Path → Feature Path — Green
- Type: epic / planning
- Priority: P0 (umbrella)
- Initial planning size: L
- Current planning size: L
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Examples 01–15 friction review drove ADR 0060/0061 Accept + Kernel P0 and
catalog honesty (LISS-0004…0006).

| Child | Focus | Status |
|-------|--------|--------|
| [LISS-0004](LISS-0004-joint-preservation-classical-env.md) | Joint preserve + classical `phase`/`times` | **done** |
| [LISS-0005](LISS-0005-classical-module-config-harvest.md) | Classical config harvest | **done** |
| [LISS-0006](LISS-0006-examples-catalog-honesty.md) | Catalog / SV-09 / QFT honesty | **done** (optional `pi`/rename deferred) |

Work plan: [WP-0003](../work-plans/WP-0003-examples-driven-brush-up.md).

## Acceptance Notes

- [x] Review + child issues + conventions
- [x] ADR 0060 / 0061 **Accepted** and implemented
- [x] Children closed (optional deferrals noted on LISS-0006)
- [x] SV suite green (163/163)

## Dependencies

- Related: LISS-0001, LISS-0002, ADR 0054, 0060, 0061

## Work Notes

- 2026-07-23: ledger filed; later same day Feature Path executed end-to-end.

## Verification

- 163/163 SV PASS; unit tests in `tests/test_joint_preserve_and_harvest.py`
