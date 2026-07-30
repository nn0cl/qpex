# LISS-0082 Slice D — design intake

- Date: 2026-07-30
- Worktree: `/private/tmp/qpex-liss-0082-slice-d`
- Branch: `feature/liss-0082-slice-d-red-codex`
- Operating path: Feature Path
- Issue: LISS-0082
- Scope: Slice D Phase 1 Red preparation only
- Current phase: Phase 0 design intake
- Implementation permission: none
- Next approval required: explicit Slice D Phase 1 Red approval
- Slice E–F: not authorized

## [DESIGN CHECK]

- **Scope and expected behavior:** Define immutable, provider-neutral contracts
  for coherent control, terminal Static Kernel measurement, the minimum Dynamic
  QPU feedback marker, parameter shape independence, and explicit
  ancilla/uncompute discharge. The verifier must reject ambiguous control,
  hidden or non-terminal Static measurement, post-measure state reuse, dynamic
  feedback in a Static module, separated dynamic token/state correlation,
  runtime shape dependence, and missing resource discharge without repairing
  the module.
- **Specifications and files inspected:** `AGENTS.md`; agent quickstart;
  AT-TDD process; implementation readiness; LISS-0082 acceptance scenarios
  3–6; Quantum Semantic IR plan §§3 and 5; detailed contract §§4–7 and §11;
  ADR 0108 decisions 3–5; merged Slice A–C traces and tests; and the current
  `compiler/staqex/quantum_semantic_ir.py`.
- **Component boundaries, ports/adapters, and VO/DTO candidates:** Extend only
  the immutable Semantic IR domain module after reviewed Red. Candidate VOs
  are `SemanticLane`, `ParameterSymbol`, `OutcomeIntent`,
  `DynamicCorrelation`, `AncillaDischarge`, and
  `UncomputeObligation`. Candidate region DTOs are
  `CoherentControlRegion`, `TerminalMeasurementRegion`, and
  `DynamicControlRegion`. A dynamic measurement marker is structurally
  distinct from terminal measurement and may be represented by
  `DynamicMeasurementRegion` if the reviewed Red accepts that name. No ports
  or adapters are involved; sampling RNG and result sinks remain outside this
  IR.
- **Applicable constraints:** Never Leave the State; Static Kernel measurement
  is terminal; coherent control remains one whole-Joint-state transformation;
  compile-time selection is absent before Semantic IR; Dynamic feedback is a
  capability marker only and its executable controller belongs to LISS-0077;
  factor selectors do not imply separability; runtime parameters cannot change
  acting-space shape; ancillas cannot disappear without explicit discharge;
  no inverse synthesis; no provider, target, file, network, RNG, or sink
  behavior; no Slice E lowering or Slice F pipeline work.
- **Decisions, assumptions, and unresolved ambiguities:** The design rejects a
  generic `ControlRegion(kind=...)` and a single measurement DTO with optional
  fields because either permits illegal Static/Dynamic combinations. The
  proposed root lane values are exactly `StaticKernel` and
  `DynamicQpuContract`. The Dynamic DTO is only a correlation/capability
  marker, not controller execution. Open review points are the final dynamic
  measurement DTO name, whether lane is a VO or a closed string value, how
  terminal outcome domains are represented without classical runtime values,
  and whether ancilla discharge variants are separate DTOs or one closed
  tagged VO. These choices must be fixed by reviewed Red, not guessed in
  Green.
- **Included and omitted AI context:** Included the Slice D sections of the
  Issue, plan, detailed contract, ADR 0108, the current Semantic IR module, and
  prior Slice tests. Omitted evaluator internals, simulator sampling, QPU IR,
  provider SDKs, OpenQASM/QIR, LISS-0077 controller implementation, Slice E
  finite-evidence lowering, machine profiles, and unrelated source files.
- **Task routing (model/assistant/tool):** Boundary synthesis and
  contract-to-Gherkin shaping by the coding agent; repository/API checks,
  `py_compile`, direct test execution, and diff checks by deterministic tools.
  No external model output or runtime data is used.
- **Input/output evidence contract when AI output is involved:** Inputs are
  the cited repository artifacts and explicit Adjudicator approvals. Output is
  a reviewable acceptance proposal and, after phase approval, tests that
  expose named diagnostics. AI prose is not runtime input and no unsupported
  controller behavior is inferred.
- **Verification plan:** Phase 1 will add only
  `tests/test_quantum_semantic_ir_slice_d_red.py` and a Red trace.
  `compiler/` must remain unchanged. Red must be caused by missing Slice D API
  or verifier behavior, while Slice A–C remain green. Run direct scripts,
  `py_compile`, and `git diff --check`.

## Proposed Phase 1 Red acceptance groups

### D1 — lane and control-domain separation

1. `CoherentControlRegion` consumes one whole-Joint-state generation and
   produces one fresh generation over the same acting space. Control and target
   are ordered factor selectors inside that single Joint value, not two
   separable state inputs.
2. Control and target selectors must resolve inside the acting space, must not
   overlap, and must not imply a classical branch.
3. Compile-time/static selection has no Semantic IR DTO. A residue that claims
   unresolved static selection emits `QSEM_CONTROL_LANE_INVALID`.
4. A Dynamic marker in a `StaticKernel` module emits
   `QSEM_CONTROL_LANE_INVALID`.

### D2 — terminal and dynamic measurement boundaries

5. `TerminalMeasurementRegion` consumes one final Joint generation and yields
   an `OutcomeIntent`; it has no reusable output Joint value or mid-program
   classical value.
6. A quantum region or value use after terminal measurement emits
   `QSEM_MEASUREMENT_BOUNDARY_INVALID`.
7. The Dynamic measurement marker names a finite outcome domain, branch-region
   IDs, one post-measurement Joint generation, one phase-local token, required
   `DynamicMeasurementFeedback`, and provenance.
8. Separating, escaping, dropping, or independently consuming the paired
   dynamic token/state, or omitting exactly one merge, emits
   `QSEM_DYNAMIC_CORRELATION_INVALID`.
9. Dynamic controller construction, classical operations, termination,
   scheduling, and target support are absent and remain LISS-0077.

### D3 — parameters and resources

10. `ParameterSymbol` records semantic identity, scalar/domain type, optional
    unit/dimension, binding phase, and provenance; it carries no provider or
    target setting.
11. A runtime-bound parameter or dynamic controller that changes an acting
    space, tensor order, or local dimension emits
    `QSEM_PARAMETER_SHAPE_DEPENDENCE`.
12. `AncillaScope` records acquisition precondition and exactly one explicit
    discharge: `ReturnedZero`, `AbsorbedByIsometry`, `TracedByChannel`, or
    `TerminalMeasurement`.
13. Missing or unknown discharge emits `QSEM_RESOURCE_DISCHARGE_MISSING`.
14. `UncomputeObligation` records an obligation or accepted upstream witness
    but never synthesizes an inverse or copies ADR 0107 runtime tolerance into
    Semantic IR.
15. Slice D definition sites participate in existing deterministic identity
    and closed-provenance checks; reference IDs do not become definitions.

## Explicit exclusions

- no sampling, RNG call, measurement sink, report formatting, or reusable
  classical measurement value;
- no executable dynamic controller, classical branch evaluator, retry,
  scheduling, timing, or provider capability lookup;
- no matrix, amplitude, channel execution, inverse synthesis, gate expansion,
  mapping, discretization, or error tolerance;
- no Physics IR lowering, `pipeline.py`, QPU IR, provider adapter, or target
  profile change;
- no Phase 2 implementation, Phase 3 refactor, Slice E, or Slice F.

## Review decisions requested before Red

1. Accept distinct `TerminalMeasurementRegion` and
   `DynamicMeasurementRegion` DTOs rather than a generic measurement node with
   optional fields.
2. Accept `SemanticLane` as a closed VO with exactly `StaticKernel` and
   `DynamicQpuContract`.
3. Accept the four closed ancilla discharge variants and a separate
   `UncomputeObligation`.
4. Accept the contract diagnostic codes listed above as the Red expectations.
5. Confirm that all three acceptance groups D1–D3 belong to one Slice D Red
   review unit; otherwise authorize an explicit D1/D2/D3 phase split before
   tests are written.

## Stop condition

Stop after design intake. Do not add tests or production code until the
Adjudicator explicitly approves the Slice D Phase 1 Red boundary and resolves
the five review decisions above.
