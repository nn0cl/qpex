# ADR 0034: Vacuum mini-spec, State comparisons, Prelude — Hold unseal

## Status

Accepted (2026-07-23). Adjudicator approval of language-spec re-audit P1.

Closes open P1 items from `doc-audit-language-spec-2026-07-23.md` /
`audit-10-criteria-language-spec-2026-07-23.md`.

Companions: `qpex-language-spec.md` §12 Appendix; type system; semantics §Project.

## Context

Sync score ~9.6–9.7 required Vacuum encoding, `State` relational ops, and a
prelude for DX before declaring Architecture completeness and unsealing
Kernel PoC / parser / AST work.

## Dependency Adoption Evidence

Not applicable.

## Decision

### A. Vacuum (replaces provisional ADR 0026 wording)

1. When `project` (or equivalent) yields $Z=0$, the result is the distinguished
   **vacuum state**, written `State.vacuum()` / surface sugar, denotation
   $\lvert 0\rangle_{\mathrm{vac}}$ — **all amplitudes / masses zero** on the
   carrier support (norm $0$), not an exception.
2. **Closure:** any pure op (`map`, arithmetic pushforward, `when` arm that
   receives vacuum, `class` field update from vacuum, etc.) on vacuum yields
   **vacuum** (absorbing element for pure evolution).
3. **`measure` on vacuum:** does **not** throw. Completes safely as
   “no outcome” / empty report via `MeasureSinkPort` (host may print
   `Vacuum` / exit policy adapter-defined). No `RngPort` draw required when
   support is empty.
4. Vacuum is **not** mid-program classical `null`.

### B. Relational operators on `State`

5. Ops `==`, `!=`, `<`, `<=`, `>`, `>=` on compatible `State<T>` are
   **pointwise pushforwards** producing **`State<Bool>`** (not classical
   `bool`). Masses follow the joint of operands (correlation law).
6. `when (x >= y) { … }` is well-typed: scrutinee is `State<Bool>` (or
   carrier that patterns as bool atoms).

### C. Prelude

7. Every compilation unit automatically imports (no explicit `import` needed):
   - `qpex.state.*` — at least `dirac`, `coin`, and `State.vacuum` /
     `vacuum()` as applicable
   - `qpex.math.Math` (static members / extensions)
   - `qpex.debug.inspect` (and method `.inspect`)
   - Selected `qpex.io.File` prep/sink helpers (`readAsState` / `readText` /
     measure-destination constructors as designed)
8. Explicit `import` may still shadow or extend; prelude is a default set.

### D. Hold unseal

9. **Architecture Path language design is Accepted at sync 10/10** for the
   locks in ADRs 0021–0034.
10. **Implementation Hold is lifted** for: Kernel PoC harness, parser, AST,
    typechecker (Lit-Lift / When / Main), and eval of Kernel fixtures.
11. Still deferred until later unseals: full stdlib Math/Float, IR optimizer
    passes (ADR 0022) as mandatory, styler/linter enforcement, QPU backends.

## Consequences

Positive:

- Closed P1 blockers; agents may start PoC code under AT-TDD.
- Vacuum + Bool mixtures keep Never Leave the State without exceptions.

Negative:

- Empty-support measure UX and process exit codes need adapter defaults.
- Prelude set may grow; document changes via ADR.

## Enforcement

Reject designs that throw on $Z=0$, return classical `bool` from `State`
comparisons mid-program, or require `import` for `coin`/`dirac`/`Math.sin`/
`inspect` in normative examples.
