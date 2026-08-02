# ADR 0183: Module-relative import

## Status

**Accepted** (2026-08-03) — Adjudicator「承認」
([WP-0089](../../work-plans/WP-0089-surface-adoption-and-sugar.md)).
Architecture Accept freezes the decision below. Kernel Red authorized via
linked LISS Kernel children. No axiom rewrite.

Original draft companions retained; open checklist frozen in §Acceptance record.

Companions: [ADR 0177](0177-import-use-ergonomics.md) selective import;
[package-root-naming](../package-root-naming.md); ADR 0054 modules.

## Context

Even after selective `{A,B}` import, multi-file S01 still repeats long absolute
roots:

```text
import examples.showcase.s01_disaster.domain.ops.{CommandBoard, OpsPhase}
```

Relative imports cut reverse-path noise without hiding dependencies (unlike
wildcard deep trees). Official package root is already short `examples.…`.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Relative import syntax (recommended primary):**

   ```text
   import .domain.ops.{CommandBoard, OpsPhase}
   import ..shared.utils.{helper}
   ```

   Leading `.` means “from this file’s package”; `..` walks package parents
   (or directory parents — Accept must freeze one model).

2. **Absolute imports remain valid forever** (`import examples.showcase…`).

3. **Selective braces** compose: `import .domain.ops.{A, B}`.

4. **No** official-sample wildcard of entire deep trees without review (ADR 0177 style).

5. Resolution remains fail-closed: ambiguous or missing targets →
   `MODULE_NOT_FOUND_ERROR` (or equivalent).

### Resolution model (to freeze on Accept)

| Option | Sketch |
|---|---|
| **A — package-relative** | `.` continues the current package path segments |
| **B — directory-relative** | `.` walks filesystem next to the source file |

Recommend **A** for alignment with package identity; B is friendlier for scripts.
Accept must pick one.

### Explicit non-goals

- Changing `pub` / visibility rules
- Implicit prelude of domain types

## Consequences

Positive:

- Shorter multi-file faces; S01 chapters less enterprise
- Complements selective import without replacing it

Negative:

- Two path forms (absolute + relative) increase learning surface slightly

## Enforcement

- Red: relative + selective resolves; absolute still works; broken relative fails closed
- S01 chapters may migrate in LISS-0289 after Green

## Alternatives considered

| Option | Note |
|---|---|
| Path aliases only | Less flexible |
| Force global prelude | Hides physics dependencies |

## Acceptance checklist

- [ ] Package-relative vs directory-relative frozen
- [ ] Exact tokens (`.` / `..` / `./`) frozen
- [ ] Adjudicator Accept
- [ ] Kernel child LISS-0288 unblocked only on Accept
