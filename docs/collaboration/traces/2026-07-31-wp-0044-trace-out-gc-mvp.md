# Trace: WP-0044 Trace-Out GC fn-scope MVP

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0044-trace-out-gc-mvp` |
| Issues | LISS-0170 |
| ADRs | 0138 Accepted (amends 0022 Hold) |
| Instruction change | `CLAUDE.md`; `agent-sync-quantum-native-opts.md` |

## Shipped

- After library `fn` Calls, dead fn-local Joint axes are `trace_out`'d
- Pre-call live coordinates and result binds are kept

## Still Hold

Interference prune; Deferred Pushforward DAG; evolve/block Trace-Out GC.
