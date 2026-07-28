# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **plan pending** (2026-07-28)
- Phase: phase-0-design
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL
- Owner/agent: unassigned after plan approval
- Related branch: `docs/wp-0025-defer-rust-next-0071` (WP routing only)
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted**

## Summary

Make every normative language claim falsifiable via stable, versioned
conformance scenarios. Establish a **Python-reference** oracle first.
Rust differential execution is postponed with LISS-0070 (deferred to next
version).

## Acceptance Notes (Issue complete when)

1. Valid, invalid, semantic, numerical, provenance, and backend suite taxonomy
   is specified and reviewed.
2. Each language claim in the v1.0 normative surface maps to a stable scenario
   id (or an explicit deferral).
3. No implementation-private dictionary is treated as a public oracle.
4. Numerical comparisons state precision and confidence policy.
5. Generated-report drift from ordinary test runs is eliminated or gated.
6. Rust vs Python differential harness is **out of scope** until LISS-0070 resumes.

## Non-goals (initial plan)

- Implementing LISS-0070 / choosing Rust IR.
- CST / formatter (LISS-0072).
- Changing accepted language semantics without a separate Issue.

## Adjudicator Decision Points (plan)

- [ ] Approve opening Feature Path Phase 0 design intake for LISS-0071.
- [ ] Confirm Python-reference oracle first; Rust differential deferred.
- [ ] Confirm suite taxonomy (valid / invalid / semantic / numerical /
      provenance / backend) as the planning frame.

## Work Notes

- 2026-07-28: Issue stub opened after Adjudicator deferred LISS-0070 and set
  WP-0025 current next to LISS-0071.

## Verification

- Documentation / plan only until plan approval.
