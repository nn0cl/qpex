# AI Work Trace

## Request

- Date: 2026-07-22
- User request: Adjudicator decisions — accept positioning; HOLD Phase 1 Red;
  authorize Kernel PoC A/B; stance (a); settle docs; write formal semantics;
  create PoC fixtures.
- Current phase: Architecture Path + Kernel PoC design fixtures
- Canonical issue or work plan: `docs/issues/LISS-0001-language-axioms-mvp-spec.md`
- AI planning record: AIP-0001-002

## Context Ledger

- Included: Adjudicator decision text; positioning; prior-art note; semantics
  requirements (joint, pushforward, terminal observe).
- Omitted: Rust harness implementation; parser; Feature Path Red tests.
- Assumptions: fixtures JSON is the design contract for a future harness.
- Open decisions: exact harness crate layout; `fair_bit` surface syntax.

## Routing

- Model/assistant/tool: Cursor agent
- Reason: Architecture documentation under explicit Adjudicator decisions
- Privacy constraints: local repository only

## AI Execution Records

### Attempt 1

- Agent: Cursor
- Environment: local
- Model as displayed: Auto / Composer
- Reasoning setting as displayed: n/a
- Actual tokens: unavailable
- Actual token unavailable reason: IDE session does not expose token totals
- Scope: Accepted positioning; ADR 0016; formal semantics sketch; PoC A/B JSON;
  research note settle; README links; commit
- Result: completed pending commit
- Attempt boundary: documentation + design fixtures only

## Cost / Reasoning Control

- Operating path: Architecture Path
- Files read: positioning, prior Adjudicator message, existing specs
- Deterministic checks used: file writes; JSON structure
- Avoided LLM work: no runtime implementation

## Adjudicator Decisions

- Positioning Accepted
- Phase 1 Red HOLD; Kernel PoC track authorized; unseal when A/B + semantics settled
- Stance (a) PMF MVP with amplitude lift (ADR 0016)
- observe = terminal sampling collapse only

## Verification

- Commands/checks: files present under docs/specs, docs/architecture,
  tests/fixtures/poc
- Result: ready to commit

## Changed Files

- `docs/architecture/staqex-positioning.md`
- `docs/architecture/adr/0016-pmf-mvp-amplitude-lift.md`
- `docs/architecture/README.md`
- `docs/research/2026-07-22-prior-art-and-differentiation.md`
- `docs/specs/staqex-formal-semantics-sketch.md`
- `docs/specs/staqex-mvp-discrete-pmf-arith-measure.md`
- `tests/fixtures/poc/*`
- `CLAUDE.md` (non-decisions)
- this trace

## Next Safe Action

- Implement Kernel PoC harness that loads A/B fixtures (still not language-birth
  Phase 1 until harness is green and Adjudicator requests Phase 1).
- Or request review/PR of this documentation commit.

## Notes

- Agent operating contract lightly touched (`CLAUDE.md` non-decisions); trace
  recorded.
