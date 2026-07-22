# Agent sync: QPex architecture & syntax baseline

Status: **Canonical handoff** for other coding agents (Cursor / Claude / etc.).
Date: 2026-07-23. **Hold unsealed** (ADR 0034) for Kernel PoC / parser / AST / typechecker.

Read order for a fresh agent:

1. This file (sync snapshot).
2. `docs/collaboration/spelling-cheat-sheet.md` — old→new (ADR 0021–0035).
3. `docs/architecture/qpex-language-spec.md` — umbrella (§0 lock index).
3b. `docs/architecture/qpex-token-specification.md` — Step 2 tokens (ADR 0035).
4. `docs/collaboration/agent-sync-entry-point.md` — ADR 0027.
5. `docs/collaboration/agent-sync-host-io.md` / `agent-sync-inspect.md` — ADR 0029–0030.
6. `docs/collaboration/agent-sync-stdlib-packages.md` / `agent-sync-runtime-execution.md` — ADR 0031–0032.
7. `docs/collaboration/agent-sync-immutable-class.md` — ADR 0033.
8. `docs/architecture/qpex-positioning.md` — Language Law.
9. `docs/architecture/qpex-syntax-vocabulary.md` + `docs/style-guide/naming-conventions.md`.
10. `docs/architecture/qpex-type-system.md` / `qpex-abstraction-model.md`.
11. `docs/architecture/qpex-stdlib-combinators.md` / `qpex-stdlib-packages.md`.
12. `docs/architecture/qpex-compiler-optimizations.md` / `qpex-runtime-execution-model.md`.
13. `docs/specs/qpex-formal-semantics-sketch.md`.
14. `docs/architecture/qpex-ast-design.md`.
15. `tests/fixtures/poc/` — Kernel PoC A/B only.

Adjudicator **unsealed** Kernel PoC / parser / AST / typechecker (ADR 0034). Follow AT-TDD; IR optimizer / full Float Math / styler still later-phase.

---

## 1. Language Law (The Wedge)

- **Never Leave the State:** no early measurement/collapse; stay in superposition
  until terminal `measure`.
- Pure statements:

\[
\llbracket \mathsf{Stmt} \rrbracket : \mathsf{Joint} \to \mathsf{Joint}
\]

- Sole collapse:

\[
\llbracket \mathsf{Measure} \rrbracket : \mathsf{Joint} \times \mathsf{Rng} \to \mathsf{Joint}
\]

- **Types:** runtime values are `State<T>`; classical `T` only via lift or
  post-`measure` (ADR 0018 / `qpex-type-system.md`).
- Persona: quantum researcher reading narrative code beside Dirac / density /
  evolution notation.
- Reject classical `if` / `while` / `return` / `break` at axiom level.
- Keyboard law: lowercase ASCII, short keywords (~4–6 letters), home-row friendly
  (`measure` is 7 letters by physics preference).

---

## 2. Syntax ↔ narrative map

| Classical habit | QPex form | Role |
|-----------------|-----------|------|
| `let x = …` | `state x = …` | Bind joint coordinate |
| Bernoulli / ket prep | `coin()` / `dirac(c)` | State preparation |
| `if` / classical `switch` | `when (c) { … }` | Controlled mixture (no discard) |
| `while` / pipeline of ops | `evolve` + `{…}` block | Pure kernel; locals traced out |
| Block / stack frame | `{ let …; e }` | $U_{\mathrm{block}}:\mathsf{Joint}\to\mathsf{Joint}$ |
| Multi-return | `(a, b)` tuple | Joint extract; correlation kept |
| Modules | `package` / `import` | Subsystem borders (ADR 0024) |
| Operator chain | `|>` (reserved) | Compose pushforwards / unitaries |
| Parameterized $U(\theta)$ | Currying (reserved) | Operator factories |
| Module / object | `system` (ADR 0019) | Immutable compound joint + pure methods |
| Generics / traits | `<T>`, `trait` (ADR 0019) | Spaces over $T$; algebraic / operator axioms |
| `print` / sample mid-way | **forbidden** | Use terminal `measure` only |

### Examples

```qpex
state c = coin()
state x = dirac(5)

// binary sugar
state z = when (c) {
    0 -> x + 10
    1 -> x + 20
}

// multi-arm (match-style) — normative
state z = when (c) {
    0 -> {
        let a = x * 2
        a + 10
    },
    1 -> x + 20,
    else -> x + 30,
}

state (w1, w2) = evolve (z) {
    let a = z * 2
    let b = a + 5
    (a, b)
}

measure w1
```

---

## 3. AST policy

First-class: `StateBind`, `WhenExpr`, `BlockExpr`/`Block`, `Evolve`, `Measure`,
`Tuple`, plus module nodes (`PackageDecl`, `ClassDecl`, …). **No** `If` /
`While` / `Return` / `Break` / `Throw`. Details:
`docs/architecture/qpex-ast-design.md`. Blocks are expressions
($\mathsf{Joint}\to\mathsf{Joint}$ kernels with trace-out), not stack frames.

---

## 4. Process status

| Item | Status |
|------|--------|
| Positioning manifesto | Accepted |
| Semantics §1–2; §9 measure (Project/Interfer = §7–8) | Accepted |
| Semantics §Span / §Block / §Evolve / §Tuple | Accepted (`when` surface ≡ §Span) |
| AST design note | Accepted |
| Stance (a) PMF → amplitude lift | ADR 0016 |
| Surface vocabulary | ADR 0017 |
| `State<T>` lift / classical boundary | ADR 0018 |
| Generics / interface / class (laws) | ADR 0019 + surface ADR 0024 |
| `map` / `project` / `interfer` / `System` | ADR 0021 (supersedes 0020 names) |
| Quantum-native opts (fusion / trace-out / prune / defer) | ADR 0022 (design; IR Hold) |
| Naming conventions (case / ancilla `_` / Greek) | ADR 0023 (style; linter Hold) |
| Language spec / packages / `when` / `class` / lift | ADR 0024 |
| Failure = world-line; no exceptions | ADR 0025 |
| `fun` / `Result` / Vacuum / packages required | ADR 0026 |
| Entry `public fun main` + terminal measure | ADR 0027 |
| No threads; concurrency = when / joint | ADR 0028 |
| Host I/O at boundaries only (measure/snapshot) | ADR 0029 |
| `inspect` non-destructive debug | ADR 0030 |
| Stdlib packages (`qpex.math`, …) | ADR 0031 |
| Runtime = DAG + data-parallel (not async VM) | ADR 0032 |
| Immutable class; structural reentrancy | ADR 0033 |
| Vacuum / State compare / Prelude / Hold unseal | ADR 0034 |
| Lexer/Parser token triage | ADR 0035 |
| Language umbrella sync | **10 / 10 Accepted** |
| Kernel PoC A/B fixtures | Design fixtures present |
| Harness / AST / parser / typechecker | **Unsealed** (start AT-TDD) |
| Full Float Math / IR opts / styler enforcement | Later-phase Hold |

**Open planning (2026-07-23):** examples-driven brush-up — LISS-0003…0006,
WP-0003, ADR **0060/0061 Proposed**. Do **not** implement Joint/linker changes
until Adjudicator Accepts those ADRs. Catalog rules:
`docs/collaboration/examples-catalog-conventions.md`.

---

## 5. Implementation order (Hold unsealed — ADR 0034)

1. Kernel harness against PoC A/B (no `when`/`evolve`/packages required).
2. AST + eval for Kernel nodes only.
3. Fixtures + eval for `WhenExpr` / `Block`, then `Evolve`/`Tuple` / `MainDecl`.
4. Packages / `class` / Prelude / Vacuum / `State<Bool>` compares.
5. IR / optimizer passes (ADR 0022) and full `Math` Float — later dedicated unseal.
