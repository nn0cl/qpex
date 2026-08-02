# ADR 0177: Selective import and use ergonomics

## Status

**Accepted** (2026-08-02) — Adjudicator「承認」
([LISS-0265](../../issues/LISS-0265-adr-import-use-ergonomics.md) /
[WP-0088](../../work-plans/WP-0088-surface-modernization.md)).
Kernel Red: [LISS-0271](../../issues/LISS-0271-import-use-ergonomics-red.md).

Companions: ADR 0054 user modules; north star (FQN noise); S01 multi-file demos.

## Context

Large examples require many `import` lines and long FQNs
(`Disaster.Domain.CommandBoard`), which read as enterprise ceremony rather than
physics.

## Decision

1. **Selective import** (additive):

   ```text
   import com.example.domain.{CommandBoard, OpsPhase}
   ```

2. **Same-package short names** remain as today; selective import only reduces
   cross-package FQN.

3. **Optional `use` for enums** in `when` arms (narrow scope):

   ```text
   use OpsPhase.*
   state p = when (phase) { Tonight -> |0>, else -> |1> }
   ```

   Must not introduce classical `if`.

4. **Old** `import pkg` / fully qualified names remain valid forever in v1.

5. **No** wildcard import of entire deep trees that hide physics dependencies
   in official samples without review (style guide, not hard ban in Kernel).

## Consequences

- Parser + name resolution updates (Wave C).
- Basics/S01 can shorten call sites after ship.
- Complements ADR 0176 (short package) but is independently useful.

## Alternatives

| Option | Note |
|---|---|
| Only path aliases | Less flexible than selective import |
| Force global prelude | Hides dependencies |

## Acceptance checklist

- [x] Adjudicator Accept (2026-08-02「承認」)
- [x] Selective import `{A, B}` + enum `use` limited to when-arm name resolution
- [x] Kernel Red child: LISS-0271
