# LISS-0001: Language axioms, ADRs, and Discrete PMF MVP spec

## Metadata

- Local issue ID: LISS-0001
- GitHub issue: none
- Status: in progress
- Phase: Architecture / design intake (no Feature Path Phase 1 yet)
- Type: architecture + specification
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `docs/language-axioms-mvp-spec`

## Summary

Adopt collaboration template into QPex, fill runtime placeholders, record
language axioms and ADRs 0013–0015, and accept MVP scope A specification for
Discrete PMF arithmetic + `observe`. Dual-license the repository
(MIT OR Apache-2.0).

## Acceptance Notes

- [x] Dual license files present (`LICENSE`, `LICENSE-MIT`, `LICENSE-APACHE`).
- [x] Placeholders filled for local-first Rust CLI / ports.
- [x] `docs/architecture/qpex-language-axioms.md` exists.
- [x] ADR 0013, 0014, 0015 Accepted with Adjudicator approval date.
- [x] `docs/specs/qpex-mvp-discrete-pmf-arith-observe.md` exists.
- [x] Positioning Accepted; prior-art note settled.
- [x] Formal semantics sketch + ADR 0016 (stance a).
- [x] Kernel PoC A/B design fixtures under `tests/fixtures/poc/`.
- [ ] Kernel PoC harness green (unlocks Phase 1 Red seal).
- [ ] Adjudicator review of this branch / PR.
- [ ] Feature Path Phase 1 Red explicitly requested after unlock.

## Dependencies

- Parent: none
- Depends on: llm-project-template adoption
- Blocks: Phase 1 Red for Discrete PMF arithmetic / observe
- Related: ADR 0013, 0014, 0015

## Adjudicator Decision Points

- [x] Fill remaining placeholders (approved 2026-07-22).
- [x] MVP scope A only (arithmetic + observe) (approved 2026-07-22).
- [x] Discrete PMF first (approved 2026-07-22).
- [x] Commit on branch (approved 2026-07-22).
- [ ] Approve Phase 1 Red against the MVP spec (not yet requested).

## Context

- Included: Adjudicator chat decisions; template contracts; axioms vision.
- Omitted: parser crate choice, continuous distributions, control-flow specs.
- Assumptions: copyright holders `dstechnology co., ltd` and `nn0cl`.

## AI Planning Records

### AIP-0001-001

- Status: accepted
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-22
- Planning size: M
- Intended execution route: Architecture Path documentation only
- Intended scope: license, placeholders, axioms, ADRs, MVP spec, commit
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: n/a
- Assumptions: no Rust implementation in this issue unit
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: none

## References

- https://www.apache.org/licenses/LICENSE-2.0
- http://opensource.org/licenses/MIT
- QPex axioms from Adjudicator project brief (2026-07-22)

## Work Notes

Documentation-only unit on `docs/language-axioms-mvp-spec`. No Cargo crate yet.

## Verification

- Files exist for license, axioms, ADRs 0013–0015, MVP spec.
- Agent contract placeholders no longer list SaaS datastore templates as
  active MVP resources.
