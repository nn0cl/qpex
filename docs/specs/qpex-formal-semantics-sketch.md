# QPex formal semantics sketch (MVP / Kernel PoC)

Status: **Informative annex** (Accepted sketch for Kernel PoC track,
Adjudicator 2026-07-22). Normative summary lives in
[`qpex-language-specification.md`](qpex-language-specification.md) §5.
Surface lexicon ADR 0017, **`when`** (historical AST name Span) / Block /
Evolve / Tuple / **Project** / **Interfer** (ADR 0021 naming).
Not a full Feature Path Phase 1 authorization by itself.
Phase 1 Red unlocks when PoC A/B fixtures are green under a harness.

Scope: Discrete PMF simulator under stance **(a)** — PMF now, amplitude lift later.
Companions: `qpex-positioning.md`, `qpex-syntax-vocabulary.md`,
`qpex-ast-design.md`, `qpex-type-system.md`, `qpex-stdlib-combinators.md`,
`docs/collaboration/agent-sync-qpex-baseline.md`,
`docs/collaboration/agent-sync-project-interfer-system.md`,
ADR 0013–0021,
`docs/specs/qpex-mvp-discrete-pmf-arith-observe.md`, `tests/fixtures/poc/`.

---

## 0. Notation

- Carrier types `T` decorate joint axes; runtime values are `State<T>`
  (see `qpex-type-system.md`, ADR 0018).
- Finite support atoms live in a carrier $T$ (MVP Kernel: $T = \mathbb{Z}$,
  concretely `i64`).
- A **Discrete PMF** on a finite set $S \subset T$ is a map
  $\mu : S \to [0,1]$ with $\sum_{s \in S} \mu(s) = 1$ (within MVP tolerance
  $10^{-9}$ after normalizing ops).
- $\delta_c$ denotes the Dirac mass $\{(c, 1)\} = \mathsf{lift}(c)$.
- $\mathsf{Joint}$ is the type of finite-support joints
  $\mathcal{D}(T_1 \times \cdots \times T_n)$.
- Pure statement denotation (everything except `measure`):

\[
\llbracket \mathsf{Stmt} \rrbracket : \mathsf{Joint} \to \mathsf{Joint}
\]

- Surface binder: `state`. Terminal collapse: `measure`.
- Classical literals in expressions **lift** to Dirac before pushforward;
  they are not a parallel classical store (ADR 0018).
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

- `dirac(c)` (and, provisionally, numeric literal sugar) denotes $\delta_c$.
- `coin()` denotes the Bernoulli$(1/2)$ PMF on $\{0,1\}$.
- Binding `state x = e` **extends or replaces** the joint so that the
  coordinate for $x$ is the pushforward of the denotation of $e$ under the
  current joint (see §2). Fresh names enlarge the product; rebinding replaces
  that coordinate consistently with the joint semantics.
- There is **no** first-class classical scalar store in the object language
  during uncollapsed execution (ADR 0018). Dirac is still a `State<T>`
  (support size 1). Literals lift via $\mathsf{lift}(c)=\delta_c$.

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
`state z = x ⊕ y` defines a measurable map on the product space

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

### Purity

Evaluating $+$ / $-$ / $\times$, `state` without `measure`, `when`,
`evolve`, bare `{…}` blocks, and pure stdlib combinators (`map`, `project`,
`interfer` — ADR 0021) is a **deterministic** $\mathsf{Joint}\to\mathsf{Joint}$
map. No entropy is consumed until §9 `measure`. Note: `project` renormalizes
but does **not** sample.

---

## 3. `when` — controlled superposition / pushforward mixture

**Surface spelling (ADR 0024):** `when (ctrl) { … }`. Historical docs and
AST node names may say `span` / `Span`; the denotation below is unchanged.

Surface (binary sugar — illustrative; prefer `when`):

```qpex
state z = when (c) { 0 -> e0, 1 -> e1 }
```

Surface (multi-arm / match-style — normative general form):

```qpex
state z = when (c) {
    0 -> x + 10,
    1 -> x + 20,
    else -> x + 30,
}
```

Binary `{ e0, e1 }` is sugar for `{ 0 -> e0, 1 -> e1 }` when the control is a
bit-like coordinate; otherwise prefer explicit patterns.

### MVP denotation (stance a — convex / pushforward mixture)

Let $\rho$ be the current joint and $c$ a control expression with finite
support $U \subseteq \mathbb{Z}$. A span has an ordered list of arms

\[
(p_i \Rightarrow e_i)_{i=1}^{m}
\]

where each $p_i$ is either a concrete atom $u_i \in \mathbb{Z}$ or a wildcard
`_` (at most one wildcard; it matches the residual atoms of $U$ not covered by
concrete patterns).

For each control atom $u \in U$, select the unique matching arm $e_{i(u)}$
(concrete match wins; else wildcard). Define the restricted pure evaluation

\[
\rho^{(u)} = \llbracket e_{i(u)} \rrbracket(\rho \mid c = u)
\]

(restriction is *arm-local restrict-and-renormalize for evaluation*, not
program-level Bayesian conditioning).

Let $p(u) = \rho(c = u)$. The span result is the **mixture that retains every
positively weighted arm**:

\[
\rho'(z)
  = \sum_{u \in U} p(u)\, \mathsf{bind}_z\bigl(\rho^{(u)}\bigr)
\]

(with other coordinates updated consistently from the same restricted joints).
Supports of all selected arms are **unioned**; no arm with $p(u) > 0$ is
discarded.

Special case (bit control, binary sugar):

\[
\rho'(z)
  = p(0)\,\llbracket e_0 \rrbracket(\rho\mid c=0)
  + p(1)\,\llbracket e_1 \rrbracket(\rho\mid c=1).
\]

### Laws

1. **No short-circuit:** evaluating `when` / §Span never drops mass of an arm that
   matches some $u$ with $p(u) > 0$.
2. **No RNG:** `when` / §Span does not call `RngPort`.
3. **Not classical `if` / `switch`:** there is no jump that abandons a branch.
4. **Exhaustiveness (static intent):** every $u \in U$ with $p(u)>0$ must match
   some arm (wildcard may close the cover).

### Amplitude lift (stance a — later)

Under ADR 0016, the same AST node `Span` may be reinterpreted as a coherent
linear combination of amplitudes controlled by $c$. MVP implements only the
non-negative mixture above (phase $0$).

### Kernel PoC note

PoC A/B do **not** require `when`. The section is normative for language
design and for future fixtures.

---

## 4. Block — internal state transformer kernel

Surface: a brace group `{ … }` used as an **expression** (not a classical
stack-frame of imperative statements).

```qpex
{
    let a = z * 2
    let b = a + 5
    b
}
```

Nested inside `span` arms or as the body of `evolve`:

```qpex
state z = span (c) {
    0 => {
        let a = x * 2
        a + 10
    },
    1 => x + 20,
}
```

### Definition (pure state transformer)

A block is **not** “run these commands in order on a mutable stack.” It is a
single pure operator on joints:

\[
\llbracket \mathsf{Block} \rrbracket
  : \mathsf{Joint}_{\mathrm{in}} \to \mathsf{Joint}_{\mathrm{out}}
\]

Equivalently, the whole block behaves as one unitary-/pushforward-like kernel
$U_{\mathrm{block}}$: however many internal lines exist, the outside sees
**one** pure state transformation. No collapse and no decoherence occur inside
the block (MVP: no `RngPort` calls).

### Three laws inside a block

#### (1) Local coordinates (`let`)

Each `let name = expr` **extends** the current joint with a temporary axis
(ancilla-like coordinate), correlated with the inputs via pushforward — the
same algebra as top-level `state`, but scoped to the block.

#### (2) Trace-out at the boundary

Let the block-extended joint after all locals be $\rho_{\mathrm{ext}}$ on
coordinates $(\mathsf{in},\;\ell_1,\ldots,\ell_k,\;\ldots)$, and let the
**result expression** $e_{\mathrm{res}}$ mention a set of coordinates
$R$ (possibly a tuple; §6).

Coordinates among $\{\ell_i\}$ that are **not** part of $R$ are
**traced out** (marginalized / discarded as free axes) when forming
$\mathsf{Joint}_{\mathrm{out}}$:

\[
\rho_{\mathrm{out}}
  = \mathrm{Tr}_{\{\ell_i \notin R\}}
      \bigl(\llbracket e_{\mathrm{res}} \rrbracket(\rho_{\mathrm{ext}})\bigr)
\]

**Physical narrative:** ancilla axes used for intermediate calculation are
discarded; only the extracted subsystem leaves the block. Correlation with
what remains may survive in the extracted joint (entanglement / dependence
encoded in $\rho_{\mathrm{out}}$), but the ancilla names themselves do not
leak to the outer scope.

**Not measurement:** trace-out is a pure marginalization of unused axes, not
a projective collapse and not an `RngPort` draw.

**Optimizer note:** Trace-Out GC (ADR 0022 /
`qpex-compiler-optimizations.md`) is the engine realization of this law via
liveness — it must not change the denotation above.

#### (3) Block is an expression

- There are no imperative “statements” that return unit; the block **is** an
  expression whose value is $e_{\mathrm{res}}$ (last line, no trailing
  semicolon required in the narrative grammar).
- `return` / `break` / early exit are **Language Law violations**: leaving
  mid-block would tear the joint pipeline.
- The type of $e_{\mathrm{res}}$ (single state coordinate or tuple) is the
  type of the whole block.

For an ordinary `fun` or class method, the surface form may declare the result
type as `-> T`; the terminal expression is checked against that type. `main`
is the deliberate exception: it has no result value and terminates through
terminal `measure`.

### Composition

- `evolve (seeds) { … }` = seed wiring + $\llbracket\mathsf{Block}\rrbracket$
  + outer `state` bind (§5–§6).
- `when` arm bodies may be any `Expr`, including a nested `Block` (§3).
- Nested blocks compose: each applies local extend → result → trace-out
  before the parent continues.

### Kernel PoC note

PoC A/B do not require nested blocks. Normative for `evolve` / `when` design.

---

## 5. Evolve — pure state pipeline

Surface:

```qpex
state w = evolve (z) {
    let a = z * 2
    let b = a + 5
    b
}
```

### Denotation

`evolve` is sugar for: take seed coordinates from the outer joint, evaluate a
**Block** (§4) as $U_{\mathrm{block}}$, then bind the block’s result into
the outer joint via `state` / tuple pattern (§6).

1. **Seeds:** expressions in `evolve (…)` name input coordinates already in
   $\rho$ (not sampled).
2. **Body:** $\llbracket \mathsf{Block} \rrbracket$ — local `let` axes,
   result expression, trace-out of unused locals (§4).
3. **Bind-out:** `state w = …` or `state (w1,w2) = …` pushes the block result
   into outer coordinates.

\[
\llbracket \texttt{evolve} \rrbracket(\rho)
  = \mathsf{bind}_{\mathrm{outer}}
      \bigl(\llbracket \mathsf{Block} \rrbracket(\rho)\bigr)
\]

### Laws

1. Inherits §4: no `return` / `break`; no RNG; unused locals traced out.
2. **Repetition (`times` / `until`)** remains reserved (compose $U_{\mathrm{block}}$
   repeatedly without mid-pipeline `measure`). Grammar open.

### Narrative vs mathematics

Docs may call this “time evolution.” MVP meaning is **pure block
composition**, not a literal Hamiltonian simulator. Amplitude / unitary lift
remains ADR 0016 territory.

---

## 6. Tuple — compound coordinate extract / extend

Surface:

```qpex
state (w1, w2) = evolve (z) {
    let a = z * 2
    let b = a + 5
    (a, b)
}
```

### Denotation

A tuple expression $(e_1,\ldots,e_k)$ under joint $\rho$ denotes the
**simultaneous** pushforward that binds $k$ coordinates at once:

\[
f(\omega) = \bigl(\llbracket e_1 \rrbracket(\omega),\;\ldots,\;\llbracket e_k \rrbracket(\omega)\bigr)
\]

evaluated on the **same** atomic assignment $\omega$ drawn from $\rho$. The
outer `state (w1,…,wk) = …` extends the product space with coordinates
$w_1,\ldots,w_k$ whose **joint** is $f_\#\rho$ (or the block result before
outer bind).

As a block result (§4), `(a, b)` means: **do not** trace out `a` or `b`;
extract the compound subsystem so both axes leave the block together,
preserving correlation.

### Laws

1. **Correlation preserved:** components are not independently re-sampled.
2. **Arity match:** pattern `(w1,…,wk)` must match tuple arity $k$.
3. **Still pure:** tuple construction does not call `RngPort`.

---

## 7. Project — subspace projection + renormalization

Surface / stdlib:

```qpex
state even = dice.project(v => v % 2 == 0)
```

Normative name **`project`** (ADR 0021). Not `measure`.

### MVP Discrete PMF denotation

Let $\mu$ be a Discrete PMF on carrier $T$, predicate $P : T \to \{\mathsf{true},\mathsf{false}\}$,
$A = \{ t \mid P(t)=\mathsf{true} \}$, $Z = \sum_{t \in A} \mu(t)$.

\[
\llbracket \mathsf{project}(P) \rrbracket(\mu)
  =
  \begin{cases}
    t \mapsto \mu(t)/Z & t \in A,\ Z > 0 \\
    \mathsf{Vacuum}\ (\lvert 0\rangle_{\mathrm{vac}},\ \mathrm{norm}\,0)
      & Z = 0 \quad\text{(ADR 0034; not an exception)}
  \end{cases}
\]

On a joint, restrict the selected coordinate consistently with other axes
(conditional joint on $A$), then renormalize the joint mass.

### Density-matrix narrative (stance a lift)

With orthogonal projector $\Pi$ onto the subspace selected by $P$,

\[
\rho' = \frac{\Pi \rho \Pi}{\mathrm{Tr}(\Pi \rho \Pi)}
\qquad (\mathrm{Tr}(\Pi \rho \Pi) \neq 0).
\]

MVP implements the phase-0 / probability shadow of this law.

### Laws

1. Pure; no `RngPort`.
2. Support may remain multi-atom — **not** collapse.
3. Drop-without-renormalize is forbidden.
4. Distinct from terminal `measure` (§9).
5. Vacuum is absorbing under pure ops; `measure` on vacuum reports empty
   outcome without throw (ADR 0034).

---

## 8. Interfer — combine / interfere a list of states

Surface / stdlib:

```qpex
state sum = coins.interfer(0, (acc, c) => acc + c)
```

Normative name **`interfer`** (ADR 0021).

### MVP denotation (independent list)

Given $\mu_1,\ldots,\mu_n$ on carrier $T$ and combiner
$f : \mathsf{State}\langle Acc\rangle \times \mathsf{State}\langle T\rangle
  \to \mathsf{State}\langle Acc\rangle$
with classical `init` lifted to $\delta_{\mathrm{init}}$:

1. Form the product joint $\mu_1 \otimes \cdots \otimes \mu_n$ on fresh axes
   (independence default).
2. Iterate $f$ left-to-right starting from $\delta_{\mathrm{init}}$.
3. Result is a single `State<Acc>` marginal (other temp axes traced as needed).

Correlation law: if list elements are the same joint coordinate, do **not**
form an independent product — reuse the shared axis (cf. §2 `x + x`).

### Amplitude narrative (lift)

Under complex amplitudes, combining subsystems can exhibit constructive /
destructive interference. MVP PMF `interfer` only merges non-negative masses
(no negative interference until amplitude IR / ADR 0016).

### Laws

1. Pure; no per-element sampling.
2. Combiner `f` must itself be measure-free.
3. Init of classical `Acc` lifts via $\mathsf{lift}$ (ADR 0018).

---

## 9. Terminal measurement — sole collapse

### Meaning of `measure`

`measure e` is the **only** nondeterministic state-collapse operation in MVP
programs. In packaged programs it must be the **final statement of
`public fun main`** (ADR 0027). Kernel scripts are implicit-`main` sugar.


1. Compute the (still joint-consistent) Discrete PMF $\mu$ of expression $e$
   by pushforward / marginalization — still **without** RNG.
2. Draw one atom $c \sim \mu$ via `RngPort` (exactly one entropy use for that
   measure, unless a future spec says otherwise).
3. Replace the relevant part of the store with $\delta_c$ (Dirac on the
   sampled atom), and report $c$ through `MeasureSinkPort`
   (stdout by default, or `measure e to File(…)` / other sinks — ADR 0029).

The observer is consequently outside the object-language function graph:
`RngPort` chooses the atom, `MeasureSinkPort` emits it, and the user or host
consumer reads the emitted data. A QPex function cannot bind or branch on that
atom after `measure`; terminal observation ends the language-level computation.

This is **projective sampling collapse**, not Bayesian conditioning / not
`project`. PPL-style conditioning must not reuse `measure`.

If the measured marginal is **vacuum** (empty support / norm 0), skip the
`RngPort` draw and report no atom via the sink (ADR 0034).

### Deferred RNG law (PoC B)

Until the first `measure` executes, evaluation of a Kernel PoC program must
invoke `RngPort` **zero** times. The entire preceding program — including any
`when` (§Span) / `evolve` / `block` / tuple / `map` / `project` / `interfer` forms —
is a pure function $\mathsf{Joint} \to \mathsf{Joint}$.

Conceptually, a complete program is one deferred measurement: classical bits
appear only at the terminal `measure`.

**Optimizer note:** Deferred Pushforward / Operator Fusion / Interference
Pruning (ADR 0022) may delay or fuse materialization of that pure function,
but must agree with eager denotation under the same RNG stream at `measure`.

---

## 9b. Snapshot — non-collapsing host log (ADR 0029)

`snapshot e to S` may serialize the current joint / marginal of $e$ to a host
sink **without** calling `RngPort` and **without** replacing the store by
Dirac. Denotation of the continuing program is unchanged. Distinct from §9.

## 9c. Inspect — non-destructive debug (ADR 0030)

`inspect(e)` (optional label) has joint denotation **identity**:
$\llbracket \mathsf{inspect}(e) \rrbracket(\rho) = \llbracket e \rrbracket(\rho)$.
No `RngPort`. Host may pretty-print the support of that marginal as **external
log text** (not an object-language `State` or scalar). Distinct from §9
(`measure`) and §9b (`snapshot` file checkpoints).

## 10. Forbidden behaviors (reviewer checklist)

| Forbidden | Why |
|-----------|-----|
| Environment as `Var → scalar` | Breaks joint / correlation |
| Resampling $x$ on each mention | Breaks `x+x` / tuple / `interfer` laws |
| Collapsing inside `+`/`-`/`*` / `when` / `evolve` / `block` / `map` / `project` / `interfer` | Leaves the state early |
| Calling RNG before `measure` | Violates deferred measurement |
| Classical `if` / `return` / `break` / early `measure` | Violates Never Leave the State |
| Treating block `{…}` as an imperative stack frame | Breaks §4 kernel view |
| Discarding a `when` / §Span arm with positive control weight | Breaks §3 |
| `project` without renormalization | Breaks §7 |
| Equating `project` with `measure` | Naming / law collision |
| Using `measure`/`observe` to mean condition | Naming collision with PPL |
| Mid-pure `File.write` that samples State | Early collapse (ADR 0029) |
| Treating `snapshot` / `inspect` as `measure` | Wrong collapse law |
| Using `measure` only to dump a PMF | Use `inspect` |

---

## 11. Kernel PoC acceptance (unlocks Phase 1 Red)

| PoC | Fixture | Must hold |
|-----|---------|-----------|
| A | `tests/fixtures/poc/poc-a-correlated-self-sum.json` | Mass on `{0,2}` only; mass@1 = 0 |
| B | `tests/fixtures/poc/poc-b-deferred-rng.json` | `rng_calls_before_measure = 0` |

When both fixtures are green under a reviewed Kernel PoC harness, Feature Path
Phase 1 Red against the MVP arith+measure spec is **unsealed** per
Adjudicator decision 2026-07-22; surface `when` ADR 0024. `when` / `evolve` / `block` / tuple /
`project` / `interfer` need separate fixtures before they enter Phase 1 scope.
