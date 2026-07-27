# Trace: LISS-0068 normative rebaseline slice 2

- Date: 2026-07-27
- Task: Reconciled v1 §1–§2 outline after ADR 0106 acceptance
- Agent: Cursor (Auto)
- Phase: Architecture Path / LISS-0068 slice 2

## Delivered

- `docs/specs/qpex-v1-normative-outline-s12.md` — v1 header target, §1 execution
  model lane table, §2 lexical transition rules, drift resolution map.
- `docs/architecture/qpex-language-axioms.md` — Axiom 4 + MVP table aligned with
  ADR 0068 (`return`) and ADR 0079 (`evolve until`).

## Drift IDs addressed

DR-001 (header), DR-002 (lanes), DR-003 (return/axioms), DR-006/007/008/009/010
(outline rows; full promotion deferred).

## Verification

- Documentation-only; no compiler or test changes.

## Next safe action

- LISS-0068 slice 3 — diagnostic catalog merge (Kernel vs Host appendix).
