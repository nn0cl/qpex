# LISS-0107: Examples linker/runtime prerequisite (Phase 0)

## Metadata

- Local issue ID: LISS-0107
- GitHub issue: not created
- Status: **done** (2026-07-27) — Phase 2 Green
- Phase: Phase 2 Green → closed
- Type: bug / kernel / examples prerequisite
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: blocks catalog v2 multi-file migration
- Owner/agent: unassigned
- Parent: [LISS-0106](LISS-0106-examples-catalog-v2-refresh.md)
- Related branch: `docs/liss-0106-examples-catalog-v2-refresh` (Red tests);
  Green fix expected on `bug/liss-0107-examples-linker-runtime`

## Summary

Official multi-file examples fail at runtime while `compile_path` symbol merge
tests still pass. This blocks [LISS-0106](LISS-0106-examples-catalog-v2-refresh.md)
Phase 1 migration for any linked `domain/` / `operators/` layout.

### Observed failures (2026-07-27, `main`)

| Entry | Suite | Symptom |
|-------|-------|---------|
| `examples/09_complex_simulations/main_quantum_walk.staqex` | SV-09, SV-31 | `RUNTIME_ERROR: unbound Operator / scalar 'Coin'` |
| `examples/10_topological_physics/main_ssh_topological.staqex` | SV-09 | `RecursionError` in `op_space` during linked `build_ssh_hamiltonian()` |
| `examples/15_orbital_mesh_walk/main_orbital_mesh.staqex` | SV-09 | linker/runtime (same class as 09) |
| `examples/16_quantum_observatory/main_observatory.staqex` | SV-09 | linker/runtime |
| `examples/09/.../main_quantum_walk.staqex` | SV-31 `sv31-linked-run` | runtime after successful `sv31-link-symbols` |

Spec Verification gate: **160/165 PASS** (was 165/165 on 2026-07-24 per report
snapshot in WP-0016).

## Acceptance Notes

### Phase 1 Red (filed 2026-07-27)

- [x] Minimal linked coin-factory fixture reproduces `unbound Operator / scalar`
- [x] Minimal linked Hamiltonian fixture reproduces `op_space` recursion
- [x] Official SV-09 / SV-31 entries covered in
      `tests/test_liss0107_examples_linker_runtime_red.py`
- [x] Tests fail for the stated reason (not compile failure)

### Phase 2 Green

- [x] Root cause: factory `return Coin` / `return Hssh` parsed as `OpVar`, not `Var`;
      `_resolve_operator_expr` only inlined `Var` returns, leaking unresolved locals
- [x] Fix: resolve `OpVar` returns through measure-free `fn` Operator locals
- [x] All currently registered multi-file SV-09 entries run with `seed=0`
- [x] SV-31 `sv31-linked-run` PASS
- [x] No example source changes that mask Kernel defects
- [x] Full SV suite PASS (165/165)

## Dependencies

- Blocks: [LISS-0108](LISS-0108-examples-basics-track-migration.md) B09,
  [LISS-0109](LISS-0109-examples-applied-track-migration.md) A02, A10, and any
  linked Applied entry
- Related: ADR 0054 (module linker), ADR 0068 (explicit returns), LISS-0025

## Adjudicator Decision Points

- Confirm this is Kernel Feature Path work (not examples-only workaround).
- Approve Phase 1 Red tests that reproduce failures without editing official
  examples to hide bugs.

## Verification

- `python3 tests/spec_verification/run_all.py`
- `python3 -m compiler.staqex run examples/09_complex_simulations/main_quantum_walk.staqex --seed 0`
- `python3 tests/test_liss0107_examples_linker_runtime_red.py` (expect failure until Green)
