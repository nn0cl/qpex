# Trace: LISS-0073 Slice C Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Slice | C — `⟨φ|A|ψ⟩` matrix element |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0073-slice-c-red` |

## [DESIGN CHECK]

- Scope: parse `⟨φ|A|ψ⟩` → `inner(φ, A(ψ))`; reject State middle with
  `OPERATOR_ALGEBRA_TYPE_ERROR`; EBNF `bra_op_ket`; preserve A/B.
- Refactor: `_inner_call` / `_take_ket_lit`; shared `_PAULI_ATOM_NAMES`.
- Verification: Slice C/B/A + unicode math PASS.

## Delivered

- `compiler/qpex/parser.py` — speculative mid-expr + ket in `_bra_or_inner`
- `compiler/qpex/typecheck.py` — `_check_matrix_element_middle`
- `docs/specs/grammar/qpex.ebnf` — `bra_op_ket`

## Verification

- `python3 tests/test_dirac_slice_c_red.py` PASS
- `python3 tests/test_dirac_slice_b_red.py` PASS
- `python3 tests/test_dirac_slice_a_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: 行列要素 `⟨φ|A|ψ⟩` を `inner(φ, A(ψ))` に
  畳み込み、State 中間を代数エラーにし、Pauli 名集合を共有定数化。

### 残存リスク・検証の溝 (Verification Gap)
- mid-expr の speculative `_call()` は失敗時にバックトラックするが、副作用の
  ある parse 経路が増えると復元漏れに注意。
- Slice D（outer/projector）は ket 直後の `BRA` 並置が必要で別設計。

## Next safe action

Adjudicator Slice C completion → Slice D plan; merge PR.
