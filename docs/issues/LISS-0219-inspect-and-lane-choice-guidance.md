# LISS-0219: Physicist guidance for `inspect` vs measure, and circuit vs Hamiltonian lane

## Metadata

- Local issue ID: LISS-0219
- Status: **open** (design / docs only — no Kernel Red)
- Phase: phase-0-design
- Type: docs
- Priority: P3
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: friction ledger F-06 and F-10;
  [`physicist-dx-harmony.md`](../architecture/physicist-dx-harmony.md)

## Intent

Two Class B frictions in the ledger are teaching problems, not language
problems. Neither has an ADR or an Issue, and the ledger's §5 asks for exactly
that decision.

## Evidence (from the friction ledger, verified 2026-08-01)

**F-06 — expectation / `inspect` choreography:**

> low–medium ceremony; meaning OK if taught.
> **Bad if samples imply `inspect` is measurement.**

`inspect` is not measurement — the state is not collapsed — but a reader
skimming an example can easily take it for a read-out. The risk is a physicist
forming a wrong model of the central axiom (terminal `measure`, Never Leave the
State).

**F-10 — QPU / circuit lane vocabulary:**

> Static/parametric QPU surfaces … are a **second dialect** beside Hamiltonian
> `evolve`. Honest when the mission is circuits; **corrosive when a many-body
> paper is rewritten as gates "because that is what runs."**

The ledger's own §5 next step: "Optionally promote remaining Class B decisions
to ADRs once Adjudicator picks design options — **not** silent Kernel patches
inside showcases."

## Design questions

1. Is this docs-only guidance, or does F-06 warrant a surface change (e.g. a
   diagnostic or naming change that makes `inspect` un-mistakable)? If a surface
   change, it needs its own ADR and this Issue is only the intake.
2. Where does the guidance live — `physicist-dx-harmony.md`, the examples
   conventions, or a new short teaching note?
3. F-10: is a written lane-choice rule enough ("use `evolve` when the source is
   a Hamiltonian; use the circuit lane when the mission is circuits"), or should
   examples that cross lanes carry an explicit note?
4. Do any shipped examples currently imply `inspect` is measurement? That is a
   concrete audit, and its result decides whether this is P3 or higher.

## Non-goals

- Kernel implementation or Red
- Changing `inspect` or `measure` semantics
- Rewriting existing examples before the audit in question 4

## Exit (design)

- [ ] Audit of shipped examples for `inspect`-as-measurement implications
- [ ] Ruling: docs-only guidance vs surface change needing an ADR
- [ ] Guidance written where the Adjudicator chooses
- [ ] Ledger F-06 / F-10 rows updated with the outcome
