# ADR 0022: Quantum-native compiler / runtime optimizations

## Status

Accepted as **design baseline** (2026-07-22).

Design note: `docs/architecture/staqex-compiler-optimizations.md`.
**Partial unseal (2026-07-31):** thin pipeline Operator Fusion MVP —
[ADR 0137](0137-pipeline-operator-fusion-mvp.md). Trace-Out / prune /
Deferred Pushforward remain Hold.

## Context

Never Leave the State forces pure $\mathsf{Joint}\to\mathsf{Joint}$ regions
until terminal `measure`. That purity is not only a semantic law — it is an
optimization surface: unitary / pushforward fusion, partial trace of dead
axes, support merge / interference prune, and deferred materialization until
measurement.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Document four normative optimization *families* for future IR / engine:
   - **Operator Fusion** — compose pure transformers before applying to state.
   - **Trace-Out GC** — realize §Block / §Evolve partial trace via liveness.
   - **Interference Pruning & Support Merging** — merge colliding atoms;
     drop exact-zero mass / amplitude.
   - **Deferred Pushforward** — lazy DAG until `measure`; then batch + sample.
2. Passes must preserve denotation (and RNG-stream samples after `measure`).
3. Trace-out ≠ `measure` ≠ `project`; prune/merge ≠ `project`.
4. Kernel PoC A/B may evaluate eagerly; fusion / deferred mode are later
   engine profiles, not PoC correctness requirements.
5. Concrete IR opcode set stays open pending amplitude / QPU IR (ADR 0016).

## Consequences

Positive:

- Clear wedge: physics laws as compiler passes.
- Aligns optimizer work with existing §Block trace-out and deferred RNG laws.

Negative / cost:

- IR design and numeric zero policy still open.
- Agents must not treat this ADR as unsealing optimizer implementation.

## Enforcement

Reject designs that (a) sample before `measure` “for speed,” (b) skip
trace-out of dead block locals, or (c) claim classical DCE alone covers the
Staqex optimization story without these four families.
