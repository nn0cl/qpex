# A04 — HP protein folding

2D **HP lattice** ground-state search as a Grover toy over discrete
conformations — narrative absorbed from `14_genome_motif_grover` (alphabet →
conformation index).

## Honesty

| Claim | Status |
|-------|--------|
| Real protein structure prediction / MD / Rosetta-class tooling | **No** |
| Clinical or drug-discovery claims | **No** |
| Grover mark + diffuse on 4-way conformation superposition | **Yes** |

## Bibliography

- Lau, K. F., Dill, K. A. "A lattice statistical mechanics model of the conformational and sequence spaces of proteins." *Macromolecules* **22**, 3986–3997 (1989).
- Grover, L. K. "A fast quantum mechanical algorithm for database search." *STOC* (1996).

## Run

```bash
python3 -m compiler.qpex run examples/applied/A04_hp_protein_folding/main_hp_protein_folding.qpex --seed 0
```
