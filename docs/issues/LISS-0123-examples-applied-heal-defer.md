# LISS-0123: Examples applied heal or defer (rebaseline Gate P0)

## Metadata

- Local issue ID: LISS-0123
- GitHub issue: none
- Status: **ready** — P0 authorized; **unblocked** by LISS-0119 complete
- Phase: ready for Feature Path Red (sample heal / defer)
- Type: examples / conformance repair (applied)
- Priority: P0
- Initial planning size: L
- Depends on: [LISS-0119](LISS-0119-examples-health-inventory.md) (**complete**)
- Blocks: rebaseline Gate P0 exit (with LISS-0122)
- Related: inventory (A01–A10 red; A11 green+catalog gap); QUICKSTART→A06
- Implementation permission: **yes** (P0 authorize + 0119 exit)
- Branch: `feature/liss-0123-examples-applied-heal`

## Summary

Bring **applied** catalog entries to **green** or **explicitly deferred** with
physicist-readable rationale. Align QUICKSTART so it links **only** to green
entries. Resolve A11 README / SV-09 registration or mark explicit defer per
LISS-0119 findings.

## Acceptance (EARS)

1. **Given** LISS-0119’s applied classification, **when** this Issue completes,
   **then** every applied entry is green or deferred-with-rationale (no silent
   broken demos in the default catalog path).
2. **Given** QUICKSTART and track READMEs, **when** this Issue completes,
   **then** linked applied demos are green only.
3. **Given** A11 (Noether Forge lineage), **when** this Issue completes,
   **then** it is either registered (README + SV-09) as green, or explicitly
   deferred — not an invisible orphan.

## Non-goals

- Basics heal (LISS-0122).
- Reclaiming LISS-0120 / showcase S*.
- Silent Kernel fixes inside samples for language bugs.

## Exit

- [ ] LISS-0119 exit recorded as dependency satisfied
- [ ] Applied green-or-deferred table
- [ ] QUICKSTART / README / SV-09 alignment for non-deferred entries
- [ ] Language follow-ups linked if any

## Next allowed operation

Start Feature Path heal/defer per LISS-0119. Retarget QUICKSTART off A06 until
green. Register or defer A11. Language Issue for BinOp before A01/A02/A04-only
sample claims.
