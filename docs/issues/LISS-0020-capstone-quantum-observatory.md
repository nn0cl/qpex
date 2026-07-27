# LISS-0020: Quantum Observatory capstone example

## Metadata

- Local issue ID: LISS-0020
- GitHub issue: none
- Status: Complete for the expanded Kitchen Sink slice — Adjudicator approval 2026-07-27
- Phase: Architecture Path → Feature Path → Phase 3 Refactor → closed
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

Working theme: **Quantum Observatory** — a fictional molecular-spectrum mission
that combines topological transport, interferometry, quantum walks, search, an
entangled deep-space link, static QFT/IQFT, and an open-system detector. The
theme is one coherent narrative, not a claim of real cryptanalysis, astronomy,
or hardware performance.

The example must exercise every accepted language surface that is appropriate
to the Kernel, while explicitly documenting surfaces that remain reserved or
deferred. CPU execution is authoritative for the open-system and continuous
story; the static qubit lane records QFT/Suzuki lowering and emits OpenQASM 3
where the existing backend boundary supports it.

## Acceptance Notes

### Documentation and design

- [x] `docs/specs/qpex-quantum-observatory-capstone.md` records the observable
      acceptance specification.
- [x] A coverage matrix maps each implemented syntax/runtime capability to a
      named module and executable verification case.
- [x] A honesty table identifies toy assumptions, CPU-only analyses, and the
      QPU-compatible subset.
- [x] README explains the physics narrative, module graph, learning path, and
      how to run CPU/check/inspect/snapshot/QASM lanes.
- [x] Accepted QFT/IQFT, density/Lindblad, `|>`, Trait `impl`, Suzuki S2, and
      static/parametric declarations are presented with their actual lanes.
- [x] Deferred capabilities remain explicit: effect marking, provider/cloud
      submit, higher-order Suzuki beyond S2, and bare Operator `H` sugar.

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
- [x] Static `QubitRegister<N>`, workflow `Param<Angle>`, QFT/IQFT, both
      accepted Suzuki S2 policy forms, and `DensityState`/Lindblad `JumpSet`
      input are used in the main narrative.
- [ ] Grover diffusion, DTQW/position-grid behavior, Fock/quadrature
      behavior, sparse Pauli Hamiltonians, trace-out, and physical diagnostics
      are each used where physically meaningful.
- [ ] OpenQASM 3 emission is demonstrated by a portable Bell/search/link lane;
      unsupported Fock/grid lowering is explicitly rejected or kept CPU-only.

### Verification

- [ ] New example files are included in the official catalog and SV-09 or its
      successor discovery mechanism.
- [x] Feature-specific tests cover module linking, surface coverage, honest
      output, CPU execution, and QASM emission.
- [x] Full spec verification remains green.
- [x] Each executable entry has deterministic seeded execution where measurement
      is used.
- [x] Student path and physicist path are documented and runnable.

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
- Depends on the accepted slices of LISS-0010…LISS-0019; each newer surface is
  used only in its documented static, CPU, or QPU lane.
- Blocks: next large official example family and capstone teaching material
- Related: WP-0016, `docs/specs/qpex-quantum-observatory-capstone.md`

## Adjudicator Decision Points

- [x] Accept the Quantum Observatory theme and the CPU-full/QPU-subset split.
- [x] Accept the coverage matrix as the meaning of “all implemented surface”.
- [x] Accept that no new language feature is added solely to make the example
      more impressive.
- [x] Feature Path Phase 1 Red, Phase 2 Green, and Phase 3 Refactor were
      reviewed for the expanded slice.

## Context

- Included: shipped Python Kernel, official examples 01–15, SV-01…SV-31,
  OpenQASM 3 backend, physicist DX documents.
- Omitted: implementation of open-work backlog, real cryptanalysis, real QPU
  credentials/submit, and claims of experimental physics accuracy.
- Assumptions: one QPex semantics serves the Python Kernel and future Rust
  generation; examples remain readable source-first artifacts.

## AI Planning Records

### AIP-0020-001

- Status: reviewed
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
- 2026-07-24: Phase 1 Red → Phase 2 Green expanded the main narrative with
  accepted trait/pipeline, static register/QFT, Suzuki S2, workflow parameter,
  and numeric Lindblad slices. No language semantics were added.
- 2026-07-24: Phase 3 review completed. Readability, lane separation, honesty
  documentation, acceptance evidence, and status synchronization were checked.
- 2026-07-27: Adjudicator approved completion of the expanded Kitchen Sink
  slice. Existing QFT/IQFT coverage is the official example path; no new QFT
  example Issue is required. Remaining unchecked rows describe deferred or
  carrier-specific follow-ups, not hidden implementation scope.

## Verification

- Documentation review first.
- Phase 3 review evidence is recorded above; the next independent language task
  must use its own LISS and phase-specific branch.
