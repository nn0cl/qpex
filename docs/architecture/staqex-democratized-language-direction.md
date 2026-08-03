# Staqex language direction for quantum-computing democratization

| Field | Value |
|---|---|
| Status | **Design direction** — accepted for exploration 2026-08-03; not a normative v2 specification |
| Parent | [State-transformer language review](staqex-state-transformer-language-review.md) |
| Audience | Physicists, engineers, educators, and new quantum-computing users |
| Decision question | What should make Staqex materially easier to learn and more faithful to quantum physics? |

## 1. Executive direction

The main differentiator should not be “every value is automatically quantum.”
That is useful as an implementation and teaching principle, but it is not by
itself a new programming model. Automatic lifting can also make it difficult
for a beginner to tell whether a value is a parameter, an observable, a state,
or a terminal classical result.

The stronger direction is:

> Staqex lets a user write a physical theory, an initial state, an experiment,
> and an observation plan in the same order as a research notebook, then makes
> the simulator/QPU realization explicit and honest.

The primary innovation candidate is therefore **H-first scientific authoring**:
Hamiltonians, operators, constraints, dimensions, basis choices, preparation,
evolution, and observables are first-class language concepts. “Quantization” is
the semantic bridge that turns a classical model into operators and states; it
should not be a magical replacement for understanding the model.

## 2. Design axes

| Axis | Benefit | Risk | Direction |
|---|---|---|---|
| Automatic quantization | Removes boilerplate and exposes quantum behavior early | Hides what is classical, quantum, measured, or merely a parameter | Use explicit named bridges; do not make all numerics implicitly quantum everywhere |
| H/operator authoring | Matches physicists' primary abstraction and supports analog, digital, and simulator targets | Requires careful units, domains, basis, Hermiticity, and discretization diagnostics | **Primary differentiator** |
| State-transformer calculus | Makes “apply to the whole state” precise and composable | Similar ideas exist in functional and quantum languages | **Semantic foundation** |
| No Static Kernel `if` | Prevents accidental collapse/short-circuit narratives | Cannot cover real-time feed-forward alone | Keep in Static Kernel; provide a named Dynamic QPU lane |
| Automatic uncompute | Reduces ancilla ceremony | Can be unsafe when values are entangled or measured | Make lifetime and reversibility explicit in types/effects |
| Circuit generation | Gives users a route to hardware | Can pull the surface back toward gate tourism | Backend projection only; do not make gates the source language |
| Notebook-like surface | Lowers adoption barrier | Can become loose or underspecified | Combine readable surface with strict typed diagnostics |

## 3. What “quantization” should mean in Staqex

The word has at least three different meanings and they must not be conflated.

### 3.1 Literal lifting

```text
1.0 -> State<Float> concentrated at 1.0
```

This is convenient runtime sugar. It is not the central research contribution.

### 3.2 Model quantization

```text
classical coordinate x
    -> Hilbert space basis |x_i>
    -> operator X
    -> discretized Hamiltonian H(X, P)
```

This is scientifically meaningful. It requires an explicit domain, basis,
boundary condition, grid or truncation, error policy, and provenance. Staqex
should expose this as a named bridge such as `finiteize` or `quantize` rather
than silently inventing a grid.

### 3.3 State-space quantization

```text
classical probability / parameter
    -> quantum register or amplitude state
```

This is useful for algorithms, but it is not always canonical. A probability
distribution, a coherent amplitude encoding, and a parameter sweep are
different objects. The language should ask for the intended encoding when the
choice affects physics or resource cost.

**Policy:** automatic literal lifting may remain. Model and state-space
quantization must be explicit, typed, and diagnosable.

## 4. H-first authoring model

The ideal authoring sequence should be:

```text
theory        // symbols, units, domains, operators, laws
model         // Hamiltonian, channels, constraints, symmetries
prepare       // initial state and basis
evolve        // state transformer or time evolution
observe       // expectation / correlation / spectrum plan
measure       // terminal classical result
realize       // simulator/QPU target and capability profile
```

`theory`, `model`, and `realize` are candidate names, not accepted grammar.
The important property is that target hardware appears after the physical
meaning, not before it.

### 4.1 Ideal trial program

```text
theory Ising {
  coordinate site: Lattice<2>
  parameter J: Energy
  parameter h: Energy

  operator H(J, h) =
      -J * sum(site.neighbor(i, j), Z[i] * Z[j])
      -h * sum(site, X[i])
}

experiment quench(J = 1.0, h = 0.5) {
  state ψ = prepare plus over Ising.site
  ψ |> evolve under Ising.H(J, h) for 0.7

  observable energy = expect(Ising.H(J, h), ψ)
  observable correlation = expect(Z[0] * Z[1], ψ)

  measure ψ
}
```

The intended reading is almost identical to a physics notebook. `sum` is a
theory-level indexed construction, not a classical runtime loop. The compiler
may lower it to a sparse Pauli operator, a matrix, a tensor network, or QPU
instructions, subject to an explicit capability profile.

### 4.2 Shipping-compatible trial

Until the ideal syntax is accepted, the current language can express the same
idea without pretending that the new surface already exists:

```text
pub fn main() -> Unit {
    Energy J = 1.0
    Energy h = 0.5
    Operator H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
    state psi = |+>
    state psi = evolve psi under H for 0.7
    state energy = expect(H, psi)
    measure psi
}
```

The gap between these forms is a design target, not permission to add syntax
without an acceptance specification.

## 5. Democratization principles

### 5.1 Progressive disclosure

The first program should need only preparation, an operator, evolution, an
observable, and measurement. Advanced users can add dimensions, channels,
discretization, resource profiles, lanes, and target capabilities without
rewriting the physical core.

### 5.2 One concept, one reading

- `State` means a state, not a mutable object or a sampled scalar.
- `Operator` means a physical operator, not a generic service object.
- `Transform` means an operation on states.
- `Observable` means a non-collapsing question.
- `Outcome` means a classical result after `measure`.
- `Host` means orchestration outside the physical model.

### 5.3 Helpful failure

Diagnostics should answer physics questions:

- Is `H` Hermitian?
- Are the units compatible?
- Is the state basis compatible with the operator?
- Was discretization or truncation requested explicitly?
- Is the transform unitary, a channel, or measurement-bearing?
- Can the chosen target realize this model?

“Unsupported gate” is a backend fact; “Hamiltonian is not Hermitian” is a
theory error. They should not be reported as the same kind of failure.

### 5.4 Preserve the equation, expose the cost

The author writes the physical model in its natural form. The compiler reports
dimension, qubit, depth, truncation, approximation, and target costs. It does
not rewrite the source into Java/Kotlin ceremony or a gate list merely because
the backend prefers that representation.

## 6. Candidate language mechanisms

### 6.1 Indexed theory algebra

Provide declarative constructors for `sum`, `product`, lattice adjacency,
boundary conditions, and symmetry sectors. These elaborate at compile time or
to a symbolic Operator IR. They are not ordinary `for` loops in the Static
Kernel.

### 6.2 Explicit quantization bridges

Candidate forms:

```text
operator X = quantize coordinate x on basis position_grid
operator H = finiteize classical(H_classical)
state ψ = encode distribution ρ as amplitudes by amplitude_encoding
```

Every bridge must record its basis, domain, approximation, and provenance.

### 6.3 Transform capabilities

Candidate inferred characteristics:

```text
Transform<S,S> is Pure + Unitary + Adj + Ctl
Transform<S,S> is Channel
Observable<S,A> is Observe
```

This allows the compiler to reject an invalid `adjoint`, uncontrolled
measurement-bearing transform, or impossible coherent control before lowering.

### 6.4 Named control semantics

```text
when label { ... }                    // probabilistic/classified state
controlled(control, transform, ψ)     // coherent control
dynamic qpu ...                       // measured classical feed-forward
```

The three forms must never be silently interchangeable.

## 7. Direction choice

For the next design cycle, adopt this priority order:

1. **H/operator authoring** as the main user-visible differentiator.
2. **Explicit quantization bridges** as the scientific bridge from models to
   quantum representations.
3. **State-transformer semantics** as the common execution foundation.
4. **Capability/effect diagnostics** as the trust mechanism for democratization.
5. **Circuit lowering** as a backend projection, not the language's identity.

This gives Staqex a clearer identity than “a language where values are
quantized.” The promise becomes: “write the physical model naturally; the
language preserves its meaning while exposing the quantum realization.”

## 8. Design questions for the next review

1. Is `quantize` the right word for model-to-Hilbert-space conversion, or should
   the language use more precise forms such as `finiteize`, `encode`, and
   `represent`?
2. Should `theory` / `model` / `experiment` be additive v1 syntax or a v2
   surface?
3. Which indexed operator forms are essential for the first H-authoring slice?
4. What is the minimal type/effect set for `Unitary`, `Channel`, `Adj`, `Ctl`,
   and `Observe`?
5. Which quantization choices must be explicit because they affect scientific
   validity or resource estimates?
6. Can a single source preserve both Hamiltonian and circuit lanes without
   making either one the default representation?

## 9. Recommended next artifact

The next approved design package should be a small acceptance specification
for **H-authoring slice H1**:

- indexed Pauli/operator sums;
- typed parameters and units;
- explicit basis/domain declaration;
- Hermiticity and dimensional diagnostics;
- `prepare → evolve under H → expect → measure`;
- symbolic/operator IR evidence;
- one simulator realization and one fail-closed target profile.

No new `quantize` keyword should be implemented until its scientific meaning,
provenance record, and distinction from amplitude encoding are accepted.
