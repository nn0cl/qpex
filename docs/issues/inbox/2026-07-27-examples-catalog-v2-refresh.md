# Challenge intake: Examples catalog v2 refresh (basics + applied)

| Field | Value |
|-------|-------|
| Received | 2026-07-27 |
| Channel | Adjudicator request (full catalog redesign; docs-first) |
| Local ledger | **[LISS-0106](../LISS-0106-examples-catalog-v2-refresh.md)** (parent) |
| Children | LISS-0107 (linker prerequisite), LISS-0108 (basics), LISS-0109 (applied) |
| Work plan | **[WP-0026](../../work-plans/WP-0026-examples-catalog-v2-refresh.md)** |
| Acceptance spec | **[qpex-examples-catalog-v2.md](../../specs/qpex-examples-catalog-v2.md)** |
| Supersedes layout | `examples/01`–`17` numeric catalog (delete non-reused paths after migration) |
| Prior art | [LISS-0003](../LISS-0003-examples-driven-kernel-brush-up.md) / [WP-0003](../../work-plans/WP-0003-examples-driven-brush-up.md) (done) |
| GitHub | ignored (project-local management only) |

## Objective

Replace the legacy `examples/01`–`17` numeric catalog with a two-track layout:

- **`examples/basics/`** — language axioms, syntax, and policy (one concept per
  sample).
- **`examples/applied/`** — research- and industry-themed demos that reuse
  shipping Kernel surfaces honestly at toy scale.

Reuse migratable assets from the current catalog. Consolidate narrative clones
(Grover/DTQW skins). Keep [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md)
and [WP-0025](../../work-plans/WP-0025-qpex-v1-north-star.md) as separate
Architecture Path work; this refresh targets the **shipping v0.1 Kernel**.

## Adjudicator decisions captured in intake

| Decision | Status |
|----------|--------|
| Full refresh (not incremental patch) | **Approved in consultation** |
| Two-track `basics/` + `applied/` | **Approved in consultation** |
| Reuse migratable examples where honest | **Approved in consultation** |
| A01 LLM / attention toy included provisionally | **Approved; proceed with attention-inspired toy wording** |
| Legacy `01`–`17` disposition (archive vs delete) | **Delete by default; migrate only reusable content** |
| Shor toy (`11`) retention | **Drop from official v2 catalog if no direct reuse** |
| A10 capstone thickness vs slim integration story | **Slim integration capstone (retain lane matrix discipline)** |

## Prerequisite finding (2026-07-27)

Spec Verification on `main` reports **160/165 PASS**. Multi-file official
examples fail at runtime (`unbound Operator / scalar`, linker-related). Phase 0
([LISS-0107](LISS-0107-examples-linker-runtime-prerequisite.md)) must precede
or gate Basics B09 and Applied multi-file migration.

## Scope guardrails

- Documentation and planning only until Adjudicator approves LISS-0106 scope
  and Phase 1 Red for example file moves.
- No Kernel semantics changes under this parent unless a prerequisite bug is
  filed as LISS-0107.
- Applied READMEs MUST include Honesty tables per
  [examples-catalog-conventions.md](../../collaboration/examples-catalog-conventions.md).
- Primary research citations MUST be verified before each Applied example
  ships; unverified titles stay in the catalog spec bibliography as **TBD**.

## Agent prompt (short)

Execute docs ledger first: inbox → LISS-0106 → WP-0026 → catalog spec →
conventions update. Do not move `examples/` files until Adjudicator approves
LISS-0106 acceptance notes and Phase 1 Red. Fix linker/runtime regressions
under LISS-0107 before claiming SV green on migrated multi-file entries.
