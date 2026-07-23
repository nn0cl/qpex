# Agent sync addendum: Type-First + dimensions + structured units (ADR 0037)

Date: 2026-07-23.

## Lock

1. **Type-First:** `Q name = expr` / `State<Q> name = expr` normative.
   `state name = expr` = inferred sugar. **`val x: T = …` non-normative.**
2. **Dimensional algebra:** $\mathbf{d}=(L,M,T)$; `+`/`-` match; `*`/`/`
   add/sub exponents; mismatch → `DIMENSION_MISMATCH_ERROR`.
3. **Units:** `.m` / `.kg` / `.s` / … are compile-time tags; runtime = magnitude.
4. **Structure:** top-level = `package`/`import`/`fn`/`class`/`interface` only.
   Executables → inside `pub fn main() { … }`.
   Top-level exec → `TOPLEVEL_EXECUTION_ERROR`. Implicit-main **retired**.
5. **Verification:** SV-15 (Type-First / dims), SV-16 (structure).

Canonical: ADR 0037, `qpex-dimensional-types.md`, language-spec §4,
`qpex-spec-verification-protocol.md`.

Implementation: `compiler/qpex/{parser,typecheck,dimensions}.py`,
`examples/**/*.qpex`.
