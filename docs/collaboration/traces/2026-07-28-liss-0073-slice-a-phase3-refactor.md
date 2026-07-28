# Trace: LISS-0073 Slice A Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | A — BraLit primary wiring |
| Phase | phase-3-refactor |
| Branch | `feature/liss-0073-slice-a-red` |
| Implementation | readability only |

## [DESIGN CHECK]

- Scope: collapse ket/bra typecheck path; tighten adjacent parser matches; no
  behavior change.
- Specs: Slice A Green + Red suite.
- Verification: `python3 tests/test_dirac_slice_a_red.py` PASS.

## Delivered

- `compiler/qpex/typecheck.py` — `isinstance(expr, (KetLit, BraLit))`
- `compiler/qpex/parser.py` — adjacent KET/BRA matches without blank line gap

## Verification

- `python3 tests/test_dirac_slice_a_red.py` PASS; behavior unchanged from Green.

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: Slice A Green 後の可読性整理。ket/bra の
  同一キャリア推論を一つの分岐にまとめ、parser の Dirac リテラル分岐を隣接配置。

### 残存リスク・検証の溝 (Verification Gap)
- **AIが推測で補った部分、またはハルシネーションが発生しやすい箇所**: alone
  bra を `State<Qubit>` とみなすのは Slice A の暫定契約。Slice B の並置
  (`⟨φ|ψ⟩`) で意味論が締まるまで、bra を State として measure する利用は未定義。
- **人間がコードレビューで重点的に見るべきポイント**: `BraLit` が Expr 連合に
  入った一方、evaluator / unitarity / physical_axioms はまだ `KetLit` 専用のまま
  （Slice A 非目標）。実行パスに bra を流すと後続 Issue で穴が出る。

## Next safe action

Adjudicator Refactor / Slice A completion → Slice B plan intake（`⟨φ|ψ⟩` →
`inner`）.
