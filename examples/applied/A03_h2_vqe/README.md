# A03 — H₂ VQE (minimal)

Demonstrates `FermionOperator` construction, `map(…, JordanWigner)`, and
Schrödinger `evolve` on the mapped qubit Hamiltonian — a **toy** stand-in for
variational chemistry workflows.

## Honesty

| Claim | Status |
|-------|--------|
| Full VQE optimizer loop / parameter-shift gradients | **No** |
| Production molecular integrals or basis sets | **No** |
| Fermion → JW → `evolve` on 2 qubits | **Yes** |

## Bibliography

- Peruzzo, A. et al. "A variational eigenvalue solver on a quantum processor." *Nature Communications* **5**, 4213 (2014).
- Kandala, A. et al. "Hardware-efficient variational quantum eigensolver for small molecules." *Nature* **549**, 242–246 (2017). (Context.)
- Cerezo, M. et al. "Variational quantum algorithms." *Nature Reviews Physics* **3**, 625–644 (2021). (Survey.)

## Run

```bash
python3 -m compiler.staqex run examples/applied/A03_h2_vqe/main_h2_vqe.sqx --seed 0
python3 -m compiler.staqex emit-qasm examples/applied/A03_h2_vqe/main_h2_vqe.sqx
```
