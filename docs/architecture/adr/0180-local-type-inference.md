# ADR 0180: Local type inference (classical + safe state)

## Status

**Accepted** (2026-08-03) — Adjudicator「承認」
([WP-0089](../../work-plans/WP-0089-surface-adoption-and-sugar.md)).
Architecture Accept freezes the decision below. Kernel Red authorized via
linked LISS Kernel children. No axiom rewrite.

Original draft companions retained; open checklist frozen in §Acceptance record.

Companions: [surface-modernization north star](../surface-modernization-north-star.md);
[minimal dialect](../physicist-minimal-dialect.md); ADR 0095; ADR 0115 typed surface;
ADR 0176 experiment profile.

## Context

Teaching samples still require `Float J = 1.0`, `Operator H = …`, `state s0 = |+>`
on every line. That annotation noise reads as enterprise ceremony after package/
`main` wrappers were removed by the experiment profile. Modern notebook languages
infer obvious locals without erasing types from the public API.

Physicist-first constraint: inference must not blur Classical vs State, must not
invent mid-program collapse, and must fail closed on ambiguity.

## Dependency Adoption Evidence

Not applicable (language surface only).

## Decision

### Scope (local only)

1. **Eligible bindings** (when RHS has a unique elaboration type):
   - Classical numeric / unit literals and pure classical arithmetic
   - `Operator` algebra expressions with known operator result
   - Ket literals and pure Joint transformers when the RHS is already a State-forming form
   - `expect` / `dirac` / similar known factory results when unambiguous
2. **Still required annotations:**
   - Public / exported library API signatures (`pub fn`, fields that define contracts)
   - Ambiguous overload or Classical-vs-State dual readings
   - Explicit `State<T>` when the programmer documents the payload type for pedagogy
3. **Desugaring:** omitted type is filled by the typechecker; Host ABI and IR are unchanged.
4. **Fail-closed:** if both Classical and State elaborations fit, reject with a
   diagnostic that names both candidates (no silent pick).
5. **Type-First:** unit-carrying literals (e.g. `12.0.km`) already carry dimension;
   inferred locals keep those dims (no silent cast to bare `Float`).

### Explicit non-goals

- Global Hindley–Milner redesign or whole-program inference
- Inferring across module boundaries for `pub` APIs
- Restoring classical `if` / loops via “inferred control”
- Free-fn Call bind fixes for Type-First carriers (related, separate; see LISS-0277 notes)

### Teaching target (illustrative)

```text
// staqex-profile: experiment
J = 1.0
h = 0.5
H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
s0 = |+>
s1 = |+>
(s0, s1) = evolve (s0, s1) under H for 0.7 using Suzuki(order = 2, steps = 6)
measure s0 tracing_out s1
```

(`state` keyword may remain optional sugar for State-forming binds if Accept prefers
keeping the keyword as NLTS pedagogy.)

## Consequences

Positive:

- Shorter chalk; aligns with minimal dialect ideal
- Complements ADR 0176 without a second entry ABI

Negative:

- Diagnostics for ambiguity must be excellent or learners thrash
- Spec § typed surface needs a small amendment after Accept

## Enforcement

After Accept + Kernel Green:

- Red tests: positive inference cases + fail-closed Classical/State clash
- Official B08 may drop redundant annotations in LISS-0289

## Alternatives considered

| Option | Why not sole choice |
|---|---|
| Keep mandatory types forever | Leaves enterprise noise after profile ship |
| Infer everything including pub APIs | Hides library contracts |
| Only classical inference | Misses ket/Operator teaching lines |

## Acceptance checklist

- [x] Adjudicator Accept or amend (2026-08-03)
- [x] Classical vs State fail-closed rules frozen
- [x] Optional: bare `s0 = |+>` — `state` keyword retained for NLTS pedagogy
- [x] Kernel child LISS-0282 unblocked only on Accept

## Residual conformance (post–0282 / 0289)

Intake 2026-08-03: typecheck updates `env` for some inferred binds but often
leaves `StateBind.ty is None`. QASM lower and classical Call evaluation still
require explicit `ty`. Tracked as Kernel conformance (not a new ADR):
[LISS-0290](../../issues/LISS-0290-adr-0180-residuals.md).
Decision §3 (“omitted type is filled by the typechecker”) remains authoritative.