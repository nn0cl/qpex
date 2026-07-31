# Agent sync addendum: quantum-native optimizations

Date: 2026-07-22; amended 2026-07-31 (ADR 0137 Hold partial unseal).
Append to `agent-sync-staqex-baseline.md` read order.

## Lock

Four optimization families (ADR 0022):

1. Operator Fusion — **MVP unsealed** for pure unary `fn` pipe chains only
   ([ADR 0137](../architecture/adr/0137-pipeline-operator-fusion-mvp.md) /
   WP-0043). Algebraic rewrite and broader fusion remain deferred.
2. Trace-Out GC (partial trace / liveness) — **Hold**
3. Interference Pruning & Support Merging — **Hold**
4. Deferred Pushforward until `measure` — **Hold**

Canonical note: `docs/architecture/staqex-compiler-optimizations.md`.

## Relation to existing semantics

- Trace-Out GC **implements** formal §Block / §Evolve, not a new meaning.
- Deferred Pushforward **implements** deferred RNG law (§Measure).
- Fusion / prune must not break the correlation law.

## Hold (remaining)

Do not implement Trace-Out / prune / deferred-DAG IR passes until Adjudicator
unseals those tracks. Do not expand Operator Fusion beyond ADR 0137 without a
new ship ADR.
