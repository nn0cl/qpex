# Trace: Tier-2 contract sync to shipping Kernel facts

- Date: 2026-07-23
- Path: Architecture (contract-file change control)
- Reason: Align agent operating contracts with **implemented** Kernel reality
  (Python shipping evaluator; modern OOP / `pub` / `_`), per
  `docs/collaboration/prompt-instruction-change-control.md`.

## Effective-content agreement (ADR 0006)

Updated in lockstep:

- `AGENTS.md` — new **Project (adopter facts)** block
- `CLAUDE.md` — project one-liner + Selected Stack + Open Topics
- `.github/copilot-instructions.md` — stack + `measure` (not obsolete `observe`)
- `.cursor/rules/01-quickstart.mdc` — stack one-liner
- `.grok/rules/01-quickstart.md` — stack one-liner + DX pointers

Shared facts:

1. Shipping Kernel = Python `compiler/staqex/`
2. Long-term target = Rust VM behind **same** language semantics
3. Physicist DX docs: `physicist-dx-harmony.md`, `QUICKSTART.md`, ADR 0054–0056/0058

## Adjudicator note

Contract-file PRs require explicit Adjudicator review (not CI alone).
This trace records the stated reason for the Tier-2 edit.
