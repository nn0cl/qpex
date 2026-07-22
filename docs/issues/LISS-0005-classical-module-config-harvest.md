# LISS-0005: Classical module config harvest (extend ADR 0054)

## Metadata

- Local issue ID: LISS-0005
- GitHub issue: none
- Status: **done** (2026-07-23)
- Phase: Feature Path — Green
- Type: feature + architecture
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Shipped ADR 0061 candidate A: harvest `Float`/`Int`/`Bool` from `public fun`
bodies into entry main. Collisions → `CONFIG_HARVEST_COLLISION_ERROR`.

## Acceptance Notes

- [x] ADR 0061 **Accepted** (candidate A)
- [x] Path-linked classical harvest in `modules.py`
- [x] Visibility: `pub` fun bodies only
- [x] Collision hard diagnostic
- [x] Examples 11/12/14 consume harvested config (no sync comments)
- [x] Unit tests + SV suite green (163/163)

## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Depends on: ADR 0061 Accept; LISS-0004 (post-Grover inspect)
- Related: ADR 0054, 0058

## Work Notes

- 2026-07-23: implemented + verified. Candidate B (`pub const`) deferred.

## Verification

- `tests/test_joint_preserve_and_harvest.py` harvest + collision cases
- Examples 11/12/14 linked runs
