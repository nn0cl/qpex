# Trace: LISS-0112 Slice A Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0112 |
| Slice | A — D=3 ket + measure |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0112-slice-a-red` |

## [DESIGN CHECK]

- Scope: lift `UNSUPPORTED_LOCAL_DIMENSION` on measure for `Qutrit` /
  `Qudit<3>` only; encode `Qudit<D>` in Ty payload; ket label `2`; Qubit
  cardinality check via dim=2; evolve/apply remain rejected. No Identity (B).
- Refactor: `allow_mvp_d3` flag on runtime check; helpers stay local.
- Verification: Slice A + D + B + E suites PASS.

## Delivered

- `compiler/qpex/typecheck.py` — MVP D=3 measure allow; `Qudit<D>` payload;
  Qubit local-dim=2 for ket labels
- `compiler/qpex/runtime/quantum_ops.py` — ket label `2`
- `tests/test_qudit_slice_d_red.py` — measure assertions updated for 0112

## Verification

- `python3 tests/test_qudit_d3_sv_slice_a_red.py` PASS
- `python3 tests/test_qudit_slice_{b,d,e}_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: D=3 の ket+measure を本物の局所次元として
  実行可能にし、黙った qubit SV / 未対応 evolve は拒否したままにした。

### 残存リスク・検証の溝 (Verification Gap)
- Identity evolve/apply（Slice B）は未着手。
- QASM は引き続き qudit を拒否（意図どおり）。
- `State<Qubit> = |2⟩` は型検査で拒否（dim=2）；単独 untyped `|2⟩` は実行時に通る可能性。

## Next safe action

Adjudicator Slice A completion → PR / merge; Slice B plan/Red.
