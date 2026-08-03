# LISS-0282: Kernel — local type inference

## Metadata

- Local issue ID: LISS-0282
- GitHub issue: _(none yet)_
- Status: **complete** — Kernel shipped 2026-08-03 (WP-0089)
- Phase: Feature Path Red → Green → Refactor (**after** LISS-0281 Accept)
- Type: Feature Kernel
- Priority: P2
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0281](LISS-0281-adr-local-type-inference.md) **Accepted**
- Paths: `compiler/staqex/**`, `tests/test_liss_0282_*` (name at Red)

## Summary

Implement Accepted local type inference. Red tests match ADR Then-clauses.
Do not edit tests to force Green.

## Exit

- [ ] Phase 1 Red: failing tests for Accepted cases + fail-closed negatives
- [ ] Phase 2 Green: minimal implementation
- [ ] Phase 3 Refactor + regression SV
- [ ] No axiom regression

## Verification

- Named pytest + `python3 tests/spec_verification/run_all.py` as required by DoD
