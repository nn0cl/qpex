# LISS-0196: Trait specialization / effect-row surface examples (design)

## Metadata

- Local issue ID: LISS-0196
- Status: **draft ready for Adjudicator review** (2026-08-03) — no Kernel Red
- ADR boundary: [0128](../architecture/adr/0128-trait-effect-expansion-boundary.md) **maintained**
- Program: backlog ship plan (docs sync)
- Branch: `feature/liss-0196-trait-surface-design-draft`
- Design draft: [staqex-v1-trait-effect-surface-examples.md](../specs/staqex-v1-trait-effect-surface-examples.md)

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

- [x] Surface-example draft written ([spec](../specs/staqex-v1-trait-effect-surface-examples.md))
- [ ] Surface-example draft **reviewed** by Adjudicator
- [ ] Ship ADR proposed only after examples are accepted (recommendation: **none now**)
- [x] No Kernel change in this Issue

## Recommendation (for review)

Prefer **no new ship ADR** yet. Shipped `interface`/`impl` + free-fn
interface-typed params (S01) and fixed `effects {…}` are enough. Optional
later: pure interface default method bodies only — never overlapping
specialization or provider effect rows.
