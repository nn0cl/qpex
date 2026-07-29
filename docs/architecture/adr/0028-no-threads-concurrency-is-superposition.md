# ADR 0028: No threads — concurrency is superposition / joint product

## Status

Accepted (2026-07-23).

Companions: `staqex-language-spec.md` §1.4, ADR 0022 (engine parallelism),
ADR 0032 (DAG runtime), ADR 0025 (no exceptions), formal §Span / §Tuple.

## Context

Engineers reach for `Thread` / `async`/`await` to exploit cores. In Staqex those
abstractions are redundant at the *language* level: mixture and joint product
already express simultaneous world-line evolution. Surface threads would invite
shared mutation and early collapse narratives.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **No** object-language `Thread`, `async`, `await`, `spawn`, mutexes, or
   shared-mutable concurrent stores.
2. Programmer-facing concurrency is expressed by:
   - **`when`** (controlled mixture of arms),
   - **tuples / joint `class` fields** ($\mathcal{H}_A \otimes \mathcal{H}_B$),
   - pure `step` / `evolve` / stdlib combinators on those joints.
3. **Runtime/IR may parallelize** independent support atoms (SIMD/GPU/CPU
   workers) without exposing threads in source (ADR 0022).
4. AST **rejects** `Async` / `Await` / `Spawn` / `Mutex` / `Thread` nodes.
5. Host adapters may use OS threads *outside* the object language (CLI I/O),
   never as Staqex surface.

## Consequences

Positive:

- No races/deadlocks in the joint model; clear GPU/TPU mapping story.
- Keeps Never Leave the State free of classical schedulers.

Negative:

- Host I/O is boundary-only (ADR 0029); not solved by threads.

## Enforcement

Reject examples that teach `async`/`Thread` as Staqex concurrency, or that mutate
shared state across “background tasks.”
