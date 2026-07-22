# QPex dimensional types (Type-First + dimensional algebra)

Status: **Accepted** (2026-07-23). ADR **0037**.
Companions: `qpex-type-system.md`, `qpex-language-spec.md`,
`docs/testing/qpex-spec-verification-protocol.md` (SV-15).

---

## 1. Thesis

Physical quantities are **not** OOP class hierarchies. They are elements of a
**dimensional algebra**: integer exponent vectors over base dimensions, with
operators that mirror blackboard arithmetic.

```text
  Type-First surface          Compile-time vector            Runtime
  ─────────────────          ───────────────────            ───────
  Length x = 1.0.m     →     d = (L=1,M=0,T=0)       →     value 1.0
  dt / m * p           →     (0,0,1)−(0,1,0)+(1,1,−1)
                       →     (1,0,0) = Length         →     float pushforward
```

Programmers never write `.add()` / `new Meter()` / `extends Length`.

---

## 2. Type-First declaration

```qpex
Delta<Time>     dt = 0.05.s
Mass            m  = 1.0.kg
Stiffness       k  = 1.0.N_m
State<Length>   x  = dirac(1.0.m)
State<Momentum> p  = dirac(0.0.kg_m_s)
```

| Form | Meaning |
|------|---------|
| `Q name = expr` | Bind `name` as `State` with quantity / dim of `Q` |
| `State<Q> name = expr` | Explicit State wrapper; payload dim from `Q` |
| `Delta<Q> name = expr` | Increment of `Q` (same $\mathbf{d}$ as `Q`) |
| `state name = expr` | Inferred `State<_>` (no quantity head) |
| `(x, p) = expr` | Tuple bind inside `main` |

**Non-normative / retired as object syntax:** `val name: Type = …`.

---

## 3. Base dimensions and named quantities

$\mathbf{d} = (L, M, T) \in \mathbb{Z}^3$.

| Name | $\mathbf{d}$ | Typical unit suffix |
|------|--------------|---------------------|
| `Length` | $(1,0,0)$ | `.m` |
| `Mass` | $(0,1,0)$ | `.kg` |
| `Time` / `Delta<Time>` | $(0,0,1)$ | `.s` |
| `Momentum` | $(1,1,-1)$ | `.kg_m_s` |
| `Force` | $(1,1,-2)$ | `.N` |
| `Energy` | $(2,1,-2)$ | `.J` |
| `Stiffness` | $(0,1,-2)$ | `.N_m` |
| `Frequency` | $(0,0,-1)$ | `.Hz` |
| `Angle` / dimensionless | $(0,0,0)$ | `.rad` / bare number |

Suffixes are **dimension tags** only (MVP does not convert `ms`→`s` scales).

---

## 4. Algebraic rules (typechecker)

1. **`+` / `-`:** require $\mathbf{d}_L = \mathbf{d}_R$; else
   `DIMENSION_MISMATCH_ERROR`
   (e.g. `dimension mismatch for '+': [L] vs [T] — physically incompatible`).
2. **`*`:** $\mathbf{d}_L + \mathbf{d}_R$ (componentwise).
3. **`/`:** $\mathbf{d}_L - \mathbf{d}_R$.
4. **Inference:** unnamed compound dims may map back to a known quantity
   name when $\mathbf{d}$ matches the table; otherwise keep numeric payload
   with the computed vector.
5. **`sin` / `cos` / `exp` / `log` / `cis` / `phase` angle:** argument
   $\mathbf{d} = \mathbf{0}$.
6. **`evolve … for dt`:** $\mathbf{d}(dt)$ is Time / `Delta<Time>` (or
   dimensionless step). **`times N`:** discrete integer iterations.

### Worked example

\[
\frac{\mathrm{d}t}{m}\,p
=
\frac{(0,0,1)}{(0,1,0)}\cdot(1,1,-1)
=
(1,0,0)
= \mathsf{Length}
\]

so `x + (dt / m) * p` typechecks when `x : Length`.

---

## 5. Structured placement

Dimensional Type-First binds are **executable statements**. They belong
inside `public fun main() { … }` (ADR 0037 §C / ADR 0027 as amended).
Top-level `Delta<Time> dt = …` → `TOPLEVEL_EXECUTION_ERROR`.

---

## 6. Out of scope (later)

- Full SI coherent system with scale factors and prefixes
- Temperature, current, amount, luminous intensity bases
- Dependent types / units of measure as runtime witnesses
- Automatic rewriting of numerically unstable unit mixes
