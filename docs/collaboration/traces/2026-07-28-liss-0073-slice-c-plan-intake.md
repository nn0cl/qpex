# Trace: LISS-0073 Slice B completion + Slice C plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Path | Feature Path — Slice B closeout + Slice C plan (docs) |
| Phase | slice-b done; slice-c phase-0-design |
| Branch | `feature/liss-0073-slice-b-red` |
| Implementation | **forbidden** for Slice C until plan approval |

## [DESIGN CHECK]

- Scope: close Slice B after Refactor approval; propose Slice C only —
  `⟨φ|A|ψ⟩` → `Call(inner, [BraLit, Call(A, [KetLit])])` with domain mismatch
  diagnostics; preserve A/B.
- Specs: LISS-0073 plan §4; ADR 0087; Slice B lexer evidence (`BRA`, mid,
  `KET`); Refactor verification gap on matrix-element collision.
- Boundaries: no outer/`†`/brackets.
- Decisions pending: AST lowering shape; mid-expr precedence (`_call`); Red
  authorization.
- Verification: docs + merge Slice B PR; no Slice C Green yet.

## Slice B completion evidence

- Red / Green / Refactor traces present
- `python3 tests/test_dirac_slice_b_red.py` PASS
- `python3 tests/test_dirac_slice_a_red.py` PASS

## Slice C requested approval

**Plan approval** for Slice C only with recommended defaults above.

## Next safe action

Adjudicator Slice C plan approval → Slice C Phase 1 Red only.
