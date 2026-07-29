# AI Work Trace

## Request

- Date: 2026-07-22
- User request: Adopt intermediate syntax summary as design baseline
  (`state` / `span` / `evolve` / `measure`, persona, keyboard law).
- Current phase: Architecture Path (syntax baseline alignment)
- Canonical issue: LISS-0001

## Context Ledger

- Included: user intermediate summary prompt; existing positioning/semantics/PoCs
- Omitted: evolve repetition grammar decision; span amplitude denotation; harness code
- Assumptions: Kernel PoC laws unchanged; surface lexicon migrates

## Adjudicator / design decisions applied

- ADR 0017 surface vocabulary Accepted as working baseline
- `observe` retired as surface spelling → `measure`
- Open Qs 2–3 already settled; noted in syntax vocabulary §5

## Changed Files

- `docs/architecture/staqex-syntax-vocabulary.md` (new)
- `docs/architecture/adr/0017-surface-vocabulary.md` (new)
- positioning, axioms, architecture README, formal semantics, MVP spec
- PoC A/B fixtures + README
- `AGENTS.md`, `.grok/rules/02`, `CLAUDE.md` port names

## Next Safe Action

- Discuss open: `evolve times` / `until` grammar
- Or implement Kernel PoC harness against updated fixtures
- Commit when Adjudicator requests

## Notes

- Agent contract files touched (AGENTS/CLAUDE/grok); this trace recorded.
