# QPex v1 language north star

| Field | Value |
|---|---|
| Status | North-star target; normative after LISS-0068 rebaseline (ADR 0106 **Accepted with conditions**, 2026-07-27) |
| Design horizon | Ideal final form under ADR 0095 |
| Existing conformance target | `qpex-language-specification.md` v0.1 |
| Architecture | ADR 0106 and `qpex-v1-compiler-blueprint.md` |
| Migration owner | LISS-0068 / WP-0025 |

This document answers what QPex should ultimately look like. It is deliberately
more ambitious than the currently shipping Python Kernel, but it preserves
QPex's defining laws:

- physical meaning shapes the source;
- quantum values do not become ordinary classical values by accident;
- measurement, approximation, mapping, and external execution are explicit;
- the compiler never repairs, truncates, normalizes, emulates, or reorders a
  program silently.

## 1. The language in one sentence

QPex is an executable notation for a physical theory, an experiment over that
theory, and an explicit plan for realizing the experiment on a simulator or a
quantum computer.

It is not:

- Python with quantum objects;
- a gate-list language;
- a provider SDK;
- a general-purpose classical language with a `qubit` primitive;
- a symbolic algebra package that stops before execution.

## 2. Source organization and phase law

### 2.1 Scientific phases

```qpex
theory IsingMatter {
    // Hilbert space, physical quantities, operators, laws
}

experiment CriticalResponse using IsingMatter {
    // concrete system, preparation, parameters, observations
}

workflow FieldSweep using CriticalResponse {
    // immutable Host feedback and termination contract
}

execution HeronStudy using FieldSweep {
    // target capabilities, shots, budgets, lowering policy
}

report CriticalReport from HeronStudy {
    // typed result projections
}
```

Declarations in these blocks are order-independent unless a construct is
explicitly ordered. Legal dependency direction is:

```text
report -> execution -> workflow -> experiment -> theory
```

Examples of illegal leakage:

```qpex
theory Bad {
    Hamiltonian<QubitRegister<4>> H =
        when shots > 1_000 { ... } // PHASE_SCOPE_DIRECTION_ERROR
}
```

```qpex
experiment Bad using IsingMatter {
    backend = "provider.device"     // execution concern in Experiment
}
```

### 2.2 Ordered regions

Mathematical operator products, state transformations, dynamic QPU protocols,
and explicit procedures retain source order. A resolver may reorder
declarations but not these regions.

## 3. Lexical and notation policy

### 3.1 Canonical UTF-8 mathematical source

QPex v1 source is UTF-8 and NFC-normalized. It supports a restricted
Unicode-identifier profile suitable for Greek symbols and subscripts while
diagnosing confusable public identifiers.

Canonical mathematical tokens include:

| Concept | Canonical source |
|---|---|
| Ket | `|ψ⟩`, `|0⟩`, `|2⟩` |
| Bra | `⟨ψ|` |
| Matrix element | `⟨φ|A|ψ⟩` |
| Adjoint | `A†` |
| Tensor product | `ψ ⊗ φ` |
| Pipeline | `ψ |> prepare |> evolve_for(t)` |
| Indexed operator | `Z[spin[i]]` |

The formatter emits one spelling. Editor input helpers may accept commands
such as `\ket`, `\bra`, `\dagger`, or `\otimes` and insert the canonical token;
those commands are editor behavior, not additional language syntax.

The closing Ket delimiter `⟩` makes named Kets lexically distinct from the
pipeline token `|>`.

### 3.2 Formula structure is preserved

`sum`, `product`, `tensor`, and `integral` are pure binders, not imperative
loops:

```qpex
Hamiltonian<QubitRegister<N>> H =
    -J * sum (i in Index<0..N-2>) {
        Z[spin[i]] * Z[spin[next(i)]]
    }
    -h * sum (i in Index<0..N-1>) {
        X[spin[i]]
    }
```

The compiler retains the binder, domain, constraints, order, source span, and
expansion provenance even when a finite target requires full expansion.

## 4. Physical and structural types

### 4.1 States and acting spaces

```qpex
State<Qubit>
State<Qutrit>
State<Qudit<12>>
State<QubitRegister<8>>
DensityState<QubitRegister<8>>
Operator<QubitRegister<8>>
Hamiltonian<QubitRegister<8>>
Channel<QubitRegister<8>, QubitRegister<8>>
POVM<QubitRegister<8>, SpinOutcome>
```

`State<S>` never promises a state-vector representation. A backend may use a
state vector, tensor network, stabilizer tableau, decision diagram, or physical
device while preserving the same type meaning.

`DensityState<S>` is distinct because mixed states obey channel algebra and
trace/positivity invariants rather than pure-state vector algebra.

### 4.2 Static degrees of freedom

```qpex
system Spectrometer {
    register probe    : QubitRegister<4>
    register readout  : QutritRegister<1>
    register resonator: QuditRegister<12, 1>
}
```

Register declarations specify physical degrees of freedom, not runtime
allocation calls. Declaration order fixes tensor order. Register identity is
preserved through logical QPU IR even when a target later assigns physical
wires.

### 4.3 Meaningful discrete carriers

```qpex
enum SpinOutcome { Down, Up }
enum Parity { Even, Odd }

basis EnergyLevel : Basis<16>
quantity MagneticField : Tesla
```

The following are deliberately distinct:

```text
Dimension       compile-time size
Index<N>        compile-time finite binder index
ShotCount       Host execution count
EnergyLevel<N>  physical finite value
Basis<N>        Hilbert basis label
Param<Angle>    symbolic circuit parameter
Controller<Bit> dynamic-QPU measurement result
```

No implicit conversion exists merely because several representations are
machine integers.

### 4.4 Symbolic parameters and Host inputs

```qpex
experiment RamseyScan using RamseyTheory {
    input detuning : Param<AngularFrequency>
    input duration : Param<Time>
    input pulse    : Dataset<Time, FieldAmplitude>
}
```

`Param<T>` survives to an executable artifact and is bound before execution.
`Dataset<K,V>` is an immutable typed Host input. A Source/Host adapter loads
CSV, HDF5, JSON, a database record, or an instrument stream into the same
validated contract; file and network APIs never enter Theory.

Every binding carries source identity, units, schema version, capture time
when available, and validation status.

## 5. State preparation

### 5.1 Qubits

```qpex
State<Qubit> ground = |0⟩
State<Qubit> excited = |1⟩
State<Qubit> plus = (|0⟩ + |1⟩) / sqrt(2)
State<Qubit> phased = (|0⟩ + cis(θ) * |1⟩) / sqrt(2)
```

Normalization is checked. `normalize(expr)` is available only as an explicit
mathematical operation:

```qpex
State<Qubit> prepared = normalize(α * |0⟩ + β * |1⟩)
```

The compiler never inserts `normalize` to repair invalid source.

### 5.2 Qutrits and qudits

```qpex
State<Qutrit> atom =
    normalize(α₀ * |0⟩ + α₁ * |1⟩ + α₂ * |2⟩)

State<Qudit<12>> cavity =
    normalize(sum (n in Basis<12>) {
        coefficient[n] * |n⟩
    })
```

Ket labels are checked against the local carrier dimension at compile time.

### 5.3 Tensor products

```qpex
State<(Qubit, Qutrit)> composite = plus ⊗ atom

State<QubitRegister<N>> vacuum_chain =
    tensor (i in Index<0..N-1>) { |0⟩ }
```

Tensor order is source order and is part of the type/provenance contract.

## 6. Operators, Dirac notation, and Hamiltonians

### 6.1 First-class algebra

```qpex
Operator<Qubit> Pψ = |ψ⟩⟨ψ|
Operator<Qubit> B = A†
Complex overlap = ⟨φ|ψ⟩
Complex matrix_element = ⟨φ|A|ψ⟩
Energy expected_energy = ⟨ψ|H|ψ⟩

Operator<S> comm = [A, B]
Operator<S> anti = {A, B}
```

The parser lowers these forms to typed algebra nodes. It does not evaluate
them as strings or macros.

### 6.2 Many-body Hamiltonian

```qpex
theory HeisenbergChain {
    meta N : Dimension
    parameter Jx : Energy
    parameter Jy : Energy
    parameter Jz : Energy

    system Chain {
        register spin : QubitRegister<N>
    }

    pub fn hamiltonian() -> Hamiltonian<RegisterSet<Chain>> {
        Hamiltonian<RegisterSet<Chain>> H =
            sum (i in Index<0..N-2>) {
                Jx * X[spin[i]] * X[spin[next(i)]]
              + Jy * Y[spin[i]] * Y[spin[next(i)]]
              + Jz * Z[spin[i]] * Z[spin[next(i)]]
            }
        return H
    }
}
```

Periodic topology is explicit:

```qpex
sum (i in Index<0..N-1>) {
    J * Z[spin[i]] * Z[spin[wrap(i + 1)]]
}
```

### 6.3 Second quantization

```qpex
FermionHamiltonian<Orbitals> Hf =
    sum (p in orbitals, q in orbitals) {
        h[p, q] * a[p]† * a[q]
    }
  + 0.5 * sum (
        p in orbitals,
        q in orbitals,
        r in orbitals,
        s in orbitals
    ) {
        g[p, q, r, s]
        * a[p]† * a[q]†
        * a[r] * a[s]
    }

Hamiltonian<QubitRegister<M>> Hq =
    map Hf using JordanWigner(order = orbitals)
```

Statistics, orbital order, mapping, tapering, and approximation provenance
are retained. A compiler never treats fermionic products as generic
commutative multiplication.

## 7. Functions, classes, interfaces, and pipelines

### 7.1 Pure functions

```qpex
pub fn rotate(
    ψ: State<Qubit>,
    θ: Param<Angle>
) -> State<Qubit> {
    State<Qubit> rotated = apply(RY(θ), ψ)
    return rotated
}
```

The result type and terminal `return` are explicit. `return` does not measure,
sample, print, or leave `State<T>`.

### 7.2 Physical systems and capability interfaces

```qpex
interface Evolvable<S> {
    fn advance(ψ: State<S>, dt: Time) -> State<S>
}

class Oscillator : System {
    val mass: Mass
    val frequency: AngularFrequency

    fn init(mass: Mass, frequency: AngularFrequency) {
        this.mass = mass
        this.frequency = frequency
    }
}

impl Evolvable<OscillatorSpace> for Oscillator {
    fn advance(
        ψ: State<OscillatorSpace>,
        dt: Time
    ) -> State<OscillatorSpace> {
        Hamiltonian<OscillatorSpace> H =
            P^2 / (2 * this.mass)
          + 0.5 * this.mass * this.frequency^2 * X^2
        return evolve ψ under H for dt
    }
}
```

`class` models a physical system, not mutable enterprise identity.
`impl Interface for Type` makes capability conformance explicit. There is no
inheritance or `protected`.

### 7.3 State-preserving pipeline

```qpex
State<Qubit> final =
    |0⟩
    |> apply(H)
    |> rotate(θ)
    |> apply(Z)
```

`lhs |> f(args...)` is left-associative function application with `lhs`
inserted as the first unbound argument. A pipeline cannot hide Measure, Host,
Snapshot, or other undeclared effects.

## 8. Closed-system evolution

### 8.1 Direct time evolution

```qpex
State<QubitRegister<N>> ψ1 =
    evolve ψ0 under H for 1.0.s
    using Suzuki(
        order = 2,
        steps = 8,
        term_order = Source
    )
```

Or derive a static step count from an explicit planning target:

```qpex
State<QubitRegister<N>> ψ2 =
    evolve ψ0 under H for 1.0.s
    using Suzuki(
        order = 2,
        tolerance = 1e-4,
        error = EmpiricalEstimate,
        term_order = Canonical
    )
```

`steps` and `tolerance` are mutually exclusive. `Source` preserves the
physicist's term order. `Canonical` uses the standard package's documented
deterministic ordering. A backend cannot substitute one for the other.

Future algorithms such as QDrift, higher-order Suzuki, LCU, qubitization, or
Krylov evolution implement a common evolution-planner contract rather than
adding unrelated syntax.

### 8.2 Schrödinger equation as a theory declaration

```qpex
theory WaveMechanics {
    equation Schrödinger(
        ψ: WaveFunction<Position>,
        H: Hamiltonian<Position>
    ) {
        i * ℏ * ∂ψ/∂t = H * ψ
    }
}
```

An equation is symbolic and is not automatically executable. A finite
execution requires an explicit bridge:

```qpex
discretization PositionGrid {
    domain = Position(range = [-10.0.m, 10.0.m])
    basis = FourierBasis
    resolution = 256
    boundary = Periodic
    approximation = Spectral
    error = Empirical(tolerance = 1e-8)
}

bridge WaveMechanics.Schrödinger
    using PositionGrid
    as FiniteWaveEvolution
```

## 9. Open-system evolution and noise

```qpex
DensityState<Qubit> ρ0 = DensityState(
    Ensemble([
        (0.7, |0⟩),
        (0.3, |1⟩)
    ])
)

JumpSet<Qubit> jumps = JumpSet([
    sqrt(γ) * annihilate
])

DensityState<Qubit> ρ1 =
    evolve ρ0
    under Lindblad(H, jumps)
    for 10.0.us
    using RK4(step = 0.01.us)
```

`RawMatrix` remains an explicit low-level/test input:

```qpex
DensityState<Qubit> ρ = DensityState(
    RawMatrix([
        [0.5, 0.0],
        [0.0, 0.5]
    ])
)
```

Trace-one, Hermiticity, positivity, channel completeness, and numerical defect
checks are hard contracts. No silent clipping or normalization occurs.

Noise models attached to a circuit execution are Execution declarations, while
Lindblad dynamics defined as physical theory remain Theory/Experiment
concepts. The compiler records which meaning is used.

## 10. Measurement

### 10.1 Static Kernel: terminal only

```qpex
pub fn main() -> Unit effects { Measure } {
    QubitRegister<3> phase = system()
    State<QubitRegister<3>> ψ = prepare_phase_state(phase)
    Operator<QubitRegister<3>> F_inv = iqft(phase)
    State<QubitRegister<3>> spectrum = apply(F_inv, ψ)

    measure spectrum in ComputationalBasis()
}
```

The Host receives a typed result envelope after execution. The source program
does not read the sampled value back, print it implicitly, or continue after
measurement.

General terminal measurements are typed:

```qpex
POVM<Qubit, PolarizationOutcome> analyzer =
    povm {
        Horizontal -> |H⟩⟨H|
        Vertical   -> |V⟩⟨V|
    }

measure photon with analyzer
```

Effects must be positive and complete on the measured acting space.

### 10.2 Dynamic QPU: explicit feedback controller

```qpex
dynamic qpu fn correct_bit_flip(
    data: State<QubitRegister<3>>,
    ancilla: State<QubitRegister<2>>
) -> State<QubitRegister<3>>
effects { Measure }
requires { MidCircuitMeasure, FeedForward, Reset } {
    Controller<Bit> s0 = measure ancilla[0] in Z
    Controller<Bit> s1 = measure ancilla[1] in Z

    State<QubitRegister<3>> corrected =
        match (s0, s1) {
            (0, 0) -> data
            (1, 0) -> apply(X[data[0]], data)
            (1, 1) -> apply(X[data[1]], data)
            (0, 1) -> apply(X[data[2]], data)
        }

    return corrected
}
```

`Controller<T>` is not a general classical value:

- it is created only by dynamic measurement;
- it is consumed only by finite control accepted by the target profile;
- it cannot be returned to Theory/Experiment code;
- it cannot determine register size or a mathematical binder domain;
- it may be included in completed execution metadata if the measurement plan
  explicitly requests it.

Unsupported hardware produces a capability error; Host-side emulation is not
substituted silently.

## 11. Failure and error handling

### 11.1 Kernel alternatives are physical branches

```qpex
enum DomainFailure { OutsideSupport, Singular }
enum Outcome<T, E> { Success(T), Failure(E) }

pub fn guarded_prepare(
    x: State<Position>
) -> State<Outcome<WavePacket, DomainFailure>> {
    State<Outcome<WavePacket, DomainFailure>> outcome =
        when valid(x) {
            true  -> Outcome.Success(prepare(x))
            false -> Outcome.Failure(DomainFailure.OutsideSupport)
        }
    return outcome
}
```

No exception unwinds a quantum evolution. Projection or terminal measurement
is required to select a branch.

### 11.2 Compiler errors are structured diagnostics

Diagnostics contain:

- stable code;
- primary source span;
- related spans;
- physical explanation;
- violated type/phase/effect invariant;
- suggested correction only when it preserves meaning;
- lowering/provenance path when the failure occurs after source analysis.

### 11.3 Host failures are Job outcomes

Submission, cancellation, timeout, provider rejection, and partial-result
policy belong to immutable Host result types. They are not QPex exceptions and
do not become quantum state.

## 12. Real-world data, workflow, and results

```qpex
experiment Spectroscopy using CavityQED {
    input pulse : Dataset<Time, FieldAmplitude>
    input detuning : Param<AngularFrequency>

    prepare initial = GroundState
    evolve initial under DrivenHamiltonian(pulse, detuning)
    observe transmission
}

workflow DetuningSweep using Spectroscopy {
    sweep detuning over LinearGrid(
        start = -20.0.MHz,
        stop = 20.0.MHz,
        points = 201
    )
    collect transmission
}

execution ReproducibleScan using DetuningSweep {
    target = capability("gate-model.dynamic")
    shots = 10_000
    seed = 42
    resource_policy = Abort
    result_policy = CompleteOnly
}

report Spectrum from ReproducibleScan {
    table frequency, transmission, uncertainty
    preserve input_provenance, lowering_provenance, target_snapshot
}
```

The source states scientific intent. Concrete provider identifiers,
credentials, queue polling, retry transport, files, and database connections
are Host adapter configuration.

## 13. Deployment model

The same resolved experiment may be:

```text
qpex check study.qpex
qpex inspect study.qpex --stage physics-ir
qpex simulate study.qpex --engine statevector
qpex simulate study.qpex --engine density-matrix --noise measured-noise.json
qpex build study.qpex --target openqasm3
qpex build study.qpex --target qir --profile adaptive
qpex submit study.qpex --execution ReproducibleScan
qpex result <job-id> --report Spectrum
```

These are Host commands. They do not change the QPex source semantics.

## 14. Debugging without accidental observation

Simulation supports explicit observation plans:

```qpex
inspect ψ at checkpoint "after-preparation"
```

`inspect`:

- is non-collapsing in simulators;
- records cost and representation limits;
- is rejected for a QPU target unless the execution plan provides an explicit
  additional experiment or supported non-destructive diagnostic;
- never becomes a hidden `measure`.

Compiler inspection exposes each IR and provenance edge. Hardware debugging
uses separate calibration/diagnostic jobs and completed result metadata, not
access to an unknowable mid-circuit wavefunction.

## 15. Core static invariants

1. No unknown quantum state is cloned.
2. No live quantum information is discarded implicitly.
3. Static register shapes are compile-time known.
4. Acting spaces and physical dimensions match.
5. Ordinary functions are pure unless effects are declared.
6. Static Kernel measurement is terminal.
7. Dynamic controller values remain in the dynamic control phase.
8. Approximation, discretization, mapping, routing, and mitigation provenance
   are explicit.
9. Unsupported capability is a hard diagnostic.
10. No implicit normalization, truncation, fallback, Host emulation, or target
    substitution is permitted.

## 16. v0.1 migration classification

| v0.1 surface | v1 target | Classification |
|---|---|---|
| `State<T>`, `DensityState<T>` | retained and generalized | preserve |
| `QubitRegister<N>` | retained | preserve |
| `pub fn`, `->`, `return` | retained | preserve |
| `impl Interface for Type` | retained | preserve |
| `\|>` | retained | preserve |
| `evolve ... using Suzuki(...)` | retained under common planner | preserve |
| `dynamic qpu { ... }` rejection boundary | typed `dynamic qpu fn` | additive + migration |
| reserved ASCII Kets | canonical Unicode Dirac notation | breaking migration |
| `*|*` | `⊗` | breaking migration |
| function-shaped public Dirac algebra | canonical notation lowering to the same core nodes | breaking surface, preserved semantics |
| v0.1 phase contracts | body-level phase typing | additive |
| one-qubit POVM/Lindblad boundaries | general typed forms | additive |
| Python internal dict projections | typed multi-level IR | implementation migration |

No compatibility alias is promised for a breaking surface. LISS-0068 must
produce a source migrator and a versioned conformance corpus before removal.
