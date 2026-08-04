# AI work trace: WP-0090 Trace topic consolidation

| Field | Record |
|---|---|
| User request | Consolidate remaining Trace records by topic and retain Git recovery pointers. |
| Operating path | Architecture Path — documentation/process maintenance. |
| Phase | Documentation compaction implementation and verification. |
| Canonical work plan | [WP-0090](../../work-plans/WP-0090-documentation-canonicalization.md) |
| Decision boundary | [ADR 0187](../../architecture/decision-themes/dec-0007-documentation-and-decision-records.md) |
| Evidence contract | Deterministic file classification, exact source-path inventory, baseline recovery checks, link and spec verification. |

## Decision

One representative Trace is kept for each repeated LISS/WP topic. Redundant
phase and planning logs are deleted only when they have no current unresolved,
approval, review, or direct-reference role. The [Trace topic register](../../architecture/trace-topic-register.md)
and [compression map](../../architecture/documentation-compression-map.md)
retain the representative, deleted paths, baseline tag, and source commit.

## Verification

- 233 existing Trace files were classified into 147 topics.
- 85 redundant paths were selected for deletion; 148 existing representatives
  remain, including 14 directly referenced records.
- All selected paths exist in `docs/pre-canonicalization-2026-08-03`.
- Final checks are recorded in the PR and must include link, execution-batch,
  specification, and source-recovery verification.

## Omitted context

No compiler, runtime, language semantics, tests, or application files are in
scope. This trace does not replace normative ADR/spec content.
