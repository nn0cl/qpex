# Quantum Semantic IR contract

## Status and authority

**Draft for Adjudicator architecture review. No implementation permission.**

This document deepens the LISS-0082 plan under:

- [Staqex language axioms](staqex-language-axioms.md);
- [ADR 0106](adr/0106-staqex-v1-north-star-language-and-compiler.md);
- [compiler blueprint §4.3](staqex-v1-compiler-blueprint.md);
- [LISS-0082](../issues/LISS-0082-quantum-semantic-ir.md).

If this draft conflicts with an Accepted ADR, the Accepted ADR wins. The
proposed decisions are summarized in [ADR 0108](adr/0108-quantum-semantic-ir-value-region-contract.md).
Machine-scale, local-appliance, and computation-model constraints are proposed
separately in
[ADR 0109](adr/0109-quantum-machine-scale-and-model-envelope.md).
Optimistic household and same-world supercomputer stress profiles are proposed
in [ADR 0110](adr/0110-optimistic-quantum-capacity-horizon.md).
Current-machine acceptance and 2026–2031 planned-system stress profiles are
proposed separately in
[ADR 0111](adr/0111-current-hardware-first-delivery-horizon.md).

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: define a provider-neutral, immutable Quantum
  Semantic IR contract for finite whole-Joint-state meaning; preserve
  terminal measurement in Static Kernel; expose verifiable region, resource,
  exactness-obligation, and provenance boundaries.
- Specifications and files inspected: AGENTS.md; agent quickstart; readiness
  checklist; Staqex axioms; physicist/DX harmony; ADR 0106/0107; compiler
  blueprint; LISS-0080/0081/0082 and WP-0025; current HIR, Physics IR,
  Physics lowering, pipeline, and QPU IR implementations.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  immutable domain DTOs and pure verifier/lowering functions in the Shipping
  Kernel; no provider, file, network, RNG, sink, or target adapter. Candidate
  VOs are ActingSpaceId, QuantumValueId, RegionId, ResourceId, ParameterSymbol,
  SemanticOrigin, and ApproximationObligation.
- Applicable constraints: Never Leave the State; one language/two
  implementation generations; Clean Architecture; no hidden measurement;
  static shape; linear ownership; deterministic provenance; AT-TDD and
  Adjudicator gates.
- Decisions, assumptions, and unresolved ambiguities: value semantics and
  explicit region kinds are proposed in ADR 0108. How Physics IR obtains all
  finite carrier evidence remains a bounded lowering-input question. Dynamic
  controller behavior remains LISS-0077.
- Included and omitted AI context: included project architecture, affected
  source boundaries, and primary IR/profile research; omitted provider SDKs,
  credential/config data, opcode catalogs, unrelated evaluator internals, and
  private user data.
- Task routing (model/assistant/tool): architecture synthesis by the coding
  agent; repository and link inspection by deterministic tools; primary-source
  web research for external evidence.
- Input/output evidence contract when AI output is involved: input is cited
  repository artifacts plus public primary sources; output is reviewable
  design prose with proposed decisions and explicit inference labels, not
  hidden reasoning or generated runtime data.
- Verification plan: internal link/path inspection, terminology and status
  sync, prohibited-boundary search, Markdown/diff checks; no source or test
  execution because implementation is forbidden in this design batch.
```

## 1. Architectural position

```text
Typed HIR
  -> Physics IR                 symbolic physical meaning
  -> finite-evidence boundary   source-native or already-reviewed finite facts
  -> Quantum Semantic IR       executable finite quantum meaning
  -> Algorithm Plan IR         realization and approximation choices
  -> Logical QPU / simulator plan
  -> Target IR / adapter
```

Quantum Semantic IR answers:

> What finite state transformation, control law, measurement boundary, and
> resource obligation does the program mean?

It does **not** answer:

> Which encoding, decomposition, product formula, simulator algorithm, gate
> set, target profile, device, shot count, or error budget should realize it?

Consequently, a simulator and QPU path derive from one semantic module. They
may choose different plans, but they may not fork language meaning.

## 2. Core laws

1. **One Joint state value, not qubit locations.** Quantum data is represented
   as an immutable `PureJointStateValue` or `DensityJointStateValue` generation
   over the complete current `ActingSpace`. Factor/resource IDs refer to
   coordinates inside that Joint value and do not assert separability.
   Physical qubits, mutable registers, pointers, and provider handles are
   forbidden.
   **The value identity is the generation.** `QuantumValueId` alone denotes one
   immutable whole-Joint-state generation; there is no separate generation
   field, counter, sequence index, version number, or `lineage_id + index`
   pair. Ordering between generations, where needed at all, is a property of
   the producer/consumer region graph, not of a number stored on the carrier.
2. **One generation, one consuming path.** A quantum value has one producer
   and at most one consuming successor path. Branch joins must name their merge
   contract; copying a value into multiple quantum uses is invalid.
3. **Shape is static.** Acting-space identity, tensor order, and local
   dimensions are finite and fixed before Quantum Semantic IR construction.
   Runtime/controller values cannot alter them.
4. **Measurement is explicit and lane-specific.** Static Kernel measurement
   consumes a state at a terminal boundary. Dynamic feedback is represented
   only by a separate dynamic-lane obligation for LISS-0077.
5. **No silent realization choice.** Semantic nodes may declare that an
   approximation is required, but cannot select a method, tolerance, bound,
   gate expansion, mapping, or target.
6. **Provenance is closed.** Every semantic identity traces to source and
   upstream evidence through a deterministic transformation record.
7. **No silent repair.** Invalid shape, resource, region, measurement, or
   provenance contracts produce named diagnostics.
8. **Scale without flattening.** Region containment/call relationships and
   symbolic repetition may remain hierarchical. No verifier or consumer may
   require eager expansion merely because a target could eventually use a flat
   form.
9. **No deployment assumption.** The same semantic module may feed local,
   on-premises, remote, or facility planning. It contains no cloud, household,
   power, network, computation-model, or provider field.

## 3. Semantic module and identities

Candidate names are contracts for review, not frozen Python APIs.

```text
QuantumSemanticModule
  schema_version
  lane: StaticKernel | DynamicQpuContract
  acting_spaces[]
  parameters[]
  regions[]
  resource_obligations[]
  approximation_obligations[]
  origins[]
  roots[]
```

`regions` may form deterministic containment and call relationships. Canonical
serialization preserves that structure without mandatory inlining.
Recursive/unbounded semantics remain invalid unless separately specified.

All IDs are semantic identities, not list indexes:

- `ActingSpaceId`
- `QuantumValueId` = whole-Joint-store generation (the identity *is* the
  generation; no accompanying counter or index)
- `RegionId`
- `ResourceId` = factor ownership identity inside the Joint store
- `ParameterId`
- `OriginId`
- `ObligationId`

IDs must be deterministic from stable upstream identity, containing semantic
scope, semantic kind, and a canonical local ordinal. They must not depend on
object addresses, Python `repr`, hash randomization, provider names, or
filesystem traversal order. Identity encoding must permit nested/callable
regions without requiring them to be flattened first.

### 3.1 Acting spaces

`ActingSpace` records:

- stable identity;
- ordered tensor factors;
- finite positive local dimensions;
- total dimension, validated against the factors;
- domain labels needed for diagnostics;
- provenance.

It does not allocate qubits, choose an encoding, or flatten factors into target
indices. A symbolic or continuous space must be resolved by an explicit
upstream evidence boundary before entering this IR.

### 3.2 Quantum carriers

The carrier category is part of the whole-Joint-value contract:

- `PureJointStateValue(value_id, space, resources)`
- `DensityJointStateValue(value_id, space, resources)`

Each carrier **is** one generation, identified by its `value_id`. No generation
number is stored; see law 1 and ADR 0108 §1a.

`PureJointStateValue` may be promoted explicitly to
`DensityJointStateValue`; the reverse requires a separately proven
purification result and is not an implicit cast. Neither carrier contains
amplitudes or density matrices. Multiple independent state values are not
created merely because a source program names multiple coordinates. An
eventual tensor-composition operation would require explicit separability
evidence and is outside LISS-0082.

## 4. Region contracts

The IR uses distinct region kinds rather than a bag of optional flags.

| Region | Signature law | Semantic obligation |
|---|---|---|
| `UnitaryRegion` | `PureJoint<S> -> PureJoint<S>`; mixed lifting may be declared separately | same acting space; reversible intent; no measurement |
| `IsometryRegion` | `PureJoint<A> -> PureJoint<B>` | finite `dim(A) <= dim(B)`; introduced environment/ancilla obligation explicit |
| `ChannelRegion` | `PureJoint<A> or DensityJoint<A> -> DensityJoint<B>` | channel identity and physicality obligation explicit; no hidden purification |
| `MeasurementRegion` | Static: Joint state -> terminal outcome; Dynamic: Joint state -> correlated post-measurement Joint state + phase-local token | irreversible boundary; lane and correlation rules apply |
| `CoherentControlRegion` | one Joint state input -> one Joint state result; control/target are factor selectors | preserves entanglement and superposition; not classical branching or two separable register inputs |
| `DynamicControlRegion` | correlated post-measurement Joint state + token -> finite branch regions -> one merged Joint generation | dynamic lane only; correlation cannot be discarded; controller behavior delegated to LISS-0077 |

Mathematical validity is represented in three levels:

1. `Declared`: source/upstream contract claims the property;
2. `Verified(witness_ref)`: a deterministic verifier has evidence;
3. `Required(obligation_id)`: a later verified pass must establish it.

LISS-0082 does not invent matrices to prove declarations and must not label an
unverified declaration as verified.

### 4.1 Control-domain separation

Three notions must not be collapsed:

- **coherent quantum control** is a state transformation and remains inside the
  whole-Joint-state graph;
- **compile-time/static selection** is resolved before Quantum Semantic IR and
  leaves provenance, not runtime branches;
- **measurement feedback** is a Dynamic QPU lane contract and creates a
  phase-local dynamic value.

This separation prevents a classical `if` from being smuggled into Static
Kernel semantics under the generic word “control”.

## 5. Measurement lanes

### 5.1 Static Kernel

- A `MeasurementRegion` consumes the final Joint state generation, even when
  its outcome intent names only selected factors or observables.
- No quantum operation may consume that Joint generation afterward.
- The region yields an `OutcomeIntent` for the terminal application boundary,
  not a reusable mid-program classical value.
- Output formatting, sampling RNG, and sinks remain behind existing ports and
  outside this IR.

### 5.2 Dynamic QPU contract

LISS-0082 may represent only the minimum semantic marker needed to prove that
an operation requires dynamic feedback:

- measurement identity and measured resource;
- finite outcome domain;
- branch-region identities;
- paired post-measurement Joint generation and phase-local token identities;
- correlation and single-merge obligations for the pair;
- required capability `DynamicMeasurementFeedback`;
- provenance.

Controller construction, lifetime, allowed classical operations, termination,
target support, and execution are LISS-0077. A Static Kernel module containing
this marker is invalid. The token may not escape its dynamic phase, and neither
the token nor the paired post-measurement Joint state may be discarded or used
independently. This preserves state continuity without pretending that
LISS-0082 defines adaptive execution.

## 6. Linear resources, ancillas, and uncomputation

Each state transformation consumes one input Joint generation and produces a
fresh output Joint generation. A verifier builds no hidden aliases. Resource
IDs track factor ownership within that value; they are not independently
copyable state objects.

Ancilla use is represented by an `AncillaScope`:

```text
acquire(resource, zero/vacuum precondition)
  -> live generations
  -> discharge:
       ReturnedZero(witness)
     | AbsorbedByIsometry(obligation)
     | TracedByChannel(explicit environment)
     | TerminalMeasurement
```

Dropping an ancilla without a discharge is invalid. Quantum Semantic IR
records an `UncomputeObligation` or an accepted upstream witness; it does not
synthesize an inverse operation. ADR 0107's runtime tolerance remains a
simulator-equivalence policy and is not copied into this IR.

## 7. Parameters and shape independence

`ParameterSymbol` records identity, scalar/domain type, unit/dimension where
known, binding phase, and provenance.

Parameter uses may alter a transformation's numerical realization while
preserving its semantic signature. They may not:

- change acting-space factors or local dimensions;
- select a provider or device;
- encode a shot count or target calibration;
- read a dynamic measurement result in the Static Kernel lane.

## 8. Exactness and approximation boundary

Quantum Semantic IR records only semantic exactness:

- `Exact`
- `ApproximationRequired(obligation_id, reason, provenance)`

It does not record `epsilon`, Trotter steps, product-formula order, empirical
error, resource estimates, or `ProvenBound`. Those belong to Algorithm Plan IR
under the blueprint's error ledger.

A pass that changes exact meaning must create or propagate an approximation
obligation. A missing obligation is a verifier failure. Merely carrying
floating-point data does not by itself authorize an approximation.

## 9. Provenance and finite lowering input

`SemanticOrigin` contains:

- source span/origin;
- ordered upstream Physics/HIR evidence IDs;
- deterministic pass identity and version;
- parent origin IDs;
- semantic reason for introduced nodes.

Quantum Semantic lowering must accept a narrow, immutable input contract:

```text
QuantumSemanticInput
  physics_module
  finite_carrier_evidence[]
  linear_resource_evidence[]
  lane
```

It must not inspect `CompilationUnit`, AST nodes, CLI settings, files, provider
capabilities, or evaluator state. If required finite evidence is absent, the
lowering emits `QSEM_FINITE_EVIDENCE_MISSING`; it does not infer a private
discretization.

LISS-0082 lowering accepts only source-native or already-reviewed finite
carrier evidence. It does not choose a discretization or encoding. Continuous
or encoding-dependent Physics IR therefore emits
`QSEM_FINITE_EVIDENCE_MISSING` in this Issue.

### 9.1 Ordering ambiguity boundary

The current blueprint says Quantum Semantic IR follows explicit
discretization/mapping, while also assigning discretization and mapping choices
to the later Algorithm Plan IR. General continuous-to-finite and
operator-to-carrier lowering therefore has an unresolved ordering dependency.

LISS-0082 must not hide that dependency. Its accepted MVP boundary is:

- source-native finite carriers and previously accepted finite evidence may
  lower;
- the lowering records evidence provenance but makes no choice;
- unsupported continuous/mapping-dependent inputs fail with the named missing-
  evidence diagnostic;
- a follow-on architecture decision must define whether planning has a
  pre-semantic decision stage, an iterative refinement loop, or a revised
  stage ordering.

Whether finite evidence is eventually stored in an extended Physics IR or
assembled by a dedicated boundary pass is part of that follow-on. LISS-0082's
first slices can define and verify the input DTO without changing Physics IR.

## 10. Verifier contract

The verifier is deterministic and side-effect-free. At minimum it checks:

| Code | Condition |
|---|---|
| `QSEM_IDENTITY_CONFLICT` | duplicate or nondeterministic semantic identity |
| `QSEM_PROVENANCE_INCOMPLETE` | missing source/upstream/transform ancestry |
| `QSEM_ACTING_SPACE_INVALID` | non-finite, non-positive, inconsistent, or unknown shape |
| `QSEM_VALUE_USE_INVALID` | Joint generation has a missing producer, fan-out, use-after-consume, invalid join, or independently used factor |
| `QSEM_REGION_SIGNATURE_INVALID` | carrier/space signature violates region kind |
| `QSEM_MEASUREMENT_BOUNDARY_INVALID` | hidden, non-terminal Static measurement or post-measure use |
| `QSEM_CONTROL_LANE_INVALID` | dynamic feedback in Static Kernel or unresolved static selection |
| `QSEM_DYNAMIC_CORRELATION_INVALID` | dynamic token and post-measurement Joint state are separated, escape, or lack one merge |
| `QSEM_PARAMETER_SHAPE_DEPENDENCE` | runtime parameter/controller changes shape |
| `QSEM_RESOURCE_DISCHARGE_MISSING` | ancilla/resource leaves scope without accepted discharge |
| `QSEM_APPROXIMATION_OBLIGATION_MISSING` | non-exact transformation lacks explicit obligation |
| `QSEM_FINITE_EVIDENCE_MISSING` | lowering lacks reviewed finite carrier evidence |
| `QSEM_FORBIDDEN_REALIZATION_DETAIL` | provider, target, gate, shot, or plan choice leaked into module |
| `QSEM_FORBIDDEN_DEPLOYMENT_DETAIL` | cloud/local/facility, network, power, QEC, or model-profile data leaked into semantics |
| `QSEM_UNBOUNDED_MATERIALIZATION` | a consumer requests eager expansion without a finite approved artifact budget |

Diagnostics include code, origin, affected IDs, and a public explanation. They
must not silently mutate the module. Compile-hard promotion remains a separate
reviewed decision; the verifier contract itself is defined now.

## 11. Consumer contract

- Algorithm Plan lowering consumes a verified `QuantumSemanticModule` and
  resolves every `ApproximationRequired` and realization obligation.
- Simulator and QPU planning derive from that same verified module through
  Algorithm Plan or another reviewed, semantics-preserving pass.
- Existing `qpu_ir.py` is not rewritten by LISS-0082. Its eventual migration
  must stop reading source-adjacent structures as semantic authority.
- Target profiles and capabilities may reject a downstream plan; they cannot
  reinterpret the semantic module.

## 12. Versioning and serialization

The first Python DTO form is in-memory and immutable. It still carries
`schema_version = 1` and canonical tuple ordering so future serialization and
the Rust generation can reproduce meaning.

Unknown schema versions are rejected. Forward-compatible “ignore unknown
semantic field” behavior is forbidden until separately specified because it
could erase measurement or resource obligations.

## 13. Issue boundaries

LISS-0082 owns:

- immutable semantic identities and root module;
- finite acting-space and whole-Joint-state-value contracts;
- region signatures;
- lane markers;
- resource/ancilla obligations;
- semantic exactness obligations;
- provenance and verifier diagnostics;
- minimal Physics-to-Semantic lowering evidence.

It does not own:

- general channel/POVM execution (LISS-0084);
- dynamic controller behavior/execution (LISS-0077);
- realization choices and error/resource ledgers (LISS-0083);
- verified pass manager (LISS-0087);
- simulator/QPU ports and target capability negotiation;
- gate/circuit/target IR;
- provider adapters or Rust implementation.

## 14. Review decisions

Adjudicator architecture approval is required for:

1. value semantics and generation-based linear use, **including that the value
   identity is the generation and no generation number is stored** (ADR 0108
   §1a; the Python Kernel conforms after LISS-0082 gap 3 Green);
2. distinct region kinds and three-way control-domain separation;
3. Static Kernel terminal measurement versus Dynamic QPU marker boundary;
4. `Exact` versus `ApproximationRequired` responsibility split;
5. narrow `QuantumSemanticInput` and no raw AST/CompilationUnit access;
6. proposed ADR 0108.
7. scale-free hierarchy and no-deployment assumptions from proposed ADR 0109;
8. compact-plan scalability under proposed ADR 0110 QP-2/QS-2 profiles,
   without per-expanded-operation allocation.
9. current CH0/CH1 and planned-system NH5 profiles remain downstream
   acceptance fixtures under proposed ADR 0111 and never become semantic
   fields or language limits.

Decision 1's value-identity/generation clause received **scoped architecture
approval** on 2026-07-30. The remaining decisions and ADR 0108 as a whole remain
unapproved.

This document alone authorizes no tests or implementation. LISS-0082 gap 3
removed the redundant field under separate Red and Green approvals; Phase 3
review remains gated.
