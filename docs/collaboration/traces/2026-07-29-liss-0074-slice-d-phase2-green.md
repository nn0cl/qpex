# Trace: LISS-0074 Slice D Phase 2 Green + Phase 3 Refactor

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | D — hard unsupported qudit runtime |
| Phase | phase-2-green + phase-3-refactor |
| Branch | `feature/liss-0074-slice-d-red` |

## [DESIGN CHECK]

- Scope: hard `UNSUPPORTED_LOCAL_DIMENSION` on measure / evolve / apply of
  deferred qudit State or Operator domains; keep annotation-only programs
  typecheckable for A–C; no D=3 SV; exclude E.
- Refactor: helpers next to local-dimension diagnostics; no further split.
- Verification: Slice D + A + B + C suites PASS.

## Delivered

- `compiler/qpex/pipeline.py` — hard code registration
- `compiler/qpex/typecheck.py` — measure / evolve / apply entry checks

## Verification

- `python3 tests/test_qudit_slice_d_red.py` PASS
- `python3 tests/test_qudit_slice_{a,b,c}_red.py` PASS

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: qudit の measure / evolve / apply を
  名前付き診断で fail-closed し、黙った qubit SV を止めた。

### 残存リスク・検証の溝 (Verification Gap)
- 混合積 `State<(Qubit, Qutrit)>` の実行経路は未ゲート（注釈は Slice C 用に残す）。
- QASM/QPU / conformance（Slice E）は未着手。
- 本物の D=3 SV は別 Issue。

## Next safe action

Adjudicator Slice D completion → PR / merge; Slice E plan intake.
