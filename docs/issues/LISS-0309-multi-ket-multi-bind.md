# LISS-0309: Multi-ket multi-bind LINEAR residual (reopen)

## Metadata

- Local issue ID: LISS-0309
- Status: **complete** (2026-08-03)
- Type: Feature Kernel residual
- Priority: P1
- Depends: ADR 0184 / LISS-0305 classical multi-bind
- Branch: `feature/liss-0309-multi-ket-multi-bind`
- Authority: Adjudicator「1をreopenして着手」

## Problem

```text
s0, s1 = |+>, |+>
measure s0 tracing_out s1
```

failed with ``tracing_out` name `s1` is not a live linear carrier`` (HIR never
introduced multi-name ket binds) and runtime ``cannot evaluate KetLit as value``
(TupleExpr multi-bind used classical `_eval_value`).

## Fix

1. HIR: multi-name StateBind with TupleExpr of state-forming items introduces
   linear roots; classical tuple items stay non-linear.
2. Evaluator: per-name `_bind` for TupleExpr multi-bind (KetLit-safe).
3. B08 teaching face uses multi-ket multi-bind.

## Exit

- [x] HIR + evaluator
- [x] Tests (multi-ket, ideal chalk, classical non-linear)
- [x] B08 seed-0 + QASM regression
