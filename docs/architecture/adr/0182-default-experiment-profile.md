# ADR 0182: Default experiment profile (marker optional)

## Status

**Proposed** (2026-08-03) — Architecture candidate under
[WP-0089](../../work-plans/WP-0089-surface-adoption-and-sugar.md) /
[LISS-0285](../../issues/LISS-0285-adr-default-experiment-profile.md).
Does **not** authorize Kernel Red ([LISS-0286](../../issues/LISS-0286-kernel-default-experiment-profile.md))
until Adjudicator **Accept**.

Companions: [ADR 0176](0176-experiment-surface-profile.md) (**Accepted**);
[package-root-naming](../package-root-naming.md).

## Context

ADR 0176 shipped `// staqex-profile: experiment` as a **source-visible** marker.
That marker is itself meta-ceremony. Single-file chalk programs with no package
and bare top-level statements should default to the experiment profile so the
marker is optional for the common teaching case.

Multi-file / packaged libraries must not silently enter experiment desugaring.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Default experiment profile** when **all** of the following hold:
   - No `package` declaration in the entry file, and
   - No explicit `// staqex-profile: …` line (or profile is `experiment`), and
   - Entry is a single compilation unit without cross-package imports that require
     a non-default package identity  
   **OR** (Accept may narrow) only the first bullet — no package ⇒ experiment.
2. **Explicit marker** `// staqex-profile: experiment` remains valid and recommended
   in official basics for honesty until default ships and docs catch up.
3. **Multi-file packages** (`package examples.…`) keep classic `pub fn main` rules;
   no silent bare-main desugar for packaged entries.
4. Host entry ABI remains `main -> Unit` after desugar (ADR 0176).
5. Interaction with `// staqex-lane:` unchanged (ADR 0178).

### Explicit non-goals

- Deleting packages
- Second entry semantics
- Auto-profile for multi-package S01 trees

## Consequences

Positive:

- Ideal notebook face needs no meta-comment
- Aligns with minimal dialect “≈10 lines”

Negative:

- Need clear diagnostics when bare statements appear under a package by mistake

## Enforcement

- Red: no-package bare body runs without marker; packaged entry without main still errors
- Basics may drop markers in LISS-0289 after Green

## Alternatives considered

| Option | Note |
|---|---|
| CLI `--profile experiment` only | Less honest in source |
| Always require marker | Status quo; meta-ceremony remains |

## Acceptance checklist

- [ ] Exact default trigger (no-package only vs also CLI)
- [ ] Adjudicator Accept
- [ ] Kernel child LISS-0286 unblocked only on Accept
