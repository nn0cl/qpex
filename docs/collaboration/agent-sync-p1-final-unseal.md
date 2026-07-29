# Agent sync: ADR 0034 + Hold unseal

Date: 2026-07-23. Sync **10 / 10**.

## Locks

1. **Vacuum:** `State.vacuum()`; norm 0; absorbing; `measure` → empty outcome.
2. **Compare:** `State` ops → `State<Bool>` for `when`.
3. **Prelude:** `state.*`, `Math`, `inspect`, selected `File` auto-imported.

## Unsealed

Kernel PoC harness, parser, AST, typechecker — **may implement** (AT-TDD).

## Still later

IR optimizer mandatory passes, full Float Math, styler enforcement, QPU.

Canonical: `staqex-language-spec.md` §12; ADR 0034.
