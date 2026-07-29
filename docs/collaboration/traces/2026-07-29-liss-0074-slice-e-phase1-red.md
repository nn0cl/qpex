# Trace: LISS-0074 Slice E Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | E — QASM/QPU hard reject + closeout |
| Phase | phase-1-red |
| Branch | `feature/liss-0074-slice-e-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for `run.HARD_CODES` sync, CLI emit-qasm reject on Qutrit
  measure, emitter reject for annotation-only Qutrit / QutritRegister; qubit
  path unchanged. Exclude D=3 SV / qudit opcodes.
- Specs: Slice E plan approval; probes confirmed Red gaps.
- Verification: suite must fail before Green on the new Red cases.

## Delivered

- `tests/test_qudit_slice_e_red.py`

## Expected Red

1. `UNSUPPORTED_LOCAL_DIMENSION` / `LOCAL_DIMENSION_TYPE_ERROR` absent from
   `run.HARD_CODES`.
2. CLI `emit-qasm` exits 0 with OPENQASM on `State<Qutrit>` measure.
3. Annotation-only `State<Qutrit>` / `QutritRegister` emit OPENQASM.

Regression (already Green): qubit `emit-qasm` succeeds.

## Next safe action

Adjudicator Red approval → Slice E Phase 2 Green.
