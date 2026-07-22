# QPex positioning: never leave the state

Status: **Accepted** (Adjudicator 2026-07-22). Architecture Path manifesto.
Companion: `docs/research/2026-07-22-prior-art-and-differentiation.md`.
Semantics: `docs/specs/qpex-formal-semantics-sketch.md`.

## Language Law (highest)

While a program runs, evaluation **never leaves** the uncollapsed state:
every name lives in one **joint distribution** on the product of declared
supports. Classical bits appear only at an explicit terminal `observe`
(sampling collapse). QPex `observe` is **not** PPL conditioning.

## One sentence

**QPex is a general-purpose executable language whose runtime never leaves a
probabilistic / quantum state until an explicit terminal observation.**

## The problem with everyone else

- **Classical languages** collapse reality to one number at every step.
- **Probabilistic programming languages** keep a classical host and sprinkle
  `sample` / `observe` (usually for *inference*, not for living in Dist).
- **Quantum languages** keep a classical controller; mid-circuit measurement
  returns classical bits that steer the next classical `if`.

All three leave the interesting state early. QPex refuses that exit.

## The appeal (what to sell)

1. **Deferred classicalization as the programming model**  
   Not a circuit optimization you apply later — the default way you write
   programs. Computation is pushforward / mixture / (eventually) unitary on
   state; classical bits are an output channel, not a working memory.

2. **One ontology for values**  
   Literals, variables, arithmetic results, and (later) branch outcomes are the
   same kind of thing: distributions / amplitudes. There is no second-class
   “real program” underneath a probabilistic veneer. The store is a joint, not
   a map to independent scalars.

3. **Bridge story without bait-and-switch (stance a)**  
   Near term: exact Discrete PMF simulator (classical probability; phase 0).  
   Mid term: approximation / MCMC when support explodes.  
   Long term: lift the same late-observe programs toward amplitude / QPU IR,
   where deferred measurement is already native folklore.

4. **Intellectual honesty about naming**  
   QPex `observe` (MVP) means *collapse by sampling at the end*. It is not
   Stan/Pyro *condition*. If conditioning arrives, it gets a different word.

## Non-goals (protect the wedge)

- Not “Pyro with Rust syntax.”
- Not “OpenQASM with nicer sugar” while classical mid-measure control remains
  the default mental model.
- Not a Bayesian inference product first.
- Not a claim that MVP PMF *is* full quantum mechanics (amplitudes /
  interference are a planned lift, ADR 0016).

## Killer examples (Kernel PoC track)

### A. Correlated reuse — fixture `poc-a-correlated-self-sum`

```text
let x = fair_bit();   // joint / marginal {(0,½),(1,½)}
let y = x + x;
observe y;            // only here may classical bits appear
```

Charm: `y` is never allowed to become the binomial `{0,1,2}`. The language
refuses the classical habit of resampling.

### B. Whole program as one deferred measurement — fixture `poc-b-deferred-rng`

A multi-statement arithmetic program that makes **zero** calls to entropy until
the final `observe`. The evaluator’s purity is the demo.

### C. Superposed branch (next language slice; not Kernel PoC yet)

```text
let c = fair_bit();
let z = if c { 10 } else { 20 };
observe z;
```

Charm: both arms contribute mass; there is no classical short-circuit that
discards half the universe mid-program.

## Process decisions (locked 2026-07-22)

1. This manifesto is **Accepted**.
2. Feature Path Phase 1 Red (language birth) is **HOLD**. Kernel PoC fixtures
   A/B are authorized now. Phase 1 Red **unseals** when A/B fixtures and the
   formal semantics sketch are settled.
3. Amplitude timeline: **stance (a)** — Discrete PMF MVP with lift-ready IR
   toward complex amplitudes / QPU (ADR 0016).

## Foundation checklist

1. [x] Manifesto Accepted.
2. [x] Prior-art note linked from architecture README.
3. [x] PoC A/B fixtures under `tests/fixtures/poc/`.
4. [x] Formal semantics sketch (joint domain, pushforward, terminal observe).
5. [x] Amplitude stance recorded (ADR 0016).
