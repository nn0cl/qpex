# ADR 0178: Lane annotation (experiment / circuit / host)

## Status

**Accepted** (2026-08-02) — Adjudicator「承認」
([LISS-0266](../documentation-compression-map.md) /
[WP-0088](../documentation-compression-map.md)).
Kernel Red: [LISS-0272](../documentation-compression-map.md).

Companions: vision §3.1; minimal dialect D4; QPU honesty catalog.

## Context

Staqex has multiple legitimate lanes (Static Kernel experiment, circuit
register/`forEach`, open systems, Host). Unmarked mixing makes the product look
like one enterprise soup and confuses `forEach` vs forbidden bare `for`.

## Decision

1. Introduce a **source-visible lane marker** (choose one at Accept):

   ```text
   // staqex-lane: experiment
   // staqex-lane: circuit
   // staqex-lane: open
   // staqex-lane: host-companion   // docs/Python only; not Kernel object language
   ```

   or attribute form `@lane(experiment)` if grammar prefers.

2. **Default** for unmarked single-file basics: `experiment` (no hard error).

3. **Diagnostics (soft → hard in stages):**
   - Soft: warn when circuit-only constructs appear in `experiment` without
     `circuit` lane (e.g. `forEach` on `QubitRegister`) once profile ships.
   - Official samples: spines labeled `experiment`; burst/QFT labeled `circuit`.

4. **Does not change** evolve/measure semantics or placeability rules — labels
   teaching and diagnostics only (v1).

5. Host Python companions stay outside Kernel; lane note in README is enough
   unless a future Kernel `host` block is designed separately.

## Consequences

- Sample policy updates; optional compiler warnings.
- Clearer pedagogy for multi-lane trees (S01 constellation).

## Alternatives

| Option | Note |
|---|---|
| Directory-only convention | Invisible in source paste |
| Hard error on any mix | Too strict for showcases |

## Acceptance checklist

- [x] Adjudicator Accept (2026-08-02「承認」)
- [x] Marker: `// staqex-lane: experiment|circuit|open` (file-level comment form first)
- [x] Soft diagnostics first; hard only after sample migration
- [x] Kernel Red child: LISS-0272
