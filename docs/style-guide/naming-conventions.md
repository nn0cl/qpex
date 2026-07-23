# QPex naming conventions

Status: **Working baseline** (2026-07-22). ADR **0023**.
Audience: physicists/researchers reading narrative code **and** software
engineers maintaining it. Feeds future parser / styler / linter rules.

Companions: `qpex-syntax-vocabulary.md`, `qpex-type-system.md`,
`qpex-abstraction-model.md`, `qpex-compiler-optimizations.md` (Trace-Out GC),
ADR 0017–0022.

---

## 0. Goals

1. **Zero-latency role recognition** — from the glyph shape alone, know whether
   a name is a superposition (`State<T>`), a classical scalar constant, a
   `system` / `trait` type, or a function.
2. **Paper ↔ code sync** — single-letter Dirac / Greek names stay natural
   (`psi`, `x`, `theta`) without fighting Java/Python class-case habits.
3. **State vs classical** — never rely on “remember the inferred type”; bind
   form and case make the role obvious.

These are **style** rules (lint / review). They do not change Language Law
semantics. Leading `_` does **not** replace liveness-based Trace-Out GC; it
*documents* expected ancilla axes.

---

## 1. Case rules (primary discriminator)

| Role | Case | Examples | Reader intuition |
|------|------|----------|------------------|
| Superposition / `State<T>` binding | `snake_case` or single lowercase letter | `c`, `x`, `psi`, `phi_0`, `state_a` | $\lvert x\rangle$, $\lvert\psi\rangle$, r.v. $x$ |
| Classical scalar **constants** | `ALL_CAPS` | `DT`, `MAX_STEPS`, `PI` | Fixed parameters |
| `class` / types / `interface` | `PascalCase` | `HarmonicOscillator`, `System`, `Additive` | $\mathcal{H}$, algebraic structure |
| Packages | dot-separated lowercase | `com.physics.optics` | Subsystem path |
| Functions / methods | `snake_case` | `step`, `run_simulation`, `shift` | Operators / maps $U(\theta)$ |

### Notes

- Prefer short physics-native state names over JavaBeans (`getPosition` ✗).
- Normative domain capability remains **`System`** (ADR 0021); other
  `interface`s also use `PascalCase`. Surface keyword: `interface` / `class`
  (ADR 0024).
- After `measure`, a classical sample may use `snake_case` (it is no longer a
  `State`). Prefer not to reuse the same bare name as the pre-measure state
  in the same scope when that would confuse readers.
- Optional emphasis prefix for states: `s_` (e.g. `s_position`) when a file
  mixes many classical locals and states. Not required when `state` binds.

---

## 2. Leading symbols and math transcription

### 2.1 Underscore

| Form | Meaning |
|------|---------|
| `_` alone | Anonymous / wildcard pattern (`when` arm `else` / `_`) |
| Leading `_name` | **Ancilla / local joint axis** expected to be traced out at block / `evolve` exit (style signal for Trace-Out GC) |

```qpex
state w = evolve (z) {
    let _temp1 = z * 2
    let _temp2 = _temp1 + 5
    _temp2
}
```

Do **not** use leading `_` for “unused import” theatre on long-lived `state`
coordinates that escape the block.

### 2.2 Subscripts, Greek, primes

| Math | Code |
|------|------|
| $\psi_0$, $x_{\mathrm{init}}$ | `psi_0`, `x_init` |
| $\lvert\psi\rangle$, $\phi$, $\theta$, $\rho$ | `psi`, `phi`, `theta`, `rho` |
| $x'$ | `x_prime` or `x1` (pick one style per module) |

Use English spellings for Greek; do not invent Unicode identifiers in MVP
surface (ASCII-first keyboard law).

---

## 3. State vs classical — bind form

Do not leave role to silent type inference alone.

```qpex
// Preferred: keyword + case make the role immediate
state x = coin()
let DT = 0.01

// Optional extra emphasis
state s_position = dirac(0.0)
```

| Bind | Expected name case | Role |
|------|--------------------|------|
| `state name = …` | lowercase / `snake_case` | Joint coordinate / `State<T>` |
| `let NAME = …` (const) | `ALL_CAPS` | Classical constant in a pure block |
| `let _name = …` | leading `_` + snake | Ancilla axis inside block / `evolve` |

---

## 4. Narrative example (conventions applied)

```qpex
class HarmonicOscillator : System {
    state x: State<Float>
    state p: State<Float>

    fn step(self) -> HarmonicOscillator {
        let DT = 0.01

        let _x_next = self.x + self.p * DT
        let _p_next = self.p - self.x * DT

        HarmonicOscillator {
            x: _x_next,
            p: _p_next
        }
    }
}

state psi_0 = HarmonicOscillator {
    x: dirac(1.0),
    p: dirac(0.0)
}
state psi_final = run_simulation(psi_0)
```

Paper sync: $\psi_0$, $(x,p)$, step $U_{\Delta t}$ with scalar $\Delta t$ as `DT`.

---

## 5. Linter / styler hooks (future)

Suggested diagnostics (non-blocking until a style unseal):

| Id | Rule |
|----|------|
| `qpex-name-state-case` | `state` bindings should be lowercase / `snake_case` |
| `qpex-name-const-case` | Classical scalar constants should be `ALL_CAPS` |
| `qpex-name-type-case` | `system` / `trait` / type names should be `PascalCase` |
| `qpex-name-fn-case` | `fn` names should be `snake_case` |
| `qpex-name-ancilla` | Block locals not in the result set should prefer leading `_` |
| `qpex-name-greek` | Prefer `psi`/`phi`/`theta` transcriptions over ad-hoc abbrevs |

Parser still accepts any legal identifier; style is layered on top.

---

## 6. Anti-patterns

| Avoid | Why |
|-------|-----|
| `state MaxSteps = …` | Looks like a type / const; breaks Dirac muscle memory |
| `let psi = 0.01` | Greek name for a classical constant |
| `fn RunSimulation` / keyword `fun` | PascalCase or retired `fun` (use `fn`) |
| `class harmonic_oscillator` | Types should be `PascalCase` |
| Leading `_` on escaping `state` fields | Lies about ancilla / trace-out |
| Normative `filter` / `fold` / `QSystem` names | Superseded (ADR 0021) |

---

## 7. Open questions

- Enforce leading `_` for *all* traced locals, or only recommend?
- Measured classical results: `x_obs` vs reuse `x`?
- Unicode identifiers later for true $\psi$ glyphs (out of MVP keyboard law)?
- `s_` prefix: team default or opt-in per module?
