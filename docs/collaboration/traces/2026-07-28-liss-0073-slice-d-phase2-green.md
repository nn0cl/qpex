# Trace: LISS-0073 Slice D Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | D — `\|ψ⟩⟨φ\|` outer / projector |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0073-slice-d-red` |

## [DESIGN CHECK]

- Scope: parse `\|ψ⟩⟨φ\|` → `Call(outer, [KetLit, BraLit])`; matching labels →
  `Call(projector, [KetLit])`; `Operator` bind routes KET/BRA to `_expression`;
  EBNF `ket_bra_outer` + OpHop note; preserve A/B/C.
- Refactor: shared `_algebra_call` for `inner` / `outer` / `projector`.
- Verification: Slice D/B/C/A Red suites PASS.

## Delivered

- `compiler/qpex/parser.py` — `_ket_or_outer`; Operator bind KET/BRA routing;
  `_algebra_call`
- `docs/specs/grammar/qpex.ebnf` — `ket_bra_outer` in `primary`

## Verification

- `python3 tests/test_dirac_slice_d_red.py` PASS
- `python3 tests/test_dirac_slice_c_red.py` PASS
- `python3 tests/test_dirac_slice_b_red.py` PASS
- `python3 tests/test_dirac_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: ket–bra 並置 `\|ψ⟩⟨φ\|` を
  `outer` / ラベル一致時 `projector` の代数 `Call` に畳み込み、`Operator`
  束縛でも Dirac 表面を式パーサへ委譲し、EBNF に `ket_bra_outer` と OpHop
  注記を追加。

### 残存リスク・検証の溝 (Verification Gap)
- `Operator` 束縛の KET/BRA ルーティングは OpDSL ではなく式 AST を返す —
  型検査は関数形 `outer`/`projector` に依存（意図どおり）。
- Slice E（式 postfix `†`）は未着手。

## Next safe action

Adjudicator Slice D completion → PR / merge; Slice E plan intake.
