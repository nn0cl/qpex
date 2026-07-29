# LISS-0081: Physics IR for equations and operator algebra

## Metadata

- Local issue ID: LISS-0081
- Status: **Slice E Phase 1 reviewed and accepted — follow-up work remains**
- Phase: Slice E Phase 1 (documentation/fixture preparation)
- Type: semantic IR / physics domain
- Priority: P0
- Initial planning size: XL
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md) E2 — Semantic IR
- Depends on: [LISS-0073](LISS-0073-named-dirac-notation-and-algebra-ast.md)
  **complete**; [LISS-0074](LISS-0074-qutrit-qudit-finite-local-dimension-types.md)
  **complete**; [LISS-0080](LISS-0080-phase-resolved-typed-hir.md) **complete**
- Authority: [ADR 0106](../architecture/adr/0106-staqex-v1-north-star-language-and-compiler.md),
  [compiler blueprint §4.2](../architecture/staqex-v1-compiler-blueprint.md),
  [v1 language north star §§6, 8](../specs/staqex-v1-language-north-star.md)

## Summary

Introduce a provider-neutral Physics IR on the Python Shipping Kernel. The IR
must preserve the recognizable mathematical structure of equations and
operator algebra instead of eagerly expanding formulas into gates or finite
matrices. It is the semantic boundary between phase-resolved HIR and a later
Quantum Semantic IR.

The first implementation is additive: it consumes reviewed HIR/typed source
contracts and does not replace the parser, typechecker, evaluator, or existing
symbolic projections in one rewrite.

## Acceptance scenarios

1. **Given** a typed formula containing Hilbert spaces, tensor factors, an
   operator expression, and a source span, **when** it is lowered to Physics
   IR, **then** the IR retains the space/factor structure, operator tree, and
   source provenance without gate expansion.
2. **Given** an equation with symbolic coefficients, units, dimensions,
   initial conditions, and a measurement intent, **when** it is lowered,
   **then** those records remain explicit and independently inspectable.
3. **Given** a mathematical binder with a domain and constraints, **when** it
   is lowered, **then** binder order, domain, constraints, and body structure
   remain present; finite expansion is a later pass.
4. **Given** fermionic, bosonic, or spin operator expressions, **when** they
   are lowered, **then** statistics, domain, and canonical source order remain
   explicit; no implicit mapping to qubits occurs.
5. **Given** symmetry or conservation declarations, **when** they are lowered,
   **then** the declarations retain their names, operands, and provenance and
   are available to later algebraic passes.
6. **Given** Ising, Heisenberg, Hubbard, molecular electronic, oscillator, or
   Lindblad formulas, **when** each is represented in Physics IR, **then** its
   equation/operator/binder structure remains recognizable in a golden
   inspection projection.
7. **Given** an IR node without valid source ancestry or with an invalid
   domain/unit/statistics relationship, **when** the verifier runs, **then** it
   returns a named diagnostic and does not silently repair the node.

## Non-goals

- no gate or matrix expansion;
- no numerical equation solving or simulator execution;
- no Quantum Semantic IR or Algorithm Plan IR;
- no automatic discretization, mapping, approximation, or provider choice;
- no provider SDK, QPU type, OpenQASM type, or database dependency;
- no new language surface unless a separately approved frontend issue requires
  it;
- no replacement of HIR or evaluator semantics in this Issue.

## Proposed slices

| Slice | Scope | Gate |
|---|---|---|
| A | Immutable Physics IR DTOs, provenance, verifier, and HIR-to-IR build boundary | Phase 1 Red after plan approval |
| B | Hilbert spaces, tensor factors, states, operators, observables, equations, coefficients, units, dimensions | Separate Red approval |
| C | Binders, domains, constraints, statistics, second-quantized order | Separate Red approval |
| D | Channels, POVMs, initial conditions, measurement intent, symmetries, conservation laws | Separate Red approval |
| E | Formula-family golden inspection for Ising/Heisenberg/Hubbard/molecular/oscillator/Lindblad; docs/catalog sync | Separate Red approval |

Each slice must remain additive and provider-neutral. Phase 2 may implement only
reviewed Red assertions; Phase 3 is limited to behavior-preserving cleanup.

## Design decisions requested

1. Approve the scope and acceptance scenarios above as the authoritative
   LISS-0081 acceptance specification.
2. Approve the recommended slice order A–E and authorize **Slice A Phase 1
   Red only**.
3. Confirm that the initial DTOs belong in a new focused module adjacent to
   `compiler/staqex/hir.py` (proposed `physics_ir.py`), with no adapter layer.
4. Confirm that existing AST/HIR nodes remain the input contract and that
   Physics IR does not become a second parser or typechecker.
5. Confirm that unit conversion, discretization, mapping, and numerical
   positivity/completeness checks remain later pass or plan concerns unless a
   slice-specific acceptance scenario explicitly adds them.

## Slice A completion evidence

- Phase 1 Red test was approved without modification.
- Phase 2 Green added the smallest immutable DTO/verifier boundary.
- Phase 3 extracted the diagnostic code/type and preserved behavior.
- `python3 tests/test_physics_ir_slice_a_red.py` PASS.
- pytest was unavailable in the environment (`No module named pytest`).

## Adjudicator review

- [x] Slice A Phase 1 Red, Phase 2 Green, and Phase 3 Refactor accepted.
- [x] Slice B plan intake opened; Phase 1 Red still requires separate approval.
- [x] Slice B Phase 1 Red, Phase 2 Green, and Phase 3 Refactor accepted.
- [x] Slice C plan and Phase 1 Red approved.
- [x] Slice C Phase 1 Red, Phase 2 Green, and Phase 3 Refactor accepted.
- [x] Slice D plan intake and Phase 1 Red approved.
- [x] Slice D Phase 1 Red, Phase 2 Green, and Phase 3 Refactor accepted.
- [x] Slice E Phase 1 documentation/fixture preparation accepted.

### Slice E review result

- [x] Docs-only closeout scope accepted.
- [x] Six-family golden catalog remains fixture-only.
- [x] Four verifier diagnostics are documented as non-compile-hard.
- [x] HIR lowering, Equation/Unit DTOs, and source-backed golden loading remain
      explicit follow-up work; LISS-0081 is not marked globally complete.

### Slice E completion evidence

- Added fixture-only six-family golden catalog.
- Registered four Physics IR verifier diagnostics as non-compile-hard.
- Synchronized remaining-work boundary: HIR lowering, Equation/Unit DTOs, and
  source-backed golden loading remain open.
- No compiler or test files changed in Slice E.
- `git diff --check` reports no whitespace errors.

Follow-up Issues: [LISS-0115](LISS-0115-hir-physics-ir-lowering.md),
[LISS-0116](LISS-0116-equation-unit-dto.md), and
[LISS-0117](LISS-0117-source-backed-physics-ir-goldens.md).

No new ADR is required for the current additive boundary. Return to
Architecture Path if HIR ownership/pass ordering, unit/coefficient policy,
source ownership, or public-oracle semantics change.

### Slice D completion evidence

- Slice D Red tests were approved without modification.
- Phase 2 added deterministic inspection DTOs and family/provenance verifier.
- Phase 3 extracted inspection record and diagnostic helpers without changing
  behavior.
- Slice A, B, C, and D direct test runners all PASS.
- pytest remains unavailable in the environment.

## Slice E plan intake — golden/catalog closeout

### Scope

Slice E will synchronize the public documentation boundary for the reviewed
Physics IR slice. It will add a stable formula-family golden catalog, register
the Physics IR verifier diagnostics in the promoted diagnostic catalog, and
reconcile the Issue/plan/trace status records.

This is a documentation and deterministic-fixture closeout slice. It does not
add HIR lowering, unit/equation DTOs, runtime execution, or a new parser.

### Acceptance scenarios

1. **Given** the six approved formula families, **when** the golden catalog is
   read, **then** each family has a stable ID, required recognizable structure,
   provenance requirement, and current implementation status.
2. **Given** each `PHYSICS_IR_*` verifier diagnostic emitted by Slices A–D,
   **when** the diagnostic catalog is read, **then** its meaning, severity/
   boundary, and owning Issue are documented without promoting it to a Kernel
   compile-hard code accidentally.
3. **Given** the Issue, plan, trace, and work-plan references, **when** closeout
   review runs, **then** their Slice status and remaining HIR/Equation gaps are
   consistent.
4. **Given** a golden marked as a fixture-only inspection artifact, **when** a
   reviewer reads it, **then** it is clear that it is not a public runtime
   oracle until the stable DTO/projection boundary is accepted.

### Proposed artifacts

- `docs/specs/staqex-v1-physics-ir-golden-catalog.md`;
- diagnostic catalog entries for `PHYSICS_IR_PROVENANCE_ERROR`,
  `PHYSICS_IR_DOMAIN_ERROR`, `PHYSICS_IR_STATISTICS_ERROR`, and
  `PHYSICS_IR_FAMILY_ERROR`;
- synchronized Issue/plan/trace status and an explicit remaining-work note;
- optional work-plan row update only after the Adjudicator confirms the
  implementation boundary.

### Decisions requested

- [ ] Approve the docs-only Slice E closeout scope.
- [ ] Confirm fixture-only golden status versus promotion to a public oracle.
- [ ] Confirm that HIR-to-Physics-IR lowering and Equation/Unit DTOs remain
      follow-up work rather than being silently closed by Slice E.
- [ ] Approve Slice E Phase 1 documentation/fixture preparation.

## Slice D plan intake — formula-family golden inspection

### Scope

Slice D will define a deterministic, non-destructive inspection projection for
Physics IR. The projection must show recognizable structure and source
provenance for six formula families: Ising, Heisenberg, Hubbard, molecular
electronic, oscillator, and Lindblad.

It consumes the DTOs from Slices A–C and existing source/type contracts. It does
not parse new syntax, evaluate formulas, expand gates, select discretization or
mapping, or execute a simulator/provider.

### Acceptance scenarios

1. **Given** an Ising formula, **when** it is inspected, **then** tensor factors,
   Pauli products, symbolic coefficients, and binder structure are visible.
2. **Given** a Heisenberg formula, **when** it is inspected, **then** component
   operators, site order, binder structure, and coefficient structure remain
   recognizable.
3. **Given** a Hubbard or molecular-electronic formula, **when** it is
   inspected, **then** orbital/site domains, fermionic statistics, atom order,
   and coefficient provenance remain visible without implicit qubit mapping.
4. **Given** an oscillator equation, **when** it is inspected, **then** the
   continuous domain, symbolic units/coefficients, equation relation, and
   source ancestry remain visible without discretization.
5. **Given** a Lindblad formula, **when** it is inspected, **then** density
   state, channel/jump references, evolution relation, and measurement intent
   remain visible without numerical integration.
6. **Given** any supported formula family, **when** the same Physics IR is
   inspected twice, **then** the projection is deterministic and every
   top-level item has source ancestry.
7. **Given** a formula node missing provenance or a required family marker,
   **when** inspection verification runs, **then** a named diagnostic is
   returned rather than a best-effort rendering.

### Proposed DTO/API boundary

- `InspectionRecord`: family, stable node identity, structure summary, and
  provenance references;
- `PhysicsInspection`: immutable ordered records plus diagnostics;
- `inspect_physics_ir(module)`: deterministic read-only projection;
- `verify_physics_inspection(result)`: named provenance/family checks.

### Decisions requested

- [ ] Approve the six-family golden corpus and acceptance scenarios.
- [ ] Confirm that the inspection projection is read-only and does not imply
      numerical execution or target lowering.
- [ ] Confirm that synthetic DTO fixtures may represent formulas without
      adding a second parser.
- [ ] Approve Slice D Phase 1 Red only.

### Slice C completion evidence

- Slice C Red tests were approved without modification.
- Phase 2 added immutable channel, measurement-intent, initial-condition, and
  symmetry DTOs with named domain diagnostics.
- Phase 3 extracted shared domain/statistics diagnostic helpers and preserved
  Slice A/B behavior.
- Slice A, B, and C direct test runners all PASS.
- pytest remains unavailable in the environment.

## Slice C plan intake — channels, observations, and symmetries

### Scope

Slice C will retain mixed-state/channel and measurement intent as Physics IR
structure, together with initial conditions and named symmetry/conservation
declarations. It consumes existing typed contracts such as `Channel`, `POVM`,
`DensityState`, Lindblad, and observation declarations. It does not execute
channels, validate numerical positivity, insert measurements, or choose a
simulator/provider.

### Acceptance scenarios

1. **Given** a channel with input and output Hilbert domains, **when** it is
   represented in Physics IR, **then** channel kind, domains, operation form,
   and source origin remain explicit.
2. **Given** a POVM or observable measurement intent, **when** it is
   represented, **then** measured domain, outcome/projection identity, intent,
   and source origin remain explicit without creating a runtime measurement.
3. **Given** an initial state or density-state condition, **when** it is
   represented, **then** the initial-condition relation and its target domain
   remain explicit and ordered before subsequent dynamics.
4. **Given** a Lindblad-style evolution with jump/channel references, **when**
   it is represented, **then** the evolution relation and referenced operators
   remain structured; no numerical integration or matrix expansion occurs.
5. **Given** a symmetry or conservation declaration, **when** it is
   represented, **then** name, operands/domain, law kind, and source origin
   remain inspectable.
6. **Given** a channel, POVM, initial-condition, or symmetry node with missing
   domain/origin references, **when** the verifier runs, **then** a named
   diagnostic is returned and the node is not repaired.

### Proposed DTO additions

- `ChannelNode`: operation, input/output domains, operands, origin;
- `MeasurementIntent`: observable/POVM identity, measured domain, outcome
  contract, terminal/dynamic intent, origin;
- `InitialCondition`: target state/domain, preparation expression, source order,
  origin;
- `SymmetryNode`: law kind, name, operands/domain, origin;
- `PhysicsModule` collections for channels, measurement intents, initial
  conditions, and symmetries.

### Boundaries and decisions requested

- Existing runtime contracts remain source evidence, not adapters inside
  Physics IR.
- Numerical trace/positivity/completeness checks remain construction/runtime
  concerns; Slice C records their intent and provenance only.
- Terminal measurement remains distinct from observation reporting and is not
  inserted by this slice.
- [ ] Approve Slice C acceptance scenarios and DTO candidates.
- [ ] Confirm no runtime execution or numerical validation in Slice C.
- [ ] Approve Slice C Phase 1 Red only.

### Slice B completion evidence

- Slice B Red tests were approved without modification.
- Phase 2 added immutable binder/statistics/atom DTOs and named diagnostics.
- Phase 3 extracted verifier node diagnostics and preserved Slice A behavior.
- `python3 tests/test_physics_ir_slice_a_red.py` PASS.
- `python3 tests/test_physics_ir_slice_b_red.py` PASS.
- pytest remains unavailable in the environment.

## Slice B plan intake — binders and statistics

### Scope

Slice B will add Physics IR structure for mathematical binders and
second-quantized operator metadata, consuming existing typed AST/HIR contracts.
It will preserve structure for inspection; it will not expand finite domains,
perform Jordan–Wigner mapping, or choose a numerical method.

### Acceptance scenarios

1. **Given** a typed `sum` or `product` binder, **when** it is represented in
   Physics IR, **then** binder kind, ordered variables, domain, constraints,
   body, and source origin remain explicit.
2. **Given** a binder whose body contains a nested binder, **when** it is
   represented, **then** nesting and source order remain intact and no
   expansion occurs.
3. **Given** a fermion, boson, spin, or qubit operator family, **when** its
   algebra is represented, **then** family, domain, statistics, atom order,
   and source origin remain explicit.
4. **Given** a fermionic expression with a non-canonical source order, **when**
   it is represented, **then** source order is retained and any canonical-order
   metadata is explicit rather than silently replacing the source tree.
5. **Given** a binder or operator node without a valid origin or with a missing
   domain/statistics reference, **when** the verifier runs, **then** it returns
   a named diagnostic and does not repair the node.

### Proposed DTO additions

- `BinderNode`: kind, ordered variables, domain, constraints, body, origin;
- `Statistics`: family and exchange/commutation policy identifier;
- `OperatorAtom`: family, symbol, index, source order, origin;
- `OperatorNode` extension: domain, statistics, atoms, algebra expression;
- `PhysicsModule` collections for binders and operators, preserving root order.

### Red boundary

Phase 1 Red should add DTO/verifier tests only. Existing parser, typechecker,
finite expansion, evaluator, and mapping tests are evidence of source contracts
but must not be modified for this slice. Phase 2 may add only the minimum
Physics IR representation needed by the reviewed tests.

### Adjudicator decisions requested

- [ ] Approve Slice B acceptance scenarios and DTO candidates.
- [ ] Confirm that finite expansion and Jordan–Wigner mapping remain out of
      scope for Slice B.
- [ ] Confirm that source atom order and canonical-order metadata are both
      retained when they differ.
- [ ] Approve Slice B Phase 1 Red only.

## Verification

- Phase 0: review this Issue and its companion plan; no tests or implementation.
- Phase 1: new failing tests only, focused on DTO invariants and the verifier.
- Phase 2: minimum implementation against unchanged reviewed tests.
- Phase 3: standalone slice tests plus the Shipping Kernel verification gate.
