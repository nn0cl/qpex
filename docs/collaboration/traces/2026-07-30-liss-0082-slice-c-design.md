# LISS-0082 Slice C — design intake

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-c-red`
- Operating path: Feature Path
- Issue: LISS-0082
- Scope: Slice C Phase 1 Red preparation only
- Current phase: Phase 0 design intake
- Implementation permission: none
- Next approval required: explicit Slice C Phase 1 Red approval
- Slice D–F: not authorized

## [DESIGN CHECK]

- **Scope and expected behavior:** Define the provider-neutral, immutable
  transformation-region boundary for `Unitary`, `Isometry`, and `Channel`.
  The acceptance surface must expose carrier and acting-space signatures and
  report invalid signatures or unfulfilled validity obligations without
  repairing the module. `Unitary` preserves one acting space and pure-carrier
  category; `Isometry` maps finite `A` to finite `B` with `dim(A) <= dim(B)`;
  `Channel` maps pure or density input to density output without hidden
  purification. Validity is one of `Declared`, `Verified(witness_ref)`, or
  `Required(obligation_id)`.
- **Specifications and files inspected:** `AGENTS.md`; `docs/architecture/agent-quickstart.md`;
  `docs/at-tdd/process.md`; `docs/architecture/implementation-readiness.md`;
  `docs/architecture/testing-strategy.md`; `docs/collaboration/ai-human-scheme.md`;
  `docs/architecture/ai-request-routing.md`; LISS-0082; the Quantum Semantic
  IR plan §3 and §5; the detailed contract §2 and §4; ADR 0108; the shipped
  `compiler/staqex/quantum_semantic_ir.py`; and the merged Slice A/B tests and
  traces.
- **Component boundaries, ports/adapters, and VO/DTO candidates:** Extend the
  existing immutable domain module only after Red review. Candidate DTOs are
  `TransformationRegion` subtypes (`UnitaryRegion`, `IsometryRegion`,
  `ChannelRegion`), a `ValidityClaim` value object, and a module-level
  `regions` tuple. Existing `SemanticId`, `SemanticOrigin`, acting-space IDs,
  and whole-Joint-state value IDs remain references rather than new physical
  resource objects. No ports or adapters are involved; no matrix, amplitude,
  density payload, simulator, QPU, file, network, RNG, or sink is introduced.
- **Applicable constraints:** Never Leave the State; one language and two
  implementation generations; static shape; closed provenance; no silent
  repair; no eager flattening; no hidden purification; no provider or target
  semantics; no general channel execution (LISS-0084); and strict AT-TDD
  phase separation. Slice C must not add measurement, control lanes,
  parameters, lowering, pipeline wiring, or provider behavior from later
  slices.
- **Decisions, assumptions, and unresolved ambiguities:** The Red tests may
  pin only the minimum signatures and named validity states. The exact DTO
  inheritance shape, diagnostic code names/details, whether `Unitary` mixed
  lifting is represented now, and the representation of explicit ancilla or
  environment obligations remain review points. `Channel` physicality is an
  obligation boundary, not a matrix or proof check. Producer/consumer graph
  resolution is not silently reimplemented in this slice. `regions` is a
  candidate additive root field because Slice B intentionally excluded it;
  its exact field order and identity definition require Red review.
- **Included and omitted AI context:** Included only the Issue/plan Slice C
  boundary, contract region table and validity levels, ADR 0108 region law,
  the current Semantic IR module, and prior Slice A/B acceptance evidence.
  Omitted provider SDKs, QPU IR, evaluator internals, gate catalogs, matrix
  algebra, current/future machine profiles, LISS-0077 dynamic controller
  behavior, LISS-0084 channel execution, unrelated Physics IR consumers, and
  private or generated data.
- **Task routing (model/assistant/tool):** Contract-to-Gherkin shaping and
  ambiguity review by the coding agent; repository structure and API searches
  by deterministic tools; direct test execution and `py_compile` only after a
  reviewed Red exists. No external model or runtime data is used.
- **Input/output evidence contract when AI output is involved:** Inputs are
  the cited repository artifacts and reviewed local acceptance language.
  Output is a proposed, reviewable test/API boundary plus this trace. No AI
  output is consumed as runtime data. Any diagnostic or DTO choice not stated
  by the contract is marked as a proposal and requires Adjudicator review.
- **Verification plan:** Before Phase 1, inspect the proposed test names and
  ensure they cover only signatures, dimensions, carrier categories,
  validity-state shape, and deterministic diagnostics. Phase 1 will add tests
  only under `tests/` and a Red trace; `compiler/` must remain unchanged.
  Deterministic checks will be `py_compile`, direct script execution, and
  `git diff --check` after Red.

## Proposed Red acceptance scenarios

1. A `UnitaryRegion` accepts a pure Joint-state input and output over the same
   acting space, while a changed space, density-only carrier, or measurement
   behavior is rejected.
2. An `IsometryRegion` accepts finite input/output spaces with
   `dim(input) <= dim(output)` and reports the invalid reverse relation. Any
   introduced environment/ancilla obligation must be explicit rather than
   silently discharged.
3. A `ChannelRegion` accepts pure or density input only when the output is a
   density carrier, and rejects a pure output or hidden purification claim.
4. `Declared`, `Verified(witness_ref)`, and `Required(obligation_id)` remain
   distinguishable; an unverified declaration is not reported as verified.
5. Region identity and embedded provenance follow Slice A definition-site
   rules, while references are not counted as duplicate definitions.

## Explicit exclusions for this Red

- no region execution, matrix or amplitude payload, channel physicality proof,
  proof synthesis, gate decomposition, or simulator/QPU invocation;
- no measurement, coherent/dynamic control, parameter, ancilla discharge
  implementation beyond a declared obligation shape;
- no `pipeline.py`, Physics IR, QPU IR, provider adapter, or LISS-0077 change;
- no Phase 2 implementation and no Phase 3 refactor.

## Stop condition

Stop here and request review of the proposed Slice C acceptance boundary and
the exact DTO/diagnostic choices. Do not create the Phase 1 tests until the
Adjudicator explicitly approves Slice C Phase 1 Red.
