# Trace: LISS-0074 Slice E Phase 2 Green + Phase 3 Refactor + closeout

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | E — QASM/QPU hard reject + Issue closeout |
| Phase | phase-2-green + phase-3-refactor + closeout |
| Branch | `feature/liss-0074-slice-e-red` |

## [DESIGN CHECK]

- Scope: sync CLI HARD_CODES; reject qudit TypeRefs in QASM emit/lower;
  conformance E06-002; catalog; close Issue; no D=3 SV / qudit opcodes.
- Refactor: shared `qudit_capability_reject` used by emitter and lower.
- Verification: Slice E + D + C + QASM function-call Red PASS.

## Delivered

- `compiler/qpex/run.py` — HARD_CODES sync
- `compiler/qpex/backend/qasm/lower.py` — `qudit_capability_reject`
- `compiler/qpex/backend/qasm/emitter.py` — reject before QPU/lower paths
- Diagnostic catalog + conformance `E06-002`

## Verification

- `python3 tests/test_qudit_slice_e_red.py` PASS
- `python3 tests/test_qudit_slice_{c,d}_red.py` PASS
- `python3 tests/test_qasm_function_call_rejection_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: qudit プログラムが qubit OPENQASM として
  黙って emit されないよう CLI/QASM 境界を fail-closed し、LISS-0074 を閉じた。

### 残存リスク・検証の溝 (Verification Gap)
- FunDecl 内のみの qudit 注釈は main スキャン外（Red は main 束縛を固定）。
- 本物の D=3 SV / OpenQASM qudit opcode は follow-up。

## Next safe action

Adjudicator Issue completion → PR / merge; optional follow-up Issue for D=3 SV.
