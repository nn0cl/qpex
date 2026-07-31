# ADR 0140: Deferred Pushforward MVP (Hold partial unseal)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0172 under WP-0046.
Amends [ADR 0022](0022-quantum-native-optimizations.md) Hold for Deferred
Pushforward MVP only. Companions:
[`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §4;
[`staqex-runtime-execution-model.md`](../staqex-runtime-execution-model.md)
(ADR 0032); existing DAG lowerer `compiler/staqex/ir/dag.py`.

## Context

ADR 0022 / 0032 describe lazy DAG materialization until `measure`. The Kernel
already lowers ASTs to a computation DAG for backends/CLI, and RNG stays zero
until terminal measure. Adjudicator unseals a **Kernel-local** thin runtime
slice: batch StateBind materialization for eligible `main` bodies.

## Decisions

1. **Hold partial unseal.** Full GPU/data-parallel DAG scheduling, algebraic
   DAG rewrites, and forced whole-program lazy IR remain later. Operator
   Fusion / Trace-Out GC / Interference prune MVPs (ADR 0137–0139) stay as
   previously unsealed.
2. **Eligibility.** `main` body is `StateBind*` (ty `None` or `State` only)
   followed by a single terminal `Measure`. Bodies with `inspect` (in any bind
   expr), `snapshot`, `forEach`, Operator/class binds, or other stmts use the
   eager path.
3. **Mechanism.** Eligible programs record StateBinds without applying them,
   compute the free-var **dependency cone** of the measure expression, then
   apply only cone binds in source order at measure time. Denotation under a
   fixed RNG stream ≡ eager eval + terminal sample.
4. **Compile DAG.** `lower_source_ast` / `staqex dag` remains the authorized
   compile-time Deferred Pushforward surface (ADR 0032 Phase 3).
5. **Evidence.** `EvalResult.deferred_pushforward` and
   `deferred_binds_applied` record whether the MVP path ran.

## Non-goals

GPU batch workers (CUDA); automatic worker sizing; algebraic DAG rewrites;
forced whole-program lazy IR. CPU data-parallel Joint world workers are
unsealed by [ADR 0159](0159-cpu-data-parallel-workers.md).

## Consequences

- Simple pure mains materialize joints in one measure-timed batch.
- Agents must not treat this ADR as authorizing approximate pre-measure
  sampling or a second language semantics.
