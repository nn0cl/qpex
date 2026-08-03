# LISS-0106: Examples catalog v2 refresh (parent)

## Metadata

- Local issue ID: LISS-0106
- GitHub issue: not created
- Status: done
- Phase: complete
- Type: epic / examples / catalog
- Priority: P1
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: full catalog restructure across basics, applied,
  SV registration, and migration from legacy `01`–`17`.
- Owner/agent: unassigned after design review
- Related branch: `docs/liss-0106-examples-catalog-v2-refresh`
- AI planning record: AIP-0106-001 (to be filed at scope approval)

## Summary

Design and execute a two-track official examples catalog:

| Track | Path | Purpose |
|-------|------|---------|
| Basics | `examples/basics/` | Teach Staqex axioms, syntax, and language policy |
| Applied | `examples/applied/` | Research- and industry-themed toy models with Honesty tables |

Authoritative acceptance specification:
[`docs/specs/staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md).

Work plan: [WP-0026](../work-plans/WP-0026-examples-catalog-v2-refresh.md).

### Child issues

| Child | Focus | Status |
|-------|--------|--------|
| [LISS-0107](LISS-0107-examples-linker-runtime-prerequisite.md) | Multi-file linker/runtime regression (Phase 0) | **done** |
| [LISS-0108](LISS-0108-examples-basics-track-migration.md) | Basics track B01–B12 migration | **done** |
| [LISS-0109](LISS-0109-examples-applied-track-migration.md) | Applied track A01–A10 migration | **done** |

### Relationship to prior work

- Supersedes the **layout** of [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
  (done); does not reopen ADR 0060/0061 Kernel work.
- Complements [LISS-0020](LISS-0020-capstone-quantum-observatory.md) by relocating
  capstone narrative to Applied **A10** with a slim integration scope and
  explicit lane matrix discipline.
- Independent of [LISS-0068](LISS-0068-staqex-v1-normative-rebaseline.md) / WP-0025
  v1 north star (proposed Architecture Path).

## Acceptance Notes

Documentation phase (this Issue gate):

- [x] Inbox filed:
  [`2026-07-27-examples-catalog-v2-refresh.md`](inbox/archive/2026-07-27-examples-catalog-v2-refresh.md)
- [x] Catalog acceptance spec drafted:
  [`staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md)
- [x] Work plan drafted: [WP-0026](../work-plans/WP-0026-examples-catalog-v2-refresh.md)
- [x] Child issues LISS-0107…0109 drafted
- [x] Conventions doc updated for v2 layout

Implementation phase:

- [x] Phase 0: LISS-0107 closed; SV gate green on prerequisite multi-file paths
- [x] `examples/basics/` B01–B12 created per catalog spec
- [x] `examples/applied/` A01–A10 created per catalog spec
- [x] Legacy `01`–`17` retired; reusable content migrated; non-reused paths deleted
- [x] SV-09 registers all official entry points (22 + docs case)
- [x] Root and track READMEs include learning paths
- [x] Each Applied folder README includes verified bibliography + Honesty table
- [x] A01 attention-inspired toy shipped with non-LLM-inference Honesty boundary
- [x] Full `python3 tests/spec_verification/run_all.py` PASS after migration

## Dependencies

- Depends on:
  - [LISS-0107](LISS-0107-examples-linker-runtime-prerequisite.md) for multi-file
    migration (blocks B09, A02, A10, and other linked entries)
  - Adjudicator approval of catalog spec bibliography policy
- Blocks: none (examples-only; does not block LISS-0068)
- Related:
  - [LISS-0006](LISS-0006-examples-catalog-honesty.md),
    [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md)
  - [LISS-0067](LISS-0067-multi-register-acting-space-and-qpu-mapping.md) (A08)
  - [LISS-0032](LISS-0032-typed-second-quantized-operators.md) (A03)
  - current SV-09 allowlist in `tests/spec_verification/suites/sv09_examples.py`

## Adjudicator Decision Points

- Approve two-track layout and catalog spec as Phase 1 Red authority.
- Confirm legacy `01`–`17` disposition: migrate reusable content only; delete the rest.
- Confirm Shor toy treatment: drop from official v2 unless direct reusable slices exist.
- Confirm A10 stance: keep as slim integration capstone, not a kitchen-sink canonical source.
- Confirm A01 wording guardrail: attention-inspired toy only, no GPT-scale inference claims.
- Approve Phase 1 Red for example file moves (no Kernel changes except via
  LISS-0107).

## Verification

- Documentation: `git diff --check` on `docs/`.
- After implementation: full SV suite, example-specific tests, `staqex check` on
  every registered entry, README Honesty table review.
