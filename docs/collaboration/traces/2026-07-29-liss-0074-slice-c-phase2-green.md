# Trace: LISS-0074 Slice C Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | C — acting-space / Operator / no silent qubit coerce |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0074-slice-c-red` |

## [DESIGN CHECK]

- Scope: resolve qudit declared acting space; LocalRegister equivalence for
  QutritRegister ≅ QuditRegister<3,N>; reject silent qubit Operator in
  qudit-only context. No SV (D) / backend (E).
- Refactor: helpers next to Operator bind / `_ty_from_ref`; binder message
  generalized. No further structural split needed.
- Verification: Slice C + A + B suites PASS.

## Delivered

- `compiler/staqex/finite_binder.py` — `operator_declared_space` for qudit
- `compiler/staqex/typecheck.py` — `_operator_domain_payload`,
  `_check_silent_qubit_operator_coercion`

## Verification

- `python3 tests/test_qudit_slice_c_red.py` PASS
- `python3 tests/test_qudit_slice_a_red.py` PASS
- `python3 tests/test_qudit_slice_b_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: qudit の acting-space を宣言どおり解決し、
  qudit 専用文脈での無言 qubit Operator 強制を禁止した。

### 残存リスク・検証の溝 (Verification Gap)
- SV / backend（D/E）は未着手。
- RegisterSet 複合の qudit 拡張は ADR 0105 フォロー。
- `LocalRegister` は型検査ペイロードの正規化であり、ソース表面の別名ではない。

## Next safe action

Adjudicator Slice C completion → PR / merge; Slice D plan intake.
