# QPex stdlib combinators and `interface System`

Status: **Working baseline** (2026-07-22). Normative names per **ADR 0021**.
Implementation **Hold**. Not Kernel PoC A/B scope.

Companions: ADR 0019–0021 / **0031**, `qpex-stdlib-packages.md`,
`qpex-abstraction-model.md`, formal semantics §Project / §Interfer,
`qpex-ast-design.md`.

---

## 0. Naming (normative)

| Role | Normative name | Retired spellings |
|------|----------------|-------------------|
| Pushforward on values | `map` | — |
| Subspace projection + renorm | `project` | `given`, `where`, `restrict`, `filter` |
| Combine / interfere list of states | `interfer` | `fold`, `combine` |
| Step-capable domain trait | `System` | `QSystem`, `Evolvable` |

All are pure $\mathsf{Joint}\to\mathsf{Joint}$ (or `system`→`system`). No RNG.
`project` ≠ `measure`.

---

## 1. `map` — pushforward

```text
fun map<T, U>(self: State<T>, f: T -> U) -> State<U>
```

\[
\llbracket \mathsf{map}(f) \rrbracket(\mu) = f_\#\mu
\]

Weights follow atoms (merge on collision). No renormalization beyond that.

```qpex
state x = coin()
state y = x.map(val => "Val: " + val)
```

---

## 2. `project` — projection + renormalization

```text
fun project<T>(self: State<T>, pred: T -> Bool) -> State<T>
```

### MVP (Discrete PMF) denotation

$A = \{ t \mid \mathrm{pred}(t) \}$, $Z = \sum_{t \in A} \mu(t)$.

- $Z = 0$: → **`State.vacuum()`** (ADR 0034); never throw; absorbing under pure ops.
- $Z > 0$: $\mu'(t) = \mathbf{1}_{A}(t)\,\mu(t)/Z$.

### Amplitude / density narrative (stance a lift)

With projector $P$ onto the subspace selected by `pred`,

\[
\rho' = \frac{P \rho P}{\mathrm{Tr}(P \rho P)}
\]

when the denominator is nonzero. MVP implements the classical-probability
shadow (phase 0) of this law.

### Laws

- Pure; no `RngPort`.
- Not terminal collapse: support may stay multi-atom.
- Classical “drop without renorm” is **forbidden**.

```qpex
state dice = uniform(1, 6)
state even_dice = dice.project(v => v % 2 == 0)
// {2,4,6} @ 1/3 each

// Failure arms: keep Success world-lines only (ADR 0025) — not exceptions
state valid = result.project(res -> res is Success)
```

---

## 3. `interfer` — combine / interfere states

```text
fun interfer<T, Acc>(
    items: List<State<T>>,
    init: Acc,                                 // lifts to Dirac State<Acc>
    f: (State<Acc>, State<T>) -> State<Acc>
) -> State<Acc>
```

### Denotation (default: independent list)

Form the product joint of list elements (fresh axes if independent), lift
`init`, then iterate pure combiner `f`. Example: three `coin()` → binomial
masses on $\{0,1,2,3\}$.

If elements share joint identity, **correlation law** applies (no silent
independent copies).

### Amplitude narrative

Combining amplitudes from multiple subsystems may produce constructive /
destructive interference under stance-(a) lift. MVP PMF `interfer` is the
non-negative shadow (masses add on merge; no negative interference until
amplitude IR).

```qpex
let coins = [coin(), coin(), coin()]
state sum = coins.interfer(0, (acc, c) => acc + c)
```

---

## 4. Generics and `interface System`

```qpex
interface System {
    fun step(self) -> Self
}

class Oscillator : System {
    state x: State<Float>
    state p: State<Float>

    fun step(self) -> Oscillator {
        Oscillator {
            x: self.x + self.p * 0.1,
            p: self.p - self.x * 0.1,
        }
    }
}

fun run_simulation<S: System>(sys: S) -> S {
    evolve (sys) {
        sys.step()
    }
}
```

Laws: measure-free methods (ADR 0019); classical `steps`/`dt` only as
parameters when `times` / `evolve_dt` exist; immutable return of new `Self`.

---

## 5. `Result<T, E>` (fallible carrier)

Locked name (ADR 0026). Typical use:

```qpex
state r: State<Result<Int, String>> = when (coin()) {
    0 -> Success(dirac(1))
    else -> Error("boom")
}
state ok = r.project(x -> x is Success)  // Z=0 → Vacuum
```

## 6. Kernel vs later

| Item | Kernel A/B | Design |
|------|------------|--------|
| `map` / `project` / `interfer` | No | Yes |
| `interface System` / `class Oscillator` | No | Yes |
| `uniform` helper | No | TBD |

---

## 7. Package map

See `qpex-stdlib-packages.md` (ADR 0031): `math` / `io` / `state` / `collection`
/ `debug`. Combinators here are the `State` core.

## 8. Open follow-ups

- Method sugar (`x.project(p)` vs `project(x, p)`).
- `project` inside multi-field `system` joints.
- Continuous predicates on `State<Float>`.
- When amplitude `interfer` diverges from PMF shadow — ADR 0016 lift tests.
