# AI work trace: LISS-0298 QMD surface modernization

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `feature/liss-0298-qmd-surface-modernization` |
| Issue | [LISS-0298](../../architecture/documentation-compression-map.md) |

## Done

- QMD packs: free scores / Operator factories; `DiscoveryModel` mut clock kept.
- Main: selective import + short names; `ising_hamiltonian(c)` (LISS-0297).
- Friction ledger + README + WP-0089 residual note.

## Verification

```bash
python3 -m compiler.staqex run --seed 0 \
  examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx
```
