# QPex Language Specification

| Field | Value |
|-------|-------|
| Status | **Normative Draft v0.1** (2026-07-23) |
| Conformance target | Reimplementable compiler / interpreter |
| Decision log | ADR 0013–0069 in `docs/architecture/adr/` |
| Architecture umbrella | `docs/architecture/qpex-language-spec.md` |
| Formal grammar | [`grammar/qpex.ebnf`](grammar/qpex.ebnf) |
| Verification | `docs/testing/qpex-spec-verification-protocol.md` (SV-01–SV-17) |

**Normative** text defines required behavior. **Informative** text aids understanding
and must not contradict Normative rules. Implementation strategies (host language
data structures, GC, etc.) are **non-normative**.

**Conformance:** An implementation conforms if it accepts all Valid programs in
this document (and the SV harness), rejects Invalid programs with the stated
diagnostic codes, and matches the semantic evaluation rules of §5.

**Official examples fidelity:** Programs under `examples/` that name a physical
model (e.g. “quantum walk”) MUST realize that model’s definition; mislabeling a
classical process as quantum is a documentation defect.

---

## 1. Introduction

### 1.1 Purpose and design thesis

QPex（キューペックス） is a quantum–probabilistic programming language for
physicists. Source programs describe **joint state evolution**; classical
collapse occurs only at a terminal **`measure`**.

Three non-negotiable constraints:

1. **Never Leave the State** — mid-program values are `State<T>` in a joint store.
2. **Kotlin-like DX** — `package` / `fn` / `when` / `class` without classical
   `if` / `while` / exceptions / threads.
3. **Blackboard surface** — Type-First quantities, dimensional algebra, Dirac
   kets, Hamiltonian evolve, non-destructive `expect`.

### 1.2 Execution model (Normative summary)

- **Store:** a finite-support **Joint** over named coordinates; each world carries
  a complex amplitude $c$ with Born weight $|c|^2$.
- **Pure statements:** $\llbracket S \rrbracket : \mathsf{Joint}\to\mathsf{Joint}$
  (deterministic transformers).
- **Sole nondeterminism:** terminal `measure` draws once via host RNG.
- **Evaluation order:** left-to-right for binary operators; arguments left-to-right.
- **Concurrency:** object-language threads are forbidden; parallelism is an
  engine concern (ADR 0028 / 0032).
- **Host execution:** execution lifecycle is outside the language. The
  provider-neutral Job/JobResult contract is proposed by ADR 0065; it does not
  add Job/Task syntax to QPex.
- **QPU classical boundary:** ADR 0069 defines a QPU lane where
  ordinary classical runtime control is absent and static `forEach` is
  elaborated before backend submission. See the companion specification for
  the review boundary; it is not yet a conformance feature.
- **Static Hilbert shape:** the normative surface is type-level
  `QubitRegister<N>`; historical `register(N)` is rejected in the static
  `forEach` boundary. MVP resource checks are explicit; target profiles remain
  a later backend concern.
- **Parametric / Dynamic lanes:** ADR 0070 and ADR 0071 are proposed separate
  extensions and are not part of this normative conformance target.

### 1.3 Terminology

| Term | Meaning |
|------|---------|
| **Value** | Always a `State` (distribution / amplitude support), never a mid-program raw scalar island |
| **Joint** | Finite map from assignments of coordinate names → complex amplitude |
| **Vacuum** | Empty support; norm $0$ |
| **Lit-Lift** | Literals lift to Dirac `State` |
| **measure** | Terminal collapse to one classical outcome |
| **Type-First** | Declaration form `Q name = expr` (quantity heads the line) |
| **Dimension** | Exponent vector $\mathbf{d}=(L,M,T)$ |

### 1.4 Valid / Invalid

```qpex
(* Valid *)
package com.demo
pub fn main() -> Unit {
    state x = dirac(1)
    measure x
}
```

```qpex
(* Invalid — Forbidden keyword *)
pub fn main() -> Unit {
    if (true) { }   (* FORBIDDEN_KEYWORD *)
}
```

---

## 2. Lexical Structure

Normative companion: `docs/architecture/qpex-token-specification.md` (ADR 0035).
Full productions: [`grammar/qpex.ebnf`](grammar/qpex.ebnf).

### 2.1 Character set and case

- Source encoding: UTF-8.
- Identifiers: ASCII `letter (letter | digit)*` with `letter = [A-Za-z_]`.
- **Case-sensitive** (`state` ≠ `State`).

### 2.2 Comments and whitespace

- Line comments: `//` to end of line.
- Whitespace separates tokens; indentation is **not** significant (no off-side rule).
- Newline before `(` after a primary **does not** start a call (tuple / evolve safety).

### 2.3 Literals

| Form | Example | Notes |
|------|---------|-------|
| Integer | `42` | Lit-Lift → `State<Int>` |
| Float | `0.05` | Lit-Lift → `State<Float>` |
| Unit suffix | `0.05.s`, `1.0.kg` | Attr on numeric → dimension tag (runtime magnitude only) |
| Boolean | `true`, `false` | Contextual keywords |
| String | `"…"`, `'…'` | |
| Ket | `\|0>`, `\|+>`, `\|->`, `\|01>` | `KetLit` (ADR 0038) |

### 2.4 Keyword triage

| Class | Role |
|-------|------|
| **Active** | Grammar keywords (`state`, `when`, `evolve`, …) |
| **Contextual** | Soft: `else`, `times`, `for`, `under`, … |
| **Forbidden** | Hard error `FORBIDDEN_KEYWORD` (`if`, `while`, `null`, `throw`, `async`, …) |
| **Retired** | `RETIRED_KEYWORD` + fix-it (`observe`→`measure`, `span`→`when`, …) |

Bare C-style `for (` is ungrammatical. Lexeme `for` is contextual inside
`evolve … for …` only.

### 2.5 Valid / Invalid

```qpex
(* Valid *)
state psi = |+>
Delta<Time> dt = 0.5.s
```

```qpex
(* Invalid *)
state x = null    (* FORBIDDEN_KEYWORD *)
```

---

## 3. Syntax and Grammar

Normative grammar file: [`grammar/qpex.ebnf`](grammar/qpex.ebnf).

### 3.1 Statements vs expressions

- **Statements** (in `main` / blocks): binds, `measure`, `snapshot`.
- **Expressions:** yield `State` values (or lift to them); include `when`,
  `evolve`, calls, arithmetic, kets.

### 3.2 Operator precedence (low → high)

| Level | Operators | Associativity |
|-------|-----------|---------------|
| 1 | `\|>` | left |
| 2 | `== != < <= > >=` | left |
| 3 | `+ -` | left |
| 4 | `* /` | left |
| 5 | `*|*` (tensor) | left |
| 6 | unary `-` | right |
| 7 | call `f(…)` / attr `.` | left |
| 8 | primary | — |

### 3.3 Program structure (Normative — ADR 0037)

Top-level may contain only: `package`, `import`, `fn`, `class`, `interface`.

Executable statements at top level → **`TOPLEVEL_EXECUTION_ERROR`**.

Runnable programs place executables in **`pub fn main() -> Unit { … }`**.

Ordinary functions and class methods may declare a result type and end with a
single terminal expression:

```qpex
fn add(a: State<Int>, b: State<Int>) -> State<Int> {
    return a + b
}
```

The terminal `return` expression is a pure result. The result
may remain a `State<T>` and therefore does not constitute observation.

Type-First: `Type name = expr` (e.g. `Mass m = 1.0.kg`,
`Operator H = N + 0.5`, `State<(Qubit, Position)> (c, x) = …` — ADR 0044).
Sugar: `state name = expr`, `(x, p) = expr`.

### 3.4 Control and evolution forms

```text
when (ctrl) { pat -> expr, … else -> expr }
evolve (seeds) times N { let…; result }
evolve (seeds) for duration { let…; result }
evolve seed under H for t
```

**Nested `when` is illegal (Normative — ADR 0039).** Arm bodies MUST NOT
contain another `when`. Diagnostic: **`NESTED_WHEN_ERROR`**. Aligns with
OpenQASM / QIR: branching on unmeasured quantum wires is not expressible;
use `cnot` / `evolve` / `expect`, `project`, or a joint pushforward
(`s0 == s1`, `b0 * 2 + b1`).

Single-level `when` remains the Discrete mixture form (ADR 0024).

### 3.5 Valid / Invalid

```qpex
(* Valid *)
pub fn main() -> Unit {
    state (x, p) = evolve (x0, p0) times 2 {
        (x + 0.5 * p, p - 0.5 * x)
    }
    measure x
}
```

```qpex
(* Valid — joint pushforward, not nested when *)
pub fn main() -> Unit {
    state s0 = coin()
    state s1 = coin()
    state agree = when (s0 == s1) { true -> 1, else -> 0 }
    measure agree
}
```

```qpex
(* Invalid — nested when *)
pub fn main() -> Unit {
    state s0 = coin()
    state s1 = coin()
    state agree = when (s0) {
      0 -> when (s1) { 0 -> 1, else -> 0 },
      else -> when (s1) { 0 -> 0, else -> 1 },
    }   (* NESTED_WHEN_ERROR *)
    measure agree
}
```

```qpex
(* Invalid — top-level exec *)
state x = dirac(1)   (* TOPLEVEL_EXECUTION_ERROR *)
measure x
```

```qpex
(* Invalid — early collapse *)
pub fn main() -> Unit {
    state x = coin()
    measure x
    state y = x      (* EARLY_COLLAPSE_ERROR *)
}
```

---

## 4. Type System and Dimensional Algebra

Companions: `qpex-type-system.md`, `qpex-dimensional-types.md` (ADR 0018, 0037).

### 4.1 Universal `State<T>`

Every object-language expression has kind `State` with a payload carrier
(`Int`, `Float`, `Bool`, `Length`, …). Mid-program classical islands are
forbidden. Literals Lit-Lift to Dirac states.

### 4.2 Type-First declarations

| Form | Meaning |
|------|---------|
| `Q name = expr` | Bind with quantity / dim of `Q` |
| `State<Q> name = expr` | Explicit State wrapper |
| `Delta<Q> name = expr` | Same $\mathbf{d}$ as `Q` |
| `state name = expr` | Inferred `State<_>` |

Non-normative: `val name: Type = …`.

Assignment checks declared vs inferred dimensions; mismatch →
**`DIMENSION_MISMATCH_ERROR`**.

### 4.3 Dimensional algebra

$\mathbf{d}=(L,M,T)\in\mathbb{Z}^3$.

| Op | Rule |
|----|------|
| `+`, `-` | Require identical $\mathbf{d}$ |
| `*` | Add exponents |
| `/` | Subtract exponents |
| `sin`/`cos`/`exp`/`log`/`cis`/`phase` angle | Argument dimensionless |
| `evolve … for dt` | `dt` is Time / `Delta<Time>` or dimensionless |

Diagnostic messages prefer quantity names: `[Length] vs [Time] — physically incompatible`.

### 4.4 Comparisons

Relational operators yield `State<Bool>` (superposition of truth values), not
classical short-circuit booleans.

### 4.5 Valid / Invalid

```qpex
(* Valid *)
pub fn main() -> Unit {
    Delta<Time> dt = 0.5.s
    Mass m = 1.0.kg
    State<Length> x = dirac(1.0.m)
    State<Momentum> p = dirac(0.0.kg_m_s)
    state y = x + (dt / m) * p
    measure y
}
```

```qpex
(* Invalid *)
pub fn main() -> Unit {
    State<Length> x = dirac(1.0.m)
    Delta<Time> dt = 0.5.s
    state bad = x + dt   (* DIMENSION_MISMATCH_ERROR *)
    measure bad
}
```

---

## 5. Semantics

Informative detail: `docs/specs/qpex-formal-semantics-sketch.md`.
This section is **Normative** for required observable behavior.

### 5.1 Joint and amplitudes

A Joint is a finite set of worlds $(a,c)$ with assignment $a$ and
$c\in\mathbb{C}$. Born marginal of coordinate $x$: $\sum |c|^2$ over worlds
with that $x$-value. Coalesce **sums amplitudes** on identical assignments.

### 5.2 Expression evaluation (pushforward)

Arithmetic and `when` act as pushforwards / mixtures on the joint. They MUST NOT
sample. `coin()` splits amplitudes with factor $1/\sqrt{2}$ on $\{0,1\}$.

### 5.3 Combinators (selected)

| Form | Behavior |
|------|----------|
| `map` | Pushforward on labels |
| `project(psi, k)` | Hilbert $\|k\rangle\langle k\|$ (Lüders + renorm); not a predicate |
| `interfer(a,b,…)` | Sum amplitude marginals; cancel → empty support; then renorm |
| `phase(src, θ[, only])` | Coordinate phase $e^{i\theta}$ (shared amp intact) |
| `grover_diffuse(src)` | Grover inversion-about-mean |
| `expect(O, psi)` / `expect(ZZ, a, b)` | Classical $\langle O\rangle$ — **not** `measure`-able |
| `cnot(ctrl, tgt)` | Computational CNOT; bind $t\oplus c$ (amps preserved) |
| `evolve … under H for t` | $U=e^{-iHt}$: Pauli / Fock `N`/`Q`/`P` / Position-grid `X`/`P` |
| `wavepacket(xmin,xmax,n,x0,σ)` | Gaussian on a uniform Position grid |
| `vacuum()` / `empty()` | $\|0\rangle$ prep / empty support |
| `left *|* right` | Tensor product of independent states / wire relabel (ADR 0041) |
| `trace_out(coord)` | Born partial trace over a coordinate; $\sqrt{p}$ amps on remainder |
| `apply(U, w…)` / `hadamard(w)` | Unitary on wires ($U\otimes I$); not $e^{-iHt}$ (ADR 0042) |
| `walk_shift(coin, pos)` | DTQW conditional shift |
| `capply(c, U, t…)` | Controlled-$U$ ($|0\rangle\langle0|\otimes I+|1\rangle\langle1|\otimes U$); ADR 0043 |
| `capply(c0,c1,…, U, t…)` / `toffoli` | $C^n(U)$ multi-ctrl (ADR 0046) |
| `ocapply(c…, U, t…)` | Open control: $U$ iff ctrls $\|0\rangle^{\otimes n}$ (ADR 0047) |
| `capply(a, !b, U, t)` | Mixed ●/○ polarities (ADR 0048) |

### 5.4 Control: `when`

Arms with positive weight are retained (no classical discard). Nested `when`
preserves correlation through the joint.

### 5.5 Block / Euler `evolve`

`evolve (seeds) times N { lets; result }` copies seeds to working names and
applies the body $N$ times as correlated pushforwards (`bind_multi`).

`for duration` validates Time dimension and runs one body step unless `times`
is also used in other forms.

### 5.6 Ket literals

| Ket | Prep |
|-----|------|
| `\|0>`, `\|1>` | Dirac |
| `\|+>` | Equal amp $1/\sqrt{2}$ on $\{0,1\}$ |
| `\|->` | $(|0\rangle-|1\rangle)/\sqrt{2}$ |
| `\|01>`… | Dirac on binary integer |

### 5.7 Measurement and Early Collapse

- At most one `measure`, and it MUST be the **last** statement of `main`.
- Mid-body `measure` → **`EARLY_COLLAPSE_ERROR`**.
- Vacuum measure reports vacuum; does not throw.

### 5.8 Failure model

No exceptions. Failure arms are world-lines (`Result` / `when` / `project`)
(ADR 0025).

### 5.9 Open / Deferred (explicitly non-normative for v0.1)

- `evolve … until` runtime repetition (grammar/type boundary is tracked by
  LISS-0012; execution remains deferred)
- Tensor-network / fully symbolic operator IR beyond Pauli-sum MVP (ADR 0050)
- Continuum / open-boundary $(x,p)$ HO — truncated Position grid with
  context-typed `X`/`P` shipped (ADR 0051/0053); infinite continuum still Open
- General Boolean / classical `!` on states — **Rejected**
- Full static proof of **every** pushforward (ADR 0045–0053 catch clear cases)
- SI scale conversion (`ms` vs `s` magnitudes)
- Full Float Math library beyond listed `Math.*`
- Continuous distributions

### 5.10 Valid / Invalid

```qpex
(* Valid — destructive interference → vacuum *)
pub fn main() -> Unit {
    state z = dirac(0)
    state zp = phase(z, pi)
    state out = interfer(z, zp)
    measure out
}
```

```qpex
(* Valid — Schrödinger *)
pub fn main() -> Unit {
    state psi0 = |0>
    state psi = evolve psi0 under X for 1.5707963267948966
    measure psi
}
```

---

## 6. Program Structure and Modules

### 6.1 Packages and imports

```text
package dotted.path
import qpex.math
import qpex.math.*
```

Packages namespace declarations. Same simple class name in different packages
must not collide (ADR 0024).

### 6.2 Entry point

```text
pub fn main() -> Unit
pub fn main(args: State<List<String>>) -> Unit
```

No classical `Int` return from `main`. Termination via terminal `measure`
(ADR 0027, amended by 0037).

ADR 0064 makes the explicit host-lifecycle signature `pub fn main(...) ->
Unit` normative. Bare `main` declarations are rejected with
`MISSING_RETURN_TYPE`; `init` is the only declaration without a return type.

### 6.3 Scopes

- `main` / `fn` bodies and `evolve` / `when` braces introduce nested scopes.
- Working names in `evolve` shadow seeds for the body duration.
- Library units without `main` are valid (no entry).
- Ordinary `fn` / method bodies must have a terminal `return` statement. `measure`
  and `snapshot` remain forbidden inside those measure-free boundaries.
- `main` has no ordinary quantum result and must terminate with its terminal
  `measure`.

### 6.4 Namespace, enum, struct, class (Normative — ADR 0055 / 0056)

- `namespace A.B { … }` flattens to qualified decl names (`A.B.Name`).
- `enum E { V0, V1 }` — values `E.V0`; Int/Float/String literals →
  `ENUM_TYPE_MISMATCH`.
- `struct S { val … }` — immutable value type; copy-on-pass; `S(…)` positional.
- `class C { … }` — reference system; `fn` methods; `this`; the terminal
  `return` expression in a method is the return value.
- `fn init(…)` — constructor; `C(…)` invokes `init` when present. Assigning
  `val` fields is allowed **only** inside `init`.
- Keywords: `fn` Active; `fn` Retired → `fn`; `new` Forbidden.

### 6.5 Visibility (Normative — ADR 0058 revised)

| Surface | Meaning |
|---------|---------|
| *(default)* | Module-private |
| `pub` | Public API |
| leading `_` (or legacy `private`) | Class-private / same-file |

- `protected` is **Forbidden** (no inheritance access).
- `module-info.qpex` is optional metadata; missing `exports` does **not**
  hard-fail local multi-file scripts.
- Diagnostics: `PRIVATE_ACCESS_VIOLATION_ERROR`, `MODULE_PRIVATE_ACCESS_ERROR`.

### 6.6 Valid / Invalid

```qpex
(* Invalid *)
package com.demo
Delta<Time> dt = 0.05.s   (* TOPLEVEL_EXECUTION_ERROR *)
```

```qpex
(* Invalid — class-private *)
class S { var _t: Float = 0.0 }
pub fn main() -> Unit {
  S s = S()
  Float x = s._t   (* PRIVATE_ACCESS_VIOLATION_ERROR *)
  measure x
}
```

---

## 7. Standard Library and Runtime Environment

### 7.1 Prelude (always in scope)

| Group | Names |
|-------|-------|
| Prep | `coin`, `dirac`, `vacuum` |
| Debug / boundary | `inspect`, `snapshot`, `measure` |
| Combinators | `map`, `project`, `interfer`, `phase`, `cis`, `diffuse`, `expect`, `cnot` |
| Facades | `Math`, `Complex` |

### 7.2 `Math` / `Complex`

- `Math.sin` / `cos` / `exp` / `sqrt` / `abs` / `log` / `tan` — pointwise
  pushforward on `State` (argument dims as §4).
- `Complex.cis(θ)` / `cis(θ)` — $e^{i\theta}$ prep.

### 7.3 Host I/O boundary (ADR 0029)

- `inspect` — non-destructive host table; identity on Joint.
- `snapshot … to sink` — non-collapsing log.
- `measure [to sink]` — collapse + classical write.
- `measure` is not a function return: `RngPort` samples, `MeasureSinkPort`
  emits (stdout by default), and the user or external host consumer observes
  that emission. QPex code cannot read the sampled value back.
- No free mid-evolution file/network side effects.

### 7.4 Backend targets (Informative — ADR 0036)

`qpex run --target cpu|gpu|qpu:*` selects evaluation / codegen after DAG IR.
Source remains portable (no vendor imports required).

### 7.5 Runtime architecture (Informative — ADR 0032)

Preferred engine model: pure DAG + data-parallel batching; not an
async/await object-language VM.

---

## 8. Appendix

### Appendix A — Full EBNF

See [`grammar/qpex.ebnf`](grammar/qpex.ebnf). That file is **Normative** and MUST
match `compiler/qpex/lexer.py` and `parser.py`. Drift is a specification bug.

### Appendix B — Diagnostic codes

| Code | Meaning |
|------|---------|
| `LEX_ERROR` | Illegal character / unterminated ket |
| `PARSE_ERROR` | Grammar violation |
| `FORBIDDEN_KEYWORD` | ADR 0035 Forbidden |
| `RETIRED_KEYWORD` | ADR 0035 Retired |
| `EARLY_COLLAPSE_ERROR` | Non-terminal `measure` |
| `NESTED_WHEN_ERROR` | Nested `when` on State (ADR 0039) |
| `INTERFER_INDEPENDENT_STATE_ERROR` | `interfer` without shared lineage |
| `EXPECT_CLASSICAL_ONLY_ERROR` | Mix `expect` scalar into State arith |
| `COIN_IN_EVOLVE_ERROR` | `coin()` inside `evolve` |
| `TOPLEVEL_EXECUTION_ERROR` | Exec stmt outside `main` |
| `DIMENSION_MISMATCH_ERROR` | Dimensional algebra failure |
| `PRODUCT_BIND_ERROR` | Product `State<(…)>` on a single name (ADR 0044) |
| `PRODUCT_ARITY_ERROR` | Product arity ≠ bind names |
| `PRODUCT_TYPE_MISMATCH` | Incompatible product component carriers |
| `NON_UNITARY_TRANSFORM_ERROR` | Non-isometric remap / non-unitary apply / bad H (ADR 0045–0052) |
| `TYPE_NOT_STATE` | Non-State expression where State required |
| `NORM_MISMATCH` | Harness: Born norm |
| `SUPERPOSITION_MISMATCH` | Harness: support / masses |
| `NOT_VACUUM` | Harness: expected Vacuum |
| `PACKAGE_RESOLVE_ERROR` | Import / namespace failure |
| `MODULE_NOT_FOUND_ERROR` | Unresolved user-module import (ADR 0054) |
| `ENUM_TYPE_MISMATCH` | Non-enum literal assigned to enum (ADR 0055) |
| `IMMUTABLE_ASSIGNMENT_ERROR` | Write to `val` / struct field (ADR 0056) |
| `PRIVATE_ACCESS_VIOLATION_ERROR` | `_` / private member outside class (ADR 0058) |
| `MODULE_PRIVATE_ACCESS_ERROR` | Non-`pub` symbol across modules (ADR 0058) |
| `UNEXPECTED_EXCEPTION` | Harness: object language must not throw |

Canonical list also lives in `docs/testing/qpex-spec-verification-protocol.md` §4;
the two tables MUST stay identical.

### Appendix C — ADR ↔ section ↔ SV suite

| ADR | Spec §§ | Suites |
|-----|---------|--------|
| 0013–0018 | §1, §4–§5 | SV-01 |
| 0024–0027 | §3, §6 | SV-02, SV-04, SV-06, SV-16 |
| 0025 | §5.8 | SV-03 |
| 0034 | §5.7 | SV-05 |
| 0031–0032 | §7 | SV-08 |
| 0035 | §2 | SV-06 |
| 0036 | §7.4 | SV-10, SV-11 |
| 0037 | §3.3, §4, §6 | SV-15, SV-16 |
| 0038 | §2.3, §5.3–§5.6 | SV-14, SV-17 |
| 0039 | §3.4 | SV-06 |
| 0040 | §5 (axioms) | SV-18 |
| 0041 | §3.2–§3.3, §5.3 | SV-19 |
| 0042 | §5.3 | SV-20 |
| 0043 | §5.3 | SV-21 |
| 0044 | §3.3, §5.3 | SV-22 |
| 0045 | §5.9 | SV-23 |
| 0046 | §5.3 | SV-24 |
| 0047 | §5.3 | SV-25 |
| 0048 | §5.3 | SV-26 |
| 0049 | §5.3 | SV-27 |
| 0050 | §5.3 | SV-28 |
| 0051 | §5.3 | SV-29 |
| 0052 | §5.3 / unitarity | SV-30 |
| 0053 | §5 surface | SV-23, SV-29, SV-30 |
| 0054 | §6 packages / import | SV-31 |
| 0055 | §6.4 namespace / enum | `tests/test_enum_support.py`, `tests/test_oop_namespace_enum_struct.py` |
| 0056 | §6.4 struct / class / `init` / `this` | `tests/test_modern_oop_and_visibility.py` |
| 0058 | §6.5 visibility `pub` / `_` | `tests/test_modern_oop_and_visibility.py`, `tests/test_encapsulation_and_module_info.py` |
| — | §5 (kernel) | SV-07, SV-13 |
| — | examples | SV-09 |

### Appendix D — Open / Deferred checklist

See §5.9. Implementations MAY reject deferred constructs with `PARSE_ERROR`
or document extensions as non-conforming profiles.

---

## Document history

| Version | Date | Notes |
|---------|------|-------|
| 0.1 | 2026-07-23 | Initial Normative Draft — Language Spec Consolidation |
| 0.1.1 | 2026-07-23 | §6.4–§6.5 OOP + modern visibility (ADR 0055–0058); diagnostics |
