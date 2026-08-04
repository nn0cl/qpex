# Agent sync addendum: quantum-native optimizations

Date: 2026-07-22; amended 2026-07-31 (ADR 0137–0155 Hold expansions / SI / Trace-Out).
Append to `agent-sync-staqex-baseline.md` read order.

## Lock

Four optimization families (ADR 0022):

1. Operator Fusion — **MVP unsealed** for pure unary `fn` pipe chains
   ([ADR 0137](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) /
   WP-0043), **affine algebraic collapse**
   ([ADR 0141](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) /
   WP-0047), and **one-hole Call/Partial stages**
   ([ADR 0143](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) /
   WP-0049). Sequential multi-hole Partial pipe fill is shipped
   ([ADR 0149](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) /
   WP-0055); tuple simultaneous multi-hole fill
   ([ADR 0152](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) /
   WP-0058); **polynomial≥2** remain later.
2. Trace-Out GC — **MVP unsealed** for library `fn` scopes
   ([ADR 0138](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) / WP-0044)
   and block `evolve`
   ([ADR 0142](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) / WP-0048) and
   bare `{ let …; e }`
   ([ADR 0153](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) / WP-0059).
   Interprocedural liveness remain deferred.
3. Interference Pruning & Support Merging — **MVP unsealed**
   ([ADR 0139](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) / WP-0045):
   amp-sum coalesce + exact-zero prune via `Joint.merge_support`.
4. Deferred Pushforward until `measure` — **MVP unsealed**
   ([ADR 0140](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) / WP-0046):
   eligible `StateBind* + measure` mains batch materialization at measure;
   compile DAG via `ir/dag.py`. GPU/data-parallel workers remain later.

Canonical note: `docs/architecture/staqex-compiler-optimizations.md`.

## Relation to existing semantics

- Trace-Out GC **implements** formal §Block / §Evolve obligations eagerly for
  the authorized MVP scopes; it is not a new meaning and ≠ `measure`.
- Deferred Pushforward **implements** deferred RNG law (§Measure) plus
  measure-timed bind batching for eligible mains.
- Fusion / prune must not break the correlation law.

## Hold (remaining expansions)

Do not implement interprocedural Trace-Out, GPU DAG workers,
or polynomial≥2 rewrites beyond ADR 0137–0143 / 0152–0153
without a new ship ADR (sequential multi-hole pipe: ADR 0149;
tuple simultaneous fill: ADR 0152; bare-block Trace-Out: ADR 0153).
