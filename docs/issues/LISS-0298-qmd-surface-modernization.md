# LISS-0298: Quantum-matter discovery surface modernization

## Metadata

- Local issue ID: LISS-0298
- Status: **complete** (2026-08-03)
- Type: Feature examples
- Priority: P2
- Depends: LISS-0296 selective import; LISS-0297 Operator free-fn struct coeffs
- Branch: `feature/liss-0298-qmd-surface-modernization`

## Summary

Bring Showcase S1 (`quantum_matter_discovery`) to the same post–WP-0089 face
as S01 / applied:

| Pack | Before | After |
|---|---|---|
| Couplings | class methods for pure scale | struct + `field_scale`; class only for mut `mark_step` |
| KindBox | class DTO | free `is_ising_tag` + enum |
| IsingDrive | class | free `ising_hamiltonian` / `named_coeff_sum` |
| QuenchSchedule | class | struct + free duration/intent |
| SimEvidence | class | struct + free `honesty` |
| Main | bare module imports + FQN | selective braces + short names |

## Exit

- [x] Domain / physics / protocol / provenance demotions
- [x] Main selective import
- [x] seed-0 QMD main
- [x] README + friction ledger
