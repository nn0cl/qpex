# QPex Official Examples

Physics-oriented sample programs for **QPex（キューペックス）**.

Axiom: **Never Leave the State** — every mid-program value is `State<T>`;
collapse happens only at terminal `measure`.

## Layout

| Dir | Topic |
|-----|--------|
| [`01_classical_mechanics`](01_classical_mechanics/) | Phase-space ensemble / Euler pushforward |
| [`02_quantum_basics`](02_quantum_basics/) | Double-slit + spontaneous phase cancel |
| [`03_quantum_information`](03_quantum_information/) | Bell / EPR correlation & CHSH-style project |
| [`04_quantum_algorithms`](04_quantum_algorithms/) | Grover oracle phase + `diffuse` |
| [`05_harmonic_oscillator`](05_harmonic_oscillator/) | Classical HO phase-space Euler (Type-First) |
| [`06_statistical_physics`](06_statistical_physics/) | 1D Ising + Boltzmann reweight |
| [`07_quantum_walk`](07_quantum_walk/) | Classical vs quantum walk spread |
| [`08_qft_and_fields`](08_qft_and_fields/) | U(1)-style gauge invariance of observables |

## Program structure

Every example is a structured compilation unit:

```qpex
package com.qpex.examples.…

public fun main() {
    // Type-First binds, evolve, measure — never top-level script soup
}
```

Top-level executable statements are rejected (`TOPLEVEL_EXECUTION_ERROR`, SV-16).

## Kernel note (stance a)

The evaluator is a **complex-amplitude Joint** runtime: each world carries
$c\in\mathbb{C}$ with Born weight $|c|^2$. `phase` / `cis` / `Complex.cis`
attach phases; `interfer` sums amplitudes then takes $|\sum c_i|^2$
(destructive cancel → vacuum). `diffuse` is Grover inversion-about-mean.

Surface vocabulary: `when` / `map` / `project` / `interfer` / `phase` /
`diffuse` / `inspect` / `measure` / `evolve`.

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
