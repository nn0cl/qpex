# ADR 0037: Type-First declarations, dimensional algebra, structured units

## Status

Accepted (2026-07-23).

Companions:
- `docs/architecture/staqex-dimensional-types.md`
- `docs/architecture/staqex-type-system.md` (§Dimensional)
- `docs/testing/staqex-spec-verification-protocol.md` (SV-15, SV-16)
- Amends ADR **0027** (implicit-main sugar **retired**)

## Context

Physicists think **quantity-first** (“a length $x$”, “a time step $\mathrm{d}t$”),
not “declare a variable then annotate a type.” OOP unit libraries that model
`Meter extends Length` with `.add()` / `.multiply()` destroy algebraic
readability.

Independently, script-style top-level `state` / `measure` soup hid entry
points and scopes, conflicting with Kotlin-like DX (ADR 0024) and the
normative `pub fn main` lifecycle (ADR 0027, amended by ADR 0066).

The compiler already carries complex amplitudes (SV-14) and physical surface
syntax (`evolve`, tuple bind). This ADR locks the **declaration surface**,
**dimensional type algebra**, and **compilation-unit structure**.

## Dependency Adoption Evidence

Not applicable.

## Decision

### A. Type-First declarations (quantity as subject)

1. Normative bind form is **`Type name = expr`** (Type-First), e.g.
   `Delta<Time> dt = 0.05.s`, `Mass m = 1.0.kg`,
   `State<Length> x0 = dirac(1.0.m)`.
2. **`state name = expr`** remains legal sugar for an inferred `State<_>`
   bind (no explicit quantity head). Tuple form
   `state (x, p) = …` and bare `(x, p) = …` inside `main` are allowed.
3. Classical / Kotlin-like **`val name: Type = …`** and mid-program raw
   classical binders are **not** part of the object language (unchanged
   Never Leave the State). Any future `val` keyword is **retired /
   non-normative** — do not revive as Type-First sugar.
4. Unit suffixes on numeric literals (`0.05.s`, `1.0.kg`, `1.0.N_m`,
   `1.0.kg_m_s`, …) are **compile-time dimension tags**. Runtime values
   remain bare magnitudes (floats / ints); dimensions do not allocate
   objects.

### B. Dimensional algebra (not class hierarchy)

1. Each quantity / `State` payload carries a dimension vector
   $\mathbf{d} = (L, M, T) \in \mathbb{Z}^3$ (extensible later with $I$,
   $\Theta$, …).
2. Named heads map to vectors, e.g. `Length → (1,0,0)`,
   `Momentum → (1,1,-1)`, `Delta<Q>` shares $\mathbf{d}(Q)$.
3. **Addition / subtraction** require identical $\mathbf{d}$; mismatch →
   **`DIMENSION_MISMATCH_ERROR`** (physicist-facing message, not cast /
   class hierarchy errors).
4. **Multiplication / division** add / subtract exponent vectors; the
   result type is inferred (e.g. $(\mathrm{d}t/m)\cdot p$ → `Length`).
5. Transcendental / phase formers (`sin`, `cos`, `exp`, `log`, `cis`,
   `phase` angle) require a **dimensionless** argument.
6. `evolve … for dt` requires `dt` to be `Time` / `Delta<Time>` (or an
   explicitly dimensionless step count). `evolve … times N` remains the
   discrete iteration form (integer literal).

This is **compile-time meta-arithmetic on exponents**, not an OOP unit
object model. No `class Meter extends Length`, no `.add()`.

### C. Structured compilation units (amends ADR 0027)

1. Top-level may contain only: optional **`package`**, **`import`**
   (including `staqex.math.*`), **`fn`**, **`class`**, **`interface`**.
2. Executable statements (`Type-First` / `state` / `evolve` / `measure` /
   `snapshot` / …) at top level → **`TOPLEVEL_EXECUTION_ERROR`**.
3. Runnable programs **must** place executables inside
   **`pub fn main() -> Unit { … }`** (or `main` with lifted `args`).
4. **Implicit-main script sugar is retired** (supersedes ADR 0027
   Decision §6). Library-only units without `main` remain valid.
5. `when` arms and `evolve` bodies continue to require `{ … }` blocks.

### D. Verification

| Suite | Locks |
|-------|--------|
| **SV-15** | Type-First parse; unit literals; dim-ok evolve; `x + dt` → `DIMENSION_MISMATCH_ERROR` |
| **SV-16** | `package` + `main` runs; top-level exec → `TOPLEVEL_EXECUTION_ERROR`; `import ….*` |

Hard diagnostic codes (compile / run gate):
`DIMENSION_MISMATCH_ERROR`, `TOPLEVEL_EXECUTION_ERROR`.

## Consequences

Positive:

- Blackboard-shaped surface: quantity heads the line; operators stay `+ - * /`.
- Dimensional safety without unit-object boilerplate.
- Clear entry / scope; no top-level script scatter.
- Spec ↔ compiler ↔ SV harness stay aligned.

Negative:

- Existing script-style snippets must wrap in `main` (test helper
  `as_main`).
- SI scale conversion (ms vs s) is out of MVP — suffixes tag dimension only.

## Enforcement

Reject:

- Normative docs or examples using `val x: Type = …` as Staqex object syntax.
- OOP unit hierarchies as the dimensional model.
- Top-level executable statements outside `main`.
- Implicit-main / script-desugar as a supported language mode.
- Dimensional errors phrased as classical cast / class-hierarchy failures.

Implementation anchors: `compiler/staqex/parser.py`,
`compiler/staqex/typecheck.py`, `compiler/staqex/dimensions.py`,
`examples/**/*.staqex`, `tests/spec_verification/suites/sv15_*.py`,
`sv16_*.py`.
