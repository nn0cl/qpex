# LISS-0108: Examples basics track migration

## Metadata

- Local issue ID: LISS-0108
- GitHub issue: not created
- Status: **done** (2026-07-27) — B01–B15 shipped
- Phase: migration complete (core basics slice)
- Type: examples / documentation / migration
- Priority: P1
- Initial planning size: L
- Current planning size: L
- Owner/agent: unassigned
- Parent: [LISS-0106](LISS-0106-examples-catalog-v2-refresh.md)
- Depends on: [LISS-0107](LISS-0107-examples-linker-runtime-prerequisite.md) for B09 only
- Related branch: TBD

## Summary

Migrate the Basics curriculum **B01–B15** defined in
[`staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md) into
`examples/basics/`. One folder per concept; minimal narrative; no Honesty table
required except where a basics sample uses an applied-style story (discouraged).

## Acceptance Notes

- [x] Folders `examples/basics/B01_*` … `B15_*` created per catalog spec
- [x] B13–B15 shipped (2026-07-27, WP-0027 Wave 2)
- [x] Each shipped basics folder has `README.md` stating the single concept taught
- [x] Basics entry points registered in SV-09 successor suite
- [x] `python3 -m compiler.staqex check` and `run` succeed on B01–B15 entries
- [x] No `fun` / `public` / missing `main -> Unit` / missing return types

## Verification

- SV suite (successor allowlist)
- `tests/test_fn_keyword_red.py`, `tests/test_pub_visibility_red.py`,
  `tests/test_main_signature_red.py`, `tests/test_missing_return_annotations_red.py`
