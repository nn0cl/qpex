# QPex standard library packages

Status: **Working baseline** (2026-07-23). ADR **0031**.
Implementation **baseline** (Phase 3): `compiler/qpex/stdlib/`.
Kernel PoC A/B remain Discrete PMF; `Math.*` on Float is implemented as
pointwise pushforward.

Companions: `qpex-stdlib-combinators.md` (ADR 0021), `qpex-language-spec.md`
(§5 I/O, §5.5 inspect), ADR 0029–0030, type system (universal `State<T>`).

---

## 0. Design law

Every stdlib API in the object language takes and returns **`State<_>`**
(or `class` packages of such), except host-boundary facades that **lift into**
or **sink out of** the joint (ADR 0029). There is no `Math.sin(Double): Double`.

Pointwise classical carrier ops (`native_sin` on `Float` atoms) exist only
**inside** a pushforward / `map` — they are not mid-program scalar islands.

---

## 1. Package tree (required modules)

```text
qpex/
├── math/          # State→State operators (Math, Complex, LinearAlgebra)
├── io/            # Boundary I/O (File, Console, Network sinks)
├── state/         # Preparation / distributions (Distribution, …)
├── collection/    # Immutable state collections (StateList, StateMap)
└── debug/         # Non-destructive inspect (Inspector)
```

Core combinators `map` / `project` / `interfer` live on `State` (ADR 0021) and
are re-exported or inherent methods; not a separate package name required.

---

## 2. `qpex.math` — operators on distributions

### 2.1 `Math`

Elementary functions are **pointwise pushforwards** on `State<Float>`
(or richer carriers later):

```qpex
package qpex.math;

pub class Math {
    pub static fn sin(x: State<Float>): State<Float> {
        x.map(v -> native_sin(v))
    }
    pub static fn cos(x: State<Float>): State<Float> { /* … */ }
    pub static fn exp(x: State<Float>): State<Float> { /* … */ }
    pub static fn sqrt(x: State<Float>): State<Float> { /* … */ }
    pub static fn abs(x: State<Float>): State<Float> { /* … */ }
}
```

Surface DX: `Math.sin(phase)` and extension `phase.sin()` (desugar to the same
`map`). Example:

```qpex
state phase = when (coin()) {
    0 -> dirac(0.0)
    else -> dirac(1.57079632679)  // π/2
};
state sin_value = Math.sin(phase);
// ≈ State { |0⟩: ½, |1⟩: ½ }  (masses follow; merge if collision)
```

**Kernel PoC:** `State<Int>` `+,-,*` only. `Math.*` on `Float` is design-accepted,
fixtures later (stance a / continuous policy open).

### 2.2 `Complex` & `LinearAlgebra`

Design-accepted for amplitude lift (ADR 0016):

- `Complex` — build / map complex carriers under `State`.
- `LinearAlgebra.applyUnitary(U, psi)` — pure operator on amplitude IR when
  present; PMF MVP may stub or reject until lift.

---

## 3. `qpex.state` — preparation / distributions

```qpex
package qpex.state;

pub class Distribution {
    pub static fn <T> dirac(value: T): State<T>;
    pub static fn <T> vacuum(): State<T>;  // ADR 0034
    pub static fn coin(): State<Int>;              // fair bit (surface coin())
    pub static fn coin(p: State<Float>): State<Int>;
    pub static fn uniform(min: State<Float>, max: State<Float>): State<Float>;
    pub static fn gaussian(mean: State<Float>, std: State<Float>): State<Float>;
}
```

Surface builtins `coin()` / `dirac(c)` remain sugar / aliases into this module.
Continuous constructors need representation policy (bins / samples) — open.

---

## 4. `qpex.collection` — immutable state collections

```qpex
state items = StateList.of(dirac("Apple"), dirac("Banana"), dirac("Cherry"));
state index = coin();  // 0 or 1
state selected = items.get(index);  // State<String> mixture
```

Indexing by `State<Int>` is a pushforward over (list, index) joints — not a
classical bounds-check exception (use `Result` / `Vacuum` narratives per
ADR 0025–0026). Exact `StateList` / `StateMap` API — open detail.

---

## 5. `qpex.io` — boundary only (ADR 0029)

```qpex
package qpex.io;

pub class File {
    pub static fn readAsState(path: /* host path / State<String> */): State<String>;
    pub static fn readJson<T>(path: …): State<T>;
}
```

- Prep: read → `State<_>`.
- Out: `measure e to File("…")` / `snapshot` — not `File.write(State)` mid-pure.
- Path literals lift; host path strings are preparation-boundary inputs.

---

## 6. `qpex.debug` — non-destructive inspect (ADR 0030)

```qpex
package qpex.debug;

pub class Inspector {
    pub static fn <T> inspect(state: State<T>, label: String): State<T>;
}
```

Method sugar: `state.inspect(label)`. Host text only; identity on the joint.

---

## 7. Relation to Kernel PoC

| API | PoC A/B |
|-----|---------|
| `coin` / `dirac` / `+,-,*` / `measure` | Yes |
| `map` / `project` / `interfer` | Design; after When fixtures |
| `Math.sin` / Float / gaussian | Later |
| `File` / `inspect` / `StateList` | Later (ports / debug) |

---

## 8. Prelude (ADR 0034)

Auto-imported: `qpex.state.*` (incl. `vacuum`), `qpex.math.Math`,
`qpex.debug.inspect`, selected `qpex.io.File`.

## 9. Open questions

- Default import prelude (`coin`, `dirac`, `Math`)?
- `native_*` carrier ops: which Float lib; NaN / domain of `sqrt` under mixture?
- Continuous `uniform` / `gaussian` encoding.
- `StateList.get` OOB — prefer Vacuum (ADR 0034) vs Result — still open.
