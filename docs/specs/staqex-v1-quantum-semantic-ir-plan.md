# Staqex v1 Quantum Semantic IR plan (LISS-0082)

| Field | Value |
|---|---|
| Status | **review** — Slices A and B complete; Slice C gated |
| Authority | WP-0025 E2; ADR 0106 D9/D11; compiler blueprint §4.3 |
| Depends on | LISS-0075 complete; LISS-0081 complete |
| Shipping target | Python package `compiler/staqex` |
| Rust target | Deferred; shared contracts may be mirrored later |

Detailed architecture:
[Quantum Semantic IR contract](../architecture/quantum-semantic-ir-contract.md).
Proposed decision:
[ADR 0108](../architecture/adr/0108-quantum-semantic-ir-value-region-contract.md).
Scale/model envelope:
[ADR 0109](../architecture/adr/0109-quantum-machine-scale-and-model-envelope.md)
and its
[detailed contract](../architecture/quantum-machine-scale-and-model-envelope.md).
Capacity stress horizon:
[ADR 0110](../architecture/adr/0110-optimistic-quantum-capacity-horizon.md)
and its
[scenario envelope](../architecture/quantum-capacity-horizon-scenarios.md).
Current/NH5 delivery horizon:
[ADR 0111](../architecture/adr/0111-current-hardware-first-delivery-horizon.md)
and its
[delivery envelope](../architecture/current-hardware-delivery-envelope.md).
Research:
[Quantum Semantic IR foundations](../research/2026-07-29-quantum-semantic-ir-foundations.md).

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive, immutable Quantum Semantic IR
  contracts for finite whole-Joint-state values, typed regions, terminal/dynamic
  measurement lanes, linear resources, approximation obligations, and closed
  provenance; no provider or realization types.
- Specifications and files inspected: WP-0025 LISS-0082 row; ADR 0106/0107;
  compiler blueprint §4.3–4.6; language axioms; LISS-0080/0081 boundaries;
  current HIR, Physics IR/lowering, pipeline, and QPU IR code; cited primary
  research on value IRs, regions, target profiles, and uncomputation.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  new `quantum_semantic_ir.py`; pure lowering/verifier over immutable DTOs;
  ActingSpaceId, QuantumValueId, RegionId, ResourceId, ParameterSymbol,
  SemanticOrigin, and ApproximationObligation; no file/network/provider/RNG
  adapters.
- Applicable constraints: Clean Architecture; Never Leave the State; terminal
  Static Kernel measurement; static shape; AT-TDD and Adjudicator phase gates;
  Physics IR remains upstream symbolic/algebra level; local-to-utility scale
  must not force eager flattening or cloud assumptions.
- Decisions, assumptions, and unresolved ambiguities: ADR 0108–0111 are
  Proposed;
  finite evidence arrives through a narrow lowering input, but its eventual
  upstream storage remains follow-on; Dynamic QPU behavior remains LISS-0077;
  soft compile wire remains optional Slice F.
- Included and omitted AI context: include architecture, affected code
  boundaries, and public primary-source evidence; omit provider SDKs,
  credentials, unrelated evaluator internals, and opcode catalogs.
- Task routing (model/assistant/tool): design synthesis by capable assistant;
  repository/link inspection by deterministic tools; Red/Green later on
  Shipping Kernel Python.
- Input/output evidence contract when AI output is involved: cited repository
  artifacts and primary public sources in; reviewable proposed contracts and
  explicit inferences out; no hidden reasoning or runtime-generated evidence.
- Verification plan: link/path and claim sync, prohibited-boundary search,
  `git diff --check`; no compiler source or tests in this intake.
```

## 1. Boundary

```text
Physics IR + reviewed finite evidence
  -> narrow QuantumSemanticInput
  -> Quantum Semantic IR lowering
  -> Quantum Semantic IR verifier
  -> later Algorithm Plan IR (LISS-0083)
  -> Logical QPU IR / simulator plans
```

Quantum Semantic IR is the backend-neutral level for **finite quantum
meaning**. It does not choose encodings, Trotter orders, shot plans, grids,
or providers. Those decisions belong to Algorithm Plan IR.

The lowering is a UseCase-facing domain transformation over immutable DTOs. It
does not inspect AST/`CompilationUnit`, evaluator state, files, network,
provider capabilities, database, RNG, or measurement-sink adapters.

## 2. Proposed DTO vocabulary

Names are design candidates, not implementation authorization.

- `QuantumSemanticInput`: Physics module plus reviewed finite-carrier, linear-
  resource, and lane evidence.
- `SemanticOrigin`: source, upstream identities, transform identity, and parent
  origins.
- `ActingSpace`: ordered finite tensor factors and dimension metadata.
- `PureJointStateValue` / `DensityJointStateValue`: whole-Joint-store
  generation, identified by `value_id` with no stored generation number; factor
  resources never imply separability or physical qubits.
- `UnitaryRegion` / `IsometryRegion` / `ChannelRegion` /
  `MeasurementRegion`: distinct carrier/acting-space signatures.
- `CoherentControlRegion`: factor-selected coherent control over one Joint
  state, preserving superposition and entanglement.
- `DynamicControlRegion`: capability marker only; behavior and controller
  lifetime remain LISS-0077. Compile-time selection is absent after lowering.
- `ParameterSymbol`: symbolic parameter identity, type/unit, binding phase,
  and provenance; never shape-defining at runtime.
- `AncillaScope` / `UncomputeObligation`: linear lifetime and explicit
  discharge evidence.
- `Exact` / `ApproximationRequired`: semantic obligation only; no method,
  tolerance, bound, or resource choice.
- `QuantumSemanticModule`: immutable, schema-versioned root.
- structured region containment/call references and symbolic repetition
  identities; no mandatory eager expansion.

See the detailed contract for signatures, verifier codes, and ownership.

## 3. Refined slice plan

Each slice needs its own reviewed Red before Green.

| Slice | Acceptance boundary | Explicit exclusions |
|---|---|---|
| **A — identities and root** | immutable hierarchy-capable IDs, `SemanticOrigin`, schema-versioned root/region-root references, deterministic identity/provenance diagnostics | no region behavior, eager flattening, builder stub, or pipeline wire |
| **B — acting spaces and Joint state values** | finite ordered spaces; pure/density Joint carriers; generation-based one-producer/one-consumer verification; factor IDs do not imply separability | no matrices, amplitudes, encoding, allocation |
| **C — transformation regions** | unitary/isometry/channel signatures and declared/verified/required validity state | no general channel execution (LISS-0084), proof synthesis, gates |
| **D — control, measurement, resources** | coherent/static/dynamic separation; terminal Static measurement; dynamic marker; ancilla discharge and uncompute obligations; parameters | no controller runtime (LISS-0077), inverse synthesis, RNG/sinks |
| **E — exactness and lowering** | `Exact`/`ApproximationRequired`; narrow `QuantumSemanticInput`; minimal Physics-to-Semantic evidence and named unsupported/missing-evidence diagnostics | no mapping/discretization choice, error bound, AST fallback |
| **F (optional) — soft pipeline wire** | additive, non-hard `CompileResult` field after A–E review | no existing QPU IR migration or compile-hard promotion |

The former Slice A “builder stub” is removed. A stub that constructs an empty
or weak module before finite-evidence and value invariants exist would create a
false integration contract.

## 4. Slice A acceptance boundary

- Importable module `compiler/staqex/quantum_semantic_ir.py`.
- Immutable semantic IDs, `SemanticOrigin`, and schema-versioned root DTO.
- IDs/root references can address future nested/callable regions without
  requiring region behavior or flattening in Slice A.
- Deterministic named verifier diagnostics for duplicate identities, missing
  ancestry, and unsupported schema version (non-compile-hard).
- Canonical tuple ordering and no mutable collections in the accepted DTO
  surface.
- Tests contain no builder, lowering, region, target, or provider behavior.
- No Physics IR DTO edits; no evaluator changes; no QPU adapter changes.

### 4.1 Slice B acceptance boundary (approved Red scope shipped 2026-07-30)

Fixed by the reviewed Slice B Red assertions in
`tests/test_quantum_semantic_ir_slice_b_red.py` and shipped by Green/Refactor.
The Adjudicator re-review confirmed this scope but ruled the Slice B **contract
incomplete**; see §4.2.

- `ActingFactor` / `ActingSpace`: ordered finite tensor factors, positive local
  dimensions, `total_dimension` consistent with the factor product, non-empty
  factor tuple, embedded provenance.
- `PureJointStateValue` / `DensityJointStateValue`: whole-Joint-store
  generations over one `ActingSpace`, explicit purity, and **no** amplitude or
  density-matrix payload. ADR 0108 §1a makes `value_id` the generation identity;
  gap 3 Green removed the former bare integer field.
- `JointValueUse`: one consuming path per generation; a use naming a factor is
  invalid because factor IDs are coordinates, not separable state values.
- `QuantumSemanticModule` additive fields: `acting_spaces`, `values`,
  `value_uses` only.
- Approved design decisions:
  1. Slice B DTOs hold `SemanticOrigin` directly; `OriginId` is deferred to a
     later Slice or follow-up Issue so the Slice A API is unchanged.
  2. No `regions` field and no lowering field enters the root in Slice B.
  3. `producer_id: SemanticId` is an opaque reference; producer well-formedness
     is Slice C.
  4. Slice B emits only `QSEM_ACTING_SPACE_INVALID` and
     `QSEM_VALUE_USE_INVALID`.
- Out of Slice B: matrices, amplitudes, encodings, qubit allocation, region
  kinds, measurement and control lanes, lowering, pipeline, provider.

### 4.2 Slice B open verification gaps (Adjudicator re-review 2026-07-30)

Slice B is **not complete** until these are Red-covered. Authoritative record:
[re-review trace](../collaboration/traces/2026-07-30-liss-0082-slice-b-review.md).

| # | Gap | Code | State |
|---|---|---|---|
| 1 | duplicate **definition** IDs across `ActingSpace`, factors, and Joint values | `QSEM_IDENTITY_CONFLICT` | **closed** — follow-up 1 Red/Green/Refactor |
| 2 | `SemanticOrigin` embedded in Slice B DTOs is never validated | `QSEM_PROVENANCE_INCOMPLETE` | **closed** — follow-up 1 Red/Green/Refactor |
| 5 | `resources` checked for arity only, not identity **and order** against the factors | `QSEM_ACTING_SPACE_INVALID` | **closed** — follow-up 1 Red/Green/Refactor |
| 4 | no ordering model for consuming uses | `QSEM_VALUE_USE_INVALID` | **decided** — see below; no code change |
| 3 | bare integer `generation` carries no verified meaning | — | **closed** — ADR 0108 §1a; Red/Green/Refactor complete |

Gaps 1 and 2 extend the **Slice A** identity and provenance diagnostics to
Slice B *definition sites*. Gap 5 uses the Slice B shape code
`QSEM_ACTING_SPACE_INVALID`, strengthening its existing resource check from
arity to ordered identity. An identity appearing as a reference — `value.space_id`,
`value.resources`, `producer_id`, `JointValueUse` targets,
`SemanticOrigin.upstream_ids` — is not a definition and is never a duplicate.

**Gap 4 decision (2026-07-30).** No ordering field is added to Slice B. Two or
more consuming uses of one generation are a linearity violation whether they are
sequential or parallel, reported as a violation of *"one generation, at most one
consuming path"*. Use-after-consume is **not** described as a mere alias of
fan-out. Producer/consumer cycle detection is delegated to the Slice C region
graph.

**Diagnostic detail keys (2026-07-30).** Gap 5 changed the resource diagnostic's
detail keys from `resource_count` / `factor_count` to `resources` / `factors`.
The Adjudicator accepted this: there is no downstream consumer and the contract
does not fix detail keys. **When a diagnostic schema is published, detail keys
become a compatibility surface** and may not be changed this freely.

**Gap 3 decision (2026-07-30).** Option (a): remove only the bare integer
`generation` field. The *generation* semantics remain, carried by `value_id` as
the identity of one immutable whole-Joint-state generation.
`lineage_id + generation index` is rejected because it introduces lineage
identity and local ordering before the producer/consumer region graph defines
branching and merging. Join support would require additional parentage and merge
relations, duplicating or prematurely constraining graph semantics without an
accepted requirement. As a subtraction from an approved API this must not ride
along with follow-up 1; it needs its own reviewed Red.

**Gap 3 design update (2026-07-30).** The Architecture Path update received
scoped architecture approval for ADR 0108 §1a and the matching detailed-contract
change:

- [ADR 0108](../architecture/adr/0108-quantum-semantic-ir-value-region-contract.md)
  §1a states that the value identity *is* the generation and that the IR
  carries no generation field, counter, sequence index, version number, or
  `lineage_id + index` pair. Both rejected shapes are recorded under
  "Rejected alternatives".
- [detailed contract](../architecture/quantum-semantic-ir-contract.md) law 1,
  §3 `QuantumValueId`, §3.2 carrier signatures, and §14 decision 1 carry the
  same statement. The carrier signature becomes
  `PureJointStateValue(value_id, space, resources)` /
  `DensityJointStateValue(value_id, space, resources)`.
- Ordering between generations, where it is ever needed, is a property of the
  Slice C producer/consumer region graph, not of a stored number.

ADR 0108 as a whole remains **Proposed**. No implementation or test changed in
the design update. The separate gap 3 Red/Green/Refactor removed the field and
closed the final Slice B gap.

## 5. Issue-wide verifier laws

- each whole-Joint-state generation has exactly one producer and at most one
  consuming path; factor IDs are not independent state values;
- every referenced acting space, value, region, resource, obligation, and
  origin resolves inside the module;
- region input/output carriers and spaces match the region kind;
- Static Kernel measurement is terminal and no state is used afterward;
- dynamic feedback markers are rejected in Static Kernel;
- a Dynamic marker pairs one post-measurement Joint generation with one
  phase-local token; the pair cannot escape, split, or omit a single merge;
- compile-time selections do not survive into the module;
- runtime parameters/controllers do not alter acting-space shape;
- ancillas leave scope only through an explicit accepted discharge;
- non-exact semantic transformations carry an approximation obligation;
- provider, target, gate, shot, and plan-choice details are rejected;
- local/cloud/facility deployment, power, QEC, and computation-model details
  are rejected from Semantic IR;
- structured regions cannot be eagerly flattened without a finite approved
  materialization budget;
- routine validation and transformation cost is stated against compact
  hierarchy size, not expanded operation cardinality;
- validation reports diagnostics and never repairs the module.

## 6. Out of scope (Issue-wide)

- Numerical solving and simulator execution.
- Gate / matrix expansion and circuit synthesis.
- Jordan–Wigner and other mapping **execution** (LISS-0083).
- Provider SDK / OpenQASM-as-semantics / QIR-as-semantics.
- Equation DTO extension / auto-extraction.
- Algorithm Plan IR (LISS-0083), pass manager (LISS-0087).
- General channel/POVM execution (LISS-0084).
- Dynamic controller behavior and execution (LISS-0077).
- Existing QPU IR migration.
- Compile-hard diagnostic promotion.
- Soft `CompileResult` wire unless optional Slice F is separately approved.

General continuous-to-finite and mapping-dependent lowering is also gated by a
follow-on architecture decision because the blueprint currently places
Quantum Semantic IR after explicit finitarization while assigning realization
choices to later Algorithm Plan IR. LISS-0082 accepts only source-native or
already-reviewed finite evidence and must diagnose the rest.

## 7. Dependency and unlock graph

```text
LISS-0081 complete
LISS-0075 complete
    |
    +--> LISS-0082 (this Issue)
              |
              +--> LISS-0083 Algorithm Plan IR
              +--> LISS-0077 Dynamic QPU (also needs 0076)
              +--> later 0087 / Logical QPU consumers
```

## 8. Next allowed operation

Completed: Slice A Red/Green/Refactor (PR #138); Slice B **approved-Red scope
only** Red/Green/Refactor (2026-07-30) with its four design decisions approved.
The Adjudicator re-review ruled the Slice B contract **incomplete**.

Follow-up 1 (§4.2 gaps 1, 2, 5) is complete through Red/Green/Refactor: 10/10
pass, full sweep 97/47 with the failure set unchanged. Gap 4 is decided and
needed no code change.

Next:

1. Stop — obtain final Adjudicator review of Slice B.
2. Obtain explicit push, PR, and merge approval.
3. Slice C remains separately gated even after Slice B merges.
4. Slices C–F stay unauthorized: no region kinds, measurement, control lanes,
   lowering, `pipeline.py` edits, or provider work.
