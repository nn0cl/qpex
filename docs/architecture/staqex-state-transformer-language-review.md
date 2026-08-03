# Staqex state-transformer language review

| Field | Value |
|---|---|
| Status | **Accepted as project direction** (Adjudicator, 2026-08-03) — implementation and normative spec changes remain separately gated |
| Date | 2026-08-03 |
| Scope | Review of the shipping Python Kernel and a candidate next language model |
| Parent law | [Adjudicator language vision](adjudicator-language-vision.md), [language axioms](staqex-language-axioms.md), [physicist minimal dialect](physicist-minimal-dialect.md) |
| Verification baseline | `python3 tests/spec_verification/run_all.py` — 161/161 passed |

```markdown
[DESIGN CHECK]
- Scope and expected behavior: review the current Staqex Kernel and propose a
  physicist-first state-transformer model that keeps all pure amplitudes/worlds
  in play, removes JVM-era ceremony from the experiment surface, and makes
  coherent control, probabilistic branching, observation, and Host orchestration
  distinct.
- Specifications and files inspected: AGENTS.md; agent quickstart and readiness;
  language vision; axioms; normative language specification; runtime evaluator,
  Joint store, typechecker, representative B01/B02/B04/B08/A11 programs;
  minimal dialect and destructive simplification sketch.
- Component boundaries, ports, and VO/DTO candidates: Experiment Kernel owns
  State/Operator/Transform/Observable; Host owns Job, parameters, I/O, and
  classical orchestration; RngPort and MeasureSinkPort remain ports. Candidate
  IR values are State, Transform, ObservationPlan, and MeasurementEnvelope.
- Applicable constraints: Never Leave the State; `when` not `if` in Static
  Kernel; no hidden measurement; writeable is not executable; no business logic
  in adapters; no new syntax or semantics is accepted by this note.
- Decisions, assumptions, and unresolved ambiguities: this note treats
  `when` as probabilistic/classification branching, not as a general coherent
  quantum conditional. Whether to add a dedicated coherent-control spelling,
  and whether to make ownership/effects surface-visible, require Architecture
  approval.
- Included and omitted AI context: included source-level semantics and public
  research references; omitted unrelated Host/provider implementation details,
  private data, and hidden reasoning.
- Task routing: deterministic repository inspection plus primary documentation
  and research-paper review.
- Input/output evidence contract: findings cite repository paths and stable
  external sources; proposals are marked Proposed and are not treated as facts.
- Verification plan: preserve the current SV corpus; add differential tests for
  coherent control vs mixture, adjoint/controlled capabilities, state ownership,
  and terminal observation before any implementation phase.
```

## 1. Review result

The current implementation is a healthy, passing v1 baseline, but its public
idea and its internal evaluator are no longer the same abstraction. The next
step should not be another collection of syntax additions. It should be a
small state-transformer calculus with explicit semantic categories.

### What is already correct

- `if`, `while`, and bare `for` are rejected in the Static Kernel.
- `when`, `evolve`, terminal `measure`, `inspect`, `Joint`, amplitude merging,
  partial trace, and fail-closed target diagnostics are present.
- Hamiltonian and circuit work have named lanes, and Host orchestration is
  already separated from the experiment body.
- The minimal dialect and destructive-simplification documents correctly
  demote `inspect` floods, ritual sibling kills, DTO-style `class`, and
  coverage-driven source shape.

### Main semantic gaps

1. **The “all values are Joint” law is only partially true in the evaluator.**
   `compiler/staqex/runtime/evaluator.py` keeps `self.scalars`, `self.objects`,
   and Joint coordinates as separate stores. This is practical for the current
   feature set, but it means the same source-level binding can have three
   different runtime meanings. The next model should make the distinction
   explicit in types rather than implicit in evaluator branches.

2. **`when` is not a general quantum conditional.**
   `_bind_when` selects an arm per world and scales amplitudes by a square root
   of a control mass. That is suitable for a probabilistic mixture such as
   `coin()`, but a coherent control requires a controlled linear operator that
   preserves relative phase and reversibility. The surface must not imply that
   a classical arm selector and a coherent controlled operation are identical.

3. **Rebinding looks mutable even though the meaning is functional.**
   `state psi = evolve psi ...` is readable, but it hides a consume-and-replace
   rule. The language should make state transformation the primary expression,
   with rebinding retained only as a compatibility spelling. A future checker
   should reject use of an old state after a consuming transform unless the
   operation explicitly preserves it.

4. **The evaluator contains compatibility and optimization policy in the same
   path as denotation.**
   Deferred pushforward, interprocedural tracing, fusion, scalar elaboration,
   class execution, and measurement are interleaved in the large evaluator.
   These are valid implementation techniques, but they should lower from one
   semantic IR and be proven denotationally equivalent. Optimization must not
   decide what a physicist's source means.

5. **`trace_out` and uncompute are related but not interchangeable.**
   `Joint.trace_out` intentionally removes coherence by Born-summing the
   discarded coordinate. Reversible uncomputation restores an ancilla before
   disposal. The language should use separate words and effect/capability
   checks for `uncompute` and `trace_out`/discard.

6. **The surface still has a few Java/Kotlin-shaped escape hatches.**
   `class`, `fn init`, mutable members, broad Type-First bindings, and DTO-like
   object paths are useful compatibility features, but they should not define
   the experiment dialect. `struct`/`enum` and operator/transform declarations
   should be the default teaching surface; `class` belongs to a physical system
   that genuinely owns setup and evolution, or to Host/library code.

## 2. Candidate next model: State Transformer Calculus

This is a proposal for the next design review, not a ship decision.

### Semantic categories

| Category | Meaning | May collapse? | Typical operations |
|---|---|---:|---|
| `State<A>` | Joint amplitude state over a typed carrier | No | prepare, tensor, apply, evolve |
| `Transform<A,B>` | Pure linear/unitary/channel transformation | No | compose, control, adjoint, evolve |
| `Observable<A>` | Non-collapsing question about a state | No | expect, inspect as Host view |
| `Outcome<A>` | Terminal classical result | Yes | measure only |
| `Host<T>` | Outer orchestration and I/O value | Not in Kernel | sweep, submit, report |

The central rule is: a Kernel expression is either a state or a transformer
over states. A classical computation may calculate parameters for a transformer,
but it may not silently become a state control path.

### Control taxonomy

The language should distinguish three cases instead of overloading `when`:

```text
// probabilistic / classified state: all weighted arms remain in the Joint
state result = when phase {
  Ground -> prepare(|0>)
  Excited -> prepare(|1>)
}

// coherent quantum control: a linear controlled operator, no readout
state target = controlled(control, rotate(angle), target)

// terminal classical feed-forward: only in the explicitly named Dynamic QPU lane
dynamic qpu fn correct(measured: Controller<Bit>, target: Qubit) -> Unit { ... }
```

The first form is a mixture/classification construct. The second is the
quantum analogue of “apply the operation to every amplitude branch.” The third
is real-time classical control after a mid-circuit measurement and must remain
capability-gated. No form should be spelled `if` inside the Static Kernel.

### Ideal experiment shape

The preferred new-program trial should read as an equation graph, not as an
object lifecycle:

```text
theory Ising {
  params J: Energy, h: Energy
  operator H(J, h) = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
}

experiment IsingRun(J = 1.0, h = 0.5) {
  state ψ = |+> *|* |+>
  ψ |> evolve under Ising.H(J, h) for 0.7
  observable zz = expect(ZZ, ψ)
  measure ψ tracing_out all_else
}
```

This is intentionally an ideal trial model. Until the syntax is accepted,
the shipping-compatible spelling remains the current `pub fn main`, Type-First
bindings, `state (a, b) = evolve ...`, and terminal `measure` form. The trial
model removes `new`, getters/setters, mandatory constructors, mutable trackers,
and ceremony-only classes from the physicist-facing path; it does not delete
the existing compatibility surface in this proposal.

### Proposed operation characteristics

Borrow a proven idea without copying JVM or SDK surface syntax:

```text
fn energy(ψ: State<Spin>) -> Observable<Energy>      // pure question
transform rotate(a: Angle) -> Transform<Qubit,Qubit>  // composable
transform step(...) -> Transform<System,System>       // candidate: Adj + Ctl
```

The eventual characteristic set should be extensible and inferred where
possible: `Pure`, `Unitary`, `Adj`, `Ctl`, `Channel`, `Observe`, and `Host` are
better semantic evidence than a method/class hierarchy. `Adj` and `Ctl` are
especially useful because they expose whether an operation can be reversed or
coherently controlled. This direction is consistent with Q#'s separation of
deterministic functions from state-changing operations and its `Adj`/`Ctl`
operation characteristics, but Staqex should keep the physicist-facing
state/operator vocabulary.

## 3. Project policy candidate

Adopt the following as a proposed project rule after Architecture review:

> Staqex experiment programs are state-transformer graphs. The Static Kernel
> never branches by classical short-circuiting, never collapses mid-program,
> and never hides a classical value-to-state conversion. Probabilistic
> classification, coherent control, and post-measurement feed-forward are
> three different semantics and three different named surfaces. The shortest
> acceptable source is the one that preserves the physicist's equation, not
> the one that resembles Java/Kotlin or a backend circuit API.

The Adjudicator accepted this direction as project policy on 2026-08-03.
This approval authorizes design work and comparative evaluation, not compiler
implementation or automatic revision of the normative v1 specification.
Those remain separately gated after the following are designed:

- `when` mixture semantics versus a new coherent-control form;
- state consumption/rebinding and aliasing rules;
- `uncompute` versus `trace_out`/discard;
- operation characteristics/effects and their diagnostic contract;
- the role of `theory`/`experiment` as additive syntax versus a v2 surface;
- compatibility and migration policy for `class`, `fn init`, and `state`.

## 3.1 Acceptance record

- [x] State-transformer graph as the next language direction
- [x] Static Kernel separation of mixture, coherent control, and dynamic
      feed-forward
- [x] Physicist-first equation preservation over Java/Kotlin resemblance
- [x] Design exploration authorized; implementation not authorized by this
      record
- [ ] Normative v1 specification amendment — future Architecture review

## 4. Research cross-check

The proposal follows current ecosystem signals without making them normative:

- Q# separates deterministic functions from quantum operations and exposes
  `Adj`/`Ctl` characteristics, which supports making reversibility and coherent
  control visible in types rather than guessing from names.
- OpenQASM 3 treats classical feed-forward, timing, and pulse descriptions as
  an intermediate representation for hardware, and explicitly permits target
  implementations to reject unsupported real-time features. This supports
  Staqex's writeable-versus-executable and named-lane boundary.
- IBM's current dynamic-circuit documentation treats mid-circuit measurement
  plus classical control as a distinct execution mode, with target limitations.
- Recent work on modular uncomputation reinforces that ancilla lifetime and
  reversible cleanup are language/compiler concerns, not merely optimizer
  trivia.
- QBLUE's 2025 proposal is a useful signal for typed, second-quantized,
  Hamiltonian-first simulation surfaces, which aligns with Staqex's physicist
  audience but does not replace Staqex's accepted axioms.

## 5. Safe next phase

Do not change the compiler from this note. The next approved work should be a
small Architecture/Feature package with:

1. a semantic decision table for mixture, coherent control, channel, and
   dynamic feed-forward;
2. five Red fixtures that distinguish those meanings;
3. an ownership/uncompute acceptance specification;
4. an additive trial parser or AST fixture only after the specification is
   accepted;
5. a migration matrix that preserves the current 161 SV cases.

The current implementation remains the shipping baseline until that package
is accepted and phased.
