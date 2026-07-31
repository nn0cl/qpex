# ADR 0159: CPU data-parallel Deferred workers MVP

## Status

**Accepted** (2026-07-31) — unlocks LISS-0192 under WP-0065.
Extends [ADR 0140](0140-deferred-pushforward-mvp.md) /
[ADR 0028](0028-no-threads-concurrency-is-superposition.md) Decision 3.
Amends [ADR 0140](0140-deferred-pushforward-mvp.md) Non-goal “Multi-core/GPU
batch workers” for this **CPU** MVP only.

## Context

ADR 0028 forbids object-language threads but allows the runtime to parallelize
independent support atoms. ADR 0140 deferred GPU/data-parallel DAG workers.
Adjudicator unseals a thin **CPU** `ThreadPoolExecutor` over independent Joint
worlds. CUDA / real GPU remains a later ADR.

## Decisions

1. **Opt-in only.** Default remains sequential (`workers = 1`). Enable via
   `Evaluator(data_parallel_workers=N)`, Host `settings["data_parallel_workers"]`,
   CLI `--data-parallel-workers N`, or env `STAQEX_DATA_PARALLEL_WORKERS`.
2. **Mechanism.** `Joint.bind_pushforward` / `bind_multi` map worlds with a
   `ThreadPoolExecutor` when `N > 1` and `|worlds| ≥ 2`, scoped by a ContextVar
   for the duration of `Evaluator.run_unit`.
3. **No language threads.** Source surface stays free of `Thread` / `async`
   (ADR 0028). This is Host/Kernel runtime only.
4. **Denotation.** Same seed + same program ⇒ same terminal measure as
   sequential evaluation (world order preserved by `pool.map`).
5. **Evidence.** `EvalResult.data_parallel_workers` records the configured N.

## Non-goals

CUDA / GPU kernels; language-level parallelism; automatic worker sizing;
DAG-node scheduling beyond Joint world maps.

## Consequences

- Agents must not treat this ADR as authorizing CUDA or object-language threads.
- Callables applied per world should avoid cross-world mutable Evaluator races;
  the MVP targets independent assign maps.
