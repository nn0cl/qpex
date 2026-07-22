# Agent sync addendum: entry point (ADR 0027)

Date: 2026-07-23.

## Lock

- Entry: top-level `public fun main()` or `main(args: State<List<String>>)`.
- No classical `Int` return from `main`; end via terminal `measure` → sink.
- `measure` only as **last** stmt of `main` (Early Collapse Error otherwise).
- AST: `MainDecl` / `EntryPoint`.
- Kernel scripts = implicit `main` sugar (temporary).

Canonical: `qpex-language-spec.md` §4.
