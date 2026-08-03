# LISS-0196: Trait specialization / effect-row surface examples (design)

## Metadata

- Local issue ID: LISS-0196
- Status: **complete** (2026-08-03) — Adjudicator **採択**: examples accepted, **no ship ADR**
- ADR boundary: [0128](../architecture/adr/0128-trait-effect-expansion-boundary.md) **maintained**
- Program: backlog ship plan (docs sync)
- Design draft: [staqex-v1-trait-effect-surface-examples.md](../specs/staqex-v1-trait-effect-surface-examples.md)
- Accept record: [review](../collaboration/reviews/2026-08-03-liss-0196-trait-surface-design-review.md)

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
- [x] Surface-example draft **reviewed / 採択** by Adjudicator (2026-08-03)
- [x] Ship ADR: **none** (accepted recommendation — park expansion)
- [x] No Kernel change in this Issue

## Adjudicator decision (2026-08-03)

**Examples accepted. No ship ADR.**

Stable face remains:

- shipped `interface` / `impl` + free-fn interface-typed params (S01);
- fixed `effects { Measure, Snapshot, Inspect, Host }` (+ Uncompute witness path).

Do **not** start Kernel Red for specialization or extensible effect rows.
Optional pure interface default method bodies only if a **future** ship ADR is
Accepted separately — never overlapping specialization or provider effect rows.
