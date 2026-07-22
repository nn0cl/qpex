# QPex Official Examples

Physics-oriented sample programs for **QPex（キューペックス）**.

Axiom: **Never Leave the State** — every mid-program value is `State<T>`;
collapse happens only at terminal `measure`.

## Layout

| Dir | Topic |
|-----|--------|
| [`01_classical_mechanics`](01_classical_mechanics/) | Phase-space ensemble / Euler pushforward |
| [`02_quantum_basics`](02_quantum_basics/) | Double-slit path superposition + `interfer` |
| [`03_quantum_information`](03_quantum_information/) | Bell / EPR correlation & CHSH-style project |
| [`04_quantum_algorithms`](04_quantum_algorithms/) | Grover-style amplitude (mass) amplification |
| [`05_harmonic_oscillator`](05_harmonic_oscillator/) | Discrete oscillator / coherent-like orbit |
| [`06_statistical_physics`](06_statistical_physics/) | 1D Ising + Boltzmann reweight |
| [`07_quantum_walk`](07_quantum_walk/) | Classical vs quantum walk spread |
| [`08_qft_and_fields`](08_qft_and_fields/) | U(1)-style gauge invariance of observables |

## Kernel note (stance a)

The current evaluator is a **Discrete PMF Joint** runtime (ADR 0016).
Complex amplitudes and true destructive interference of phases land in a later
IR lift. Examples use the same **surface vocabulary** (`when` / `map` /
`project` / `interfer` / `inspect` / `measure`) so theorists can map each
construct to the textbook formula; READMEs mark where Born-rule / amplitude
semantics will replace non-negative masses.

Unrolled `state` / `map` chains stand in for surface `evolve {…}` until the
full evolve block lands in the parser.

## Run

```bash
python3 -m compiler.qpex check examples/02_quantum_basics/double_slit.qpex
python3 -m compiler.qpex inspect examples/02_quantum_basics/double_slit.qpex
python3 -m compiler.qpex run --target cpu examples/02_quantum_basics/double_slit.qpex --seed 0

# Same portable source → OpenQASM sketch (ADR 0036)
python3 -m compiler.qpex emit-qasm examples/03_quantum_information/portable_bell_qpu.qpex

# all examples + backend tests (SV-09 / SV-10)
python3 tests/spec_verification/run_all.py
```
