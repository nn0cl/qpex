# LISS-0300: B07 struct + free-fn face (post LISS-0297)

## Metadata

- Local issue ID: LISS-0300
- Status: **complete** (2026-08-03)
- Type: Feature examples (basics pedagogy)
- Priority: P2
- Depends: LISS-0297 **complete**
- Branch: `feature/liss-0300-b07-struct-freefn-face`

## Summary

Align B07 with the free Operator factory face:

- `Model.IsingChain` class → `Model.IsingParams` struct + free `ising_hamiltonian`
- Keep `_pad` as the module-private visibility seat on the struct
- Document that mutable systems remain `class` in A06 / QMD / A10

## Exit

- [x] B07 source + folder README + basics curriculum row
- [x] seed-0 B07
- [x] Friction ledger note
