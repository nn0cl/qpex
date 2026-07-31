# LISS-0136: Sparse Pauli Operator return from helper `fn`

## Metadata

- Local issue ID: LISS-0136
- Status: **ready** — filed from S1 discovery; not started
- Phase: Feature Path (awaiting Plan / batch authorize)
- Type: Kernel residual / language
- Priority: P1 (S1 workaround in place; blocks cleaner physics modules)
- Depends on: none hard; discovered by [LISS-0134](LISS-0134-showcase-s1-thin-slice.md)
- Implementation permission: **none** until Adjudicator Plan/Phase approve
- Branch: TBD (`feature/liss-0136-…`)

## Summary

Returning a sparse-Pauli `Operator` (e.g. `-J*(Z[0]*Z[1]) - h*(X[0]+X[1])`)
from a helper `fn` and using it in `evolve` fails at runtime with
`cannot compile sparse Pauli for Call` (or related Call/bind errors).

`hop`-based Operators returned from helpers **do** work (A06). Inline
construction in `main` (B08 / S1) works. Showcase S1 therefore builds Ising
`H` at the evolve site and keeps physics OOP packs classical-only.

## Repro sketch

```text
fn build() -> Operator { … Pauli tree …; return H }
Operator H = build()   // or bare import
evolve … under H …
→ RUNTIME_ERROR: cannot compile sparse Pauli for Call
```

## Exit

- [ ] Failing Red suite locked to the Repro
- [ ] Green: returned sparse Pauli usable under `evolve` (parity with hop-return)
- [ ] Showcase physics module may move Ising construction into helper without workaround notes
- [ ] Docs / friction ledger updated

## Non-goals

- Live QPU / OpenQASM lowering of returned Operators
- Changing A06 hop return semantics
