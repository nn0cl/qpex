# Trace: LISS-0075 Slice A complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Slice | A — `HirLinearVerifier` + `LINEAR_DUPLICATE_USE` |
| Phase | Red → Green → Refactor **complete** |
| Branch | `feature/liss-0075-linear-quantum-usage` |

## Delivered

- `tests/test_linear_usage_slice_a_red.py`
- `compiler/staqex/hir.py` — `HirLinearVerifier`; rejects `State alias = q`
  rebinding; tracks measure consumption of linear roots

## Expected Red (before Green)

`ImportError: cannot import name 'HirLinearVerifier'`

## Verification after Refactor

```
PASS test_linear_verifier_importable
PASS test_duplicate_quantum_use_emits_named_diagnostic
PASS test_single_quantum_consumption_is_accepted
```

## Next safe action

Slice B Phase 1 Red — `LINEAR_IMPLICIT_DISCARD` + ancilla lifetime.
