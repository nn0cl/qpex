# QPex type system design note

Status: **Accepted baseline** (updated 2026-07-23). ADR **0037** locks
Type-First + dimensional algebra; see `qpex-dimensional-types.md`.
Companions: `qpex-language-spec.md` (ADR 0024 / 0037), positioning, formal
semantics, AST design, ADR 0018–0019 / 0024, `qpex-abstraction-model.md`,
`docs/collaboration/agent-sync-qpex-baseline.md`.

QPU-lane follow-up: [ADR 0069](adr/0069-kernel-static-hilbert-space.md)
defines the proposed type-level `QubitRegister<N>` boundary; [ADR 0070](adr/0070-parametric-circuit.md)
and [ADR 0071](adr/0071-dynamic-qpu-lane.md) remain separate follow-ups.

---

## 1. Principle (one sentence)

**Runtime first-class values are always `State<T>` (or `class` packages of
such coordinates). There is no mid-program raw scalar runtime.**  
Classical `T` appears only as (a) literals / compile-time constants / type
parameters that **lift** to Dirac `State<T>`, or (b) results **after**
terminal `measure`. Every overloaded op on `State<T>` is a **pushforward on
the joint**, never an early collapse. No `null` / `None` / exceptions —
absence / failure is an orthogonal `when` basis label (`Success`/`Error`); no exceptions (ADR 0024–0025).

Generics / `interface` / `class` are pure abstractions over that ontology —
see `qpex-abstraction-model.md`, ADR 0019 / 0024, and language-spec §5.

This keeps Never Leave the State: the object-language store is still one
$\mathsf{Joint}$, whose coordinate alphabets are typed carrier sets $T$.

---

## 2. Two layers — and how they must not split the runtime

```text
  Superposed (object-language runtime)
      state x : State<Int> = coin()     // lives in the joint
                    │
                    │  measure  (sole classicalization)
                    ▼
  Classical (meta / post-measure / host)
      v : Int = …                       // Dirac support size 1 after collapse,
                                        // or a source literal before lift
```

| Layer | Surface examples | Allowed when |
|-------|------------------|--------------|
| Superposed | `state x = …`, `State<T>` | Entire program until `measure` |
| Classical | `5`, `"admin"`, type params | Lift inputs; `measure` outputs; host report |

**Forbidden:** mid-program first-class classical binders that bypass the joint
(e.g. a runtime `int v = 5` island used to drive classical `if`). Literals are
sugar that immediately lift.

---

## 3. Carrier types `T` and superposed forms `State<T>`

| Category | Carrier `T` | Superposed | MVP Kernel | Notes |
|----------|-------------|------------|------------|-------|
| Integer | `Int` | `State<Int>` | **Yes** | Finite support ⊂ `i64` |
| Float | `Float` | `State<Float>` | Later | Discretization / approx TBD |
| Bool | `Bool` | `State<Bool>` | Later | Control for `when`; no short-circuit ops |
| String | `String` | `State<String>` | Research | Finite support of string atoms only |
| Symbol | `Symbol` | `State<Symbol>` | Research | Closed finite label set (better for exhaustiveness) |
| Tuple | `(T1,…,Tk)` | `State<(T1,…,Tk)>` | Design (§Tuple) | Compound subsystem |

MVP Kernel PoC A/B stay on `State<Int>` (bit / Dirac integers) only.

### Finite-support law

Every `State<T>` coordinate in a joint has a **finite** support
$S \subset T$. Open carriers (`String`, `Float`) do not imply infinite
runtime tables: only atoms that appear in the joint are stored.

---

## 4. Lifting (universal — Lit-Lift rule)

\[
\mathsf{lift} : T \to \mathsf{State}\langle T\rangle,
\qquad
\mathsf{lift}(c) = \delta_c
\]

**Normative (ADR 0024):** the elaborator treats every value-position literal as
already `State<T>`. There is no well-typed pure-region judgment
`Γ ⊢ e : T` for runtime expressions — only `Γ ⊢ e : State<T>` (or a `class`
of such fields).

Surface:

```qpex
state z = x + 10        // 10 elaborates to dirac(10) : State<Int>
state s = dirac("Hi")   // explicit prep (same type family)
let DT = 0.01           // DT : State<Float> (fixed Dirac; ALL_CAPS style)
```

### Core rules

```text
c is a literal of carrier T
─────────────────────────────  (Lit-Lift)
Γ ⊢ c : State<T>

Γ ⊢ e1 : State<T>     Γ ⊢ e2 : State<T>     ⊕ ∈ Ops(T)
─────────────────────────────────────────────────────
Γ ⊢ e1 ⊕ e2 : State<T>

Γ ⊢ scrutinee : State<C>
Γ ⊢ armᵢ : State<U>   (join arms)
────────────────────────────────────────────────
Γ ⊢ when (scrutinee) { arms } : State<U>

Γ ⊢ e : State<T>
───────────────────────────────  (program-final)
⊢ measure e  ⇝  classical T
```

Mixed sugar `State<T>` ⊕ apparent-`T` is always `State<T>` ⊕ `lift(T)` after
elaboration. The typechecker **must not** invent `measure` coercions.

---

## 5. Operations as pushforwards

### Relational ops (ADR 0034)

`$\bowtie \in \{=,\neq,<,\le,>,\ge\}$` on `State<T>` yields **`State<Bool>`** via pointwise pushforward on the joint (correlation law). Use as `when` scrutinee.

### Vacuum

`State.vacuum()` is a distinguished empty-support value (norm 0). Pure ops absorb into vacuum; see ADR 0034.


For $\oplus : T \times T \to T$ (or unary $f : T \to T$),

\[
\llbracket e_1 \oplus e_2 \rrbracket
  = f_{\oplus\#}\,\rho
\]

on the joint (correlation law unchanged: same name ⇒ same axis).

### MVP-allowed ops (Kernel + near-term)

| Carrier | Ops | Status |
|---------|-----|--------|
| `Int` | `+`, `-`, `*` | **Normative** (semantics §2, PoC A) |
| `String` | concatenation as `+` | **Design accepted; fixtures TBD** |
| `Bool` | used as `when` control | **Design**; `&&`/`\|\|`/`!` as pushforward TBD |
| `Symbol` | equality patterns in `when` | **Design** |

### Deferred / research (do not implement in Kernel)

| Op family | Why deferred |
|-----------|----------------|
| `/`, `%` on `State<Int>` | Support blow-up; non-integral images |
| Bitwise ops | Need explicit bit-width story |
| `Float` trig / exp | Continuous / approx policy (stance a) |
| Short-circuit `&&` / `\|\|` | Classical short-circuit = early discard; must be total pushforward / `when` |

---

## 6. Worked narratives

### Integers (already Kernel law)

```qpex
state x = coin()       // State<Int> support {0,1}
state y = dirac(5)     // State<Int>
state z = x + y        // State<Int> {5,6} @ ½ each
state w = x + x        // {0,2} @ ½ — never mass on 1
```

### Strings (design)

```qpex
state s1 = when (coin()) { "Hello, ", "Hi, " }
state s2 = dirac("World!")
state s3 = s1 + s2
// {"Hello, World!", "Hi, World!"} @ ½ each — still uncollapsed
```

### Symbols / strings as `when` patterns

```qpex
state role = span (coin()) { "admin", "user" }
state access = span (role) {
    "admin" => dirac(99),
    "user"  => dirac(1),
    _       => dirac(0),
}
```

Pattern arms are still §Span mixtures: no branch discard.

---

## 7. Relation to `Joint`

Types decorate **axes**, not a second store:

\[
\rho \in \mathcal{D}(T_1 \times \cdots \times T_n)
\]

`state x : State<Int>` means “coordinate $x$ has carrier `Int`.”  
Tuples `State<(T1,T2)>` are product carriers (semantics §Tuple).  
Blocks trace out local axes regardless of `T` (semantics §Block).

---

## 8. Open research / Adjudicator queue

1. **Type-First is normative** (ADR **0037**) — `Q name = expr` /
   `State<Q> name = expr`. Inferred `state name = expr` remains sugar.
   Classical `val x: Type = …` is **non-normative** (do not revive).
2. **`Symbol` vs `String`** — prefer `Symbol` for closed `when` exhaustiveness?
3. **`State<Float>` representation** — bins, exact rationals, or sample bags?
4. **Division and partial ops** — error mass? undefined atoms? forbid until ADR?
5. **Post-`measure` classical binders** — host-only, or object-language
   `let v = measure e` sugar (still only at end)?
6. **Generic `State<T>` in AST** — when to attach types to `Expr` nodes?
7. **Traits / `system` surface** — see `qpex-abstraction-model.md` §8.
8. **Extended dimension bases** ($I$, $\Theta$, …) and SI scale conversion —
   beyond MVP $(L,M,T)$ tags (ADR 0037 out-of-scope).

---

## 9. Doc & process checklist

- [x] Principle written (this file)
- [x] ADR 0018 (lift / classical boundary)
- [x] ADR 0037 + `qpex-dimensional-types.md` (Type-First / dims)
- [x] Cross-links from semantics §0 / agent-sync / AST / README
- [x] Generics / traits / `system` design (`qpex-abstraction-model.md`, ADR 0019)
- [ ] Future: fixtures for `State<String>` concat (not Kernel A/B)
- [ ] Hold: no harness / typechecker / stdlib code until unsealed

## 10. Abstraction layer (pointer)

Polymorphic functions, traits, and `system` capsules are specified in
`docs/architecture/qpex-abstraction-model.md`. They do not change Kernel PoC
A/B scope.
