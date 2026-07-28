# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **Slice B Phase 1 Red** (2026-07-28); Slice A complete
- Phase: phase-1-red (Slice B)
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: unassigned after Red review
- Related branch: `feature/liss-0071-slice-b-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted**

## Summary

Make every normative language claim falsifiable via stable, versioned
conformance scenarios. Establish a **Python-reference** oracle first.
Rust differential execution is postponed with LISS-0070 (deferred to next
version).

Plan companion:
[`qpex-v1-conformance-plan.md`](../specs/qpex-v1-conformance-plan.md).
Slice B catalog contract:
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
| **B** | Versioned claim→scenario catalog | **Phase 1 Red** |
| **C** | Highest-gap envelope coverage (Adjudicator-selected Red) | after B |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals (Slice B)

- Filling all `gap` rows (Slice C).
- Changing SV assertions or language semantics.
- Rust differential / CST / NFC.

## Adjudicator Decision Points (Slice B plan)

- [x] Approve **Slice B** plan for Phase 1 Red (catalog schema + E-01…E-14 rows).
- [x] Confirm `scenario_id` form `E##-###` and status enum
      (`covered` / `gap` / `deferred`).
- [x] Confirm draft inventory statuses are reviewable in Green (Red locks
      schema/presence only).
- [x] Implementation: Red only until Red review (default stop before Green).

## Adjudicator Decision Points (Slice B Red)

- [ ] Approve Phase 1 Red (`tests/test_conformance_slice_b_red.py`).
- [ ] Authorize Phase 2 Green (publish `## Catalog (Normative)` table; clear
      plan-proposed status).

## Work Notes

- 2026-07-28: Slice A complete (PR #83). Slice B plan approved (PR #84).
- 2026-07-28: Phase 1 Red — `tests/test_conformance_slice_b_red.py` (4 failures:
  missing Normative section / still plan-proposed).

## Verification

- Slice B Red: 4/4 FAIL until Green.
