# 07 — Quantum walk vs classical random walk

## Physics

On $\mathbb{Z}$, a classical walker spreads as $\sim\sqrt{t}$; a coined quantum
walk exhibits ballistic peaks $\sim t$ from interference.

## QPex mapping

| Idea | Surface |
|------|---------|
| Classical coin each step | fresh `coin()` → `d_i = when (c_i) {…}` → `d1 + d2` |
| Quantum-style interfer | shared `when` paths + `interfer` |
| Compare spreads | `inspect` both position States |

**Illegal:** nested `when (c1) { when (c2) … }` → `NESTED_WHEN_ERROR` (ADR 0039).

Discrete few-step demo only. Full DTQW on $\mathcal{H}_{\mathrm{coin}}\otimes\mathcal{H}_{\mathrm{pos}}$
remains Open.
