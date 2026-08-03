# AI work trace: LISS-0308 lane markers residual

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0308-lane-markers-residual` |
| Issue | [LISS-0308](../../issues/LISS-0308-lane-markers-residual.md) |

## Done

- 18 multi-file mains: `// staqex-lane: experiment|circuit|open`
- surface-style-guide §6b + checklist
- QUICKSTART failure vocabulary table
- re-review additional findings 5/7 marked done

## Out

- Multi-ket `s0, s1 = |+>, |+>` LINEAR residual (still deferred)
- Bulk rewrite of hand `|0>` uncompute in applied

## Verification

```bash
# no unlabeled main*.sqx under examples/
python3 -m compiler.staqex run --seed 0 \
  examples/applied/A06_topological_edge_memory/main_topological_edge_memory.sqx
```
