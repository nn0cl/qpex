# LISS-0223: S01 language beauty × physicist cognitive-load review

## Metadata

- Local issue ID: LISS-0223
- GitHub issue: (none yet)
- Status: **in_progress**
- Phase: phase-0-design (Architecture Path — review / recommendations only)
- Type: design / quality review
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: Cursor agent + Adjudicator
- Related branch: `docs/liss-0223-s01-language-physicist-review`

## Summary

Review `examples/showcase/S01_quantum_disaster_response/` as the flagship
language-spec showcase under two lenses only:

1. **Programming-language beauty** — does the source read as a coherent Staqex
   program (clear layers, honest physics spelling, minimal ceremony debt), or as
   a coverage museum?
2. **Physicist cognitive load** — can a research physicist follow the story and
   the quantum/classical boundary without decoding scorecard tags, Java package
   noise, or placeholder methods?

Out of scope for this Issue: Kernel feature work, live QPU, rewriting the locked
ops scenario numbers, and “make CI green” churn unrelated to readability.

## Acceptance Notes

- [x] Local Issue claimed; branch created; review record started.
- [ ] Review record lists ranked findings (beauty / cognitive load) with Class
      A/B/C/E tags per [friction ledger](../architecture/physicist-source-friction-ledger.md).
- [ ] Adjudicator decides which findings become follow-up Issues vs accepted
      showcase debt vs won’t-fix.
- [ ] `local-issue-planning.md` next-free ID advanced after claim.
- [ ] No production Kernel changes under this Issue unless Adjudicator promotes
      a finding into a Feature Issue.

## Dependencies

- Parent: [LISS-0222](LISS-0222-s01-quantum-disaster-response.md) / WP-0070 (shipped)
- Depends on: shipped S01 tree on `main`
- Blocks: optional S01 readability refactor follow-ups
- Related: [physicist-dx-harmony](../architecture/physicist-dx-harmony.md),
  [friction ledger](../architecture/physicist-source-friction-ledger.md),
  [ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md),
  LISS-0219 (`inspect` / lane-choice guidance)

## Adjudicator Decision Points

- Accept the ranked finding list as the review baseline?
- Which Class E (sample debt) items must be fixed in a follow-up Issue before
  S01 is treated as “physicist-readable showcase”?
- Keep multi-main satellite layout, or fold more physics into the tonight spine?

## Context

- Included: S01 mains / domain / physics / protocol / provenance / README;
  friction ledger classes; physicist × DX harmony.
- Omitted: full Kernel source; Host Python deep review (note only); locked
  scenario ops arithmetic (already Accepted for WP-0070).
- Assumptions: reality-first mission lock stays; review may criticize *how*
  surfaces are demonstrated without reopening the disaster OS theme.

## AI Planning Records

### AIP-0223-001

- Status: accepted (working)
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Composer
  - Reasoning setting as displayed: N/A
- Created at: 2026-08-01
- Planning size: M
- Intended execution route: Architecture Path — docs review only
- Intended scope: Issue + review record + planning claim; stop for Adjudicator
  triage of follow-ups
- Estimated token range: mid
- Token metric: files read (S01 tree + harmony/friction)
- Assumptions: no Kernel edits in this Issue
- Confidence: high on process; medium on which findings Adjudicator will promote

## References

- Showcase: `examples/showcase/S01_quantum_disaster_response/`
- Review record: [2026-08-01-s01-language-physicist-review.md](../collaboration/reviews/2026-08-01-s01-language-physicist-review.md)
- Mission lock / S0 / locked scenario under `docs/specs/`

## Work Notes

- 2026-08-01: Issue filed; first-pass review written from primary spine + domain
  / physics / protocol samples.
- 2026-08-01 (shake): purged dead/placeholder domain APIs; wired enums + open
  weights; Classical⊕State ration wire; morning `phase()`; tri_register import;
  all `main_*.sqx` green. Kernel gaps found: `when(enum)` KeyError; OpBinder
  `evolve under` → `cannot compile sparse Pauli for OpBinder`; field name
  `state` is reserved.

## Verification

- Review document exists and cites concrete paths/lines.
- Branch is not `main`.
- `python3 -m compiler.staqex run/check` all S01 `main_*.sqx` exit 0 (seed 0).
