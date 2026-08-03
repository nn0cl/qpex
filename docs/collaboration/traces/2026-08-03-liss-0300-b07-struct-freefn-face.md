# AI work trace: LISS-0300 B07 struct + free-fn face

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0300-b07-struct-freefn-face` |
| Issue | [LISS-0300](../../architecture/documentation-compression-map.md) |

## Done

- B07: `IsingParams` + `ising_hamiltonian(p)`; visibility `_pad` retained
- basics README curriculum row; B07 folder README
- Friction ledger + WP-0089 residual note

## Verification

```bash
python3 -m compiler.staqex run --seed 0 \
  examples/basics/B07_structure_visibility/structure_visibility.sqx
```
