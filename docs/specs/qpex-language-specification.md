# QPex Language Specification

| Field | Value |
|-------|-------|
| Status | **Normative Draft v0.1** (2026-07-23) |
| Conformance target | Reimplementable compiler / interpreter |
| Decision log | ADR 0013–0046 in `docs/architecture/adr/` |
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
2. **Kotlin-like DX** — `package` / `fun` / `when` / `class` without classical
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
public fun main() {
    state x = dirac(1)
    measure x
}
```

```qpex
(* Invalid — Forbidden keyword *)
public fun main() {
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
| **Contextual** | Soft: `else`, `public`, `times`, `for`, `under`, … |
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

Top-level may contain only: `package`, `import`, `fun`, `class`, `interface`.

Executable statements at top level → **`TOPLEVEL_EXECUTION_ERROR`**.

Runnable programs place executables in **`public fun main() { … }`**.

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
public fun main() {
    state (x, p) = evolve (x0, p0) times 2 {
        (x + 0.5 * p, p - 0.5 * x)
    }
    measure x
}
```

```qpex
(* Valid — joint pushforward, not nested when *)
public fun main() {
    state s0 = coin()
    state s1 = coin()
    state agree = when (s0 == s1) { true -> 1, else -> 0 }
    measure agree
}
```

```qpex
(* Invalid — nested when *)
public fun main() {
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
public fun main() {
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
public fun main() {
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
public fun main() {
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
| `map` / `project` | Pushforward / keep arms matching predicate; all-reject → Vacuum |
| `interfer(a,b,…)` | Sum amplitude marginals per value; cancel → Vacuum; then renorm Born |
| `phase(src, θ[, only])` | Coordinate phase $e^{i\theta}$ (shared amp intact) |
| `diffuse(src)` | Grover inversion-about-mean on amplitude marginal |
| `expect(O, psi)` / `expect(ZZ, a, b)` | Dirac `Float` of $\langle O\rangle$ / $\langle Z\otimes Z\rangle$; **no collapse** |
| `cnot(ctrl, tgt)` | Computational CNOT; bind $t\oplus c$ (amps preserved) |
| `evolve … under H for t` | $U=e^{-iHt}$ (ℏ=1): named Pauli, or Type-First `Operator` (sites / Fock `N`) |
| `left *|* right` | Tensor product of independent states / wire relabel (ADR 0041) |
| `trace_out(coord)` | Born partial trace over a coordinate; $\sqrt{p}$ amps on remainder |
| `apply(U, w…)` / `hadamard(w)` | Unitary on wires ($U\otimes I$); not $e^{-iHt}$ (ADR 0042) |
| `shift(coin, pos)` | DTQW conditional shift $|c\rangle|x\rangle\mapsto|c\rangle|x+(2c-1)\rangle$ |
| `capply(c, U, t…)` | Controlled-$U$ ($|0\rangle\langle0|\otimes I+|1\rangle\langle1|\otimes U$); ADR 0043 |
| `capply(c0,c1,…, U, t…)` / `toffoli` | $C^n(U)$ multi-ctrl (ADR 0046) |

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

- `evolve … until` predicate
- Sparse / symbolic multi-qubit IR beyond dense MVP matrices
- Continuous $(x,p)$ quantum HO (Fock `N` is the MVP quantum oscillator)
- General open-control ($|0\rangle$-controlled) beyond $C^n(U)$ on $|1\rangle^{\otimes n}$
- Full static proof of **every** pushforward (MVP: ADR 0045 catches clear cases)
- SI scale conversion (`ms` vs `s` magnitudes)
- Full Float Math library beyond listed `Math.*`
- Continuous distributions

### 5.10 Valid / Invalid

```qpex
(* Valid — destructive interference → vacuum *)
public fun main() {
    state z = dirac(0)
    state zp = phase(z, 3.141592653589793)
    state out = interfer(z, zp)
    measure out
}
```

```qpex
(* Valid — Schrödinger *)
public fun main() {
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
public fun main()
public fun main(args: State<List<String>>)
```

No classical `Int` return from `main`. Termination via terminal `measure`
(ADR 0027, amended by 0037).

### 6.3 Scopes

- `main` / `fun` bodies and `evolve` / `when` braces introduce nested scopes.
- Working names in `evolve` shadow seeds for the body duration.
- Library units without `main` are valid (no entry).

### 6.4 Valid / Invalid

```qpex
(* Invalid *)
package com.demo
Delta<Time> dt = 0.05.s   (* TOPLEVEL_EXECUTION_ERROR *)
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
| `NON_UNITARY_TRANSFORM_ERROR` | Non-isometric remap / non-unitary apply (ADR 0045) |
| `TYPE_NOT_STATE` | Non-State expression where State required |
| `NORM_MISMATCH` | Harness: Born norm |
| `SUPERPOSITION_MISMATCH` | Harness: support / masses |
| `NOT_VACUUM` | Harness: expected Vacuum |
| `PACKAGE_RESOLVE_ERROR` | Import / namespace failure |
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
