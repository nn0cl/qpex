# AI work trace: WP-0091 decision theme design

| Field | Record |
|---|---|
| User request | Group current documentation by decision theme and use the tagged source commit for historical recovery. |
| Operating path | Architecture Path. |
| Phase | Phase 1 design evidence. |
| Work plan | [WP-0091](../../work-plans/WP-0091-decision-theme-canonicalization.md) |
| Design artifact | [Decision theme register](../../architecture/decision-theme-register.md) |
| Source baseline | `docs/pre-canonicalization-2026-08-03` / `8663ba72295964069ac275b93c350e762a0844d8` |

## Result

The 186 source ADR records are assigned exactly once to seven accepted
`DEC-*` themes. ADR 0188 accepted the current reading surface and archival
rule. ADRs 0001–0186 (185 files; ADR 0099 was never assigned) were removed
from the working tree after link migration; the compression map preserves
their recovery coordinates.

## Verification

- ADR coverage: 186/186 assigned, 0 unassigned, 0 duplicates.
- Accepted theme documents: 7/7 present.
- Archived ADR pointers: 185/185 present and baseline-recoverable.
- Runtime, compiler, and test files were not included in scope.

## Open review

The Adjudicator must review theme boundaries and promote or revise each draft
before historical ADR bodies are compressed or removed.
