# Staqex abstraction model: generics, traits, and `system`

Status: **Working baseline for design / research** (2026-07-22).

Surface update: prefer `class` / `interface` / `fn` (ADR 0024);
keyword `system` / `trait` / `fn` are retired spellings. Capsule
laws in this note still apply.
Implementation **Hold** (no stdlib / typechecker / harness yet).
Companions: `staqex-type-system.md`, ADR 0018–0019, formal semantics, AST design,
`agent-sync-staqex-baseline.md`.

---

## 1. Why these abstractions serve the Language Law

Never Leave the State demands that user abstractions also be
$\mathsf{Joint}\to\mathsf{Joint}$ (or packages thereof), not classical OOP
mutable objects with mid-method `measure`.

| Tool | Role under Staqex |
|------|-----------------|
| Generics `<T>` | Parameterize carriers / Hilbert-like spaces $\mathcal{H}_T$ |
| `trait` | Axiomatize algebraic / physical operator interfaces |
| `system` | Capsule for compound joints + pure methods (no inheritance) |

**Rejected:** class inheritance (`extends`) as the primary reuse model — it
encourages tangled mutable hierarchies and accidental classical control.

---

## 2. Generics — `State<T>` and polymorphic pure functions

```staqex
fn make_uniform<T>(val1: T, val2: T) -> State<T> {
    let c = coin()
    span (c) {
        0 => dirac(val1),
        1 => dirac(val2),
    }
}

state num_state: State<Int>    = make_uniform(10, 20)
state str_state: State<String> = make_uniform("Alice", "Bob")
```

### Laws

1. Type parameters `T` are **carriers** (ADR 0018). Arguments of type `T`
   lift to Dirac when entering `State` contexts.
2. A polymorphic `fn` that returns `State<_>` / `class` must be a **pure**
   transformer: no `measure` inside (static rule).
3. Mathematical reading: construct measures / states over an arbitrary set
   $T$ uniformly in $T$.

### Kernel scope

Generics in the surface language are **design-accepted**. Kernel PoC A/B do
not require `fn` / `<T>` — only monomorphic `State<Int>` arithmetic.

---

## 3. Traits — operator interfaces (not inheritance)

Prefer Rust-/Swift-like traits over OO inheritance.

```staqex
interface Additive<T> {
    fn add(self: State<T>, other: State<T>) -> State<T>
}

interface System {
    fn step(self) -> Self
}

fn run_simulation<S: System>(initial_sys: S, steps: Int) -> S {
    // `steps` is a classical *parameter* (compile-time / lifted bound),
    // not a measured mid-program scalar used for classical if.
    evolve (initial_sys) times steps {
        let s = initial_sys   // narrative; exact sugar TBD with `times`
        s.step()
    }
}
```

### Laws

1. Trait methods used on uncollapsed values must have types that stay in
   `State<_>` / `system` / `Self` where `Self` is uncollapsed.
2. Default method bodies, if any, inherit the no-`measure` rule.
3. Physical reading: traits name **axioms** (additive structure, unitary-like
   step, etc.), not class trees.

### Naming note

`Additive::add` is the trait-level story for the same pushforward already
denoted by surface `+` on `State<T>` (when `T` supports it).

---

## 4. `system` — compound capsule (immutable)

```staqex
class CoupledSystem<T> {
    state position: State<T>
    state momentum: State<T>

    fn shift(self, offset: T) -> CoupledSystem<T> {
        CoupledSystem {
            position: self.position + offset,
            momentum: self.momentum,
        }
    }
}
```

### Laws

1. Fields marked `state` are joint coordinates (possibly a named product /
   tensor-like packaging of axes).
2. Methods are **pure**: they return a **new** `system` value (new joint
   packaging). No in-place mutation of `self` that would fork classical
   identity mid-superposition.
3. Encapsulation: outer code touches internals only through pure methods
   (or explicit field projection if the design later allows read-only views
   that remain `State<_>`).
4. Physical reading: $\mathcal{H}_A \otimes \mathcal{H}_B$ (or classical
   product of carriers) plus a local pure operator family.

### Relation to `struct`

Narrative may say “struct-like.” Surface spelling is **`class`** (ADR 0024);
former keyword `system` is retired. Semantics remain Hilbert-/joint packaging,
not classical mutable records.

---

## 4b. Reentrancy and “OOP without mutation” (ADR 0033)

Classical OOP bugs (reentrancy corruption, lock deadlocks, shared mutable
races) come from **in-place field updates**. Staqex `class` methods must not do
that:

```staqex
pub class BankAccount {
    state balance: State<Float>;

    pub fn withdraw(amount: State<Float>): BankAccount {
        state new_balance = when (this.balance >= amount) {
            true -> this.balance - amount
            false -> this.balance
        };
        BankAccount(new_balance)  // new capsule; `this` unchanged
    }
}
```

Overlapping calls only build more DAG nodes / new values. The caller’s
`BankAccount` joint coordinates stay intact until rebound by `state` /
assignment-to-new-name patterns. No `synchronized` in domain code.

---

## 5. Integration map (engineer ↔ physicist)

| Modern PL concept | Staqex redefinition | Mathematical / physical meaning |
|-------------------|-------------------|----------------------------------|
| Generics `<T>` | `State<T>`, `class Foo<T>` | Family of spaces / measures over $T$ |
| Interface | `interface` of pure ops | Algebraic or operator axioms |
| Class / object | `class` + immutable methods | Compound system + local Hamiltonian-like maps |
| Inheritance | **Not adopted** | Prefer composition of classes / interfaces |
| `map` on collections | `State.map` pushforward | Apply $f$ to every basis atom |
| `filter` on collections | **`project`** (proj. + renorm) | $\Pi\rho\Pi/\mathrm{Tr}(\Pi\rho\Pi)$ shadow |
| `fold` on collections | **`interfer`** | Product + pure combine / interfere |
| Domain physics API | **`interface System`** | Measure-free `step` |

---

## 6. Standard-library direction

Normative design: `docs/architecture/staqex-stdlib-combinators.md` (ADR 0021).

| Combinator | Meaning under joint semantics | Status |
|------------|-------------------------------|--------|
| `map(f)` | Pushforward along $f : T \to U$ | Design accepted |
| `project(pred)` | Restrict + renormalize (≠ `measure`) | Design accepted (ADR 0021) |
| `interfer(…)` | Pure iterated `State` combine | Design accepted (ADR 0021) |
| `given` / `filter` / `fold` | Retired spellings | Migration only |
| `zip` / product | Expose / build correlation | Still open detail |

---

## 7. Static rules (design intent)

1. No `measure` inside `fn` / interface default / `class` method unless the
   function’s type is explicitly in a post-collapse / host effect API
   (not the default).
2. Classical parameters (`steps: Int`, `offset: T` before lift) are OK as
   **bound parameters** for pure kernels; they must not introduce classical
   `if` on measured bits mid-body.
3. `evolve … times n` (when specified) takes classical `n` or `State<Int>`
   with a defined pure unrolling story — open grammar (evolve repetition).

---

## 8. Open research

1. Exact surface for trait impl (`impl Additive<Int> for …` vs inherent ops).
2. Whether `system` values are first-class `Expr` nodes or declaration-only
   packages with construction expressions.
3. Variance / higher-kinded needs (`State<State<T>>` — likely forbidden or
   flattened).
4. Effect system: mark `measure`-capable functions vs pure kernels.
5. Conditioning combinator spelling — **`project`** (ADR 0021); do not use
   `filter`/`given` in new normative text.

---

## 9. Process

- Kernel PoC A/B: unchanged (no generics/traits/`system` required).
- Docs: this note + ADR 0019.
- Code: Hold until Adjudicator unseals abstraction-layer Phase work.
