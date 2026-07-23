# QPex Quantum Observatory capstone — acceptance specification

Status: **Proposed**, for LISS-0020. This document is an observable contract,
not implementation authorization.

## 1. Product intent

The capstone is a coherent modular program family for two audiences:

- **Student path:** follow a measurement-free state from preparation through
  evolution, projection, inspection, and terminal measurement.
- **Theoretical-physicist path:** read subsystems as Hilbert/joint factors,
  compare Hamiltonian and walk models, and inspect interference, symmetry,
  topology, and entanglement without syntax that hides physical assumptions.

Theme: a Quantum Observatory compares a topological chain, an interferometer,
a discrete-time quantum walk, a bounded search, and an entangled deep-space
link. All are educational toys with explicit honesty tables.

## 2. Module graph

The proposed folder is `examples/16_quantum_observatory/`:

```text
main_observatory.qpex
README.md
domain/
  observatory_config.qpex
  topology.qpex
  link_parties.qpex
operators/
  ssh_hamiltonian.qpex
  interferometer.qpex
  walk_step.qpex
  search_oracle.qpex
  bell_channel.qpex
qpu/
  portable_observatory_link.qpex
```

The exact names may change during design review, but the module boundaries
must remain visible in source and package-qualified imports.

## 3. Observable scenarios (Gherkin-style)

### Scenario A — source remains a joint state until terminal observation

Given the main observatory program prepares multiple State coordinates
When it applies `when`, `map`, `phase`, `evolve`, `project`, or `interfer`
Then no RNG call or mid-program collapse occurs
And terminal `measure` is the only sampling boundary.

### Scenario B — module boundaries read as physical subsystems

Given domain and operator modules have package-qualified names
When the entry module imports and composes them
Then names remain unambiguous and the linked program preserves intended joint
coordinates.

### Scenario C — the topological observatory uses structured DX

Given `namespace`, `enum`, `struct`, and immutable `class` definitions
When `fun init`, `this`, `pub`, and `_` are used in the domain model
Then public configuration is readable and private implementation state cannot
be mistaken for a physical observable.

### Scenario D — continuous and discrete physics coexist honestly

Given an SSH/sparse-Pauli Hamiltonian, a DTQW, and a position-grid or Fock toy
When the CPU target evaluates them
Then the example reports each model's representation and limitations
And no Fock/grid result is silently described as a hardware circuit.

### Scenario E — the QPU lane is portable

Given the qubit-only Bell/search/link module
When it is compiled for `qpu:openqasm3`
Then compilation emits valid OpenQASM 3 without provider SDK imports
And the same source can run on the CPU target.

### Scenario F — failure remains a world-line

Given a deliberately invalid or rejected branch in the teaching narrative
When the program evaluates the branch
Then it uses `Result`/`Error` or `vacuum`/`project` semantics
And it does not use exceptions, `if`, early `measure`, or hidden adapter policy.

### Scenario G — inspection is non-destructive

Given an intermediate observable or joint
When `expect`, `inspect`, or `snapshot` is used
Then the program remains semantically uncollapsed
And host output is clearly labeled as diagnostic or boundary output.

## 4. Coverage matrix contract

The final README must contain a row for every shipped surface in the following
families: state/lift and Result/Vacuum; `when` and joint operations; phase and
interference; `evolve` forms; Type-First dimensions; packages/imports and
visibility; namespace/enum/struct/class/init/this; unitary gates and control
polarity; Hamiltonian/Fock/grid/sparse-Pauli paths; diagnostics and terminal
measurement; OpenQASM emission. Each row names a source file and a deterministic
verification command or SV case.

The matrix must also list these as **not used because deferred**: real QFT/IQFT,
density matrix/Lindblad, `until`, `|>`/currying, Trait `impl`, effect marking,
cloud submit, higher-order Suzuki, and bare Operator `H` sugar.

## 5. Definition of done for the example

- All files compile with the shipping Kernel.
- CPU scenarios run with a fixed seed and produce documented observables.
- QPU lane emits OpenQASM 3 and passes existing backend checks.
- No README or source claims exceed the implemented Kernel surface.
- Full SV suite and new capstone tests pass.
- A reviewer can read the source top-to-bottom and identify the physical
  meaning of every module, state coordinate, operator, and measurement.
