# LISS-0071: Versioned conformance and differential oracle

## Metadata

- Local issue ID: LISS-0071
- GitHub issue: not created
- Status: **Slice C Phase 2 Green** (2026-07-28); Slice A/B complete
- Phase: phase-2-green (Slice C)
- Type: conformance / language specification / testing
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–C; D deferred)
- Owner/agent: unassigned after Green review
- Related branch: `feature/liss-0071-slice-c-green`
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
| **B** | Versioned claim→scenario catalog | **complete** |
| **C** | Close E-05 catalog gap (Static Hilbert oracles) | **Phase 2 Green** |
| **D** | Rust differential | **out** (LISS-0070) |

## Non-goals (Slice C)

- Deferred envelopes E-07 / E-13 / E-14.
- New language semantics; new SV suite number.
- Rust / CST / NFC.

## Adjudicator Decision Points (Slice C Red)

- [x] Approve Phase 1 Red (`tests/test_conformance_slice_c_red.py`).
- [x] Authorize Phase 2 Green (catalog row updates only).

## Adjudicator Decision Points (Slice C Green)

- [ ] Approve Phase 2 Green.
- [ ] Authorize Phase 3 Refactor (optional) or Slice C / Issue completion
      (deferred rows remain intentional).

## Work Notes

- 2026-07-28: Slice C Red approved; Phase 2 Green — E05-001…003 covered;
  SV-26 mis-map removed. Slice C Red tests PASS; A/B Red still PASS.

## Verification

- Slice C Green: `tests/test_conformance_slice_c_red.py` PASS; catalog has no
  remaining `gap` rows.
