# ADR 0176: Experiment surface profile (short ceremony)

## Status

**Proposed** (2026-08-02) — [LISS-0264](../../issues/LISS-0264-adr-experiment-surface-profile.md) /
[WP-0088](../../work-plans/WP-0088-surface-modernization.md).
**Not Accepted.** Architecture approval required before Kernel Red.
No axiom rewrite. Does not authorize live QPU or mid-program measure.

Companions: [surface-modernization-north-star](../surface-modernization-north-star.md)
(**Accepted**); [minimal dialect](../physicist-minimal-dialect.md); ADR 0054 modules;
ADR 0064 `main -> Unit`.

## Context

Official short experiments still open with deep JVM-style packages:

```text
package com.staqex.examples.basics.operators_hamiltonians

pub fn main() -> Unit { … }
```

That face reads as 2010s enterprise Kotlin, blunting the Accepted minimal dialect
and the de-enterprise north star. Large multi-file programs still need packages;
the gap is the **default teaching / experiment profile**, not module deletion.

## Decision (proposed)

### Profile name

**`experiment`** (working title): a conformance *profile* for single-file or
small physics scripts.

### Rules (proposed)

1. **Package optional** for experiment-profile entry files under
   `examples/basics/**` and similarly marked demos when:
   - no cross-package export is required, or
   - a default package `staqex.experiment` (or file-local anonymous package) is
     implied by the compiler for resolution.
2. **Existing** `package com.…` programs remain **fully valid** (no migration
   break for S01 multi-file trees).
3. **`pub fn main() -> Unit`** remains the normative entry for v1 Host; the
   profile may allow a documented sugar that desugars to the same ABI
   (e.g. bare top-level statements wrapped as `main` by the compiler) —
   **optional** sugar, not a second entry semantics.
4. Physics spelling (ket, `Operator`, `evolve`, `when`, terminal `measure`) is
   unchanged.
5. Official **B01/B08-class** samples **should** use the short profile once
   shipped (Wave C), so first impression is chalk-first.

### Before / after (teaching target)

**Before (shipping today):**

```text
package com.staqex.examples.basics.operators_hamiltonians

pub fn main() -> Unit {
    Float J = 1.0
    Operator H = -J * (Z[0] * Z[1])
    …
    measure s0 tracing_out s1
}
```

**After (experiment profile — illustrative):**

```text
// staqex-profile: experiment
Float J = 1.0
Operator H = -J * (Z[0] * Z[1])
state s0 = |+>
state s1 = |+>
state (s0, s1) = evolve (s0, s1) under H for 0.7 using Suzuki(order = 2, steps = 6)
measure s0 tracing_out s1
```

(Exact marker syntax is part of Accept; alternatives: file extension policy,
`experiment { … }` block, or CLI `--profile experiment` only — Prefer a
**source-visible** marker for honesty.)

## Consequences

- Host `run_path` / `submit_path` continue to resolve an entry `main`.
- Multi-package S01-style trees keep current package/import rules.
- Wave C Kernel Issue under LISS-0269 after Accept.
- Formatter / SV cases for short profile samples.

## Alternatives considered

| Option | Why not sole choice |
|---|---|
| Delete packages entirely | Breaks multi-file / library scale |
| Only document “ignore package lines” | Does not change the face of source |
| Force `com.staqex` always | Worsens enterprise feel |

## Acceptance checklist

- [ ] Adjudicator Accept / revise / reject marker syntax
- [ ] Confirm default package name and Host entry desugar
- [ ] On Accept: spawn Kernel Red child Issue (not this ADR alone)
