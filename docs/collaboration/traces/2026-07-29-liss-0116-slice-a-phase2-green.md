# Trace: LISS-0116 Slice A Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0116 |
| Slice | A — Coefficient / Unit |
| Phase | Phase 2 Green |
| Branch | `feature/liss-0116-slice-a` |
| Approval | Adjudicator (“承認”) after Red |

## [DESIGN CHECK]

- Scope: smallest immutable `Unit` + `Coefficient` + `verify_physics_equation`
  in owned module only.
- Forbidden paths untouched: `physics_ir.py`, `physics_ir_lower.py`, pipeline.
- Verification: `python3 tests/test_physics_equation_slice_a_red.py` PASS.

## Delivered

- `compiler/staqex/physics_equation.py`

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: Slice A Red を通す最小の Unit/Coefficient
  DTO とモジュール verifier を追加した。

### 残存リスク・検証の溝 (Verification Gap)
- **AIが推測で補った部分**: `(L,M,T)` を `dimensions: tuple[int,int,int]` とした。
- **人間がコードレビューで重点的に見るべきポイント**: diagnostic コード名が
  catalog 未登録（意図的・非 compile-hard）。

## Next safe action

Adjudicator Slice A completion → Slice B plan / Red、またはコミット／PR。
