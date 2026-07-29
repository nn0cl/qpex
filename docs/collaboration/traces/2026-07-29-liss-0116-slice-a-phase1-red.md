# Trace: LISS-0116 Slice A Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0116 |
| Slice | A — Coefficient / Unit / dimension tags |
| Phase | Phase 1 Red |
| Branch | `feature/liss-0116-slice-a` |
| Parallel | LISS-0115 A–B owned by another agent |

## [DESIGN CHECK]

- Scope: immutable `Unit` `(L,M,T)` tags + `Coefficient` + module verifier
  diagnostics; no `EquationNode` yet (Slice B); no `physics_ir.py` edits.
- Specs: LISS-0116 Issue; WP-0028 exclusive paths; SourceOrigin from
  `physics_ir` (read-only import).
- Verification: `python3 tests/test_physics_equation_slice_a_red.py` fails
  with ImportError until Green.

## Delivered

- `tests/test_physics_equation_slice_a_red.py`
- Issue / claim / register status → Agent A in progress

## Next safe action

Adjudicator Slice A Red approval → Phase 2 Green (`physics_equation.py` only).
