# Completion status synchronization process review

## Incident

LISS-0083's implementation PR #146 passed CI and merged successfully, but the
Issue, WP-0025 row, and design trace still said `final review gated`. A second
documentation-only PR #147 was required to synchronize the completion state.

## Root cause

The workflow treated implementation completion and status synchronization as
separate moments. Phase 3 documentation recorded the pre-merge gate, while the
final PR packet did not require a status-bearing completion diff before merge.
The existing Definition of Done required synchronization in the same
reviewable unit, but did not provide an ordered pre-PR/pre-merge checklist or
an explicit stop condition.

## Corrective procedure

The Definition of Done now requires:

1. Phase 3 closeout is recorded as `final-review-ready`.
2. Before PR creation, Issue, work plan, spec/ADR references, and trace are
   inspected as one status packet.
3. After final review approval and before merge, the same PR carries the
   `complete` status and PR evidence.
4. CI runs on that final status-bearing commit; any later commit requires CI
   again.
5. After merge, a read-only audit confirms main contains the same state.

Branch/PR discipline now makes the completion packet an explicit PR field and
forbids deferring normal status synchronization to a second post-merge PR.

## Evidence

- PR #146: implementation, tests, CI, and merge.
- PR #147: corrective status synchronization, CI, and merge.
- Corrective commits: `bd42661`, merged as `85df987`.

## Scope

This is a process/documentation correction only. It changes no application
semantics, architecture boundary, or test behavior.
