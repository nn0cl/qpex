# 16 — Quantum Observatory

The Quantum Observatory is a single teaching narrative with several physical
instruments: a topological chain, an interferometer, a walk, a search oracle,
and an entangled deep-space link. Every instrument is a small module so the
reader can move between the physics story and the language boundary.

The current Green slice proves the module graph, the CPU entry, the
portable QPU lane, and the CPU-only continuous-model diagnostics. It is
deliberately honest about the remaining coverage: deferred features are listed
as deferred, and each carrier-specific model stays in the lane that can
actually execute it.

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
| `class`, `fun init`, `this`, `pub`, `_` | `domain/observatory_config.qpex` | used |
| `fun (...) -> Type` and terminal result expression | `domain/observatory_config.qpex` | used; measure-free method result |
| Type-First `State<T>` / dimensions | `main_observatory.qpex` | used |
| `evolve under H for t` | `operators/ssh_hamiltonian.qpex` | used |
| Bell / controlled unitary | `qpu/portable_observatory_link.qpex` | used |
| OpenQASM 3 | `qpu/portable_observatory_link.qpex` | used |
| `when`, `map`, `project`, `interfer`, Grover, DTQW | `main_observatory.qpex` + `operators/` | used |
| Fock, position-grid, and sparse-Pauli CPU models | oscillator/Ising examples reused by the observatory study | CPU-only |
| `trace_out` and `snapshot` | `main_observatory.qpex` CPU diagnostics | used / CPU-only |
| QFT/IQFT, density/Lindblad, `until`, `|>`/currying, Trait `impl` | open-work register | deferred; not claimed |
| effect marking, cloud submit, higher-order Suzuki, bare `H` | open-work register | deferred; not claimed |

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

The topological chain and observatory are educational finite-system toys. The
deep-space link is an entanglement intuition example, not BB84/E91 security or
a real communications system. The CPU story is authoritative; the QPU lane is
the qubit-only Bell slice that emits vendor-neutral OpenQASM 3.

`Run.advance()` is the function-signature example: it returns `State<Float>`
through its final expression, while `main` remains responsible for the single
terminal observation.

For the CPU-only continuous models, the observatory study reuses the established
references `examples/05_harmonic_oscillator/quantum_oscillator.qpex`,
`examples/05_harmonic_oscillator/grid_oscillator.qpex`, and
`examples/06_statistical_physics/quantum_ising_4.qpex`.
