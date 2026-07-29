# Trace: LISS-0073 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0073 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design |
| Branch | `docs/liss-0073-dirac-algebra-plan` |
| Implementation | **forbidden** until plan approval; then Slice A Phase 1 Red only |

## [DESIGN CHECK]

- Scope and expected behavior: Propose named Dirac punctuation → typed algebra
  AST slices A–G; lower to LISS-0031 / ADR 0087 contracts; no macros.
- Specifications and files inspected: WP-0025 E1; ADR 0106 D5; ADR 0087;
  north-star §3.1/§6.1; compiler blueprint §3.1–3.2; LISS-0031; LISS-0069
  A.1 deferral; LISS-0072 completion; lexer BRA / parser `_primary` gap;
  `staqex-operator-algebra.md`; migration matrix M-P06.
- Component boundaries: parser / AST / typecheck only; Joint evaluator reuse;
  Physics IR (LISS-0081) out; formatter emit optional follow in Slice G.
- Applicable constraints: no phase skip; docs-only until plan approval; no
  work on `main`.
- Decisions pending Adjudicator: BraLit vs immediate desugar; matrix-element
  juxtaposition; Slice F brackets vs defer; expression-side `†`; M-P06
  dual-accept; diagnostic code reuse; Slice A Red authorization.
- Included AI context: WP row, ADR 0087/0106, shipping lexer/parser evidence.
- Omitted: full SV corpus, Physics IR design, Rust frontend.
- Task routing: deterministic docs edit; no model-critical codegen.
- Verification plan: docs PR; link check; no `compiler/` or `tests/` mutation.

## Delivered

- `docs/issues/LISS-0073-named-dirac-notation-and-algebra-ast.md`
- `docs/specs/staqex-v1-dirac-algebra-ast-plan.md`
- `docs/architecture/open-work-register.md` (LISS-0073 row + LISS-0031 note)
- `docs/work-plans/WP-0025-staqex-v1-north-star.md` (plan proposed)

## Approval outcome

Adjudicator approved the plan (“承認”) with the recommended defaults:

- slices A–G; Slice F deferred until A–E green;
- first-class `BraLit` + typecheck lowering to algebra contracts;
- matrix elements via `BRA` + expr + `KET` juxtaposition;
- expression-side `†` in Slice E;
- M-P06 function-shaped dual-accept retained;
- reuse `OPERATOR_ALGEBRA_TYPE_ERROR` where applicable;
- Phase 1 Red authorized for **Slice A only**.

## Explicitly not authorized yet

- Slice A Phase 2 Green / production parser changes (until Red review)
- Slices B–G work
- Slice F bracket disambiguation as settled architecture
- M-P06 deprecate gate
- ADR 0087 supersession (extension of deferred sugar only)

## Next safe action

Slice A Phase 1 Red — add failing tests only
(`tests/test_dirac_slice_a_red.py`).
