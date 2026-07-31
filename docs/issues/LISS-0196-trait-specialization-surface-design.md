# LISS-0196: Trait specialization / effect-row surface examples (design)

## Metadata

- Local issue ID: LISS-0196
- Status: **open** (design only — no Kernel Red)
- ADR boundary: [0128](../architecture/adr/0128-trait-effect-expansion-boundary.md) **maintained**
- Program: backlog ship plan (docs sync)

## Intent

Collect **concrete surface examples** for trait specialization and effect-row
expansion so a future ship ADR can authorize Red. Without examples, Red is
blocked (ADR 0128).

## Design questions (Architecture Path)

1. Draft `impl` / specialization syntax examples (and rejected alternatives).
2. Draft effect-row annotation examples on `fn` / `fun` call/pipeline sites.
3. Interaction with existing ADR 0081 / 0082 shipped surfaces.
4. Minimum MVP slice for a follow-on ship ADR (what is in / out of first Red).

## Non-goals (this Issue)

- Kernel implementation or AT-TDD Red
- Inventing specialization semantics without Adjudicator review
- Replacing ADR 0128

## Exit (design)

- [ ] Surface-example draft reviewed by Adjudicator
- [ ] Ship ADR proposed only after examples are accepted
- [ ] No Kernel change in this Issue
