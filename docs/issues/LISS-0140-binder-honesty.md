# LISS-0140: Binder honesty (silent deferral → hard diagnostics)

## Metadata

- Local issue ID: LISS-0140
- Status: **complete** — 2026-07-31
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel residual / honesty
- Priority: P0 (WP-0032)
- Depends on: ADR 0096 D6; ADR 0088
- Program: [WP-0032](../work-plans/WP-0032-adr-deferred-finite-slices.md)
- Implementation permission: **yes** (Adjudicator Plan 承認 2026-07-31)
- Branch: `feature/wp-0032-adr-deferred-finite`
- Tests: `tests/test_binder_honesty_red.py`

## Summary

Non-`Index` binder domains (e.g. `Basis<N>`) and unbound indexed coefficients
(`J[i]` before LISS-0143 arrays) hard-fail with explicit binder diagnostics
instead of silent no-op lowering and late RUNTIME failure.

## Exit

- [x] Red: Basis domain → `BINDER_DOMAIN_ERROR`; bare `J[i]` →
  `BINDER_LOWERING_UNSUPPORTED`
- [x] Green: typecheck + metadata paths emit those codes; no silent swallow
- [x] Docs / register updated
