# Staqex v1 S02 — indication-agnostic drug-discovery benchmark

| Field | Value |
|---|---|
| Status | **Accepted acceptance specification — Phase 2 implementation in progress** |
| ADR | [ADR 0190](../architecture/adr/0190-s02-selection-boundary-and-mix-control.md) |
| Work plan | [WP-0093](../work-plans/WP-0093-s02-language-expressiveness-and-selection.md) |
| Design | [S02 design](staqex-v1-drug-discovery-benchmark-design.md) |
| Relationship | S02 is additive; the locked disaster-response S01 remains unchanged |

## Purpose

S02 measures whether Staqex can express a finite early drug-discovery
selection experiment while keeping classical data, quantum state, constraints,
observables, terminal outcomes, and execution resources distinct.

It is a language expressiveness benchmark, not a chemistry, clinical, or
quantum-advantage claim.

## Normative benchmark shape

```text
synthetic manifest
  → Host candidate validation and deterministic ordering
  → explicit finite encoding
  → quantum selection State
  → hard-constraint Projector
  → soft-objective evolution
  → terminal measure
  → classical reranking and report
```

### Fixture limits

- Candidate count: 8–16.
- Selection size: 2–4.
- Candidate IDs: unique and stable within the manifest.
- Seed: required and recorded.
- Dataset: synthetic fixture for the first implementation.
- Encoding: one logical selection carrier per candidate for the first profile.

## Value model

### Classical records

`Candidate` contains a stable `CandidateId`, descriptor reference, score
components, tags, and provenance. A canonical chemical string is optional
evidence; it is not interpreted as a quantum value by the Kernel.

`Constraint` contains a named selection rule and its domain. `Score` contains
a normalized finite component, direction, weight, and provenance.

`SelectionProblem` contains the ordered candidates, target profile, hard
constraints, soft objective terms, selection size, seed, encoding profile, and
resource profile.

### Quantum carrier

The Kernel-facing conceptual type is:

```text
State<Selection<CandidateId>>
```

The state is not measured during validation, pruning, scoring, or evolution.
Feature vectors, strings, scores, and IDs do not become amplitudes implicitly.

## Control and observation rules

| Surface | Meaning | Sampling |
|---|---|---:|
| `mix` | State-valued probabilistic/classified alternatives | No |
| `controlled` / `Ctl` | Coherent operation control | No |
| `superpose` | Reserved for coherent phase-preserving composition | No |
| `project` | Feasible-subspace restriction; hard constraints lower to Projector | No |
| `expect` | Non-destructive observable evaluation | No |
| `measure` | Terminal `Outcome` / classical result boundary | Yes |

`when` is not part of the canonical S02 surface. Its use must fail closed with
a migration diagnostic; the compiler must not treat it as an alias for `mix`.

## Constraint and objective contract

Host validation may remove only malformed or unadmissible input records. The
selection-specific hard constraints remain explicit in the quantum problem and
lower to a feasible-subspace Projector or an equivalent named operator.

Soft preferences are normalized to a common finite scale before weighted
composition. The initial objective is a weighted finite objective; lexicographic
and Pareto objectives are later extensions.

If a penalty Hamiltonian is used, the report must identify it as a penalty
profile and must not claim that a low penalty guarantees feasibility.

## Result contract

The Host report contains:

- manifest ID, seed, compiler/profile identity, and deterministic ordering;
- terminal selection and observation metadata;
- feasibility result and violated constraints, if any;
- baseline score, objective score, and reranked score components;
- logical width, operation count, depth estimate, simulator budget, and lane;
- finiteization / lowering provenance and approximation policy;
- warnings and an explicit optimality claim, `none` by default.

An empty, missing, or unverifiable terminal observation is a failed result, not
a fabricated zero score.

## Acceptance scenarios

```gherkin
Feature: S02 classical and quantum boundary

  Scenario: candidate data stays classical
    Given a valid synthetic candidate manifest
    When the Host constructs a SelectionProblem
    Then candidate records and scores remain classical values
    And no implicit amplitude encoding is introduced

  Scenario: finite encoding is explicit
    Given a candidate set without finite encoding evidence
    When the Kernel boundary is prepared
    Then preparation fails with a finite-evidence diagnostic

  Scenario: hard constraints use a projector boundary
    Given a valid finite SelectionProblem with hard selection constraints
    When the quantum state is prepared
    Then hard constraints lower to a named Projector or equivalent operator
    And no terminal measurement occurs during projection

  Scenario: mix is not classical branching
    Given a state-valued alternative with multiple positive-weight arms
    When `mix` is evaluated
    Then every positive arm remains in the resulting State
    And no RNG call occurs

  Scenario: controlled is not mix
    Given a coherent controlled operation
    When the program requests `controlled`
    Then the operation retains its coherent-control meaning
    And it is not lowered to a probabilistic mixture

  Scenario: removed when spelling fails closed
    Given source containing `when` in the Static Kernel
    When the source is compiled
    Then compilation fails with a migration diagnostic
    And the compiler does not reinterpret the source as `mix`

  Scenario: only terminal measure crosses the classical boundary
    Given a valid evolved selection State
    When the program reaches terminal `measure`
    Then the result is an Outcome / classical selection
    And the Host report records the observation and resource metadata

  Scenario: same execution identity reproduces the result
    Given the same manifest, seed, compiler identity, and execution profile
    When the benchmark is replayed
    Then candidate ordering and report fields are identical

  Scenario: unsupported width fails before execution
    Given a finite encoding wider than the selected target profile
    When lowering is requested
    Then lowering fails with an explicit capability diagnostic
    And no classical optimizer is substituted
```

## Out of scope

- Real compound data adapters or chemical graph semantics.
- Clinical, efficacy, or ADMET claims.
- Live QPU provider SDKs and credentials.
- Automatic QUBO/QAOA rewriting.
- Pareto and lexicographic objective surfaces.
- General-purpose collection syntax.
- Compiler, grammar, evaluator, IR, or test changes before Phase 1 approval.
