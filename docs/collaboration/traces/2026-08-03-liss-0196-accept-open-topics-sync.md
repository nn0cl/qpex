# AI work trace: LISS-0196 accept + Agent Open Topics sync

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0196-accept-open-topics-sync` |
| Issue | [LISS-0196](../../issues/LISS-0196-trait-specialization-surface-design.md) |

## Why

Adjudicator「LISS-0196 を採択、Agent Open Topics 文言の同期」.

## Contract files changed

| File | Change |
|---|---|
| `CLAUDE.md` | §Current Open Topics revised 2026-08-03; trait row = accepted, no ship ADR |
| `AGENTS.md` | New **Honest backlog pointer** (register + LISS-0196 parked) |
| `.github/copilot-instructions.md` | Same pointer (effective content aligned with AGENTS) |
| `.grok/rules/01-quickstart.md` | Same pointer |
| `.cursor/rules/01-quickstart.mdc` | Same pointer (Cursor complement; root AGENTS still auto-applies) |

`CLAUDE.md` remains independently authoritative (ADR 0112); Open Topics
narrative stays there. AGENTS/copilot/grok/cursor gain a short pointer so all
families stop treating trait specialization as an open Red invitation.

## Expected agent behavior change

- Do **not** open Kernel Red / Feature Path for trait specialization or
  extensible effect rows without a **new** Accepted ship ADR.
- Treat LISS-0196 surface examples as accepted design; recommendation
  “no ship ADR” is binding until Adjudicator reopens.
- Prefer `open-work-register.md` over stale “open” mental models.

## Docs (non-contract)

- Issue, design spec, review record, open-work-register, coverage ledger,
  local-issue-planning, ADR 0128 pointer.

## Not changed

- Kernel, examples, tests.
