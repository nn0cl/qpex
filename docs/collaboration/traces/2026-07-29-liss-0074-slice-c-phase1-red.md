# Trace: LISS-0074 Slice C Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Slice | C — acting-space / Operator / no silent qubit coerce |
| Phase | phase-1-red |
| Branch | `feature/liss-0074-slice-c-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for QutritRegister identity resolution; silent qubit Operator
  reject; QutritRegister ≅ QuditRegister<3,N>; keep Qubit↛Qutrit domain error;
  typed (Qubit,Qutrit) product. Exclude D/E.
- Specs: Slice C plan approval; probes confirmed Red gaps.
- Verification: suite must fail before Green on the new Red cases.

## Delivered

- `tests/test_qudit_slice_c_red.py`

## Expected Red

1. `Operator<QutritRegister<2>> H = I` → still
   `IDENTITY_ACTING_SPACE_UNDETERMINED` at execution boundary.
2. `QutritRegister` + `Operator<QubitRegister>` → currently accepted.
3. `QutritRegister` → `QuditRegister<3,…>` → still `OPERATOR_DOMAIN_ERROR`.

Regression (already Green): QubitRegister ↛ QutritRegister; typed product.

## Next safe action

Adjudicator Red approval → Slice C Phase 2 Green.
