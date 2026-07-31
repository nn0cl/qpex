# LISS-0125: HIR `_expr_children` BinOp field mismatch

## Metadata

- Local issue ID: LISS-0125
- GitHub issue: none
- Status: **phase-3-reviewed complete** (2026-07-31)
- Phase: Phase 3 Refactor complete
- Type: language / Kernel bug fix
- Priority: P0 (blocks LISS-0122 B03 and LISS-0123 A01/A02/A04)
- Depends on: [LISS-0119](LISS-0119-examples-health-inventory.md) inventory evidence
- Blocks: clean heal of B03, A01, A02, A04 without sample-only workarounds
- Related: [LISS-0122](LISS-0122-examples-basics-heal.md),
  [LISS-0123](LISS-0123-examples-applied-heal-defer.md)
- Implementation permission: **yes** (Adjudicator 「承認」 2026-07-31)
- Branch: `feature/liss-0125-hir-binop-children`

## Summary

`hir._expr_children` reads `BinOp.left` / `BinOp.right`, but `ast_nodes.BinOp`
exposes `lhs` / `rhs`. Compiling sources that walk `when` (or other LINEAR
consumers) over binary expressions raises
`AttributeError: 'BinOp' object has no attribute 'left'` instead of emitting
diagnostics.

## Acceptance (EARS)

1. **Given** a program whose `when` control or related LINEAR walk includes a
   `BinOp`, **when** compiled, **then** the pipeline does **not** raise
   `AttributeError` on `BinOp.left`.
2. **Given** the same program, **when** compiled, **then** `compile_source`
   returns a normal `CompileResult` (ok or diagnostics — not a crash).
3. **Given** LINEAR / when semantics for programs that already passed before
   this bug, **when** recompiled, **then** no regression (existing suites).

## Non-goals

- Healing examples (LISS-0122/0123).
- Broad HIR rewrite beyond `_expr_children` field alignment (+ `TensorExpr` if
  required for the same walk).

## Exit

- [x] Phase 1 Red (`tests/test_liss_0125_hir_binop_expr_children_red.py`)
- [x] Phase 2 Green — `BinOp` → `lhs`/`rhs`; `TensorExpr` children added
- [x] Phase 3 Refactor — docstring on `_expr_children`
- [x] Docs sync (claims / open-work)
