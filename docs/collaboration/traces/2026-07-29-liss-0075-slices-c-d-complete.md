# Trace: LISS-0075 Slices C–D complete

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Slice | C — Uncompute witness; D — `build_hir` wiring + e2e |
| Phase | Red → Green → Refactor **complete** (one-time C/D approval) |
| Branch | `feature/liss-0075-linear-quantum-usage` |
| Approval | Adjudicator「今回のみ承認」— risks accumulate (R1–R10) |

## Delivered

### Slice C
- `tests/test_linear_usage_slice_c_red.py`
- Static uncompute witness: same-name rebind to `|0>` / `vacuum`
- `UNCOMPUTE_WITNESS_MISSING` when `effects { Uncompute }` lacks witness
- `build_hir` merges `"Uncompute"` onto `HirDecl.effects` when witnessed
- `TypeChecker._EFFECTS` / `_KNOWN_EFFECTS` include `Uncompute`
- **R10**: fun-local State via Type-First / in-block tracking (env alone insufficient)

### Slice D
- `tests/test_linear_usage_slice_d_red.py`
- `HirModule.linear_diagnostics` populated by `HirLinearVerifier` inside `build_hir`
- E2E covers A (duplicate), B (discard), C (Uncompute on decl)

## Provisional / parked

- R7/R9: evaluator simulator-equivalence deferred; static witness only
- R5: linear diags on HIR only — not yet hard-fail in `compile_source` / CLI

## Verification

```
PASS Slice A (3)
PASS Slice B (3)
PASS Slice C (3)
PASS Slice D (2)
PASS LISS-0080 HIR Slice D
```

## Next safe action

Adjudicator **completion approval** (or commit/PR request). Do not auto-close
R1–R10. Optional follow-up: fold linear diags into pipeline; runtime uncompute.
