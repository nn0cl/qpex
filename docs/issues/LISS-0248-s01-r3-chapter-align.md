# LISS-0248: S01-R3 align constellation chapters to locked seats

## Metadata

- Local issue ID: LISS-0248
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: P1
- Parent: [S01 redesign](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md) **S01-R3**; seats [LISS-0247](LISS-0247-s01-e1-locked-scenario-seats.md)
- Branch: `feature/liss-0248-s01-r3-chapter-align`
- Approval: Adjudicator「承認」(R3 after E1; recommended order)

## Intent

Align S01 chapters to locked constellation seats without dropping scorecard A+B:

1. README / run list use **CH-*** names from locked scenario
2. Chapter file headers cite CH-id + lane + Non-placeable where needed
3. Thin morning/day2/`inspect` floods — retain sparse chapter peeks for scorecard
4. Remove decorative Float `inspect`s on satellites (keep `expect` + measure)

## Exit

- [x] README constellation table / run commands labeled CH-*
- [x] Morning/day2 inspect thinned
- [x] Satellite float-inspect removed where safe
- [x] All listed mains still run seed 0
- [x] Scorecard / redesign R3 marked complete
- [x] No A+B row deleted

## Non-goals

- Spine domain Float theater shrink (optional later)
- `tracing_out` ADR
- Renaming package FQNs globally
