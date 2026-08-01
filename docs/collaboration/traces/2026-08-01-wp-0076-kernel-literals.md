# Trace: WP-0076 Kernel literals (LISS-0210)

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Program | WP-0076 |
| Issues | LISS-0210 |
| Branch | `batch/wp-0076-kernel-literals` |

## Reason

Adjudicator「はい」: leaf `kernel_literals.py` + approved WP-0076 batch.

## Changes

- New `compiler/staqex/kernel_literals.py`
- Rewire symbolic_ir, typecheck, evaluator, qasm/lower, finite_binder,
  lexer, migrate_unicode_math

## Post-review

Adjudicator「承認」: merge PR #235.
