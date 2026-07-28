# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **Slice B Phase 3 Refactor complete** (2026-07-28); Slice A complete
- Phase: phase-3-refactor complete (Slice B)
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: unassigned (Slice B completion review)
- Related branch: `feature/liss-0071-slice-b-refactor`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted**

## Summary

Make every normative language claim falsifiable via stable, versioned
conformance scenarios. Establish a **Python-reference** oracle first.
Rust differential execution is postponed with LISS-0070 (deferred to next
version).

Plan companion:
[`qpex-v1-conformance-plan.md`](../specs/qpex-v1-conformance-plan.md).
Slice B catalog:
[`qpex-v1-conformance-scenario-catalog.md`](../specs/qpex-v1-conformance-scenario-catalog.md).

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
| **A** | DR-011 protocol index sync + report-drift policy | **complete** |
| **B** | Versioned claim→scenario catalog | **complete** (Red→Green→Refactor) |
| **C** | Highest-gap envelope coverage (Adjudicator-selected Red) | after B |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals (Slice B)

- Filling all `gap` rows (Slice C).
- Changing SV assertions or language semantics.
- Rust differential / CST / NFC.

## Adjudicator Decision Points (Slice B Green)

- [x] Approve Phase 2 Green.
- [x] Authorize Phase 3 Refactor.

## Adjudicator Decision Points (Slice B Refactor)

- [ ] Approve Phase 3 Refactor (parser helper extract; behavior unchanged).
- [ ] Confirm Slice B complete; authorize Slice C plan (E-05 gap first candidate).

## Work Notes

- 2026-07-28: Slice B Green approved; Phase 3 Refactor —
  `tests/spec_verification/harness/scenario_catalog.py`. No behavior change.

## Verification

- Slice B through Refactor: catalog Red tests PASS; Slice A Red still PASS.
