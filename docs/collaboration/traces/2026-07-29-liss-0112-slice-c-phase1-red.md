# Trace: LISS-0112 Slice C Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0112 |
| Slice | C — conformance / catalog / closeout |
| Phase | phase-1-red |
| Branch | `feature/liss-0112-slice-c-red` |
| Implementation | **forbidden** until Red approval → Green |

## [DESIGN CHECK]

- Scope: Red for E06-003 conformance row; diagnostic catalog LISS-0112
  notes; Issue **complete** status. Regression (already Green): QASM
  reject, `Qudit<4>` / `apply(H)` unsupported. No new SV gates.
- Specs: Slice C plan approval (“承認”); Slice B on `main` via PR #111.
- Verification: catalog/Issue assertions must fail before Green.

## Delivered

- `tests/test_qudit_d3_sv_slice_c_red.py`

## Expected Red

Missing `E06-003` / `LISS-0112` in catalogs; Issue not yet **complete**.

Regression PASS: QASM reject; D≠3 / non-Identity unsupported.

## Next safe action

Adjudicator Red approval → Slice C Phase 2 Green (docs closeout).
