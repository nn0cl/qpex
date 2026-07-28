# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **Slice A Phase 3 Refactor complete** (2026-07-28)
- Phase: phase-3-refactor complete (Slice A)
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: unassigned (Slice A completion review)
- Related branch: `feature/liss-0071-slice-a-refactor`
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
| **A** | DR-011 protocol index sync + report-drift policy | **complete** (Red→Green→Refactor) |
| **B** | Versioned claim→scenario catalog | after A |
| **C** | Highest-gap envelope coverage (Adjudicator-selected Red) | after B |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals

- Implementing LISS-0070 / choosing Rust IR.
- CST / formatter (LISS-0072).
- Changing accepted language semantics without a separate Issue.
- NFC / A.1 / M-P01 / M-P05.

## Adjudicator Decision Points (Slice A Green)

- [x] Approve Phase 2 Green.
- [x] Authorize Phase 3 Refactor.

## Adjudicator Decision Points (Slice A Refactor)

- [ ] Approve Phase 3 Refactor (helpers only; behavior unchanged).
- [ ] Confirm Slice A complete; authorize Slice B plan intake next.

## Work Notes

- 2026-07-28: Plan approved (PR #80). Phase 1 Red (PR #81). Green (PR #82).
- 2026-07-28: Phase 3 Refactor — `_resolve_report_module` / `_print_run_summary`.
  No behavior change. Slice A complete pending Adjudicator sign-off.

## Verification

- Slice A through Refactor: conformance Red tests PASS; SV 160/160 PASS;
  default run does not write `reports/latest.*`.
