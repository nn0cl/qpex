# Trace: LISS-0112 Slice B Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0112 |
| Slice | B — Identity evolve / apply(I) on D=3 |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0112-slice-b-red` |

## [DESIGN CHECK]

- Scope: lift `UNSUPPORTED_LOCAL_DIMENSION` for bare Identity `apply(I)` /
  `evolve … under I` on `State<Qutrit>` / `State<Qudit<3>>`; runtime Identity
  is a no-op preserving levels including `|2⟩`. Non-Identity (`H`) and
  `Qudit<4>` stay rejected. No clock/shift, registers, Slice C.
- Specs: Slice B Red approval (“承認”).
- Verification: Slice B + A + LISS-0074 A–E PASS.

## Delivered

- `compiler/staqex/typecheck.py` — `_expr_is_identity_atom`; Identity-only
  `allow_mvp_d3` on apply/evolve seeds
- `compiler/staqex/runtime/evaluator.py` — Identity no-op in `_bind_apply` and
  `_hamiltonian_evolve_one_step`

## Verification

- `python3 tests/test_qudit_d3_sv_slice_b_red.py` PASS
- `python3 tests/test_qudit_d3_sv_slice_a_red.py` PASS
- `python3 tests/test_qudit_slice_{a,b,c,d,e}_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: D=3 上の Identity evolve/apply を許可し、
  Hilbert レベル（含 `|2⟩`）を保持する無操作パスを Runtime に入れた。

### 残存リスク・検証の溝 (Verification Gap)
- Identity は bare atom（`I`/`ID`/`IDENTITY`）のみ。束縛 `Operator = I` 経由は
  未拡張（Red 外）。
- 非 Identity / register / QASM / D≠3 は意図どおり reject。
- Slice C（conformance/closeout）未着手。

## Next safe action

Adjudicator Slice B complete → PR merge → Slice C plan.
