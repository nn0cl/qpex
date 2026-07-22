# QPex language specification (unified baseline)

Status: **Accepted** (2026-07-23). Umbrella for ADRs **0021–0035**
(plus axioms 0013–0018). Sync score **10 / 10**.
**Implementation Hold lifted** for Kernel PoC / parser / AST / typechecker
(ADR 0034). IR optimizer / full Float Math / styler enforcement remain
later-phase.

This document is the **umbrella** for surface syntax, modules, typing, entry,
I/O, and execution narrative. Detailed math:
`docs/specs/qpex-formal-semantics-sketch.md`. Companions:
`qpex-stdlib-combinators.md`, `qpex-stdlib-packages.md` (ADR 0031),
`qpex-runtime-execution-model.md` (ADR 0032),
`docs/style-guide/naming-conventions.md` (ADR 0023),
`docs/collaboration/spelling-cheat-sheet.md`,
`qpex-token-specification.md` (ADR 0035).

---

## 0. Design thesis

QPex fuses three constraints without compromise:

1. **Physical axioms** — Never Leave the State; joint store; terminal `measure`.
2. **Modern Kotlin-like DX** — familiar modules, `when`, constructors without
   `new`, extension methods.
3. **Scalable namespaces** — `package` / `import` as **subsystem boundaries**,
   not mere folders.

Prior surface spellings `span` and keyword `system` are **retired** in favor of
`when` and `class` (ADR 0024). Semantic laws are unchanged.

### Lock index (quick)

| ADR | Lock |
|-----|------|
| 0021 | `map` / `project` / `interfer` / `System` |
| 0022 | Fusion / Trace-Out / prune / deferred DAG |
| 0023 | Naming case / ancilla `_` |
| 0024 | `when` / `class` / `interface` / packages |
| 0025 | No exceptions; failure = world-line |
| 0026 | `fun` only; `Result<T,E>`; Vacuum; packages required |
| 0027 | `public fun main` + terminal `measure` |
| 0028 | No threads; concurrency = superposition |
| 0029 | Host I/O at boundaries; `measure to` / `snapshot` |
| 0030 | `inspect` non-destructive debug |
| 0031 | Stdlib packages (`qpex.math`, …) |
| 0032 | Runtime = DAG + data-parallel (not async VM) |
| 0033 | Immutable `class`; structural reentrancy |
| 0034 | Vacuum mini-spec; `State` compare → `State<Bool>`; Prelude; Hold unseal |
| 0035 | Lexer/Parser token triage (Active / Forbidden / Retired / `\|>`) |


---

## 1. Core laws

### 1.1 Never Leave the State

No early collapse, no destructive classical jump. Pure evaluation:

\[
\llbracket \mathsf{Stmt} \rrbracket : \mathsf{Joint} \to \mathsf{Joint}
\]

Sole nondeterminism:

\[
\llbracket \mathsf{Measure} \rrbracket
  : \mathsf{Joint} \times \mathsf{Rng} \to \mathsf{Joint}
\]

Forbidden as language law: mid-program `measure`, classical `if`/`while`/
`return`/`break` that discard world-lines.

### 1.2 Universal `State<T>` (no raw scalar runtime)

The object-language has **no** mid-program classical scalar islands.

- Every runtime value is `State<T>` (or a `class` packaging such coordinates).
- Numeric / string / bool **literals lift** automatically:

\[
\mathsf{lift}(c) = \delta_c = \mathsf{dirac}(c)
\]

Example: `0.01` in source is typed and evaluated as `State<Float>` with mass 1
on atom `0.01` (not a bare `float`).

- Classical `T` appears only (a) as lift inputs / type parameters, or (b)
  **after** terminal `measure` (host / sink).

Naming `ALL_CAPS` (`DT`, `PI`) still marks *fixed Dirac parameters* for
readers; their runtime type remains `State<T>` until measured (ADR 0023 + 0018).

### 1.3 No `null` / `None` / exceptions (failure = world-line)

The object-language has **no** `Exception`, `throw`, `try`, or `catch`.

#### Why exceptions are forbidden

`throw`/`catch` jumps out of the joint mid-computation. That would:

1. **Break the norm** — abandoned world-lines drop total probability below 1.
2. **Force early collapse** — deciding “which arm failed” decoheres the
   superposition (Early Collapse).

Both violate Never Leave the State.

#### How fallible computation is written

Failure is an **orthogonal basis label** coexisting with success inside one
`State<Result<T, E>>` (ADR 0026). Constructors `Success` / `Error` (or
equivalent) label arms. Programs never crash mid-pipeline; they carry error
arms to the end (or until an explicit `project` / `measure`).

```qpex
state result = when (coin()) {
    0 -> Success(data)
    else -> Error("Division by zero")
};

state next_result = result.map(res -> when (res) {
    Success(d) -> Success(d * 2)
    Error(msg) -> Error(msg)
});
```

Narrative: $\lvert\mathrm{Error}\rangle$ remains a living basis vector until
traced, projected, or measured.

#### Dropping failure arms

To keep only successful world-lines and **renormalize**, use `project`
(ADR 0021) — not exceptions:

```qpex
state valid_data = result.project(res -> res is Success);
```

When $Z=0$ (no mass on the predicate), **`project` does not throw**.
Normative (ADR **0034**): result is **`State.vacuum()`** /
$\lvert 0\rangle_{\mathrm{vac}}$ — all masses/amplitudes zero (norm $0$).
Pure ops on vacuum stay vacuum; `measure` on vacuum completes with no sample
(no throw). See §12 Appendix A.

#### Comparison

| Concept | `try` / `catch` | QPex |
|---------|-----------------|------|
| Control | Mid-program jump | Continuous $\mathsf{Joint}\to\mathsf{Joint}$ |
| Norm | Easily broken | Preserved (or explicitly renormalized by `project`) |
| Uncaught crash | Possible | Not expressible as language escape |

See ADR **0025**.

### 1.4 No threads / `async` / `await` (concurrency = superposition)

The object language has **no** `Thread`, `pthread`, `async`, `await`,
`spawn`, locks, or shared-mutable concurrent memory.

**Why:** `when` / joint evolution already denote that **all positively weighted
world-lines evolve together**. Explicit OS threads would reintroduce classical
scheduling, races, and mid-program observation pressure — fighting Never Leave
the State.

```qpex
// No Thread API — arms are concurrent in the model
state sys = when (state_choice) {
    0 -> heavy_physics_a()
    1 -> heavy_physics_b()
    2 -> heavy_physics_c()
};
```

**Background / multi-system work** is a **tensor / joint** of capsules, not a
thread pool:

```qpex
state joint_world = (sys_a, sys_b);
state next_world = joint_world.step();  // both factors advance in one pure step
```

**Engine note (not surface):** the runtime / IR **may** map independent support
atoms to SIMD / GPU / multi-core workers (ADR 0022 Deferred Pushforward). That
is an implementation schedule under a pure denotation — invisible in source.
Immutability ⇒ no data races in the object model.

See ADR **0028**. Implementer pipeline: ADR **0032**
(`qpex-runtime-execution-model.md`).

### 1.5 Immutable `class` — structural reentrancy (ADR 0033)

A `class` is an immutable capsule of `State<_>` fields. Methods are pure
transformers that **return a new** `class` / `State` value; they never
assign in place to `this` / `self`. Overlapping or recursive calls cannot
corrupt a shared mutable interior — there is none. Domain code needs no
`synchronized` / mutex. See `qpex-abstraction-model.md` §4b.

---

## 2. Packages and physical space

### 2.1 Why packages exist (not just folders)

Large programs collide on short physics names (`x`, `p`, `System`). Packages
solve that **and** give a physical reading:

> A `package` is the boundary of an independent **subsystem** /
> Hilbert factor $\mathcal{H}_A$.  
> `import` brings another factor $\mathcal{H}_B$ into scope; composition is
> treated as a **tensor / joint product** $\mathcal{H}_A \otimes \mathcal{H}_B$
> with **separate namespaces** so identically spelled locals do not silently
> alias across factors.

Folder layout may mirror package paths; the **semantic** unit is the subsystem
boundary, not the filesystem.

### 2.2 Surface

```qpex
package com.physics.optics;

import com.physics.core.System;

public class OpticalSystem : System {
    // …
}
```

| Form | Role |
|------|------|
| `package P;` | Declare this compilation unit’s namespace / subsystem id |
| `import Q.Name;` | Bring an external `class` / `interface` into scope |
| Qualified path | `com.physics.optics.OpticalSystem` when disambiguating |

Compiler obligations (design):

1. Identity of types is **package-qualified** (no global flat `System` clash).
2. Imported definitions do not merge joint axes until the program **composes**
   them in expressions / fields / tuples (correlation law still applies to
   shared axes). Composition is explicit: e.g. `(sys_a, sys_b)` or a
   wrapping `class` — narrative $\mathcal{H}_A \otimes \mathcal{H}_B$.
3. Same simple name in different packages remains distinct via qualified
   paths (`com.a.Foo` vs `com.b.Foo`).
4. Cyclic imports across packages are rejected or stratified (open detail).

### 2.3 Visibility (Kotlin-flavored)

MVP design: `public` on top-level `class` / `fun` / `interface` that escape the
package. Finer `internal` / `private` — open, follow Kotlin defaults later.

### 2.4 Requirement level (ADR 0026)

`package` (and `import` as needed) are **required** for compilation units that
declare `class` / `interface` / top-level `fun`. Kernel PoC A/B bare scripts
are temporarily exempt until the package fixture wave.

---

## 3. Kotlin-like syntax mapping

### 3.1 Vocabulary (normative surface)

| Role | Surface | Retired / alias |
|------|---------|-----------------|
| Bind joint coordinate | `state` | top-level `let` |
| Controlled superposition | **`when`** | `span` (semantic alias only) |
| Pure multi-step update | `evolve` | classical loops |
| Terminal collapse | `measure` | `observe` |
| Compound model | **`class` … `: System`** | keyword `system`; **immutable** (ADR 0033) |
| Capability interface | **`interface`** (or `trait`) | — |
| Module boundary | `package` / `import` | — |
| Construction | `Foo(args)` | **no `new`** |

Internal AST may keep historical names (`Span` ≡ `WhenExpr`) during migration.

### 3.2 No `new`

State preparation and class construction are **call-shaped**:

```qpex
state sys0 = Oscillator(dirac(1.0), dirac(0.0));
```

Literals inside args still lift (`5.0` → Dirac).

### 3.3 `when` — multi-arm superposition

`when` is **not** classical short-circuit `switch`. Every positively weighted
arm is kept (formal §Span / mixture). `else` is the wildcard arm (`_`).

```qpex
state choice = coin();
state sys1 = when (choice) {
    0 -> sys0.shift(5.0)
    1 -> sys0.shift(10.0)
    else -> sys0
};
```

Denotation: same controlled pushforward mixture as former `span`.

### 3.4 Extension functions

Users may attach pure operators to existing types (especially `State<T>` and
model `class`es) for dot-chains:

```qpex
fun State<Float>.shift(delta: State<Float>) -> State<Float> { /* pushforward */ }
```

Extensions are **measure-free** by default (ADR 0019 purity). Desugar to
static functions + method-call sugar in AST (`Call` / `MethodCall`).

### 3.5 Narrative program sketch

```qpex
package com.physics.simulation;

import com.physics.optics.Oscillator;

public fun main() {
    state sys0 = Oscillator(dirac(1.0), dirac(0.0));

    state choice = coin();
    state sys1 = when (choice) {
        0 -> sys0.shift(5.0)
        1 -> sys0.shift(10.0)
        else -> sys0
    };

    state sys_final = sys1.step();
    measure sys_final;
}
```

(`sys_final` follows ADR 0023 snake_case for states. Entry: ADR 0027.)

---

## 4. Entry Point & Execution Lifecycle

Status lock: **ADR 0027**.

### 4.1 Declaration and signature

The program entry point is a **top-level** (package-scoped) function:

```text
public fun main()
public fun main(args: State<List<String>>)
```

```qpex
package com.physics.simulation;

import com.physics.optics.Oscillator;

public fun main() {
    state sys0 = Oscillator(dirac(1.0), dirac(0.0));
    state sys_final = sys0.step();
    measure sys_final;
}
```

- Prefer **top-level** `public fun main` (not nested inside `class Main`), for
  Kotlin-script familiarity and a single obvious start glyph.
- `class Main { public static fun main … }` may be accepted later as sugar that
  desugars to the same `MainDecl`; not required for MVP.

### 4.2 Three iron rules

1. **No classical `Int` return from `main`.**  
   `main` is not a POSIX-style `int main`. The lifecycle ends by executing
   terminal `measure`, which writes the collapsed classical outcome through
   `MeasureSinkPort` (stdout / log). Host process exit codes are an **adapter**
   concern, not an object-language return type. Surface return type is
   effectively unit / void after measure.

2. **`args` are `State`.**  
   CLI arguments lift to `State<List<String>>` (typically Dirac on the argv
   list). Universal `State<T>` law is not broken at the boundary.

3. **`measure` only as the final statement of `main`.**  
   At most one `measure`, and it must be the **last** statement in that entry
   body. Mid-`main` `measure` is a compile error:
   `Early Collapse Error: measure is only allowed as the terminal statement of main`.

### 4.3 Execution lifecycle

```text
1. State Preparation
     argv / File.read* / host inputs → lift → State<_>
2. Pure State Evolution
     main body: when / map / project / interfer / class.step / Math.* / …
     → pure Joint→Joint DAG (Deferred Pushforward OK; RNG = 0; ADR 0032)
3. Terminal Measurement
     final `measure e` [to Sink] → one RngPort draw → Dirac collapse → sink
     → process ends  (file/network sinks: ADR 0029)
```

### 4.4 Compile-time checks

| Rule | Diagnostic (design) |
|------|---------------------|
| No `main` in a runnable package module | missing entry point (CLI mode) |
| `measure` not last in `main` | Early Collapse Error |
| `measure` outside `main` / Kernel script | rejected (or Kernel-script exemption) |
| More than one `measure` in `main` | rejected |
| `main` returns a typed classical `Int` | rejected — use measure sink |

### 4.5 Kernel PoC exemption

Bare PoC A/B scripts (`state`…`measure` without `package`/`main`) remain
valid until the entry-point fixture wave. They are sugar for an implicit
`main` whose body is the script and whose last stmt is `measure`.

---

## 5. Host I/O boundary (OS API)

Status lock: **ADR 0029**. Ports foundation: ADR 0015.

OS capabilities (files, network, stdio) are **indispensable** — and **forbidden
as free mid-evolution side effects**. They attach only to the **boundaries** of
the pure joint pipeline.

### 5.1 Why mid-pipeline `File.write` is illegal

Writing `x` to disk asks “which world-line’s atom?” That is Early Collapse /
decoherence mid-`main`, violating Never Leave the State.

### 5.2 Input — lift into `State`

Preparation APIs load host data as **`State<T>`**:

```qpex
package com.physics.simulation;

import qpex.io.File;

public fun main() {
    // Lift at boundary — aliases: readAsState / readText / readJson
    state initial_data = File.readAsState("initial_conditions.json");
    // state initial_data = File.readText("initial_conditions.json");  // same lift family
    state final_state = run_simulation(initial_data);
    measure final_state to File("output_result.json");
}
```

- Typical site: start of `main` (or explicit prep before pure evolution).
- `File.readText` / `readJson` / `readAsState` are **preparation lifts** into
  `State<_>` (ADR 0029 / 0031) — not mid-pure I/O.
- Uncertainty in the file may be encoded as a non-Dirac `State` (open detail).
- Implemented through ports (`StateSourcePort` / file adapter), not domain FS
  handles.

### 5.3 Output — `measure` destinations (sinks)

| Form | Meaning |
|------|---------|
| `measure e;` | Collapse + default sink (stdout / log) |
| `measure e to File("result.csv");` | Collapse + file sink |
| `measure e to <NetworkSink>;` | Collapse + send classical atom (later) |

Collapse law unchanged (semantics §9 / ADR 0027): one `RngPort` draw, Dirac
update, then sink the classical outcome.

### 5.4 Checkpoint — `snapshot` (non-collapsing host log)

For long `evolve` runs, host may log **without** collapsing the joint:

```qpex
state final_sys = evolve (sys0) {
    let next_sys = sys0.step();  // illustrative
    snapshot next_sys to File("log_step.csv");
    next_sys
};
```

| | `measure` | `snapshot` | `inspect` |
|-|-----------|------------|-----------|
| `RngPort` | Yes | **No** | **No** |
| Joint after | Dirac | **Unchanged** | **Unchanged** |
| Host effect | Classical atom | Joint/marginal file log | Formatted debug view |
| Where | Final `main` stmt | Evolve checkpoints | Anywhere in pure region |
| Returns | (ends program) | (stmt) | **Same `State` (passthrough)** |

Agents must not treat `snapshot` / `inspect` as terminal collapse.

### 5.5 Debug — `inspect` (non-destructive monitor)

Status lock: **ADR 0030**.

`inspect` prints the **in-memory distribution / amplitude table** and returns
the **same** state. It is **not** physical measurement.

**No scalar dependency:** object-language values remain `State<T>`. What
appears on the console is a **host-only text rendering** of that structure
(not a classical `Int` island and not a `State<String>` re-injected into the
graph).

```qpex
public fun main() {
    state x = dirac(10);
    x.inspect("x");
    // [DEBUG] x: State<Int> { |10⟩ (prob: 1.0) }

    state choice = coin();
    state y = when (choice) {
        0 -> dirac(100)
        else -> dirac(200)
    };
    y.inspect("y");
    // [DEBUG] y: State<Int> { |100⟩ : 50.0%, |200⟩ : 50.0% }

    measure y;
}
```

Dirac and mixtures share one format family so “certain” vs “superposed”
differs only in support cardinality / weights — never in type.

Why this is allowed: the Kernel already stores the PMF / vector as data;
`inspect` is a **read** of that structure (like a debugger watching memory),
whereas `measure` **samples and erases** other support atoms.

### 5.6 Ports map (design)

| Concern | Port / facade |
|---------|----------------|
| Entropy | `RngPort` |
| Program text | `SourcePort` |
| Classical measure output | `MeasureSinkPort` (+ file/network adapters) |
| Stateful load | `StateSourcePort` / `qpex.io.File.readAsState` |
| Snapshot / inspect log | `InspectSinkPort` / distribution-mode sink |

### 5.7 Reject

| Pattern | Why |
|---------|-----|
| `File.write(x)` inside pure `step` / `when` arm | Early collapse |
| Socket send of live `State` mid-pipeline | Same |
| Equating `snapshot` / `inspect` with `measure` | Wrong collapse law |
| Using `measure` only to print a PMF | Use `inspect` (ADR 0030) |

---

## 6. Standard library (pointer — ADR 0031)

Canonical package map: `docs/architecture/qpex-stdlib-packages.md`.

```text
qpex.math / qpex.state / qpex.collection / qpex.io / qpex.debug
```

**Math law:** APIs such as `Math.sin` have type `State<Float> → State<Float>`
(pointwise `map` / pushforward), never classical `Float → Float` as the
object-language surface. Extension sugar: `phase.sin()`.

**Debug:** `qpex.debug.Inspector.inspect` / `state.inspect(label)` — ADR 0030.

**I/O:** `qpex.io.File` — ADR 0029 (this §5).

Core combinators `map` / `project` / `interfer`: `qpex-stdlib-combinators.md`
(ADR 0021).

---

## 7. Naming conventions (pointer)

Canonical: `docs/style-guide/naming-conventions.md` (ADR 0023).

| Role | Form |
|------|------|
| States | `x`, `psi_0` |
| Ancilla | `_temp_x` |
| Constants (fixed Dirac) | `DT`, `MAX_STEPS` |
| `class` / `interface` | `Oscillator`, `System` |
| Packages | `com.physics.optics` (dot-separated lowercase) |
| Functions | `step`, `run_simulation` |

---

## 8. Lifting type-checker rule (normative)

### 5.1 Judgment sketch

```text
Γ ⊢ e : State<T>     // object-language expressions in pure regions
```

**Lit-Lift:**

```text
c is a literal of carrier T
─────────────────────────────
Γ ⊢ c : State<T>      // elaborates to dirac(c) / lift(c)
```

**Dirac / Coin:**

```text
Γ ⊢ dirac(c) : State<T>
Γ ⊢ coin()   : State<Int>     // {0,1} @ ½  (MVP)
```

**Pushforward ops** (`+`, method calls, extensions): require operands
`State<_>` (after insert-lifts); result `State<_>`.

**When:**

```text
Γ ⊢ scrutinee : State<C>
Γ ⊢ armᵢ : State<U>   (all arms same U after join)
────────────────────────────────────────────────
Γ ⊢ when (scrutinee) { arms } : State<U>
```

**Measure (program-final):**

```text
Γ ⊢ e : State<T>
───────────────────────────────
⊢ measure e : classical T   // host / sink; sole collapse
```

### Relational operators (ADR 0034)

Comparisons on `State` are pushforwards to **`State<Bool>`**:

```text
Γ ⊢ e1 : State<T>     Γ ⊢ e2 : State<T>     ⋈ ∈ {==,!=,<,<=,>,>=}
─────────────────────────────────────────────────────────────
Γ ⊢ e1 ⋈ e2 : State<Bool>
```

Thus `when (x >= y) { … }` is a mixture over boolean atoms — not classical
short-circuit `if`.

### Inserted coercions

The elaborator may insert `lift` on:

- lexical literals,
- `ALL_CAPS` constant bindings’ initializers,
- classical type-parameter defaults used as values.

It must **not** insert `measure` or sample.

### 5.3 Reject

| Pattern | Reason |
|---------|--------|
| Classical `if` on `State` | Early discard |
| Nullable types / `null` | Use `when` basis labels |
| `throw` / `try` / `catch` | Forbidden — use `Success`/`Error` + `when` / `project` (ADR 0025) |
| Raw `Int` parameter that stays unlifted in pure `fun` | Violates universal State |
| Keyword `fn` | Abolished — use `fun` (ADR 0026) |
| `Thread` / `async` / `await` / locks | Forbidden — use `when` / joint (ADR 0028) |
| In-place `this.field = …` mutation | Forbidden — return new `class` (ADR 0033) |
| Mid-program `measure` in Expr | Law |

---

## 9. AST obligations (summary)

See `qpex-ast-design.md`. Required module / DX nodes:

| Surface | AST |
|---------|-----|
| `package P;` | `PackageDecl` |
| `import Q.N;` | `ImportDecl` |
| `when (e) {…}` | `WhenExpr` (≡ former `Span`) |
| `class C : I {…}` | `ClassDecl` (replaces keyword `SystemDef` surface) |
| `interface I {…}` | `TraitDef` / `InterfaceDef` |
| `fun T.f(…) {…}` | `ExtFnDecl` |
| `Foo(args)` | `Call` / `CtorCall` (no `New` node) |
| `public fun main(…)` | `MainDecl` / `EntryPoint` | ADR 0027 |
| terminal `measure` in `main` | `Measure` (last stmt) | ADR 0027 |
| `measure e to Sink` | `Measure` + `sink` | ADR 0029 |
| `snapshot e to Sink` | `Snapshot` | ADR 0029 |
| `e.inspect(…)` | `Inspect` | ADR 0030 |
| `File.readAsState` | `Call` (effect-marked prep) | ADR 0029 |

---

## 10. Migration from prior baselines

| Old | New | Semantics |
|-----|-----|-----------|
| `span (c) {…}` | `when (c) {…}` | Unchanged mixture (§Span) |
| `system Foo : System` | `class Foo : System` | Unchanged capsule laws |
| `trait System` | `interface System` | Same capability |
| `fn` | `fun` | `fn` abolished (ADR 0026) |
| fallible ad-hoc | `Result<T, E>` | ADR 0026 |
| `project` $Z=0$ as exception / domain crash | → `Vacuum` (no throw) | ADR 0026 |
| `Thread` / `async` | `when` / `(sysA, sysB)` joint | ADR 0028 |
| In-place OOP mutation | Immutable `class` methods | ADR 0033 |
| `printf`/`measure` for PMF dump | `inspect` | ADR 0030 |
| Scalar `Math.sin` | `Math.sin: State→State` | ADR 0031 |
| Docs using `span` | Update examples to `when` | Fixtures may lag until PoC unseal |

Kernel PoC A/B fixtures remain minimal (`state` / `coin` / `dirac` /
`measure`) and are package-exempt (ADR 0026). Library/`class` units require
`package`. Prefer `when` in new examples.

---

## 11. Open questions

- Semicolons required or optional — open.
- `class Main { static fun main }` sugar vs top-level only — optional later.
- Package ↔ file path strictness; multi-file packages.
- Extension resolution / orphan rules.
- Default `E` in `Result<T, E>` when omitted — open (`String` vs `Symbol`).
- `snapshot` syntax / frequency / which marginal is logged — mini-spec.
- HDF5 / network sink adapters — post-MVP.
- `StateList.get` OOB → `Vacuum` vs `Result::Error` (lean Vacuum per 0034).
- Continuous `uniform` / `gaussian` representation (ADR 0031).
- Inspect pretty-print precision / amplitude glyphs (ADR 0030).
- Measure-on-vacuum host exit code / sink message defaults.

## 12. Appendix — P1 locks (ADR 0034)

### A. Vacuum

```qpex
state v = State.vacuum();           // or vacuum()
state w = some.project(pred);       // may be vacuum if Z=0
state u = Math.sin(w);              // still vacuum
measure w;                          // safe: no outcome / empty sink report
```

Laws: absorbing under pure ops; `measure` does not throw; not `null`.

### B. `State` comparisons → `State<Bool>`

```qpex
state ge = x >= y;                  // State<Bool>
state z = when (ge) {
    true -> x - y
    false -> dirac(0.0)
};
```

### C. Prelude (auto-import)

Every file receives without explicit `import`:

| Symbol / module | Notes |
|-----------------|-------|
| `qpex.state.*` | `dirac`, `coin`, `vacuum` / `State.vacuum` |
| `qpex.math.Math` | `sin`, `exp`, … as State→State |
| `qpex.debug.inspect` | `.inspect` method |
| `qpex.io.File` (selected) | `readAsState` / `readText`; measure destinations |

### D. Implementation unseal

Kernel PoC harness, parser, AST, and typechecker **may proceed** (AT-TDD).
Recommended order unchanged: PoC A/B → When/Block → Main/measure checks → …
