# 14 — Genome motif Grover (toy)

Dream: **spot a short genomic marker** (cancer / CRISPR guide) by amplifying
the matching base in superposition.

## Layout

```text
examples/14_genome_motif_grover/
├── domain/
│   └── dna_alphabet.qpex       # Base enum + MotifQuery
├── operators/
│   └── motif_oracle.qpex       # marker index note (G = 2)
└── main_genome_motif.qpex      # Grover on alphabet size 4
```

## Honesty

| Claim | Status |
|-------|--------|
| Real human genome / NGS | **No** — 4 bases only |
| Clinical / diagnostic use | **Out of scope** |
| Grover motif-search skeleton | **Yes** |

## Run

```bash
python3 -m compiler.qpex run examples/14_genome_motif_grover/main_genome_motif.qpex --seed 0
```
