# Agent sync addendum: quantum-native optimizations

Date: 2026-07-22; amended 2026-07-31 (ADR 0137–0138 Hold partial unseal).
Append to `agent-sync-staqex-baseline.md` read order.

## Lock

Four optimization families (ADR 0022):

1. Operator Fusion — **MVP unsealed** for pure unary `fn` pipe chains
   ([ADR 0137](../architecture/adr/0137-pipeline-operator-fusion-mvp.md) /
   WP-0043).
2. Trace-Out GC — **MVP unsealed** for library `fn` scopes
   ([ADR 0138](../architecture/adr/0138-trace-out-gc-fn-scope.md) / WP-0044).
   Evolve/block/interprocedural liveness remain deferred.
3. Interference Pruning & Support Merging — **Hold**
4. Deferred Pushforward until `measure` — **Hold**

Canonical note: `docs/architecture/staqex-compiler-optimizations.md`.

## Relation to existing semantics

- Trace-Out GC **implements** formal §Block / §Evolve obligations eagerly for
  the authorized MVP scopes; it is not a new meaning and ≠ `measure`.
- Deferred Pushforward **implements** deferred RNG law (§Measure).
- Fusion / prune must not break the correlation law.

## Hold (remaining)

Do not implement Interference prune / deferred-DAG IR / evolve-block Trace-Out
until Adjudicator unseals those tracks. Do not expand Fusion or Trace-Out
beyond ADR 0137–0138 without a new ship ADR.
