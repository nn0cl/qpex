# QPex formal semantics sketch (MVP / Kernel PoC)

Status: Accepted sketch for Kernel PoC track (Adjudicator 2026-07-22).
Not a full Feature Path Phase 1 authorization by itself.
Phase 1 Red unlocks automatically once PoC A/B fixtures and this sketch are
settled in-repo (Adjudicator decision).

Scope: Discrete PMF simulator under stance **(a)** — PMF now, amplitude lift later.
Companions: `qpex-positioning.md`, ADR 0013–0015, ADR 0016,
`docs/specs/qpex-mvp-discrete-pmf-arith-observe.md`,
`tests/fixtures/poc/`.

---

## 0. Notation

- Finite support atoms live in $\mathbb{Z}$ (concretely `i64` in the Rust MVP).
- A **Discrete PMF** on a finite set $S \subset \mathbb{Z}$ is a map
  $\mu : S \to [0,1]$ with $\sum_{s \in S} \mu(s) = 1$ (within MVP tolerance
  $10^{-9}$ after normalizing ops).
- $\delta_c$ denotes the Dirac mass $\{(c, 1)\}$.
- Object-language programs mention variables $x_1,\ldots,x_n$. Their runtime
  meaning is **not** a tuple of independent scalars.

---

## 1. Domain of values — joint distribution as the store

### Classical mistake (forbidden)

An environment $\rho : \mathsf{Var} \to \mathbb{Z}$ (or even
$\rho : \mathsf{Var} \to \mathsf{Pmf}$) that treats each name as an
*independent* marginal copy. That model cannot express correlation and will
falsely give $x+x$ a mass on $1$.

### QPex store (Language Law)

After declarations of variables $x_1,\ldots,x_n$, the store is a **single joint
distribution** on the product space:

\[
\rho \;\in\; \mathcal{D}(X_1 \times X_2 \times \cdots \times X_n)
\]

where each $X_i \subseteq \mathbb{Z}$ is finite. Marginalization recovers
per-name views; the joint is authoritative.

- A numeric literal $c$ denotes $\delta_c$ (Dirac).
- Binding `let x = e` **extends or replaces** the joint so that the
  coordinate for $x$ is the pushforward of the denotation of $e$ under the
  current joint (see §2). Fresh names enlarge the product; rebinding replaces
  that coordinate consistently with the joint semantics.
- There is **no** first-class classical scalar in the object language. Dirac
  is still a distribution (support size 1).

### Stance (a) lift hint

MVP joints are non-negative real masses (phase $0$). A future amplitude IR
may replace $\mu(s) \in [0,1]$ with complex amplitudes $\alpha(s)$ where
$|\alpha(s)|^2$ recovers a PMF. Interfaces should talk about **state on a
finite product support**, not “a bag of independent `f64`s,” so the lift stays
possible without rewriting the language law.

---

## 2. Operations — pushforward and the correlation law

Let the current joint be $\rho$ on coordinates including $x$ and $y$
(possibly the same name).

### Binary arithmetic as pushforward

For an operation $\oplus \in \{+,-,\times\}$, the statement
`let z = x ⊕ y` defines a measurable map on the product space

\[
f_{x \oplus y}(\ldots, x, \ldots, y, \ldots)
  = (\ldots,\; x \oplus y,\; \ldots)
\]

and the new joint is the **pushforward** $f_{x \oplus y\#}\,\rho$.
Masses of atoms that collide under $f$ are summed.

When $x$ and $y$ are **distinct** coordinates, independence is **not** assumed
a priori: the joint already encodes dependence. If earlier bindings produced a
product measure, convolution appears as a special case of pushforward.

### Correlation law (PoC A)

The expression `x + x` (same binding twice) is the map on the **single**
coordinate $x$:

\[
f(x) = 2x
\quad\text{i.e.}\quad
f_{\#}\,\rho_x
\quad\text{where }\rho_x\text{ is the marginal of }x.
\]

It is **not** the independent sum of two draws from $\rho_x$.

**Law:** If $x \sim \mathrm{Bernoulli}(1/2)$ on $\{0,1\}$, then

\[
\llbracket x + x \rrbracket
  = \{0 \mapsto 1/2,\; 2 \mapsto 1/2\}
\]

and the mass at $1$ is **exactly** $0$. Any implementation that yields mass on
$1$ is incorrect.

### Purity of arithmetic

Evaluating $+$ / $-$ / $\times$ (and `let` without `observe`) is a
**deterministic** transformation of the joint. No entropy is consumed.

---

## 3. Terminal observation — sole collapse

### Meaning of `observe`

`observe e` is the **only** nondeterministic state-collapse operation in MVP
programs:

1. Compute the (still joint-consistent) Discrete PMF $\mu$ of expression $e$
   by pushforward / marginalization — still **without** RNG.
2. Draw one atom $c \sim \mu$ via `RngPort` (exactly one entropy use for that
   observe, unless a future spec says otherwise).
3. Replace the relevant part of the store with $\delta_c$ (Dirac on the
   sampled atom), and optionally report $c$ through `ObserveSinkPort`.

This is **sampling collapse**, not Bayesian conditioning. PPL-style
conditioning must not reuse the keyword `observe`.

### Deferred RNG law (PoC B)

Until the first `observe` executes, evaluation of a Kernel PoC program must
invoke `RngPort` **zero** times. The entire preceding program is a pure
function $\mathsf{Joint} \to \mathsf{Joint}$ (plus Dirac introductions).

Conceptually, a complete Kernel PoC program is one deferred measurement:
classical bits appear only at the terminal observe.

---

## 4. Forbidden behaviors (reviewer checklist)

| Forbidden | Why |
|-----------|-----|
| Environment as `Var → scalar` | Breaks joint / correlation |
| Resampling $x$ on each mention | Breaks `x+x` law |
| Collapsing inside `+`/`-`/`*` | Leaves the state early |
| Calling RNG before `observe` | Violates deferred measurement |
| Using `observe` to mean condition | Naming collision with PPL |

---

## 5. Kernel PoC acceptance (unlocks Phase 1 Red)

| PoC | Fixture | Must hold |
|-----|---------|-----------|
| A | `tests/fixtures/poc/poc-a-correlated-self-sum.json` | Mass on `{0,2}` only; mass@1 = 0 |
| B | `tests/fixtures/poc/poc-b-deferred-rng.json` | `rng_calls_before_observe = 0` |

When both fixtures are green under a reviewed Kernel PoC harness, Feature Path
Phase 1 Red against the MVP arith+observe spec is **unsealed** per
Adjudicator decision 2026-07-22.
