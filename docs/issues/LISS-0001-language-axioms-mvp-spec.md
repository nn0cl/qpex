# LISS-0001: Language axioms, ADRs, and Discrete PMF MVP spec

## Metadata

- Local issue ID: LISS-0001
- GitHub issue: none
- Status: **done** (2026-07-23) — superseded by shipping Kernel + later LISS
- Phase: Architecture / design intake → Feature Path completed downstream
- Type: architecture + specification
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: Original “Phase 1 Red unlock” checkboxes were stale;
  Kernel + SV suite now ship on `main` (ADR 0013–0062 lineage).
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Adopt collaboration template into QPex, fill runtime placeholders, record
language axioms and ADRs 0013–0015, and accept MVP scope A specification for
Discrete PMF arithmetic. Dual-license the repository (MIT OR Apache-2.0).

Downstream work (parser, evaluator, SV-01…SV-31, examples, OpenQASM MVP,
examples brush-up LISS-0003…0007) has **already executed** the Feature Path
this issue was meant to unlock.

## Acceptance Notes

- [x] Dual license files present (`LICENSE`, `LICENSE-MIT`, `LICENSE-APACHE`).
- [x] Placeholders filled for local-first Rust CLI / ports.
- [x] `docs/architecture/qpex-language-axioms.md` exists.
- [x] ADR 0013, 0014, 0015 Accepted with Adjudicator approval date.
- [x] `docs/specs/qpex-mvp-discrete-pmf-arith-observe.md` exists.
- [x] Positioning Accepted; prior-art note settled.
- [x] Formal semantics sketch + ADR 0016 (stance a).
- [x] Kernel PoC A/B design fixtures under `tests/fixtures/poc/`.
- [x] Kernel / SV harness green on `main` (163/163 as of 2026-07-23) —
      historical “unlock Phase 1 Red” satisfied by shipping Kernel.
- [x] Adjudicator continued work on `main` (docs branch merged); this issue
      closed as ledger cleanup.
- [x] Feature Path executed via subsequent ADRs / LISS (not blocked on this
      checkbox).

## Dependencies

- Parent: none
- Depends on: llm-project-template adoption (done)
- Blocks: none remaining (Feature Path unblocked)
- Related: ADR 0013–0016; LISS-0002+

## Adjudicator Decision Points

- [x] Fill remaining placeholders (approved 2026-07-22).
- [x] MVP scope A only (arithmetic + observe) (approved 2026-07-22).
- [x] Discrete PMF first (approved 2026-07-22).
- [x] Commit on branch (approved 2026-07-22).
- [x] Phase 1 / Kernel path proceeded (shipping Kernel on `main`).

## Context

- Included: Adjudicator chat decisions; template contracts; axioms vision.
- Omitted at filing: parser crate choice, continuous distributions.
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
- Assumptions: no Rust implementation in this issue unit
- Confidence: high
- Revises: none
- Superseded by: none

### AIP-0001-002

- Status: accepted
- Created at: 2026-07-23
- Planning size: S
- Intended scope: close stale open checkboxes against shipping reality
- Assumptions: no new Kernel work in this unit

## Work Notes

- 2026-07-22: documentation unit on `docs/language-axioms-mvp-spec`.
- 2026-07-23: status → **done**; open items marked satisfied by shipping
  Kernel / SV / later LISS (ledger hygiene).

## Verification

- License, axioms, ADRs 0013–0015, MVP spec present.
- `python3 tests/spec_verification/run_all.py` green on `main`.
