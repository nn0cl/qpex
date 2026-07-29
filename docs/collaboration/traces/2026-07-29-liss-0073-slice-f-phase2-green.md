# Trace: LISS-0073 Slice F Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Slice | F — `[A,B]` / `{A,B}` brackets |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0073-slice-f-red` |

## [DESIGN CHECK]

- Scope: Operator-context `[A,B]` → `commutator`; `{A,B}` → `anticommutator`;
  expr `ListExpr` preserved; EBNF productions; OpDSL primary brackets.
- Refactor: `_comma_expr_items` / `_comma_op_expr_items` helpers.
- Verification: Slice F + A–E PASS; list+when smoke OK.

## Delivered

- `compiler/qpex/parser.py` — `_commutator_bracket_context`; brace primary;
  OpDSL bracket primaries; comma-item helpers
- `docs/specs/grammar/qpex.ebnf` — `bracket_commutator` / `brace_anticommutator`

## Verification

- `python3 tests/test_dirac_slice_f_red.py` PASS
- `python3 tests/test_dirac_slice_{a,b,c,d,e}_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: Operator 文脈の `[A,B]`/`{A,B}` を
  `commutator`/`anticommutator` の代数 `Call` に畳み込み、式側リスト意味を
  維持しつつ EBNF を同期。

### 残存リスク・検証の溝 (Verification Gap)
- 式側 `[A,B]` は意図的に `ListExpr` のまま（commutator は関数形または
  Operator 束縛の句読法）。
- OpDSL 内 brackets は `Call` を返すため、周囲が純 `OpExpr` のとき混在に注意。
- Slice G（モデル凍結）は未着手。

## Next safe action

Adjudicator Slice F completion → PR / merge; Slice G plan intake.
