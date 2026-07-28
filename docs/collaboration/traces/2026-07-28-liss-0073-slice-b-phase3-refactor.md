# Trace: LISS-0073 Slice B Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | B — `⟨φ|ψ⟩` → `inner` |
| Phase | phase-3-refactor |
| Branch | `feature/liss-0073-slice-b-red` |
| Implementation | readability only |

## [DESIGN CHECK]

- Scope: extract `_bra_or_inner` parser helper; tighten lexer ket-half checkpoint
  naming; no behavior change.
- Verification: Slice B + A Red suites PASS.

## Delivered

- `compiler/qpex/parser.py` — `_bra_or_inner`
- `compiler/qpex/lexer.py` — checkpoint tuple for ket-half backtrack

## Verification

- `python3 tests/test_dirac_slice_b_red.py` PASS
- `python3 tests/test_dirac_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: Slice B Green 後の可読性整理。bra/inner
  分岐を `_bra_or_inner` に抽出し、lexer の ket 半バックトラックを checkpoint
  タプルで明示。

### 残存リスク・検証の溝 (Verification Gap)
- **AIが推測で補った部分**: ket 半は bra 直後の trivia スキップ後のみ。改行を
  挟む `⟨0|\n1⟩` は受け入れ得るが、意図しない識別子+`⟩` 誤認はラベル規則で
  抑制している。
- **レビュー重点**: Slice C の `⟨φ|A|ψ⟩` と衝突しないか（今は ket 半が先に
  ラベル+閉じだけを要求するため、`⟨0|A|1⟩` は A を ket 半と誤認しうる —
  次スライスで要設計）。

## Next safe action

Adjudicator Refactor / Slice B completion → Slice C plan intake（matrix
element）+ PR merge 指示。
