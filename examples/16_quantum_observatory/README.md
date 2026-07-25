# 16 — Quantum Observatory

The Quantum Observatory is a single teaching narrative about a satellite that
measures a molecule's spectrum while its detector is exposed to an open-system
environment. It combines a topological chain, an interferometer, a walk, a
search oracle, an entangled deep-space link, static QFT/IQFT registers, and a
Lindblad detector model. Every instrument remains a small module, while the
main entry point deliberately gathers the approved surface in one readable
source.

The current Green slice proves the module graph, the CPU entry, the portable
QPU lane, the static/QPU lowering declarations, and the CPU-only continuous-
model diagnostics. Deferred features remain explicitly marked, and each
carrier-specific model stays in the lane that can actually execute it.

## Two reading paths

- **Student:** start at `main_observatory.qpex`, follow `Config` into the SSH
  state, then compare the CPU path with the two-qubit QPU link.
- **Theoretical physicist:** read `domain/` as subsystem descriptors and
  `operators/` as the boundary between a physical model and a state
  transformer. The source names the carrier, Hamiltonian, phase, correlation,
  and terminal observable explicitly.

## Run

```bash
python3 -m compiler.qpex check examples/16_quantum_observatory/main_observatory.qpex
python3 -m compiler.qpex run examples/16_quantum_observatory/main_observatory.qpex --seed 0
python3 -m compiler.qpex emit-qasm examples/16_quantum_observatory/qpu/portable_observatory_link.qpex

# Host-side Job boundary over the same QPex entry point
python3 examples/16_quantum_observatory/run_as_job.py
```

`run_as_job.py` is intentionally Python, not QPex: `Job` and `JobResult` belong
to the Host boundary. The source program still ends at terminal `measure`; the
host submits it, waits for completion, and consumes the opaque result. The
local adapter completes immediately, while a future simulator service or QPU
adapter may remain queued or running.

## Coverage matrix

| Surface | Module / role | Status |
|---|---|---|
| `package` / `import` | all domain/operator modules | used |
| `namespace`, `enum`, `struct` | `domain/topology.qpex` | used |
| `class`, `fn init`, `this`, `pub`, `_` | `domain/observatory_config.qpex` | used |
| `interface`, marker `System`, generic `impl Interface for Type` | `main_observatory.qpex` | used |
| `fn (...) -> Type` and terminal result expression | `domain/observatory_config.qpex` | used; measure-free method result |
| `|>` state pipeline | `main_observatory.qpex` | used; pure function application |
| Type-First `State<T>` / dimensions | `main_observatory.qpex` | used |
| `QubitRegister<N>` / `Param<Angle>` | `main_observatory.qpex` + `qpu/portable_observatory_link.qpex` | used; static/QPU lane |
| `evolve under H for t` | `operators/ssh_hamiltonian.qpex` | used |
| Suzuki S2 with `steps` and `tolerance` policies | `main_observatory.qpex` | used; static lowering contract |
| `qft` / `iqft` over a static register | `main_observatory.qpex` + `qpu/portable_observatory_link.qpex` | used; static/QPU lane |
| `DensityState`, `JumpSet([RawMatrix(...)])`, Lindblad | `main_observatory.qpex` | used; CPU/simulator lane |
| Bell / controlled unitary | `qpu/portable_observatory_link.qpex` | used |
| OpenQASM 3 | `qpu/portable_observatory_link.qpex` | used |
| `when`, `map`, `project`, `interfer`, Grover, DTQW | `main_observatory.qpex` + `operators/` | used |
| Fock, position-grid, and sparse-Pauli CPU models | oscillator/Ising examples reused by the observatory study | CPU-only |
| `trace_out` and `snapshot` | `main_observatory.qpex` CPU diagnostics | used / CPU-only |
| `until` / currying / effect marking | open-work register | deferred; not claimed |
| provider SDK, cloud submit, higher-order Suzuki, bare `H` | open-work register | deferred; not claimed |

The row marked `CPU-only` deliberately does not enter the OpenQASM lane. Run
the isolated continuous-model lane with:

```bash
python3 -m compiler.qpex run examples/16_quantum_observatory/cpu/continuous_models.qpex --seed 0
```

### Carrier boundary

The example keeps one physical carrier per executable lane. This is a
semantic boundary, not a missing import:

| Carrier | Entry point | What it demonstrates |
|---|---|---|
| finite qubit/position composition | `main_observatory.qpex` | SSH transport, interferometry, walk, search, controls, Bell witness |
| static register/QFT and Suzuki policy | `main_observatory.qpex` | compile-time/QPU IR contract; no dynamic register sizing |
| density matrix/Lindblad detector | `main_observatory.qpex` | CPU/simulator numerical lane |
| Fock number basis | `cpu/continuous_models.qpex` | `N`, oscillator evolution, inspection |
| position grid | `cpu/continuous_models.qpex` | `wavepacket`, `X`/`P`, grid evolution, snapshot |
| sparse Pauli register | `cpu/continuous_models.qpex` | sparse Ising-like Hamiltonian evolution |
| reduced subsystem diagnostic | both CPU entries | `trace_out` before terminal observation |

The continuous lane is intentionally a separate CPU entry because the current
Kernel does not combine Fock/grid carriers with the mixed qubit/position
carrier in one state. The split keeps the source executable and makes the
backend limitation visible to the reader.

The
DTQW step is called through `operators/walk_step.qpex`, keeping the main
narrative focused on composition rather than gate plumbing.

## Honesty table

The topological chain, molecular spectrum, and observatory are educational
finite-system toys. The deep-space link is an entanglement intuition example,
not BB84/E91 security or a real communications system. The Lindblad detector
is a finite CPU/simulator calculation, not a claim about a physical sensor.
The QPU lane is provider-neutral and remains limited to the accepted static
register and basic-gate boundary.

`Run.advance()` is the function-signature example: it explicitly returns
`State<Float>` through a terminal `return`, while `main` remains responsible
for the single terminal observation.

For the CPU-only continuous models, the observatory study reuses the established
references `examples/05_harmonic_oscillator/quantum_oscillator.qpex`,
`examples/05_harmonic_oscillator/grid_oscillator.qpex`, and
`examples/06_statistical_physics/quantum_ising_4.qpex`.
