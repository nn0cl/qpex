# Trace: LISS-0080 Slice A completion + Slice B plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0080 |
| Path | Feature Path — Slice A closeout + Slice B plan (docs) |
| Phase | slice-a done; slice-b phase-0-design |
| Branch | `feature/liss-0080-slice-a-red` |
| Implementation | **forbidden** for Slice B until plan approval |

## [DESIGN CHECK]

- Scope: close Slice A after Green approval; propose Slice B only —
  record declaration **phase** on HIR decls from existing scientific-scope
  contracts (`ScientificScopeDecl.kind` / sealed contracts). Body-level
  phase typing (LISS-0076) stays out. Effects (C) and provenance (D) out.
- Specs: Issue acceptance note 2; Slice A `HirModule` already ships
  symbols + typed.
- Verification: land Slice A PR; docs for B plan; no B Red yet.

## Slice A completion evidence

- `tests/test_hir_slice_a_red.py` PASS
- Commits: Red `610c46d` → Green `3457147`

## Slice B requested approval

**Plan approval** for Slice B only with declaration-phase policy above.

## Next safe action

Adjudicator Slice B plan approval → Phase 1 Red only.
