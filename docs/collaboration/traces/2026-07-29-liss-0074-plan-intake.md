# Trace: LISS-0074 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design |
| Branch | `docs/liss-0074-plan-intake` |
| Implementation | **forbidden** until plan approval; then Slice A Phase 1 Red only |

## [DESIGN CHECK]

- Scope and expected behavior: Propose `Qutrit` / `Qudit<D>` /
  `QutritRegister<N>` / `QuditRegister<D,N>` nominal local-dimension surface
  with label checks, acting-space honesty, and backend fail-closed; slices A–E.
- Specifications and files inspected: WP-0025 E1 LISS-0074 row; ADR 0106 D3;
  north-star §5.2; ADR 0102 / LISS-0029 / LISS-0058 / LISS-0067; LISS-0071
  complete; shipping `QubitRegister` typecheck evidence; LISS-0073 closed.
- Component boundaries: typecheck / AST TypeRef / optional small SV; no
  Physics IR; no silent qubit encoding; no Rust gate.
- Applicable constraints: docs-only until plan approval; no work on `main`.
- Decisions pending Adjudicator: Qutrit vs Qudit<3>; Slice D runtime depth;
  backend reject policy; Slice A Red authorization.
- Included AI context: WP row, ADR 0106 D3, north-star §5.2, QubitRegister
  baseline.
- Omitted: full SV corpus, photonic design, provider SDKs.
- Task routing: deterministic docs edit.
- Verification plan: docs PR; no `compiler/` or `tests/` mutation.

## Delivered

- `docs/issues/LISS-0074-qutrit-qudit-finite-local-dimension-types.md`
- `docs/specs/staqex-v1-qudit-local-dimension-plan.md`
- `docs/architecture/open-work-register.md` (LISS-0074 row)
- `docs/work-plans/WP-0025-staqex-v1-north-star.md` (next issue → 0074)

Adjudicator approved the plan (“承認”) with recommended defaults.
Slice A Phase 1 Red suite added.

## Next safe action

Adjudicator Red approval → Slice A Phase 2 Green.
