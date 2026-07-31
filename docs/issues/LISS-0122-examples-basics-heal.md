# LISS-0122: Examples basics heal to green (rebaseline Gate P0)

## Metadata

- Local issue ID: LISS-0122
- GitHub issue: none
- Status: **ready** — P0 authorized; **unblocked** by LISS-0119 complete
- Phase: ready for Feature Path Red (sample heal)
- Type: examples / conformance repair (basics)
- Priority: P0
- Initial planning size: M
- Depends on: [LISS-0119](LISS-0119-examples-health-inventory.md) (**complete**)
- Blocks: rebaseline Gate P0 exit (with LISS-0123)
- Related: [rebaseline](../specs/staqex-v1-representative-program-rebaseline.md),
  inventory heal list (B03–B06, B08–B09, B11–B15), BinOp language candidate
- Implementation permission: **yes** (P0 authorize + 0119 exit)
- Branch: `feature/liss-0122-examples-basics-heal`

## Summary

Bring **all** `examples/basics/**` official entry points to **green**, or mark
retired with an explicit replacement pointer, per rebaseline Gate P0. Scope of
which files and which failure clusters is **defined by LISS-0119** — do not
guess heal targets before inventory.

## Acceptance (EARS)

1. **Given** LISS-0119’s basics classification, **when** this Issue completes,
   **then** every basics entry is green or retired+pointer.
2. **Given** a sample defect that is actually a language bug, **when**
   discovered, **then** open or cite a language Issue — do not hide it by
   rewriting physics meaning in the sample.
3. **Given** heal edits, **when** verified, **then** `compile.ok` and
   deterministic run hold for remaining basics entries.

## Non-goals

- Applied track (LISS-0123).
- Showcase construction.
- Inventory itself (LISS-0119).

## Exit

- [ ] LISS-0119 exit recorded as dependency satisfied
- [ ] Basics green-or-retired table
- [ ] Language follow-ups linked if any
- [ ] Spec verification / relevant SV paths as applicable

## Next allowed operation

Start Feature Path Red/Green on basics red set from LISS-0119. Open language
Issue for BinOp crash before claiming B03 green via sample-only edits.
