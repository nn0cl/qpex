# Trace: LISS-0073 Slice A completion + Slice B plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Path | Feature Path — Slice A closeout + Slice B plan (docs) |
| Phase | slice-a done; slice-b phase-0-design |
| Branch | `feature/liss-0073-slice-a-red` → merge PR #96 |
| Implementation | **forbidden** for Slice B until plan approval |

## [DESIGN CHECK]

- Scope: mark Slice A complete after Refactor approval; propose Slice B only —
  `⟨φ|ψ⟩` → `Call(inner, [BraLit, KetLit])` + collision regressions.
- Specs: LISS-0073 plan §4–5; ADR 0087 `inner`; Slice A `BraLit` baseline;
  lexer `|>` vs `⟩` dual-accept (LISS-0069).
- Boundaries: no matrix element (C), outer (D), `†` (E), brackets (F).
- Decisions pending: Call(inner,[bra,ket]) vs rewrite bra→ket label; Slice B
  Red authorization.
- Verification: docs update; PR #96 merge; no Green for B yet.

## Slice A completion evidence

- Red / Green / Refactor traces present
- `python3 tests/test_dirac_slice_a_red.py` PASS after Refactor

## Slice B requested approval

**Plan approval** for Slice B only with recommended parse:

- after `BraLit`, if next token is `KET` → `Call(inner, [BraLit, KetLit])`
- alone bra unchanged
- collision tests for pipeline vs ket close
- Red suite: `tests/test_dirac_slice_b_red.py` after approval

## Next safe action

Adjudicator Slice B plan approval → Slice B Phase 1 Red only.
