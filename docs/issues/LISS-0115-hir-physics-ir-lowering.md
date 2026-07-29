# LISS-0115: HIR → Physics IR lowering

## Metadata

- Local issue ID: LISS-0115
- Status: **proposed** — ID reserved; implementation not started
- Phase: Feature Path / plan intake gated
- Type: compiler / IR
- Priority: P0
- Planning size: L (estimate; refine at plan intake)
- Parent: [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md)
  (A–D + E Phase 1 accepted; follow-up boundary)
- Related: WP-0025 LISS-0081; [LISS-0080](LISS-0080-phase-resolved-typed-hir.md)

## Claim notice

**Do not reuse this ID.** Reserved as the LISS-0081 follow-up for real HIR →
Physics IR lowering (beyond the structural `build_physics_ir` boundary already
on `main`). Earlier “Slice A Green / parallel agent” wording was a
collision-avoidance stub and is **withdrawn** — authoritative progress is on
LISS-0081.

## Summary

Lower phase-resolved HIR into Physics IR equation/operator structures without
gate expansion, and wire the builder into the compiler pipeline only under
separate Phase approval. Depends on the reviewed LISS-0081 DTO/verifier
boundary.

## Out of scope until plan approval

- Expanding binders, Jordan–Wigner mapping, evaluator execution
- Equation/Unit DTO depth (LISS-0116)
- Source-backed golden loading (LISS-0117)

## Adjudicator Decision Points

- [ ] Approve plan intake / first Red slice for LISS-0115
- [ ] Confirm relationship to any remaining LISS-0081 closeout
