# Trace: CLAUDE.md Open Topics honesty (LISS-0132)

## Request

- Date: 2026-07-31
- User request: Option B §7 confirm (“はい”) — permanent-out + annotate agent Open Topics
- Current phase: Architecture Path docs (LISS-0132)
- Canonical issue: LISS-0132; program LISS-0128 / WP-0030
- AI planning record: WP-0030

## Context Ledger

- Included: open-work register; ADR 0079/0080/0081/0082; axioms; coverage ledger; permanent-out note
- Omitted: Kernel implementation; S1 `.sqx`
- Assumptions: Adjudicator §7 accepts inventory correction and boundary-only 0057
- Open decisions: none for this docs slice; LISS-0129 Plan still required before Red

## Routing

- Model/assistant/tool: Cursor agent (Composer)
- Reason: docs + instruction contract sync
- Privacy constraints: no secrets

## AI Execution Records

### Attempt 1

- Agent: Cursor
- Environment: local repo `docs/liss-0128-open-topics-before-s1`
- Scope: Rewrite `CLAUDE.md` “Current Open Topics” into scheduled / shipped /
  permanent-out sections; add permanent-out + ADR 0057 boundary specs
- Result: contract text no longer lists shipped surfaces as “not yet Accepted”
- Attempt boundary: docs + `CLAUDE.md` only; no Feature Path Red
- Notes: Per ADR 0112, `CLAUDE.md` may diverge from `AGENTS.md`; AGENTS had no
  matching Open Topics list. Copilot/Grok mirrors unchanged (no Open Topics
  section to sync).

## Expected agent behavior change

- Agents must not propose re-implementing `evolve until`, minimal `|>`, or
  core trait/effect surfaces as if unshipped.
- Agents must treat typed surface (LISS-0129) as the primary pre-S1 language
  ship item.
- Agents must not invent Kernel work for permanent-out rows.

## Cost / Reasoning Control

- Operating path: Architecture Path
- Verification: docs review; N/A for tests
