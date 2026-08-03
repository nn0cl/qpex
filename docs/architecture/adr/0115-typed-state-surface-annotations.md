# ADR 0115: Typed `state` surface annotations

## Status

**Accepted** (Adjudicator plan authorize, 2026-07-31) — architecture for
[LISS-0129](../documentation-compression-map.md).

Amends [ADR 0037](0037-type-first-dimensions-structured-units.md) §A.

## Context

Friction F-07 and the Option B program require an explicit physicist spelling
`state x: State<T> = …` that today fails with `PARSE_ERROR`. Type-First
`State<T> x = …` already ships; inference-only `state x = …` already ships.
The missing form is **keyword `state` plus a colon annotation**.

Physicist × DX harmony prefers honest Type-First heads without forcing every
bind to drop the `state` keyword that marks Never Leave the State choreography.

## Decision

1. **Annotatable form (normative):**
   `state name: State<…> = expr`
   and tuple form
   `state (a, b): State<(A, B)> = expr`.
2. Semantics are identical to Type-First
   `State<…> name = expr` / `State<(A,B)> (a, b) = expr`:
   the annotation is a declared carrier checked against the inferred type of
   `expr` (existing `_check_assign` / product-bind rules).
3. **Inference-only** `state name = expr` and **Type-First** `State<T> name = expr`
   remain legal; no retirement.
4. The annotation type **must** be a `State` (or product `State<(…)>`) carrier.
   Annotating `state x: Float = …` or other non-State heads is a hard diagnostic
   (`STATE_ANNOTATION_TYPE_ERROR`). Classical quantities stay Type-First
   (`Float c = …`, `Mass m = …`) per ADR 0037 / 0114 — do not revive `val`.
5. Mismatch between annotation payload/dimension and `expr` uses the same
   diagnostics as Type-First State binds (`TYPE_MISMATCH`,
   `DIMENSION_MISMATCH_ERROR`, `PRODUCT_BIND_ERROR`, local-dimension checks).

## Consequences

- Parser `_state_bind` accepts optional `: TypeRef` before `=`.
- Coverage ledger F-07 → shipped after LISS-0129 Green.
- Does not authorize SI beyond (L,M,T), continuous PDF, exact rational, or
  QPU lowering changes.

## Verification

- Phase 1 Red: parse + typecheck scenarios in
  `tests/test_typed_surface_annotations_red.py`.
- Green: Kernel parse/typecheck/run for annotated binds; mismatch rejects.
