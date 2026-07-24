# Prior art and differentiation intake (2026-07-22)

Status: **Settled research note** (Architecture Path). Companion to Accepted
manifesto `docs/architecture/qpex-positioning.md`. Not an ADR by itself.

Adjudicator lock (2026-07-22): positioning Accepted; Phase 1 Red HOLD with
Kernel PoC track authorized; amplitude stance **(a)** (ADR 0016).

Companion canvas: Cursor canvas `qpex-foundation-gap.canvas.tsx`.
Formal semantics: `docs/specs/qpex-formal-semantics-sketch.md`.
PoC fixtures: `tests/fixtures/poc/`.

## 1. Why this note exists

The first MVP slice (Discrete PMF arithmetic + `observe`) is necessary but
**not sufficient** to start QPex as a language. Without a clear wedge against
existing PPL and quantum stacks, QPex risks looking like “a PMF library with a
syntax.”

This note records prior art and states the differentiation thesis Adjudicator
feedback demanded: **the program never leaves the probabilistic / quantum state
until a terminal observation.**

## 2. Differentiation thesis (working)

| Axis | Typical stack | QPex target |
|------|---------------|-------------|
| Value domain | Classical scalars; distributions are special | Every value is a distribution / state |
| Control flow | Classical `if` / loops; quantum/PPL are islands | Branch and loop stay superimposed |
| Observation | Often early (measure → classical bit; sample mid-program) | Collapse deferred to the end (`observe`) |
| Host relation | Classical host drives quantum/PPL device | There is no classical host island inside the language |
| Product goal | Inference (PPL) or circuits (QC) | **Executable** programs with late classicalization; QPU as eventual backend |

Closest physics/PL analogy: elevate the **deferred measurement principle**
(circuits with mid-measurement + classical control ≡ all measurements at the
end) from a circuit rewrite rule to the **default programming model**.

References for deferred measurement:

- Wikipedia / folklore statement of the deferred measurement principle.
- Staton, *Algebraic Effects, Linearity, and Quantum Programming Languages*
  (POPL 2015) — deferred measurement as a language axiom candidate.
- Gurevich & Blass (2021) — formalization of deferred measurements for circuits
  with classical channels.

## 3. Prior art map

### 3.1 Probabilistic programming (Bayesian / inference-first)

| System | Shape | What it optimizes for | Why it is not QPex |
|--------|-------|----------------------|--------------------|
| Stan / BUGS / JAGS | DSL + classical host | Static models, HMC / Gibbs | Not a general executable language; classical everywhere outside the model |
| Church → WebPPL, Anglican | Universal PPL embedded in JS/Clojure | Express any computable distribution; inference | Host language remains classical; `sample`/`observe` are islands |
| Pyro / NumPyro / Turing / Gen | Embedded in Python/Julia | Deep / composable inference | Same host-classical pattern; goal is posterior, not “always-on Dist VM” |

Shared PPL pattern:

```text
classical program
  └─ sample(...)   → random choice
  └─ observe(...)  → condition / reweight   ← often NOT “collapse to print”
  └─ infer(...)    → posterior approximation
```

QPex pattern (target):

```text
entire program ∈ Dist
  └─ arithmetic / control = pushforward / mixture
  └─ observe             = only classicalization point (MVP: sample)
```

**Naming collision risk:** PPL `observe` usually means *condition*. QPex MVP
`observe` means *sample / collapse*. This must stay explicit in specs and
marketing, or the brand collapses into “yet another PPL.”

### 3.2 Semantic foundations to steal carefully

- **Probability / Giry monad** (Lawvere; Giry; Ramsey & Pfeffer stochastic
  λ-calculus): `return` = Dirac, `bind` = integrate / convolve. Good classical
  probabilistic backbone for the simulator.
- **Monad-based PPLs** (e.g. Ścibior et al., practical probabilistic programming
  with monads): inference as a separate concern from the generative model.
- **Conditioning semantics** (e.g. cpGCL / conditional weakest pre-expectation):
  teaches why observation-as-condition is subtle (failure vs divergence). QPex
  must decide whether conditioning exists at all in v1.

### 3.3 Quantum programming (circuit / hybrid-first)

| System | Shape | Observation model | Why it is not QPex |
|--------|-------|-------------------|--------------------|
| Quipper | Functional embedded QC; classical controller | Dynamic lifting: measure → classical parameters for later circuit gen | Classical world still owns control |
| OpenQASM 3 | Circuit IR + real-time classical control | Mid-circuit measure drives classical `if` | Explicit classical/quantum split |
| Q# / Cirq / Qiskit | Hybrid frameworks | Measure yields classical results used immediately | Same hybrid default |

Quantum languages typically **maximize** classical feedback. QPex wants the
opposite default: **minimize** classicalization; keep the computation in state
space.

### 3.4 What “never leave the state” is *not*

- Not “no classical computer” (the Rust simulator is classical hardware).
- Not “no types other than Dist” (syntax, AST, ports exist; *runtime values*
  of the object language are Dist).
- Not “identical to quantum amplitudes from day one” (MVP PMF is a classical
  probabilistic shadow; the QPU path needs an explicit lift).

## 4. Charm that must be demonstrated (not asserted)

A language start is believable when demos force the axiom:

1. **Correlated self-use:** `x + x` with fair bit `x` → mass on `{0,2}`, never
   on `1`. Classical “sample twice” thinking fails.
2. **Terminal observe:** a multi-step program that never touches RNG until the
   last `observe` — the whole program is one deferred measurement.
3. **Superposed control (next slice):** `if` that keeps both branches weighted;
   classical short-circuit is illegal.
4. **Contrast card:** same algorithm written in Pyro / Q# mid-measure style vs
   QPex late-observe style — show where the others leave the state.

Until these exist as PoCs or golden examples, the MVP arith spec reads as a
library, not a language.

## 5. Open research / design questions

1. Is QPex primarily **probabilistic-executable** with a quantum *compilation
   target*, or **amplitude-native** from the IR up?
2. Does v1 include **conditioning**, or only **sampling collapse**?
3. Are distinct bindings always **independent** (product measure)? When do we
   need explicit joint / entangled bindings?
4. What is the complexity story when Discrete PMF support explodes?
5. How does deferred-measurement-as-language-law interact with effects (I/O)?
   Only `observe` may classicalize — is that absolute?

## 6. Recommended foundation pack (before more implementation)

| Artifact | Purpose |
|----------|---------|
| `docs/architecture/qpex-positioning.md` | Manifesto: wedge, non-goals, killer examples |
| This research note | Prior art + citation anchors |
| Semantic sketch (1–2 pages) | Denotation: Expr → Dist; observe → sample |
| PoC P0 fixtures | Dirac, convolution, `x+x`, no early RNG |
| ADR when amplitude path is chosen | Technology selection for QPU IR |

## 7. Relation to existing MVP spec

`docs/specs/qpex-mvp-discrete-pmf-arith-measure.md` remains a **valid slice** of
behavior. With positioning Accepted and Kernel PoC fixtures A/B plus the formal
semantics sketch settled, Feature Path Phase 1 Red against that slice is
**unsealed** per Adjudicator decision 2026-07-22 (still requires an explicit
Phase 1 request to execute). Until a harness turns A/B green, treat the slice as
the Kernel PoC target, not a language-birth declaration.
