# Trace: LISS-0114 Slice F + Issue completion

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0114 |
| Slice | F — runtime uncompute + tolerance (R7/R9) |
| Phase | plan gate → Red → Green → Refactor **complete**; Issue **complete** |
| Branch | `feature/liss-0114-slice-a` |
| Approval | Adjudicator「F 承認」 |

## Delivered

- `compiler/staqex/runtime/uncompute.py` —
  `LINEAR_UNCOMPUTE_AMPLITUDE_TOL`, `is_computational_basis_zero`,
  `require_computational_basis_zero`
- `hir.LINEAR_UNCOMPUTE_AMPLITUDE_TOL` re-export
- Evaluator: verify `|0>` / `vacuum` rebind; verify `effects { Uncompute }`
  return coordinates
- [ADR 0107](../../architecture/adr/0107-linear-uncompute-amplitude-tolerance.md)
  **Proposed** (1e-12 physical class)
- `tests/test_linear_hardening_slice_f_red.py`

## Expected Red (before Green)

Missing `LINEAR_UNCOMPUTE_AMPLITUDE_TOL` on `hir`

## Verification

```
PASS LISS-0114 Slice A–F
PASS LISS-0075 Slice A–D
```

## Residual note

Computed unitary round-trips that are ≈|0⟩ but not static `|0>`/`vacuum`
still do **not** clear HIR discard (consume-set unchanged). ADR 0107 Accept
is a separate Architecture Path step.

## Next safe action

Commit/PR for `feature/liss-0114-slice-a` (includes 0075 C/D + 0114 A–F),
or Adjudicator Accept of ADR 0107 / select next Issue.
