# 07 — Quantum walk vs classical random walk

## Physics

On $\mathbb{Z}$, a classical walker spreads as $\sim\sqrt{t}$; a coined DTQW
exhibits ballistic peaks from interference on
$\mathcal{H}_{\mathrm{coin}}\otimes\mathcal{H}_{\mathrm{pos}}$.

## Files

| File | Meaning |
|------|---------|
| `dtqw.qpex` | **True DTQW**: `apply(Coin,c)` then `shift(c,x)` (2 steps) |
| `classical_walk.qpex` | Independent coins → $d_1+d_2$ |
| `quantum_vs_classical_walk.qpex` | Shared-`when` + `interfer` pedagogy (not full DTQW) |

## DTQW mapping

| Idea | Surface |
|------|---------|
| Product space | `State<(Qubit, Position)> (c, x) = c0 *|* x0` |
| Coin $H$ | `Operator CoinOp = s*(X+Z)` or `hadamard(c)` / `apply(Hadamard,c)` |
| $H\otimes I$ | `apply(CoinOp, c)` on the joint |
| Conditional shift $S$ | `shift(c, x)` — $\|0\rangle\|x\rangle\mapsto\|0\rangle\|x-1\rangle$, $\|1\rangle\|x\rangle\mapsto\|1\rangle\|x+1\rangle$ |

**Illegal:** nested `when` → `NESTED_WHEN_ERROR` (ADR 0039). Use `apply` / `shift`.
