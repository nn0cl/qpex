# LISS-0080: Phase-resolved typed HIR

## Metadata

- Local issue ID: LISS-0080
- GitHub issue: not created
- Status: **Slice A Green+Refactor ready for review** (2026-07-29)
- Phase: slice-a phase-3-refactor (pending completion approval)
- Type: frontend / HIR / semantic IR
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced A–D; A Green done)
- Owner/agent: —
- Related branch: `feature/liss-0080-slice-a-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E2 — Semantic IR
- Depends on: [LISS-0071](LISS-0071-versioned-conformance-and-differential-oracle.md)
  **complete**; [LISS-0072](LISS-0072-lossless-cst-formatter-and-source-versioning.md)
  **complete**
- **Does not depend on** [LISS-0070](../work-plans/WP-0025-qpex-v1-north-star.md)
  (Rust deferred); HIR ships first on the Python Shipping Kernel
- Unlocks: [LISS-0075](../work-plans/WP-0025-qpex-v1-north-star.md) (linear usage);
  LISS-0081 / LISS-0082
- Related: [ADR 0106](../architecture/adr/0106-qpex-v1-north-star-language-and-compiler.md)
  D9; [compiler blueprint §4.1](../architecture/qpex-v1-compiler-blueprint.md);
  [`compiler/qpex/typecheck.py`](../../compiler/qpex/typecheck.py)

## Summary

Introduce an **immutable phase-resolved typed HIR** on the Python Shipping
Kernel by **additive extraction** from the existing typechecker — not a
big-bang IR rewrite (ADR 0106 D9).

Blueprint HIR carries: resolved symbols, declaration phase, typed source
expressions, explicit effects/capabilities, and source/desugaring provenance.
Frontend diagnostics remain before any Physics IR (LISS-0081).

Plan companion:
[`qpex-v1-phase-resolved-hir-plan.md`](../specs/qpex-v1-phase-resolved-hir-plan.md).

## Acceptance Notes (Issue complete when)

1. Immutable HIR DTO exists with a documented build API from `TypeChecker`
   (symbol table + typed expression map at minimum).
2. Declaration **phase** is recorded on HIR decls where the Kernel already
   has scientific-scope / phase contracts (body-level LISS-0076 remains out).
3. **Effects / capabilities** appear explicitly on HIR (lift from existing
   `effects {…}` / `fun_effects`).
4. Provenance (source spans + desugar links) is present; a small verifier
   rejects invalid HIR construction; frontend diagnostics arise at/before
   HIR build.
5. Slices A–D Red/Green land; no Physics IR, Quantum Semantic IR, or
   proof-driven uncomputation in this Issue; evaluator semantics unchanged
   unless an approved slice explicitly wires HIR (Slice A does **not**).
6. Rust HIR (LISS-0070) remains a later mirror behind the same contracts.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Immutable HIR DTO + build API from `TypeChecker` (symbols / `Ty` map);
  evaluator unwired; pipeline wiring optional/minimal | **Green+Refactor ready** |
| **B** | Declaration **phase** resolution recorded on HIR decls | plan → Red → Green → Refactor |
| **C** | **Effects / capabilities** explicit on HIR (lift `fun_effects`) | plan → Red → Green → Refactor |
| **D** | Provenance + HIR verifier + docs/catalog closeout; linear analysis
  deferred to LISS-0075 | plan → Red → Green → Refactor |

## Non-goals

- Physics IR (LISS-0081) or Quantum Semantic IR (LISS-0082).
- Proof-driven uncomputation / linear usage enforcement (LISS-0075).
- Body-level scientific phase typing (LISS-0076).
- Rust HIR / Cargo workspace (LISS-0070).
- Big-bang rewrite of `pipeline.py` / evaluator around HIR.
- OpenQASM / QPU IR changes.

## Adjudicator Decision Points (plan)

- [x] Approve Issue ID **LISS-0080**, acceptance notes, and slices A–D above.
- [x] Confirm **dependency rewrite**: LISS-0071 + LISS-0072 only; **drop
      LISS-0070** for this Issue (Python Kernel first).
- [x] Confirm architecture: **additive HIR extraction** from typecheck; no
      big-bang IR rewrite (ADR 0106 D9).
- [x] Confirm first Red batch: **Slice A only** after plan approval
      (`tests/test_hir_slice_a_red.py`; module/API missing → Red).
- [x] Confirm Slice A does **not** rewire the evaluator (API / DTO only).

## Adjudicator Decision Points (Slice A Red)

- [x] Approve Phase 1 Red assertions (`tests/test_hir_slice_a_red.py`).
- [x] Authorize Phase 2 Green for `compiler.qpex.hir` (`HirModule`,
      `build_hir`) only — symbols + typed map; evaluator unwired.

## Adjudicator Decision Points (Slice A Green / Refactor)

- [ ] Approve Phase 2 Green + Phase 3 Refactor (`HirModule` /
      `build_hir`; MappingProxyType immutability).
- [ ] Confirm Slice A complete and allow Slice B plan (declaration phase
      on HIR decls).

## Work Notes

- 2026-07-29: Plan intake opened after LISS-0112 complete; LISS-0075 blocked
  on LISS-0080; WP listed 0080 depending on deferred LISS-0070 — rewritten to
  Python Shipping Kernel path per WP critical path and Adjudicator dependency
  resolution.
- 2026-07-29: Plan merged via PR #113 (`168315b`). Plan **approved** (“承認”).
  Phase 1 Red — `tests/test_hir_slice_a_red.py`. Expected Red: missing
  `compiler.qpex.hir` / `HirModule` / `build_hir`.
- 2026-07-29: Slice A Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. `compiler/qpex/hir.py` ships immutable symbols + typed
  map; suite PASS.

## Verification

- Plan: merged PR #113.
- Slice A: `python3 tests/test_hir_slice_a_red.py` PASS.
