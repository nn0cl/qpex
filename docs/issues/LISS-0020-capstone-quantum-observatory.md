# LISS-0020: Quantum Observatory capstone example

## Metadata

- Local issue ID: LISS-0020
- GitHub issue: none
- Status: proposed
- Phase: Architecture Path → Feature Path
- Type: feature + examples + specification
- Priority: P0 (user-requested learning/physics showcase)
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: broad cross-surface example and multi-stage verification.
- Owner/agent: TBD
- Related branch: `feature/quantum-observatory-capstone`

## Summary

Build a large, modular, physics-led example suite that lets a student and a
theoretical physicist judge QPex's readability, economy, and physical
intuition from source alone.

Working theme: **Quantum Observatory** — a fictional observatory that studies
topological transport, interferometry, quantum walks, search, and an entangled
deep-space link. The theme is one coherent narrative, not a claim of real
cryptanalysis, astronomy, or hardware performance.

The example must exercise every currently implemented language surface that is
appropriate to the Kernel, while explicitly documenting surfaces that are
reserved or deferred. CPU execution is authoritative for the full story; a
small qubit-only lane must emit OpenQASM 3 for quantum-computer execution.

## Acceptance Notes

### Documentation and design

- [ ] `docs/specs/qpex-quantum-observatory-capstone.md` is accepted as the
      observable acceptance specification.
- [ ] A coverage matrix maps each implemented syntax/runtime capability to a
      named module and executable verification case.
- [ ] A honesty table identifies toy assumptions, CPU-only analyses, and the
      QPU-compatible subset.
- [ ] README explains the physics narrative, module graph, learning path, and
      how to run CPU/check/inspect/snapshot/QASM lanes.
- [ ] No deferred capability is presented as implemented: no fake QFT, density
      matrix, `until`, currying, Trait `impl`, effect system, or cloud submit.

### Program surface coverage

- [ ] `package` / `import`, qualified namespaces, `pub` and `_` visibility.
- [ ] `namespace`, `enum`, `struct`, `class`, `fn init`, `this`, immutable
      class methods, and module-level public functions.
- [ ] Type-First quantities and dimensional arithmetic using existing
      `(L, M, T)` dimensions.
- [ ] `State<T>` lifting, `dirac`, `coin`, `when`, tuple/joint correlation,
      `map`, `project`, `interfer`, `vacuum`, and Result/error world-lines.
- [ ] `phase`, `cis`, `Complex.cis`, `expect`, `inspect`, `snapshot`, and
      terminal `measure` with no early collapse.
- [ ] `evolve times N`, `evolve for duration`, and `evolve under H for t`.
- [ ] Qubit operations: `hadamard`, `apply`, `cnot`, `capply`, `ocapply`,
      mixed controls, multi-control gates, and operator unitarity checks.
- [ ] Grover diffusion, DTQW/position-grid behavior, Fock/quadrature
      behavior, sparse Pauli Hamiltonians, trace-out, and physical diagnostics
      are each used where physically meaningful.
- [ ] OpenQASM 3 emission is demonstrated by a portable Bell/search/link lane;
      unsupported Fock/grid lowering is explicitly rejected or kept CPU-only.

### Verification

- [ ] New example files are included in the official catalog and SV-09 or its
      successor discovery mechanism.
- [ ] Feature-specific tests cover module linking, surface coverage, honest
      output, CPU execution, and QASM emission.
- [ ] Full spec verification remains green.
- [ ] Each module has deterministic seeded execution where measurement is used.
- [ ] Student path and physicist path are both documented and runnable.

### Current Green slice

- [x] Modular folder, CPU entry, and QPU entry exist.
- [x] Official catalog and SV-09 include the CPU entry.
- [x] Capstone acceptance smoke tests pass.
- [x] Existing OpenQASM and full SV regression suites pass (`164/164`).
- [x] State algebra, Grover, DTQW, and controlled-gate coverage slice is Green.
- [x] CPU-only Fock/grid/sparse-Pauli execution and `trace_out`/`snapshot`
      diagnostics have a dedicated coverage slice.

## Dependencies

- Parent: none
- Depends on: LISS-0001…LISS-0009 (shipping surface and examples baseline)
- Depends on design review: LISS-0010…LISS-0019 remain deferred/open and must
  not be used as if implemented
- Blocks: next large official example family and capstone teaching material
- Related: WP-0016, `docs/specs/qpex-quantum-observatory-capstone.md`

## Adjudicator Decision Points

- [ ] Accept the Quantum Observatory theme and the CPU-full/QPU-subset split.
- [ ] Accept the coverage matrix as the meaning of “all implemented surface”.
- [ ] Accept that no new language feature is added solely to make the example
      more impressive.
- [ ] Approve Feature Path Phase 1 Red after the specification is reviewed.

## Context

- Included: shipped Python Kernel, official examples 01–15, SV-01…SV-31,
  OpenQASM 3 backend, physicist DX documents.
- Omitted: implementation of open-work backlog, real cryptanalysis, real QPU
  credentials/submit, and claims of experimental physics accuracy.
- Assumptions: one QPex semantics serves the Python Kernel and future Rust
  generation; examples remain readable source-first artifacts.

## AI Planning Records

### AIP-0020-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: XL
- Intended execution route: Architecture Path design/spec review, then Feature
  Path Phase 1 Red → Phase 2 Green → Phase 3 Refactor.
- Intended scope: one modular example family, acceptance spec, coverage tests,
  CPU execution, QASM-compatible lane, documentation, and catalog integration.
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Token metric: N/A
- Estimation basis: broad cross-surface example with multiple modules and
  deterministic verification.
- Assumptions: no new language semantics and no external dependency.
- Confidence: medium until the surface matrix is reviewed.
- Revises: none
- Revision reason: n/a
- Superseded by: none

## Work Notes

- 2026-07-23: filed as the highest-priority capstone example request; no code
  or tests authorized yet.
- 2026-07-23: Phase 1 Red added five acceptance smoke tests; Phase 2 Green
  shipped the initial module graph and CPU/QPU lanes. Phase 3 refactor is
-  limited to readability and honesty documentation for this slice.
- 2026-07-23: Phase 1 Red → Phase 2 Green → Phase 3 Refactor completed for the
  CPU-only continuous-model and diagnostics slice. The carrier boundary is
  documented; no language semantics were added.

## Verification

- Documentation review first.
- Phase 1 will add failing coverage tests only after Adjudicator approval.
