# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **complete — Slice A/B/C approved** (2026-07-28); Slice D out
- Phase: done (planned slices)
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: —
- Related branch: merged (`feature/liss-0071-slice-c-refactor` via PR #91)
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
Slice C plan:
[`qpex-v1-conformance-slice-c-e05.md`](../specs/qpex-v1-conformance-slice-c-e05.md).

## Acceptance Notes (Issue complete when)

1. Valid, invalid, semantic, numerical, provenance, and backend suite taxonomy
   is specified and reviewed. **Done** (Slice A plan + catalog schema).
2. Each language claim in the v1.0 normative surface maps to a stable scenario
   id (or an explicit deferral). **Done** (catalog E-01…E-14; deferred E-07/13/14).
3. No implementation-private dictionary is treated as a public oracle. **Done**.
4. Numerical comparisons state precision and confidence policy. **Done**
   (conformance plan §2; existing SV ε).
5. Generated-report drift from ordinary test runs is eliminated or gated.
   **Done** (Slice A `--write-report`).
6. Rust vs Python differential harness is **out of scope** until LISS-0070 resumes.
   **Confirmed** (Slice D out).

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | DR-011 protocol index sync + report-drift policy | **complete** |
| **B** | Versioned claim→scenario catalog | **complete** |
| **C** | Close E-05 catalog gap (Static Hilbert oracles) | **complete** |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals (remaining intentional)

- Deferred envelopes E-07 / E-13 / E-14 (Host/Dynamic).
- Slice D Rust differential until LISS-0070 resumes.

## Adjudicator Decision Points (Slice C Refactor / Issue)

- [x] Approve Phase 3 Refactor (helpers only; behavior unchanged).
- [x] Confirm LISS-0071 Slice A–C complete; deferred E-07/13/14 intentional;
      Slice D remains out with LISS-0070.

## Work Notes

- 2026-07-28: Slice C Green approved; Phase 3 Refactor —
  `oracle_paths` / `rows_for_envelope` / `row_by_scenario_id` in
  `scenario_catalog.py`. No behavior change.
- 2026-07-28: Slice C Refactor / Issue completion **approved** (“承認”). PR #91
  merged. Planned slices A–C closed.

## Verification

- Slice A/B/C Red suites PASS through Refactor.
- Closeout: Adjudicator approved Slice A–C completion (2026-07-28).
- WP-0025 current next: LISS-0072.
