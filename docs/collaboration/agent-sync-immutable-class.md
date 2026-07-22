# Agent sync addendum: immutable class / reentrancy (ADR 0033)

Date: 2026-07-23.

## Lock

- `class` fields are immutable `State` capsules.
- Methods return **new** values; never mutate `this`.
- No domain mutexes; reentrancy / shared-mutation races are structural non-issues.
- OOP *syntax*, pure-state *semantics*.

See `qpex-abstraction-model.md` §4b.
