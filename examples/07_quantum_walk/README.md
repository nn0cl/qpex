# 07 — Quantum walk vs classical random walk

## Physics

On $\mathbb{Z}$, a classical walker spreads as $\sim\sqrt{t}$; a coined quantum
walk exhibits ballistic peaks $\sim t$ from interference.

## QPex mapping

| Idea | Surface |
|------|---------|
| Classical coin each step | fresh `coin()` → independent shifts |
| Quantum coined walk | reuse correlated `when` structure / interfer |
| Compare spreads | `inspect` both position States |

Discrete few-step demo: classical position after 2 steps vs quantum-style
biased spread via `interfer`.
