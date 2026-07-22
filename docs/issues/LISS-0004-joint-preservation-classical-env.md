# LISS-0004: Joint coordinate preservation + classical env for phase/times

## Metadata

- Local issue ID: LISS-0004
- GitHub issue: none
- Status: **done** (2026-07-23)
- Phase: Feature Path — Green
- Type: bug + language semantics
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Shipped ADR 0060: `diffuse_copy` preserves unrelated Joint coordinates;
`phase`/`evolve times` resolve classical vars via evaluator `scalars` + Attr;
`EvolveExpr.times` accepts expressions (Float truncates toward zero).

## Acceptance Notes

- [x] ADR 0060 **Accepted**
- [x] `diffuse_copy` / `grover_diffuse` preserve unrelated `assign` keys
- [x] Float survives Grover + `inspect` (`tests/test_joint_preserve_and_harvest.py`)
- [x] `phase(…, Float only)` marks correctly (numeric Float/Int equality)
- [x] `evolve … times <expr>` with classical Float/Int
- [x] Examples 09/12/14/15 updated
- [x] SV suite green (163/163)

## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Depends on: ADR 0060 Accept
- Related: ADR 0030, ADR 0018

## Work Notes

- 2026-07-23: implemented + verified.

## Verification

- `tests/test_joint_preserve_and_harvest.py`
- `python3 tests/spec_verification/run_all.py` → 163/163
