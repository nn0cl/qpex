# ADR 0138: Trace-Out GC MVP for library `fn` scopes (Hold partial unseal)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0170 under WP-0044.
Amends [ADR 0022](0022-quantum-native-optimizations.md) Hold for Trace-Out GC
MVP only. Companion: [`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §2.

## Decisions

1. **Hold partial unseal.** Interference prune and Deferred Pushforward remain
   Hold. Trace-Out GC is authorized only for the MVP below.
2. **Scope.** After a measure-free library `fn` Call binds its results, drop
   Joint coordinates that were **not** live before the Call and are **not**
   among the Call result bind names — via existing `Joint.trace_out` (Born
   partial trace; no RNG; ≠ `measure` / ≠ `project`).
3. **Liveness.** Pre-call live set = coordinate names present on any world of
   the incoming Joint. Result names are always kept. Caller coordinates that
   remain live for the caller stay; eligible-main post-Call dead-caller GC is
   [ADR 0158](0158-interprocedural-trace-out.md).
4. **Explicit `trace_out(coord)`** surface is unchanged and remains the
   programmer-facing discard.
5. **Evolve / block / interprocedural** liveness GC: block `evolve` unsealed by
   [ADR 0142](0142-evolve-trace-out-gc.md); bare block by
   [ADR 0153](0153-bare-block-trace-out.md); interprocedural post-Call caller
   GC by [ADR 0158](0158-interprocedural-trace-out.md).

## Non-goals

Automatic evolve-temp GC; system-field liveness; density-matrix CPTP GC.

## Consequences

- `_bind_user_fun` applies Trace-Out GC before returning to the caller.
- Denotation of kept coordinates / terminal `measure` unchanged; only dead
  fn-local axes disappear from the in-memory joint.
