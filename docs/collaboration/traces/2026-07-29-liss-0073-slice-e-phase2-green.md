# Trace: LISS-0073 Slice E Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | E — expression-side postfix `†` |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0073-slice-e-red` |

## [DESIGN CHECK]

- Scope: `_call` accepts `DAGGER` → `_algebra_call("adjoint", [expr])`;
  EBNF `dagger_suffix`; OpDSL unchanged; preserve A–D.
- Refactor: reuse existing `_algebra_call` (no extra extract needed).
- Verification: Slice E + A–D + unicode math PASS.

## Delivered

- `compiler/staqex/parser.py` — `_call` `DAGGER` branch
- `docs/specs/grammar/staqex.ebnf` — `dagger_suffix` on `call_expr`

## Verification

- `python3 tests/test_dirac_slice_e_red.py` PASS
- `python3 tests/test_dirac_slice_{a,b,c,d}_red.py` PASS
- `python3 tests/test_unicode_math_source_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: 式側 postfix `†` を `Call(adjoint, …)`
  に畳み込み、Operator DSL と対称化し、EBNF に `dagger_suffix` を追加。

### 残存リスク・検証の溝 (Verification Gap)
- 式 AST は `Call(adjoint)`、OpDSL は `OpCall("adjoint")` — 型検査経路は別だが
  契約は ADR 0087 で揃う（意図どおりの二重表面）。
- Slice F（brackets）は A–E 完了後の別ゲート。

## Next safe action

Adjudicator Slice E completion → PR / merge; Slice F plan or G freeze intake.
