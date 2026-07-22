# Trace: Examples-driven brush-up ISSUE ledger

- Date: 2026-07-23
- Task: Review examples 01–15; file LISS/ADR/WP/collaboration docs
- Agent: Cursor (Auto / Composer)
- Planning size: L (parent); no Kernel implementation this attempt

## What changed

- Inbox: `docs/issues/inbox/2026-07-23-examples-driven-brush-up.md`
- Issues: LISS-0003 (parent), LISS-0004, LISS-0005, LISS-0006
- ADRs **Proposed**: 0060 (Joint preserve), 0061 (classical harvest)
- Work plan: WP-0003
- Collaboration: `docs/collaboration/examples-catalog-conventions.md`
- Architecture README index updated for 0060/0061 + LISS-0003

## Decisions

- GitHub Issues not created (local ledger only, same as LISS-0002).
- Kernel code deferred until Adjudicator Accepts ADR 0060/0061.
- Nested `when` ban and existing Honesty tables kept as non-defects.
- Default branch set to `main` (same tip as former docs branch).

## Resume hints

- Next: Adjudicator Accept/reject ADR 0060 & 0061; optional parallel LISS-0006
  SV-09 / `08` honesty work.
- Do not open Feature Path Red for Joint/linker without Accepted ADR.
- Do not treat LISS-0006 as owner of Joint/harvest/oracle work.

## Follow-up (same day)

- ISSUE ledger cleanup: scope boundaries, wrong LISS-0006 attribution for
  oracle combinators, `main` branch refs, hard vs soft deps, acceptance
  checkbox split for conventions draft vs Accept.
- **Feature Path executed:** ADR 0060/0061 Accepted; LISS-0004/0005 Kernel
  shipped; LISS-0006 honesty/SV-09 shipped; SV **163/163** PASS. Parent
  LISS-0003 closed. Optional deferred: prelude `pi`, rename `08` folder.
