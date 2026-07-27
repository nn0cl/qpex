# ADR 0106: QPex v1 north-star language and compiler

## Status

Proposed (Architecture Path, 2026-07-27).

This ADR is a design target and migration boundary. It does not supersede an
accepted ADR, authorize implementation, select a provider, or advance an
AT-TDD phase until the Adjudicator accepts it.

Companions:

- [QPex v1 language north star](../../specs/qpex-v1-language-north-star.md)
- [QPex v1 compiler blueprint](../qpex-v1-compiler-blueprint.md)
- [prior-art research](../../research/2026-07-27-quantum-language-compiler-landscape.md)
- [WP-0025](../../work-plans/WP-0025-qpex-v1-north-star.md)
- [LISS-0068](../../issues/LISS-0068-qpex-v1-normative-rebaseline.md)

## Context

QPex already has a substantial executable language and compiler. The Python
Kernel implements the joint-amplitude model, typed physical quantities,
Hamiltonian evolution, finite binders, mixed states and Lindblad evolution,
QPU IR, OpenQASM emission, Host Job contracts, scientific input binding, and
multi-register logical mapping.

The current normative specification is nevertheless a v0.1 snapshot. It
predates many accepted ADRs and still presents implemented lanes as proposed.
Several architecture notes also retain historical statements that now
contradict accepted return, effect, and lowering behavior.

The project therefore needs a zero-based answer to the design question without
pretending that implementation progress is zero:

> If QPex were designed today for a theoretical or experimental physicist,
> what source language and compiler boundaries should remain correct for the
> next hundred years?

ADR 0095 requires the ideal final form to govern the answer. Existing syntax
is preserved when it is already the ideal form. A breaking migration is
proposed when keeping an implementation-shaped spelling would impose a
permanent language defect.

## Decision proposal

### D1 — QPex is a staged scientific language, not a circuit DSL

The language has five statically separated phases:

1. `theory`: Hilbert spaces, physical carriers, equations, operators, and
   observables;
2. `experiment`: systems, initial conditions, preparations, parameters, and
   measurement plans;
3. `workflow`: immutable Host feedback and parameter-update contracts;
4. `execution`: target capabilities, resource/error budgets, shots, routing
   policy, and reproducibility metadata;
5. `report`: typed projections over completed results.

Dependency direction is:

```text
report -> execution -> workflow -> experiment -> theory
```

Reverse dependencies are hard errors. Source order inside declarative phases
is not execution order; a resolver constructs and validates the dependency
graph. Ordered mathematical products and ordered procedures retain their
source order.

### D2 — Static and dynamic quantum computation remain distinct lanes

The default Static Kernel preserves `Never Leave the State`:

- quantum values remain `State<T>` or `DensityState<T>`;
- ordinary `fn` is pure by default;
- `measure` is terminal;
- no general-purpose classical `if`, loop, exception, thread, file, network,
  Job, or provider object enters the Kernel.

Hardware feedback is expressed only in an explicit `dynamic qpu fn`:

- mid-circuit measurement creates a phase-local `Controller<T>`;
- `Controller<T>` may be inspected only by finite `match`;
- it cannot enter quantum arithmetic, escape to Theory, determine Hilbert
  shape, or masquerade as `State<T>`;
- required capabilities are part of the function contract;
- unsupported targets reject compilation or submission explicitly.

This adds real feed-forward without weakening the Static Kernel law.

### D3 — Physical system shape is typed and representation-independent

The public state model remains representation-neutral:

- `State<S>` is a pure state over acting space `S`;
- `DensityState<S>` is a mixed state over `S`;
- `Operator<S>` and `Hamiltonian<S>` act on exactly `S`;
- `Channel<A, B>` is an explicit CPTP map;
- `POVM<S, O>` maps an acting space to a finite outcome carrier.

Standard finite degrees of freedom are nominal:

- `Qubit`, `Qutrit`, and `Qudit<D>` for one local degree of freedom;
- `QubitRegister<N>`;
- `QutritRegister<N>`;
- `QuditRegister<D, N>` for a statically known local dimension `D`.

These names are not aliases for integer arrays. Multi-register systems use
the accepted named-register and `RegisterSet<SystemName>` model. Embedding,
reordering, tracing out, and changing representation are explicit operations.

### D4 — Surface numerics carry scientific meaning

A universal surface `Int` is not used as a substitute for distinct physical
or structural concepts.

- `Dimension`, `Index<N>`, `Count`, `Order`, and `ShotCount` are Meta/Host
  carriers;
- `Basis<N>`, `EnergyLevel<N>`, `SpinProjection<S>`, and user-defined finite
  carriers are quantum-domain carriers;
- `Param<T>` is a symbolic circuit parameter;
- `Controller<T>` exists only in a dynamic QPU control region;
- Host scientific inputs are immutable typed bindings with unit and provenance.

Internal implementations may use machine integers and floating-point values.
Those representations never erase the source-level distinctions.

### D5 — Mathematical notation is canonical source, not a second semantics

QPex v1 proposes one UTF-8, NFC-normalized mathematical spelling:

- `|ψ⟩`, `⟨φ|`, `⟨φ|A|ψ⟩`;
- `A†`;
- `ψ ⊗ φ`;
- pure `sum`, `product`, `integral`, and `tensor` binders;
- indexed operators such as `Z[spin[i]]`;
- explicit `evolve ... under ... for ... using ...`.

These forms lower immediately to the typed algebra already represented by
`adjoint`, `inner`, `outer`, `projector`, and tensor/operator nodes. They do
not define parallel semantics.

To obey ADR 0095, the current ASCII Ket and `*|*` forms are not retained as
permanent aliases if this proposal is accepted. A formatter/migrator rewrites
v0.1 source. Editor input methods may translate `\ket`, `\bra`, `\dagger`, and
`\otimes` to canonical characters, but the language has one emitted spelling.

Unicode identifiers follow a restricted UAX #31 profile, are NFC-normalized,
and receive confusable-identifier diagnostics. Mathematical punctuation is
tokenized structurally, so `|ψ⟩` cannot collide with the pipeline `|>`.

### D6 — Linearity, uncomputation, and effects are compile-time contracts

The type checker tracks quantum usage:

- no cloning of an unknown quantum state;
- no implicit discard of live quantum information;
- no aliasing the same logical degree of freedom into two mutable operations;
- automatic uncomputation only when the compiler proves it semantics-preserving;
- explicit `discard` only through an accepted physical operation such as
  trace-out or terminal measurement.

Function effects use the existing `effects { ... }` direction. The core set is
`Measure`, `Snapshot`, `Inspect`, `Host`, plus the dynamic-control capability
required by D2. Effects propagate transitively through calls, methods,
interfaces, modules, and pipelines.

### D7 — Functions return explicitly; failures do not throw

`pub fn`, explicit parameter types, explicit `-> Type`, and terminal `return`
remain canonical.

- `return` is a pure value boundary, not observation or early collapse;
- `main -> Unit` delegates results to terminal measurement and the Host result
  envelope;
- Kernel-recoverable alternatives are `State<Outcome<T, E>>` and remain
  coherent until projected or measured;
- compiler failures are structured hard diagnostics;
- Host/QPU failures are structured Job lifecycle results;
- `throw`, `try`, `catch`, implicit normalization, silent truncation, and
  silent Host emulation remain forbidden.

### D8 — Approximation is explicit and provenance-complete

Every non-exact transformation records:

- source expression and span;
- acting space and units;
- chosen discretization or mapping;
- algorithm and order;
- error category: proven bound, empirical estimate, or unbounded;
- requested and derived tolerances;
- resource estimate before and after lowering;
- target capability/profile assumptions.

No backend chooses a grid, mapping, Trotter step count, measurement grouping,
shot allocation, routing policy, or mitigation method without an explicit
policy or accepted default declared by the execution profile.

### D9 — The compiler uses multiple semantic IR levels

The compiler owns the following typed stages:

```text
Source/CST
  -> Phase-resolved HIR
  -> Physics IR
  -> Quantum Semantic IR
  -> Algorithm Plan IR
  -> Logical QPU IR
  -> Target IR / simulator plan
```

Host Workflow IR is separate from quantum IR and joins it only through
immutable Experiment, Job, and Result contracts.

Each lowering is a pure pass with declared input/output invariants. Provenance
links are mandatory. OpenQASM and QIR are backend artifacts, not QPex
semantics and not the compiler's only internal IR.

### D10 — Optimization is policy-aware and cannot change physics silently

The middle end distinguishes:

- exact canonicalization and algebraic simplification;
- approximation planning;
- circuit synthesis and semantics-preserving optimization;
- physical layout, routing, and scheduling;
- execution transformations such as error mitigation.

Noise mitigation is not labelled a semantics-preserving compiler
optimization. It is an explicit execution transformation because it changes
sampling cost, estimators, and result provenance.

### D11 — Simulation and QPU execution share contracts, not constraints

Simulator engines consume the same resolved semantic plan through capability
ports. State-vector, stabilizer, tensor-network, density-matrix, trajectory,
and open-system engines may have different capacities, but none changes source
semantics or silently reduces a state.

QPU backends consume logical QPU IR and target profiles. Physical mapping and
provider SDKs remain Host adapters. OpenQASM 3.1 and QIR profiles are initial
portable outputs; a target may support only a subset and must reject unsupported
capabilities explicitly.

### D12 — The production compiler evolves without a big-bang semantic fork

The Python Kernel remains the executable reference until a second
implementation passes the same conformance corpus.

The production target remains Rust, as already recorded by the repository.
Whether its IR infrastructure is fully custom or uses MLIR as an internal
implementation technology is a separate technology-selection Issue. There is
one language semantics, one diagnostic contract, and one differential
conformance suite.

## Alternatives rejected

### Treat QPex as a friendly OpenQASM frontend

Rejected. It would make circuit and target constraints shape the language and
would lose equations, domain carriers, approximation choices, and scientific
provenance too early.

### Put all classical control into the Kernel

Rejected. It recreates an ordinary imperative language, weakens `State<T>`,
and makes static, dynamic, and Host timing indistinguishable.

### Ban all mid-circuit measurement forever

Rejected. Quantum error correction and important hardware protocols require
measurement and feed-forward. The correct answer is an explicit dynamic lane,
not denial or implicit Host emulation.

### Use one generic `Int` and one generic `Operator`

Rejected. The representation may be integer- or matrix-backed, but the surface
must retain finite-domain, physical-unit, statistics, and acting-space meaning.

### Rewrite the compiler immediately

Rejected. A rewrite before a versioned conformance contract would create a
second semantics and discard working evidence.

## Consequences

Positive:

- a paper formula remains recognizable through lowering and diagnostics;
- static and dynamic quantum programs are both expressible without semantic
  leakage;
- simulator, OpenQASM, QIR, and provider backends remain replaceable;
- approximations and noise-related transformations are auditable;
- existing QPex investments become reference behavior rather than dead code.

Costs and risks:

- canonical Unicode mathematical source is a deliberate breaking migration;
- phase, linearity, and effect checking substantially increase frontend scope;
- multi-level IR and provenance validation add compiler complexity;
- dynamic control and QIR/OpenQASM support depend on target capability profiles;
- some accepted v0.1 ADRs will need explicit supersession rather than silent
  reinterpretation.

## Acceptance boundary

Acceptance of this ADR would approve the target architecture only. The first
safe implementation action remains LISS-0068 Phase 0/Phase 1 planning:

1. reconcile the normative v0.1 spec with all accepted ADRs;
2. classify every proposed v1 difference as preservation, additive extension,
   or breaking migration;
3. freeze conformance scenarios before changing lexer, parser, or runtime;
4. obtain separate approval for each implementation Issue in WP-0025.
