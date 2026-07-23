# ADR 0024: Kotlin-like DX, packages as subsystems, `when` / `class`

## Status

Accepted as **design baseline** (2026-07-23).

Umbrella: `docs/architecture/qpex-language-spec.md`.

Supersedes **surface spellings** in ADR 0017 (`span`) and ADR 0019
(keyword `system` / preferred `trait` wording) without changing joint /
mixture / capsule **semantics**.

Implementation Hold unchanged.

## Context

Agents need one integrated language story: physical axioms, scalable
namespaces (name collision + Hilbert-factor separation), and low-friction DX
for engineers familiar with Kotlin. Prior lexicon (`span`, `system`) was
physics-native but less familiar for large-module development.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Universal lift:** object-language runtime values are always `State<T>`
   (or `class` packages thereof). Literals elaborate to Dirac. No raw scalar
   islands mid-program. Strengthens ADR 0018.
2. **No null / None / exceptions:** model absence / failure as orthogonal
   basis labels under `when`; keep norm 1. Expanded in **ADR 0025**
   (`Success`/`Error` + `project`, no `throw`/`catch`).
3. **`package` / `import`:** namespaces are subsystem boundaries
   ($\mathcal{H}_A$); import enables safe composition as
   $\mathcal{H}_A \otimes \mathcal{H}_B$ without silent name aliasing.
4. **Surface `when`** replaces **`span`** (same denotation as formal §Span).
5. **Surface `class Name : Interface`** replaces keyword **`system`**.
6. Prefer surface **`interface`** for capabilities (AST may keep `TraitDef`);
   normative domain capability remains **`System`**.
7. **No `new`:** construction is `Foo(args)`.
8. **Extension functions** allowed; measure-free by default.
9. Normative function keyword DX: **`fn`** (Rust-aligned by ADR 0066).
10. AST must include `PackageDecl`, `ImportDecl`, `WhenExpr`, `ClassDecl`,
    `ExtFnDecl` (see `qpex-ast-design.md`).
11. Kernel PoC A/B fixtures need not migrate immediately.

## Consequences

Positive:

- One umbrella language spec for agents.
- Familiar DX without abandoning Never Leave the State.

Negative:

- Doc churn: examples using `span` / `system` / `fun` / `trait`.
- Tension with earlier “short physics keyword” aesthetic; packages add surface.

## Enforcement

Reject normative examples that reintroduce classical `if`, `new`, mid-program
`measure`, raw scalar runtime islands, or treat `when` as short-circuit
discard. Prefer `when`/`class`/`interface`/`fn` in new text.
