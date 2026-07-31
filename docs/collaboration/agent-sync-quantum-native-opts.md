# Agent sync addendum: quantum-native optimizations

Date: 2026-07-22; amended 2026-07-31 (ADR 0137–0140 Hold partial unseal).
Append to `agent-sync-staqex-baseline.md` read order.

## Lock

Four optimization families (ADR 0022):

1. Operator Fusion — **MVP unsealed** for pure unary `fn` pipe chains
   ([ADR 0137](../architecture/adr/0137-pipeline-operator-fusion-mvp.md) /
   WP-0043).
2. Trace-Out GC — **MVP unsealed** for library `fn` scopes
   ([ADR 0138](../architecture/adr/0138-trace-out-gc-fn-scope.md) / WP-0044).
   Evolve/block/interprocedural liveness remain deferred.
3. Interference Pruning & Support Merging — **MVP unsealed**
   ([ADR 0139](../architecture/adr/0139-interference-prune-mvp.md) / WP-0045):
   amp-sum coalesce + exact-zero prune via `Joint.merge_support`.
4. Deferred Pushforward until `measure` — **MVP unsealed**
   ([ADR 0140](../architecture/adr/0140-deferred-pushforward-mvp.md) / WP-0046):
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

Do not implement evolve-block Trace-Out, GPU DAG workers, or Fusion/prune
expansions beyond ADR 0137–0140 without a new ship ADR.
