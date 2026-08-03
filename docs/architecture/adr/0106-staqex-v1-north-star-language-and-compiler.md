# ADR 0106: Staqex v1 north-star language and compiler

## Status

**Accepted with conditions** (2026-07-27).

This ADR is the v1 **target architecture and migration boundary**. It does not
authorize lexer, parser, runtime, or provider implementation by itself, and it
does not supersede an accepted ADR except where the acceptance record below
names an explicit additive extension or a deferred follow-up Issue.

Companions:

- [Staqex v1 language north star](../../specs/staqex-v1-language-north-star.md)
- [Staqex v1 compiler blueprint](../staqex-v1-compiler-blueprint.md)
- [prior-art research](../../research/2026-07-27-quantum-language-compiler-landscape.md)
- [WP-0025](../../work-plans/WP-0025-staqex-v1-north-star.md)
- [LISS-0068](../documentation-compression-map.md)

## Context

Staqex already has a substantial executable language and compiler. The Python
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

> If Staqex were designed today for a theoretical or experimental physicist,
> what source language and compiler boundaries should remain correct for the
> next hundred years?

ADR 0095 requires the ideal final form to govern the answer. Existing syntax
is preserved when it is already the ideal form. A breaking migration is
proposed when keeping an implementation-shaped spelling would impose a
permanent language defect.

## Decision proposal

### D1 — Staqex is a staged scientific language, not a circuit DSL

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

Staqex v1 proposes one UTF-8, NFC-normalized mathematical spelling:

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
links are mandatory. OpenQASM and QIR are backend artifacts, not Staqex
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

### Treat Staqex as a friendly OpenQASM frontend

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
- existing Staqex investments become reference behavior rather than dead code.

Costs and risks:

- canonical Unicode mathematical source is a deliberate breaking migration;
- phase, linearity, and effect checking substantially increase frontend scope;
- multi-level IR and provenance validation add compiler complexity;
- dynamic control and QIR/OpenQASM support depend on target capability profiles;
- some accepted v0.1 ADRs will need explicit supersession rather than silent
  reinterpretation.

## Acceptance boundary

Acceptance approves the **north-star target** only. Implementation remains
gated by LISS-0068 reconciliation, reviewed conformance scenarios, and
per-Issue phase approval in WP-0025.

### Adjudicator acceptance record (2026-07-27)

**Decision:** Accept with scoped revisions (north-star direction).

**What acceptance authorizes now**

1. LISS-0068 slice 2+ — reconcile v0.1 normative text against accepted ADRs
   using this ADR as the v1 target.
2. Classify every v1 delta as `preserve`, `additive`, `breaking`, `bug`, or
   `defer` in the rebaseline register.
3. Plan LISS-0069 Unicode migration and later WP-0025 Issues against the
   boundaries below.

**What acceptance does not authorize**

- lexer, parser, formatter, or runtime changes without a reviewed Red slice;
- mandatory five-phase source layout for all v0.1-valid programs;
- full Unicode migration or ASCII Pauli removal in one step;
- dynamic-lane mid-circuit **execution** (capability rejection remains the
  current shipped boundary per ADR 0071 / LISS-0028);
- Rust compiler implementation or MLIR technology selection (LISS-0070);
- provider SDK, credentials, network submit, or physical routing.

### Decision disposition

| Proposal | Acceptance | v1 posture | Follow-up |
|---|---|---|---|
| D1 staged scientific phases | Accepted as target | **Additive** — existing programs need not adopt five-phase layout | LISS-0068+ |
| D2 static vs `dynamic qpu fn` | Accepted | **Additive** lane; static Kernel law unchanged | LISS-0028+ execution Issues |
| D3 typed acting spaces | Accepted | **Preserve** — aligns with ADR 0102/0105 | LISS-0068 spec sync |
| D4 semantic carriers | Accepted | **Preserve** — aligns with ADR 0070/0090 | LISS-0068 spec sync |
| D5 Unicode canonical source | Accepted as direction | **Breaking**, staged — see Unicode scope | LISS-0069 |
| D6 linearity / uncomputation | Accepted as direction | **Defer** mandatory proof-driven enforcement to later frontend Issues | post-E1 |
| D7 explicit `return` | Accepted | **Preserve** — ADR 0068 authoritative | LISS-0068 DR-003 |
| D8 explicit approximation provenance | Accepted | **Preserve** where shipped; extend in rebaseline | LISS-0068 |
| D9 multi-level semantic IR | Accepted as blueprint | **Defer** Python refactor — no big-bang IR rewrite | LISS-0070+ |
| D10 policy-aware optimization | Accepted as principle | **Defer** detailed middle-end policy to E3 Issues | WP-0025 E3 |
| D11 shared simulator/QPU contracts | Accepted | **Preserve** port boundaries; extend diagnostics | LISS-0068 |
| D12 Python reference Kernel | Accepted | **Preserve** until Rust passes the same conformance corpus | LISS-0071 |

### Unicode migration scope (LISS-0069)

North-star direction: **one canonical UTF-8 NFC mathematical spelling** per
ADR 0095. Migration is **staged**, not a single v1.0 flag day.

**In scope for LISS-0069 first slice**

- Dirac tokens: `|ψ⟩`, `⟨φ|`, bra-ket matrix elements;
- `A†` adjoint and `ψ ⊗ φ` tensor product as canonical emitted forms;
- NFC normalization, restricted UAX #31 identifiers, confusable diagnostics;
- formatter/migrator round-trip with comments and spans preserved;
- pipeline `|>` remains distinct from Ket `⟩` at lexer level (no collision).

**Staged, not day-one removal**

- ASCII Pauli atoms `X` / `Y` / `Z` / `I` remain accepted until a reviewed
  migrator and SV corpus prove parity; then deprecate, then remove in a named
  major bump.
- Editor input helpers (`\ket`, `\bra`, `\dagger`, `\otimes`) stay editor
  behavior, not additional language syntax.

**Out of LISS-0069 initial scope**

- `state` keyword → `State<T>` spelling migration (DR-007; separate Issue);
- mandatory Greek/subscript identifiers in existing pedagogy examples.

### `dynamic qpu fn` boundary (refines ADR 0071)

ADR 0071 remains authoritative for lane separation. This ADR **refines** it
without replacing it:

- mid-circuit measurement and finite classical feed-forward live only in
  `dynamic qpu fn`;
- mid-circuit results surface as phase-local `Controller<T>`, inspectable only
  by finite `match`;
- `Controller<T>` must not enter quantum arithmetic, escape to Theory, fix
  Hilbert shape, or masquerade as `State<T>`;
- required backend capabilities are part of the function contract; unsupported
  targets reject at compile or submit time;
- Host silent emulation of unsupported dynamic features remains forbidden.

**Explicitly deferred**

- dynamic-lane runtime execution and simulator conformance (ADR 0071 open items);
- `Controller<T>` composition with terminal `measure` and `JobResult`;
- capability-profile DTO details beyond the existing rejection boundary.

### Python reference implementation (D12)

- The shipping Python package `compiler/staqex/` is the **executable reference
  Kernel** until a second implementation passes the same conformance corpus.
- Rust remains the recorded long-term production target; custom IR versus
  selective MLIR is a **separate** technology-selection Issue (LISS-0070).
- One language semantics, one public diagnostic contract, one differential
  oracle — no semantic fork between implementations.

### First safe implementation actions

1. LISS-0068 — reconcile the normative v0.1 spec with all accepted ADRs using
   this acceptance record.
2. Classify every proposed v1 difference as preservation, additive extension,
   or breaking migration in the rebaseline register.
3. Freeze conformance scenarios before changing lexer, parser, or runtime.
4. Obtain separate phase approval for each implementation Issue in WP-0025.
