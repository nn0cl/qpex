# Work Plan: Examples catalog v2 refresh

## Goal

Replace the legacy `examples/01`–`17` numeric catalog with a documented
two-track layout (`basics/`, `applied/`) aligned to the shipping v0.1 Kernel,
honest research citations, and a green Spec Verification gate.

## Scope

- In:
  - [LISS-0106](../issues/LISS-0106-examples-catalog-v2-refresh.md) (parent)
  - [LISS-0107](../issues/LISS-0107-examples-linker-runtime-prerequisite.md) …
    [LISS-0109](../issues/LISS-0109-examples-applied-track-migration.md)
  - [`staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md)
  - conventions update, SV-09 successor registration, root `examples/README.md`
- Out:
  - LISS-0068 / WP-0025 v1 normative rebaseline implementation
  - Kernel feature work except LISS-0107 prerequisite fixes
  - Real-scale LLM, pharma, or industrial robot deployments
  - Provider SDK / cloud QPU adapters

## Issue Graph

| Issue | Status | Size | Planning | Depends on | Blocks | Branch |
| --- | --- | --- | --- | --- | --- | --- |
| [LISS-0106](../issues/LISS-0106-examples-catalog-v2-refresh.md) | **done** | XL | AIP-0106-001 | — | — | `feature/liss-0108-examples-basics` |
| [LISS-0107](../issues/LISS-0107-examples-linker-runtime-prerequisite.md) | **done** | M | TBD | — | 0108 B09, 0109 linked | `feature/liss-0108-examples-basics` |
| [LISS-0108](../issues/LISS-0108-examples-basics-track-migration.md) | **done** | L | TBD | 0107 (B09 only) | — | `feature/liss-0108-examples-basics` |
| [LISS-0109](../issues/LISS-0109-examples-applied-track-migration.md) | **done** | XL | TBD | 0107 | — | `feature/liss-0108-examples-basics` |

## Recommended Order

### Phase 0 — Design (current)

1. Adjudicator reviews inbox, LISS-0106, and catalog spec.
2. Approve bibliography verification policy (verified vs TBD markers).
3. Approve Phase 1 Red for example moves (no file moves before this).

### Phase 1 — Prerequisite

4. ~~LISS-0107: Red tests filed~~ **done** (`tests/test_liss0107_examples_linker_runtime_red.py`)
5. ~~LISS-0107: Green fix for linked runtime failures.~~ **done**
6. ~~Confirm SV **165/165** on legacy paths before migration.~~ **done**

### Phase 2 — Basics track

7. ~~LISS-0108: B01–B12~~ **done** (B13–B15 deferred)

### Phase 3 — Applied track

10. ~~P0 applied: A06, A08, A09, A10 (reuse-heavy).~~ **done**
11. ~~P1 applied: A02, A03, A05.~~ **done**
12. ~~P2 applied: A04, A07.~~ **done**
13. ~~A01 last: ship as attention-inspired toy with strict non-LLM-inference wording.~~ **done**

### Phase 4 — Legacy retirement

14. ~~Delete non-reused legacy `01`–`17` paths after reusable content is migrated.~~ **done**
15. ~~Update SV-09 successor, discovery tests, and `open-work-register` pointers.~~ **done** (SV suites + README/QUICKSTART; ADR cross-refs deferred)
16. ~~Phase 3 Refactor: README empathy pass (student + physicist).~~ **done**

## Current Next Issue

- None for WP-0026 core scope (optional: B13–B15 basics, ADR cross-ref sweep)
- SV gate: **157/157 PASS** on `feature/liss-0108-examples-basics`
- Adjudicator approval needed: none for Applied P0 unless scope changes

## Risks

- Migrating before LISS-0107 repeats red SV on new paths.
- Unverified research citations in Applied READMEs (hallucination / overclaim).
- A01 LLM narrative invites misleading "quantum GPT" marketing if Honesty table
  is weak.
- A10 capstone re-becomes unmaintainable kitchen sink without coverage matrix
  discipline from LISS-0020.

## Verification Plan

- Each child Acceptance Notes.
- `python3 tests/spec_verification/run_all.py` after every migration batch.
- Bibliography audit: every Applied README cites only **Verified** entries from
  catalog spec §Bibliography or newly verified sources at Red review.

## References

- Intake:
  [2026-07-27-examples-catalog-v2-refresh.md](../issues/inbox/archive/2026-07-27-examples-catalog-v2-refresh.md)
- Prior catalog work:
  [WP-0003](WP-0003-examples-driven-brush-up.md),
  [LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md)
- Capstone prior art:
  [WP-0016](WP-0016-quantum-observatory-capstone.md),
  [LISS-0020](../issues/LISS-0020-capstone-quantum-observatory.md)
- Conventions:
  [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md)
