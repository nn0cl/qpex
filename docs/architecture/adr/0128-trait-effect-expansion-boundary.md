# ADR 0128: Trait specialization / effect-row expansion — design boundary

## Status

**Accepted as design boundary** (2026-07-31) — LISS-0160 docs.

## Decision

1. Core `impl` / effect marking (ADR 0081–0082) remain shipped.
2. Dispatch specialization, effect-row tables, and provider-specific effects
   require a **future Feature Path ADR** with concrete surface examples before
   Red.
3. This reopen does not weaken coherence / no-`pub`-in-`impl` rules.

## Non-goals

Implementing specialization in WP-0038.

Next design Issue (no Kernel Red):
[LISS-0196](../../issues/LISS-0196-trait-specialization-surface-design.md)
concrete surface examples before any ship ADR.
