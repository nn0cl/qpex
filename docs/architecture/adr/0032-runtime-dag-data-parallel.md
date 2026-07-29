# ADR 0032: Runtime = DAG + data-parallel eval (not async/await VM)

## Status

Accepted as **design baseline** (2026-07-23).

Canonical: `docs/architecture/staqex-runtime-execution-model.md`.
Related: ADR 0022, 0028, 0029.

## Context

Implementers might assume Staqex needs a Node/Rust-style async runtime because
it “runs many world-lines.” That would reintroduce schedulers, colouring, and
complexity the language law already eliminates at the surface (ADR 0028).

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Object-language execution is modeled as **pure DAG construction** then
   **batch evaluation**, not as Promise/Future/`async` state machines.
2. Independent support atoms are evaluated with **data-parallel** kernels
   (SIMD/GPU/multi-core workers) under a single denotation.
3. Classical async I/O belongs only in **host adapters** for boundary lift /
   sink (ADR 0029), never as source-level colouring.
4. Kernel PoC may use eager single-threaded eval; DAG/SIMD are later engine
   profiles that must preserve semantics + RNG streams.
5. Do **not** implement an object-language async scheduler as a prerequisite
   for Hold unseal of Kernel PoC.

## Consequences

Positive:

- Simpler MVP runtime; clear GPU/QPU offload path.
- Matches Never Leave the State and deferred measure.

Negative:

- Engineers from async-heavy stacks need the execution-model note to avoid
  overbuilding.

## Enforcement

Reject designs that add `async`/`await` to Staqex source or that require a
Promise runtime for pure `when`/`map` evaluation.
