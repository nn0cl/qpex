# Agent sync addendum: entry point (ADR 0027 + ADR 0037)

Date: 2026-07-23 (amended with ADR 0037).

## Lock

- Entry: top-level `public fun main()` or `main(args: State<List<String>>)`.
- No classical `Int` return from `main`; end via terminal `measure` → sink.
- `measure` only as **last** stmt of `main` (`EARLY_COLLAPSE_ERROR` otherwise).
- AST: `MainDecl` / `EntryPoint`.
- **No implicit-main script sugar** (ADR **0037**). Top-level executables →
  `TOPLEVEL_EXECUTION_ERROR`.
- Inside `main`: Type-First (`Delta<Time> dt = 0.05.s`) + dimensional algebra
  (ADR 0037 / `qpex-dimensional-types.md`).

Canonical: `qpex-language-spec.md` §4; ADR 0027; ADR 0037.
Verification: SV-16 (structure), SV-15 (Type-First / dims).
