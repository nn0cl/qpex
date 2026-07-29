# Trace: LISS-0073 Slice B Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | B — `⟨φ|ψ⟩` → `inner` |
| Phase | phase-2-green |
| Branch | `feature/liss-0073-slice-b-red` |

## [DESIGN CHECK]

- Scope: single-bar `⟨φ|ψ⟩` → `Call(inner, [BraLit, KetLit])`; alone bra
  unchanged; EBNF `bra_ket_inner`; no matrix element / outer / `†`.
- Implementation: lexer emits optional KET half after BRA; parser folds
  BRA+KET into `inner` Call.
- Verification: Slice B + A + unicode math Red suites PASS.

## Delivered

- `compiler/staqex/lexer.py` — `_try_ket_half_after_bra`
- `compiler/staqex/parser.py` — BRA + KET → `Call(inner, …)`
- `docs/specs/grammar/staqex.ebnf` — `bra_ket_inner` in `primary`

## Verification

- `python3 tests/test_dirac_slice_b_red.py` PASS
- `python3 tests/test_dirac_slice_a_red.py` PASS
- `python3 tests/test_unicode_math_source_red.py` PASS

## Next safe action

Adjudicator Green approval → Slice B Phase 3 Refactor.
