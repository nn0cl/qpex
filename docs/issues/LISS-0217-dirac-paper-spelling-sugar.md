# LISS-0217: Dirac paper spelling `⟨φ|ψ⟩` as surface sugar (design)

## Metadata

- Local issue ID: LISS-0217
- Status: **open** (design only — no Kernel Red)
- Phase: phase-0-design
- Type: design
- Priority: P2
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Design ADR: [0165](../architecture/adr/0165-dirac-paper-spelling-sugar.md) **Proposed**
- Related: ADR 0087 (`inner` / `outer`); friction ledger F-04

## Intent

Collect the surface options for writing Dirac inner and outer products the way
they appear on a blackboard, and record the lowering rule, so a future ship ADR
can authorize Red.

The friction ledger records F-04 as an **accepted trade**, not a defect:

> Paper: ⟨φ|ψ⟩ … Kernel: `inner(phi, psi)`, `outer(psi, phi)` (ADR 0087).
> Named ket `|psi>` not accepted. … accepted trade for parser safety;
> **sugar later must lower to Calls**.

This Issue is the "sugar later" the ledger points at. `CLAUDE.md` §Language
Design Priority makes it more than cosmetic: physicist mental model is primary,
and on conflict the blackboard spelling is preferred (ADR 0095).

## Design questions (Architecture Path)

1. What exactly is spelled? `⟨φ|ψ⟩` inner product only, or also `|ψ⟩⟨φ|` outer?
2. Parser safety — the reason ADR 0087 chose Calls. `|` and `>` are already
   load-bearing (ket literals, comparison, pipeline `|>`). Which disambiguation
   rule keeps the grammar unambiguous, and what does it cost?
3. Named kets: F-04 records `|psi>` as **not accepted**. Does the sugar require
   reopening that, and if so is it a separate decision?
4. Lowering: the ledger's constraint is that sugar must lower to `inner` /
   `outer` Calls, leaving semantics untouched. Confirm no evaluator change.
5. Migration: does `migrate_unicode_math.py` gain a rule, and does the
   formatter (`format.py` / CST) round-trip the sugar?
6. Minimum first slice — what is in and out of the first Red.

## Non-goals (this Issue)

- Kernel implementation or AT-TDD Red
- Changing `inner` / `outer` semantics (ADR 0087 stands)
- Inventing a spelling without Adjudicator review

## Exit (design)

- [ ] Surface-example draft reviewed by the Adjudicator
- [ ] Parser-ambiguity analysis recorded with the rejected alternatives
- [ ] Ship ADR proposed only after the examples are accepted
- [ ] No Kernel change in this Issue
