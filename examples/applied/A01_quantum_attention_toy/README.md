# A01 — Quantum attention toy

**Attention-inspired** variational feature map on a few qubits — a QML pedagogy
demo, not language-model inference.

## Story

A toy “query / key / value” wire layout uses controlled rotations and
`expect(ZZ, …)` as a correlation readout. Controlled-unitary variants
(`capply`, `ocapply`, mixed polarity, `toffoli`) show how small circuits can
resemble attention-like mixing without any LLM stack.

## Honesty

| Claim | Status |
|-------|--------|
| GPT-scale LLM inference on QPU | **No** |
| Transformer training or billion-parameter models | **No** |
| `Param<Angle>`, `capply`, `ocapply`, `toffoli`, `expect` on ≤4 qubits | **Yes** |

## Kernel surfaces

- `QubitRegister<N>`, `forEach`, `apply`
- `capply`, `ocapply`, mixed control `!`
- `phase`, `toffoli`
- `expect(ZZ, …)`, `inspect`, terminal `measure`
- `Param<Angle>` / `parameter(…)` — QPU lane via `emit-qasm` (see Run)

## Bibliography

- Benedetti, M. et al. "Parameterized quantum circuits as machine learning models." *Quantum Science and Technology* **4**, 043001 (2019).
- Cerezo, M. et al. "Variational quantum algorithms." *Nature Reviews Physics* **3**, 625–644 (2021).

## Run

```bash
python3 -m compiler.staqex check examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.qpex
python3 -m compiler.staqex run examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.qpex --seed 0
python3 -m compiler.staqex emit-qasm examples/applied/A01_quantum_attention_toy/main_quantum_attention_toy.qpex
```
