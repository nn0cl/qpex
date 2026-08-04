# Adjudicator Review: WP-0024 plan approval

## Review Target

- Artifact: [`WP-0024`](../../work-plans/WP-0024-indexed-operator-and-binder-surface.md)
  and its constituent local Issues
  [LISS-0052](../../architecture/documentation-compression-map.md) …
  [LISS-0058](../../architecture/documentation-compression-map.md), built on
  [ADR 0096](../../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md)
  (Accepted) and [ADR 0097](../../architecture/decision-themes/dec-0004-type-first-scientific-model.md)
  (Proposed, not implemented).
- Current phase: phase-0-design complete for LISS-0052–0057; LISS-0058 is
  design intake only and explicitly not scheduled.
- Requested approval: plan approval for the WP-0024 sequence, per
  `CLAUDE.md`'s Claude Code Issue-Level Autonomy — the first of the two
  approval points that bound each Issue (plan approval here; completion
  approval separately, per Issue, after its own Phase 3 Refactor).
- Approval type: scope
- Approved scope: the WP-0024 issue graph and ordering (LISS-0052 →
  LISS-0053 → LISS-0054 → LISS-0055 → LISS-0056 → LISS-0057; LISS-0058
  unscheduled). This approval authorizes starting **LISS-0052** first; each
  subsequent Issue in the sequence still receives its own plan approval
  before its own Phase 1 Red, per the same Issue-Level Autonomy section —
  this record does not pre-approve LISS-0053–0057's implementation, only
  the plan and order.
- Implementation allowed: yes, for LISS-0052 only, starting from Phase 1 Red.
- Post-review required: yes — completion approval per Issue, per the
  two-approval cadence.
- Execution batch ID: n/a (not a bounded batch; ordinary sequential Issue
  work under Issue-Level Autonomy).

## What Changed

- [ADR 0095](../../architecture/decision-themes/dec-0003-language-surface-and-physicist-first-dx.md):
  project design horizon (ideal final form, not shortest path), accepted
  2026-07-26; revised the same day to add Decision 6 (classify evidence as
  bug / documented deferral / genuine design gap before using it as design
  evidence) and to correct its own Context, which had originally presented
  four implementation bugs as if they were evidence of accumulated
  shortest-path cost.
- [ADR 0096](../../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md):
  indexed-operator and binder surface, Accepted after an independent
  external review resolved its four original open decision points and
  corrected two of the author's positions (empty-domain materialisation
  need not be immediate; the ket-application-order objection to ascending
  `product` order does not hold) while also finding two positions of the
  reviewed alternative too weak (an f64-does-not-leak-into-semantics
  criterion; certainty that today's empty ranges are only typos).
- [ADR 0097](../../architecture/decision-themes/dec-0004-type-first-scientific-model.md):
  numeric representation horizon, split out of ADR 0096 per the same
  review — Proposed, not Accepted, and not part of this plan approval's
  authorized scope.
- `WP-0024` and `LISS-0052`…`LISS-0058` added, sequencing implementation.
- `docs/architecture/open-work-register.md` updated, including an explicit
  note that ADR 0088 Decision 3's promise is not met by its own
  implementation (the LISS-0052 bug).

## Why It Matters

This is the first work sequenced under ADR 0095's ideal-form-first horizon.
Deriving the surface from the Hamiltonians physicists actually write (rather
than from the pre-existing deferred list) surfaced two requirements absent
from every prior document: multi-index sums (required for molecular
electronic structure, the flagship application) and constrained sums. Both
were invisible while scoping incrementally, which is the concrete case for
why the project changed its design horizon.

Separately, of the seven items originally offered as evidence for that
horizon change, four turned out to be plain implementation bugs against an
already-accepted spec (ADR 0088), not evidence of a shortest-path design
philosophy. This was caught by the Adjudicator asking directly whether the
evidence was being over-read, and is recorded, corrected, and turned into a
standing review rule (ADR 0095 Decision 6) rather than quietly patched — the
practical benefit is that LISS-0052's fix is cheaper and lower-risk than a
new-surface slice would have been, since most of it is making an existing
promise true.

## Adjudicator Checklist

- [x] The phase is correct — LISS-0052 has phase-0-design complete (ADR 0096
      D7) and is ready for Phase 1 Red; LISS-0053–0057 have their design
      settled by ADR 0096 but each still needs its own plan approval before
      its own Phase 1 Red; LISS-0058 is deliberately not phased.
- [x] The included context is sufficient — ADR 0095/0096/0097, WP-0024, and
      each Issue cross-reference the specific ADR decision(s) they
      implement.
- [x] The omitted context is acceptable — ADR 0097 (numerics) and LISS-0058
      (acting-space typing) are explicitly out of this approval's scope and
      not blocking.
- [x] Assumptions are visible — each Issue's Context section states its
      assumption and names the fallback (stop and ask) if the assumption is
      wrong.
- [x] Open decisions are either answered or intentionally deferred — ADR
      0096's four original open points are resolved in the ADR itself; ADR
      0097 and LISS-0058 are intentionally left as separate, unscheduled
      decisions.
- [x] Deterministic verification is adequate for this step — WP-0024's
      Verification Plan names the regression sweep (269 tests, 5 known
      unrelated failures), spec verification (165/165), and the
      marginal-comparison pattern established by LISS-0011/LISS-0032.
- [x] The approval type and scope are explicit — scope approval for the
      plan and sequence; implementation permission is explicit for LISS-0052
      only.
- [x] Implementation permission is explicit and is not inferred from scope
      approval — recorded above: LISS-0052 Phase 1 Red only.
- [x] Any post-review requirement and execution batch are recorded — no
      batch; per-Issue completion approval required as work proceeds.

## Decision

- [x] Approved

Plan approval granted for WP-0024's sequence starting at LISS-0052. Per
`CLAUDE.md` Issue-Level Autonomy, Claude proceeds through LISS-0052's Red →
Green → Refactor without a per-phase check-in, reports immediately if an
unanticipated design decision surfaces (two candidate risk points are named
in WP-0024's Process gate section), self-verifies before reporting, and
requests completion approval for LISS-0052 bundled with updated
documentation and status.
