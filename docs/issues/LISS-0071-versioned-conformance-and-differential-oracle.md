# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **plan proposed** (2026-07-28)
- Phase: phase-0-design
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: unassigned after plan approval
- Related branch: `docs/liss-0071-conformance-plan`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted**

## Summary

Make every normative language claim falsifiable via stable, versioned
conformance scenarios. Establish a **Python-reference** oracle first.
Rust differential execution is postponed with LISS-0070 (deferred to next
version).

Plan companion:
[`qpex-v1-conformance-plan.md`](../specs/qpex-v1-conformance-plan.md).

## Acceptance Notes (Issue complete when)

1. Valid, invalid, semantic, numerical, provenance, and backend suite taxonomy
   is specified and reviewed.
2. Each language claim in the v1.0 normative surface maps to a stable scenario
   id (or an explicit deferral).
3. No implementation-private dictionary is treated as a public oracle.
4. Numerical comparisons state precision and confidence policy.
5. Generated-report drift from ordinary test runs is eliminated or gated.
6. Rust vs Python differential harness is **out of scope** until LISS-0070 resumes.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | DR-011 protocol index sync + report-drift policy | plan → Red after approval |
| **B** | Versioned claim→scenario catalog | after A |
| **C** | Highest-gap envelope coverage (Adjudicator-selected Red) | after B |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals

- Implementing LISS-0070 / choosing Rust IR.
- CST / formatter (LISS-0072).
- Changing accepted language semantics without a separate Issue.
- NFC / A.1 / M-P01 / M-P05.

## Adjudicator Decision Points (plan)

- [ ] Approve **LISS-0071** plan for Slice A Phase 1 Red after merge.
- [ ] Confirm Python-reference oracle first; Rust differential deferred.
- [ ] Confirm suite taxonomy (valid / invalid / semantic / numerical /
      provenance / backend).
- [ ] Confirm report-drift default: local `--no-write-report` + CI artifacts
      (or choose gitignore / committed golden instead).
- [ ] Confirm Slice A before catalog (B) and coverage fills (C).
- [ ] Implementation: Red only until Red review (default stop before Green).

## Work Notes

- 2026-07-28: Issue stub opened; LISS-0070 deferred; WP next = LISS-0071 (PR #79).
- 2026-07-28: Plan proposed
  ([`qpex-v1-conformance-plan.md`](../specs/qpex-v1-conformance-plan.md)).

## Verification

- Plan phase: documentation-only until plan approval.
