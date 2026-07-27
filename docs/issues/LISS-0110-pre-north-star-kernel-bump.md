# LISS-0110: Pre–north-star Kernel bump (batch parent)

## Metadata

- Local issue ID: LISS-0110
- GitHub issue: none
- Status: proposed — **plan approved** (2026-07-27); Wave 2 complete
- Phase: Feature Path batch parent (no implementation by itself)
- Type: meta / release closure
- Priority: P1
- Initial planning size: XL (aggregate)
- Related work plan: [WP-0027](../work-plans/WP-0027-pre-north-star-kernel-bump.md)
- Blocks: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) Architecture Path entry (recommended)

## Summary

Coordinate the deferred Kernel execution slices and Basics examples B13–B15 so
the shipping Python Kernel reaches a documented **v0.2 closure** before
LISS-0068 normative rebaseline. This Issue does not implement code; child Issues
and example folders carry AT-TDD work.

## Child scope

| Child | Kind | Notes |
| --- | --- | --- |
| LISS-0012 runtime | Kernel follow-up | `evolve … until` evaluator loop |
| LISS-0027 QPU IR + binding | Kernel/Host follow-up | symbolic params through QASM |
| [LISS-0111](LISS-0111-continuous-discretization-numerical-lowering-mvp.md) | Kernel follow-up | LISS-0036 numerical lowering MVP |
| B13–B15 | Examples | Host job, resource profile, multi-register Basics |
| LISS-0067 provider routing | **excluded** | ADR 0105; post-MVP Host |

## Batch exit checklist

- [x] WP-0027 and this Issue marked complete or superseded.
- [x] LISS-0012 runtime: Phase 3 reviewed.
- [x] LISS-0027 QPU IR + binding: Phase 3 reviewed.
- [ ] LISS-0111: Phase 3 reviewed.
- [x] B13–B15 in catalog spec and SV-09.
- [x] `open-work-register.md` synced (Wave 1 slices).
- [ ] Collaboration trace filed if required by CI.
- [ ] SV and full test sweep green; counts recorded in trace.
- [ ] Explicit note: provider physical routing not claimed.

## Dependencies

- Depends on: [LISS-0106](LISS-0106-examples-catalog-v2-refresh.md) / WP-0026
  complete.
- Blocks (recommended): LISS-0068 scope entry — not a hard technical dependency.

## Adjudicator decision points

- [x] Approve WP-0027 wave order and exclusions.
- [ ] Approve LISS-0111 MVP domain (default: `Position` + `UniformGrid` 1D FD).
- [x] Confirm LISS-0067 provider routing stays out of this batch.
