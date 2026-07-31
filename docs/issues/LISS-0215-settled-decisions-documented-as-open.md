# LISS-0215: Settled decisions still documented as open questions

## Metadata

- Local issue ID: LISS-0215
- Status: **proposed** (investigation intake)
- Phase: docs-only
- Type: process
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [`open-work-register.md`](../architecture/open-work-register.md)

## Intent

Two documents present already-decided or already-shipped topics as unresolved.
Both are read by agents at session entry, so the drift actively invites
re-litigation of settled decisions — exactly what
`CLAUDE.md` §Current Open Topics warns against ("Do not treat this list as
'nothing is shipped'").

## Evidence (verified 2026-08-01)

**(a) `docs/architecture/README.md` §Remaining Technology Evaluation** still
lists as open:

> - Pipeline `|>` and currying implementation (semantic boundary accepted by
>   ADR 0080; **Phase 1 Red remains**).
> - Trait `impl` surface; `system` as Expr vs decl-only.
> - Effect marking for measure-capable vs pure `fn`.
> - SI scale conversion beyond $(L,M,T)$ tags (ADR 0037).

All four have shipped per the open-work register and `CLAUDE.md` §Already
shipped (ADR 0080 / 0122 / 0123 / 0133; ADR 0081–0082; ADR 0121 / 0124 / 0129 /
0132 / 0134–0136). The section contradicts the register it sits beside.

**(b) [`physicist-source-friction-ledger.md`](../architecture/physicist-source-friction-ledger.md)
§F-08** lists

> | No user operator overload | Domain `add`/`eq` named methods — not chalk `+` on arbitrary types |

as a live friction, with no reference to the decision that already settled it:
[ADR 0114 §D5](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md)
lists "User operator overloading" under **Out of scope**. Read without that
link, F-08 looks like an open design question and invites a design Issue that
would re-open an accepted ADR.

## Adjudicator decision points

1. §Remaining Technology Evaluation: prune the shipped rows, or replace the
   whole section with a pointer to the open-work register so there is one
   source of truth? (Recommend the pointer — two hand-maintained lists is how
   this drifted.)
2. Ledger F-08: annotate the overload row as decided-out with the ADR 0114 §D5
   link. Confirm no residual design question hides behind it.

## Exit

- [ ] §Remaining Technology Evaluation agrees with the open-work register
- [ ] Ledger F-08 overload row cites ADR 0114 §D5 as decided-out
- [ ] Single source of truth chosen and recorded

## Non-goals

Reopening operator overloading — ADR 0114 §D5 decided it; this Issue only makes
the documentation say so. Changing any shipped surface.
