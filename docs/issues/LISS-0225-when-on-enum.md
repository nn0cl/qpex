# LISS-0225: `when` on classical enum control

## Metadata

- Local issue ID: LISS-0225
- GitHub issue: (none yet)
- Status: **complete** (2026-08-01)
- Phase: Phase 1 Red → Phase 2 Green (Adjudicator authorized 2026-08-01)
- Type: bug
- Priority: P0
- Initial planning size: S
- Current planning size: S
- Owner/agent: Cursor agent
- Related branch: `feature/wp-0071-binder-when-enum-gaps`
- Program: [WP-0071](../work-plans/WP-0071-s01-kernel-gaps-from-review.md)

## Summary

```staqex
N.S s = N.S.Open
state w = when (s) {
  Open -> |1>,
  else -> |0>,
}
measure w
```

crashes Joint with `KeyError: 's'` because classical enum binds live in
`self.objects`, while `_ctrl_masses` only reads `w.assign`. Even after lookup,
`_pat_match` must treat pattern `"Open"` as matching `EnumValue(..., "Open")`.

Found by S01 shake ([LISS-0223](LISS-0223-s01-language-physicist-review.md)).
Blocks enum-only classical scoring without Float twins.

## Acceptance Notes

- [x] Red: failing test for `when` on typed enum binding
- [x] Green: `run` exits 0; Open arm taken for `N.S.Open`
- [x] Else arm taken for other variants
- [x] Existing `when (coin())` / int patterns still green

## Dependencies

- Parent: LISS-0223
- Spec: [staqex-v1-liss-0225-when-on-enum.md](../specs/staqex-v1-liss-0225-when-on-enum.md)

## Adjudicator Decision Points

- None for MVP: classical enum as when-control is the natural reading of shipped
  `enum` + `when`.

## Context

- Included: `evaluator._ctrl_masses`, `_pat_match`, `EnumValue`
- Omitted: nested namespace-qualified patterns (`N.S.Open` as pattern) unless
  already parsed — arms use bare `Open` today

## AI Planning Records

### AIP-0225-001

- Status: accepted (working)
- Created at: 2026-08-01
- Planning size: S
- Intended execution route: Feature Path Red→Green

## Work Notes

- Root cause: enum binds in `self.objects`; `_ctrl_masses` only read Joint
  `assign` → KeyError. Patterns are bare strings; `EnumValue` was unhashable.
- Fix: look up `self.objects` / scalars; `_pat_match` EnumValue↔variant;
  `@dataclass(frozen=True)` on `EnumValue`.

## Verification

- `python3 tests/test_liss_0225_when_on_enum_red.py` PASS
