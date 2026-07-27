# QPex v1 acceptance envelopes (EARS / Gherkin)

| Field | Value |
|---|---|
| Status | Architecture Path draft (LISS-0068 slice 4) |
| Owner | LISS-0068 / WP-0025 E0 |
| Normative companions | Per-capability specs under `docs/specs/` |
| Diagnostic authority | [`qpex-v1-diagnostic-catalog.md`](qpex-v1-diagnostic-catalog.md) |
| Last updated | 2026-07-27 |

This document indexes **acceptance envelopes** for v1 conformance planning.
Each envelope states EARS requirements and representative Gherkin scenarios.
Detailed proofs, fixtures, and SV suite mappings remain in the linked
companion specifications and `tests/spec_verification/`.

Promotion freezes these envelopes as the Phase 1 Red contract for new
north-star work; existing shipped capabilities keep their reviewed Red modules.

## Envelope conventions

- **EARS** — normative behavioral requirements (`shall` / `shall not`).
- **Gherkin** — observable acceptance scenarios; `Then` clauses name diagnostic
  codes or SV assertions where applicable.
- **Authority** — when this envelope and a companion spec disagree before
  promotion, the companion spec wins until reconciled in LISS-0068 promotion PR.
- **Lane** — `Static` (default Kernel), `Parametric`, `Dynamic`, or `Host`.

---

## Capability index

| ID | Capability | Lane | Companion spec | SV / tests |
|---|---|---|---|---|
| E-01 | Joint store and terminal measure | Static | [`qpex-mvp-discrete-pmf-arith-measure.md`](qpex-mvp-discrete-pmf-arith-measure.md) | SV-01+ |
| E-02 | Forbidden / retired surface | Static | [`qpex-language-specification.md`](qpex-language-specification.md) §2.4 | SV-06 |
| E-03 | `when` / `evolve` / `until` | Static | ADR 0037, 0079; LISS-0012 | `test_evolve_until_runtime_red.py` |
| E-04 | Explicit returns and `main` | Static | [`qpex-explicit-return-and-scope.md`](qpex-explicit-return-and-scope.md) | SV-16 |
| E-05 | Static Hilbert / `QubitRegister<N>` | Static | [`qpex-static-hilbert-kernel.md`](qpex-static-hilbert-kernel.md) | SV-26 area |
| E-06 | Parametric circuit | Parametric | [`qpex-parametric-circuit.md`](qpex-parametric-circuit.md) | `test_parametric_circuit_runtime_red.py` |
| E-07 | Dynamic lane capability boundary | Dynamic | [`qpex-dynamic-qpu-lane.md`](qpex-dynamic-qpu-lane.md) | LISS-0028 Red |
| E-08 | Operator Hamiltonian / unitarity | Static | [`qpex-operator-algebra.md`](qpex-operator-algebra.md) | SV-19–30 |
| E-09 | Continuous discretization + lowering | Static | [`qpex-continuous-discretization.md`](qpex-continuous-discretization.md) | `test_continuous_*_red.py` |
| E-10 | Multi-register acting space | Static | [`qpex-multi-register-acting-space.md`](qpex-multi-register-acting-space.md) | LISS-0067 |
| E-11 | Finite binder lowering | Static | [`qpex-finite-binder-lowering.md`](qpex-finite-binder-lowering.md) | SV-19+ |
| E-12 | Modules and visibility | Static | [`qpex-pub-only-visibility.md`](qpex-pub-only-visibility.md) | SV-31 |
| E-13 | Host Job / submit boundary | Host | [`qpex-job-based-host-execution.md`](qpex-job-based-host-execution.md) | B13 example |
| E-14 | Scientific scopes / workflow | Static/Host | [`qpex-scientific-scopes.md`](qpex-scientific-scopes.md), [`qpex-workflow-surface.md`](qpex-workflow-surface.md) | scope Red tests |

---

## E-01 — Joint store and terminal measure

### EARS

When a program binds a quantum value, the system shall keep it as `State<T>` in
the joint store until terminal `measure` in the Static Kernel lane.

When `measure` executes, the system shall sample exactly once via `RngPort`
and shall not collapse intermediate pure expressions.

While no `measure` has run, the system shall not call `RngPort` for pure
arithmetic or evolution steps.

### Gherkin

```gherkin
Feature: Joint store and terminal measure

  Scenario: Terminal measure samples once
    Given a valid program with terminal "measure x"
    When the program runs with a deterministic RngPort
    Then exactly one RngPort draw occurs
    And the result is a collapsed outcome envelope

  Scenario: Pure evolution preserves norm
    Given a centered grid wavepacket program
    When "evolve psi under H for t" runs without measure
    Then assertNormEquals(psi, 1.0)
    And RngPort was not called
```

---

## E-02 — Forbidden and retired surface

### EARS

When source contains a Forbidden keyword, the system shall reject compilation
with `FORBIDDEN_KEYWORD`.

When source uses a Retired spelling, the system shall reject with
`RETIRED_KEYWORD` and a fix-it hint.

### Gherkin

```gherkin
Feature: Forbidden and retired keywords

  Scenario: Classical if is forbidden
    Given source containing "if (true)"
    When the program is compiled
    Then compilation fails with FORBIDDEN_KEYWORD

  Scenario: Retired observe spelling is rejected
    Given source using "observe x"
    When the program is compiled
    Then compilation fails with RETIRED_KEYWORD
```

---

## E-03 — Evolution and bounded until

### EARS

When `evolve … under H for t` is applied to a valid Hamiltonian, the system
shall evolve the joint state unitarily within numerical tolerance of the
reference Kernel.

When `evolve … until P max N` is used, the system shall repeat evolution steps
without measurement until `P` holds or `N` is exhausted.

When `N` is exhausted without `P` succeeding, the system shall fail with
`EVOLVE_UNTIL_MAX_STEPS_ERROR`.

When QPU emission is requested for `evolve until`, the system shall reject with
`E_QPU_UNSUPPORTED_CAPABILITY`.

### Gherkin

```gherkin
Feature: Evolution and evolve until

  Scenario: Bounded until succeeds within max steps
    Given a program with "evolve psi under H until converged(psi) max 10"
    When the program runs
    Then execution completes without EVOLVE_UNTIL_MAX_STEPS_ERROR

  Scenario: Until exhausts max steps
    Given a program whose predicate never succeeds within max 1
    When the program runs
    Then execution fails with EVOLVE_UNTIL_MAX_STEPS_ERROR
```

---

## E-04 — Explicit returns and main entry

### EARS

When `pub fn main` is declared, the system shall require `-> Unit`.

When an ordinary `fn` declares a return type, the system shall require a
terminal `return` expression of that type.

When `return` type disagrees with the declared type, the system shall reject
with `RETURN_TYPE_MISMATCH`.

### Gherkin

```gherkin
Feature: Explicit returns

  Scenario: Main must return Unit
    Given "pub fn main() -> Int"
    When the program is compiled
    Then compilation fails with MAIN_RETURN_TYPE_ERROR

  Scenario: Function return type mismatch
    Given a function declared "-> Operator" returning a State value
    When the program is compiled
    Then compilation fails with RETURN_TYPE_MISMATCH
```

---

## E-05 — Static Hilbert register surface

### EARS

When `QubitRegister<N>` is used, the system shall treat `N` as a compile-time
shape, not a runtime classical integer.

When static `forEach` iterates a register, the system shall elaborate before
backend submission and shall reject dynamic bounds with
`FOR_EACH_DYNAMIC_BOUND_ERROR`.

When logical qubit budget is exceeded, the system shall reject with
`STATIC_HILBERT_RESOURCE_ERROR`.

### Gherkin

```gherkin
Feature: Static Hilbert kernel

  Scenario: Dynamic forEach bound is rejected
    Given a static forEach with a runtime-dependent bound
    When the program is compiled
    Then compilation fails with FOR_EACH_DYNAMIC_BOUND_ERROR

  Scenario: QubitRegister shape is not measurable
    Given an attempt to measure QubitRegister<N> as Int
    When the program is compiled
    Then compilation fails with an acting-space or type error
```

---

## E-06 — Parametric circuit lane

### EARS

When `Param<T>` is declared, the system shall allow it only as an explicit gate
parameter, not as control flow or register shape.

When Host bindings are validated before QASM emission, missing keys shall yield
`PARAM_BINDING_MISSING` and unknown keys `PARAM_BINDING_UNKNOWN`.

When symbolic parameters are emitted to OpenQASM, the system shall preserve
parameter names without provider SDK calls in the Kernel.

### Gherkin

```gherkin
Feature: Parametric circuit

  Scenario: Param controls branching is rejected
    Given Param used in a when condition
    When the program is compiled
    Then compilation fails with PARAMETER_CONTROL_ERROR

  Scenario: Missing Host binding fails closed
    Given a parametric program without required binding
    When prepare_parametric_qasm runs
    Then the result includes PARAM_BINDING_MISSING
```

---

## E-07 — Dynamic lane capability boundary

### EARS

When mid-circuit measurement appears outside `dynamic qpu fn`, the system shall
reject with `MID_CIRCUIT_MEASUREMENT_REQUIRES_DYNAMIC_LANE`.

When a dynamic program lacks a required capability, the system shall reject
with `DYNAMIC_CAPABILITY_REQUIRED_ERROR` or `DYNAMIC_UNSUPPORTED_FEATURE_ERROR`.

The system shall not emulate unsupported dynamic features on the Host silently.

### Gherkin

```gherkin
Feature: Dynamic QPU lane boundary

  Scenario: Mid-circuit measure in static main is rejected
    Given measure inside a static kernel body before terminal measure
    When the program is compiled
    Then compilation fails with MID_CIRCUIT_MEASUREMENT_REQUIRES_DYNAMIC_LANE
      or EARLY_COLLAPSE_ERROR per surface rules
```

---

## E-08 — Hamiltonian evolution and unitarity

### EARS

When a non-Hermitian or non-unitary transform is applied to a ket, the system
shall reject with `NON_UNITARY_TRANSFORM_ERROR`.

When grid X/P Hamiltonians evolve a position grid state, the system shall
preserve norm within tolerance.

### Gherkin

```gherkin
Feature: Unitarity checks

  Scenario: Non-unitary map on ket is rejected
    Given "map(x -> x*0)" on a ket state
    When the program is compiled or run per SV-30 rules
    Then NON_UNITARY_TRANSFORM_ERROR is reported

  Scenario: Grid HO evolution preserves norm
    Given grid_oscillator.qpex or equivalent
    When evolution runs
    Then assertNormEquals(psi, 1.0)
```

---

## E-09 — Discretization contract and lowering

### EARS

When a continuous operator lacks an explicit discretization contract, the
system shall reject with `DISCRETIZATION_REQUIRED_ERROR`.

When a bridge references an unknown contract or operator, the system shall
reject with `DISCRETIZATION_BRIDGE_ERROR`.

When an MVP lowering contract is incompatible, the system shall reject with
`DISCRETIZATION_LOWERING_ERROR`.

When a lowered bridge alias evolves on the Kernel, results shall match the
direct grid Hamiltonian within stated tolerance.

### Gherkin

```gherkin
Feature: Continuous discretization lowering

  Scenario: Bridge lowering runs on kernel
    Given a Position/UniformGrid/Periodic bridge program
    When the program is compiled and run
    Then compilation succeeds
    And evolution produces normalized state

  Scenario: Non-MVP domain is rejected at lowering
    Given a Momentum-domain discretization bridge
    When the program is compiled
    Then compilation fails with DISCRETIZATION_LOWERING_ERROR
```

---

## E-10 — Multi-register acting space

### EARS

When an operator site omits register qualification in a multi-register system,
the system shall reject with `MULTI_REGISTER_INDEX_AMBIGUOUS` or
`UNKNOWN_REGISTER_ID`.

When acting spaces disagree without an explicit lift, the system shall reject
with `ACTING_SPACE_MISMATCH`.

### Gherkin

```gherkin
Feature: Multi-register mapping

  Scenario: Qualified site is accepted
    Given a RegisterSet with named registers and qualified Z[reg[i]]
    When the program is compiled
    Then compilation succeeds

  Scenario: Unknown register id is rejected
    Given an operator indexed by an undeclared register name
    When the program is compiled
    Then compilation fails with UNKNOWN_REGISTER_ID
```

---

## E-11 — Finite binder lowering

### EARS

When a supported finite sum/product body lowers to an operator, the system shall
produce an executable `OpExpr` consumed by evolve and QASM paths.

When a binder form is unsupported, the system shall reject with
`BINDER_LOWERING_UNSUPPORTED` or `MATHEMATICAL_BINDER_EFFECT_ERROR`.

### Gherkin

```gherkin
Feature: Finite binder lowering

  Scenario: Finite sum lowers and evolves
    Given a program with sum over a finite domain in an Operator bind
    When compiled and run on SV paths
    Then evolution completes without BINDER_LOWERING_UNSUPPORTED
```

---

## E-12 — Modules and visibility

### EARS

When a symbol is imported across modules without `pub`, the system shall reject
with `MODULE_PRIVATE_ACCESS_ERROR`.

When `_` private members are accessed outside the defining class, the system
shall reject with `PRIVATE_ACCESS_VIOLATION_ERROR`.

### Gherkin

```gherkin
Feature: Modules and visibility

  Scenario: Cross-module private access fails
    Given an import of a module-private function
    When the program is compiled
    Then compilation fails with MODULE_PRIVATE_ACCESS_ERROR
```

---

## E-13 — Host Job boundary (summary envelope)

### EARS

When a valid Kernel program is submitted through the Host API, the system shall
return a structured `JobResult` without partial measurements on failure.

When Kernel execution fails, diagnostics shall use stable codes from Appendix H
of the diagnostic catalog.

Detailed Host envelopes remain in companion specs; this entry indexes the
boundary only.

### Gherkin

```gherkin
Feature: Host job submission

  Scenario: Valid program submits and succeeds locally
    Given B13_host_job_api example program
    When submit_source runs
    Then JobResult status is succeeded
```

---

## E-14 — Scientific scopes and workflow (summary envelope)

### EARS

When phase dependency direction is violated, the system shall reject with
`PHASE_SCOPE_DIRECTION_ERROR`.

When workflow surface contracts are malformed, the system shall reject with
`WORKFLOW_SURFACE_ERROR`.

### Gherkin

```gherkin
Feature: Scientific scope direction

  Scenario: Execution concern in theory scope is rejected
    Given a theory block referencing shots or backend
    When the program is compiled
    Then compilation fails with PHASE_SCOPE_DIRECTION_ERROR
```

---

## Promotion and traceability

| Step | Action |
|---|---|
| 1 | Map each envelope ID to SV suite or Red module in promotion PR |
| 2 | Add missing Gherkin fixtures where envelope lacks automated coverage |
| 3 | Freeze envelope IDs in v1 spec appendix |
| 4 | LISS-0071 conformance harness references this index |

## LISS-0068 slice status

| Slice | Status |
|---|---|
| 1 Drift register | complete |
| 2 §1–§2 outline | complete |
| 3 Diagnostic catalog | complete |
| 4 Acceptance envelopes | **complete** (this document) |
| 5 Migration matrix | next |

## Next slice

**LISS-0068 E0 complete** — migration matrix in [`qpex-v1-migration-matrix.md`](qpex-v1-migration-matrix.md).
