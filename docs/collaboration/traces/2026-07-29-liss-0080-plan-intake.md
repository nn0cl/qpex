# Trace: LISS-0080 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Path | Feature Path — plan intake (docs only) |
| Phase | phase-0-design |
| Branch | `docs/liss-0080-plan-intake` |
| Implementation | **forbidden** until plan → Slice A Red approval |

## [DESIGN CHECK]

- Scope: file LISS-0080 for phase-resolved typed HIR; drop LISS-0070
  dependency; companion plan; register / WP updates. No compiler/tests.
- Specs: WP-0025 E2; ADR 0106 D9; compiler blueprint §4.1; LISS-0071/0072
  complete; LISS-0075 blocked on 0080.
- MVP default: additive HIR extraction from typecheck; slices A–D; first
  Red = Slice A only (API/DTO; evaluator unwired).
- Verification: docs PR; Adjudicator plan approval before Red.

## Delivered

- `docs/issues/LISS-0080-phase-resolved-typed-hir.md`
- `docs/specs/staqex-v1-phase-resolved-hir-plan.md`
- WP-0025 / open-work-register updates

## Next safe action

Adjudicator plan approval → Slice A Phase 1 Red only.
