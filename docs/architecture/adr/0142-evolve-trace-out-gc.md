# ADR 0142: Trace-Out GC for block `evolve` (Hold partial unseal)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0174 under WP-0048.
Extends [ADR 0138](0138-trace-out-gc-fn-scope.md) Trace-Out GC.
Companion: [`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §2.

## Context

ADR 0138 unsealed Trace-Out GC for library `fn` scopes and deferred evolve /
block / interprocedural liveness. Formal §Block / §Evolve already require
partial trace of dead axes at exit. Adjudicator unseals the **block evolve**
slice.

## Decisions

1. **Hold partial unseal.** After a measure-free **block** `evolve (… ) times N
   { let …; result }` completes, drop Joint coordinates that were **not** live
   before the evolve and are **not** among the evolve result bind names — via
   `Joint.trace_out` (same liveness rule as ADR 0138).
2. **Pre-live.** Coordinate names present on any world of the incoming Joint.
3. **Hamiltonian** `evolve … under H` paths are unchanged by this ADR (no let
   temps in that surface); interprocedural Trace-Out remains later.
   Bare block-without-evolve: [ADR 0153](0153-bare-block-trace-out.md).
4. **≠ `measure` / ≠ `project`.** Born partial trace only; no RNG.

## Non-goals

Per-step mid-evolve GC; system-field liveness; density-matrix CPTP GC.

## Consequences

- `_bind_evolve` applies Trace-Out GC before returning to the caller.
- Evolve `let` temps (e.g. `temp1`) disappear from the in-memory joint after
  exit; denotation of result binds / terminal `measure` unchanged.
