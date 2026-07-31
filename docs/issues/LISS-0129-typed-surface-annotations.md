# LISS-0129: Typed surface annotations

## Metadata

- Local issue ID: LISS-0129
- Status: **complete** — 2026-07-31
- Phase: Feature Path Phase 3
- Type: language surface
- Priority: P0
- ADR: [0115](../architecture/adr/0115-typed-state-surface-annotations.md)
- Tests: `tests/test_typed_surface_annotations_red.py`
- Branch: `feature/liss-0129-expression-and-qpu-honesty`

## Summary

Ship `state name: State<T> = …` annotations (ADR 0115), alongside existing
Type-First and inference-only forms.

## Exit

- [x] ADR 0115 Accepted
- [x] Phase 1 Red / 2 Green / 3 Refactor
- [x] Coverage ledger F-07 → shipped
- [x] Spec sync
