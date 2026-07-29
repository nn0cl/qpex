# Agent sync addendum: quantum-native optimizations

Date: 2026-07-22. Append to `agent-sync-staqex-baseline.md` read order.

## Lock

Four optimization families (ADR 0022) — design only, **Hold** on IR code:

1. Operator Fusion
2. Trace-Out GC (partial trace / liveness)
3. Interference Pruning & Support Merging
4. Deferred Pushforward until `measure`

Canonical note: `docs/architecture/staqex-compiler-optimizations.md`.

## Relation to existing semantics

- Trace-Out GC **implements** formal §Block / §Evolve, not a new meaning.
- Deferred Pushforward **implements** deferred RNG law (§Measure).
- Fusion / prune must not break the correlation law.

## Hold

Do not implement optimizer / IR passes until Adjudicator unseals that track.
Kernel PoC A/B remains the first unseal target.
