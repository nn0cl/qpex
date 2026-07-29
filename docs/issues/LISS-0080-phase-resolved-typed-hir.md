# LISS-0080: Phase-resolved typed HIR

## Metadata

- Local issue ID: LISS-0080
- GitHub issue: not created
- Status: **complete** (2026-07-29)
- Phase: closed
- Type: frontend / HIR / semantic IR
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–D; all complete)
- Owner/agent: —
- Related branch: `feature/liss-0080-slice-d-red`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md) E2 — Semantic IR
- Depends on: [LISS-0071](LISS-0071-versioned-conformance-and-differential-oracle.md)
  **complete**; [LISS-0072](LISS-0072-lossless-cst-formatter-and-source-versioning.md)
  **complete**
- **Does not depend on** [LISS-0070](../work-plans/WP-0025-staqex-v1-north-star.md)
  (Rust deferred); HIR ships first on the Python Shipping Kernel
- Unlocks: [LISS-0075](../work-plans/WP-0025-staqex-v1-north-star.md) (linear usage);
  LISS-0081 / LISS-0082
- Related: [ADR 0106](../architecture/adr/0106-staqex-v1-north-star-language-and-compiler.md)
  D9; [compiler blueprint §4.1](../architecture/staqex-v1-compiler-blueprint.md);
  [`compiler/staqex/typecheck.py`](../../compiler/staqex/typecheck.py)

## Summary

Introduce an **immutable phase-resolved typed HIR** on the Python Shipping
Kernel by **additive extraction** from the existing typechecker — not a
big-bang IR rewrite (ADR 0106 D9).

Blueprint HIR carries: resolved symbols, declaration phase, typed source
expressions, explicit effects/capabilities, and source/desugaring provenance.
Frontend diagnostics remain before any Physics IR (LISS-0081).

Plan companion:
[`staqex-v1-phase-resolved-hir-plan.md`](../specs/staqex-v1-phase-resolved-hir-plan.md).

## Acceptance Notes (Issue complete when)

1. ✅ Immutable HIR DTO exists with a documented build API from `TypeChecker`
   (symbol table + typed expression map at minimum).
2. ✅ Declaration **phase** is recorded on HIR decls where the Kernel already
   has scientific-scope / phase contracts (body-level LISS-0076 remains out).
3. ✅ **Effects / capabilities** appear explicitly on HIR (lift from existing
   `effects {…}` / `fun_effects`).
4. ✅ Provenance (source spans) is present; a small verifier rejects invalid
   HIR construction; desugar links deferred to future pass.
5. ✅ Slices A–D Red/Green land; no Physics IR, Quantum Semantic IR, or
   proof-driven uncomputation in this Issue; evaluator semantics unchanged.
6. Rust HIR (LISS-0070) remains a later mirror behind the same contracts.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Immutable HIR DTO + build API from `TypeChecker` (symbols / `Ty` map);
  evaluator unwired; pipeline wiring optional/minimal | **complete** |
| **B** | Declaration **phase** resolution recorded on HIR decls | **complete** |
| **C** | **Effects / capabilities** explicit on HIR (lift `fun_effects`) | **complete** |
| **D** | Provenance + HIR verifier + docs/catalog closeout; linear analysis
  deferred to LISS-0075 | **complete** |

## Non-goals

- Physics IR (LISS-0081) or Quantum Semantic IR (LISS-0082).
- Proof-driven uncomputation / linear usage enforcement (LISS-0075).
- Body-level scientific phase typing (LISS-0076).
- Rust HIR / Cargo workspace (LISS-0070).
- Big-bang rewrite of `pipeline.py` / evaluator around HIR.
- OpenQASM / QPU IR changes.

## Adjudicator Decision Points (all resolved)

- [x] Plan, slices A–D, dependency rewrite, architecture — all approved.
- [x] Slice A–D Red / Green / Refactor — all approved and shipped.

## Work Notes

- 2026-07-29: Plan intake opened after LISS-0112 complete.
- 2026-07-29: Plan merged via PR #113. Slice A via PR #114. Slice B via
  PR #115. Slice C via PR #116.
- 2026-07-29: Slice D Red **approved** ("承認"). Green + Refactor:
  `HirDecl.span` (`HirSpan`), `verify_hir`; all suites PASS.
- 2026-07-29: **Issue complete.**

## Verification

- Slices A–D: all suites PASS.
- `python3 tests/test_hir_slice_a_red.py` PASS
- `python3 tests/test_hir_slice_b_red.py` PASS
- `python3 tests/test_hir_slice_c_red.py` PASS
- `python3 tests/test_hir_slice_d_red.py` PASS
