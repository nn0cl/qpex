# A05 — QAOA portfolio

Small **QUBO portfolio** selection in Ising form: one QAOA layer
(mixer `X` then cost `Z`/`ZZ` terms). Harvested from `06` Ising patterns and
`12` graph-selection narrative.

## Honesty

| Claim | Status |
|-------|--------|
| Real market data, risk models, or transaction costs | **No** |
| Classical portfolio optimization baseline | **No** |
| Single-layer QAOA-style `evolve` alternation on 2 qubits | **Yes** |

## Bibliography

- Farhi, E., Goldstone, J., Gutmann, S. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014).
- Cerezo, M. et al. "Variational quantum algorithms." *Nature Reviews Physics* **3**, 625–644 (2021). (Survey.)

## Run

```bash
python3 -m compiler.qpex run examples/applied/A05_qaoa_portfolio/main_qaoa_portfolio.qpex --seed 0
```
