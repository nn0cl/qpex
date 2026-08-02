# AI work trace — WP-0085 deferred Kernel gaps (LISS-0238 / 0239)

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `batch/wp-0085-deferred-kernel-gaps` |
| Issues | LISS-0238, LISS-0239 |

## Change

- HIR: Pipe always moves linear **lhs**; rhs move still gated on State bind
  (fixes multi-hole Partial fill `LINEAR_IMPLICIT_DISCARD`).
- Evaluator `_bind_apply_multi`: Identity no-op before qubit-bit unitary
  (Qutrit `|2⟩` `apply(I)` rename path).
- Suites: LISS-0238 Red; restore LISS-0181 multi-hole pipe form; harden
  LISS-0112 Slice B runtime assert.

## Verification

`.venv/bin/pytest tests/` → 1084 passed / 0 failed.
