# DEC-0005: Quantum operations and runtime

## Status

**Draft — source review required**

## Current rules

- Runtime evaluation is joint/worldline-preserving and DAG-oriented, with
  data-parallel evaluation rather than an async/await object model.
- Operators, Hamiltonians, tensor products, controlled operations, QFT, sparse
  Pauli sums, and continuous finite lanes remain explicit quantum operations.
- Unitarity, acting-space, carrier, and correlation contracts are checked at
  the language/semantic boundary.
- Interference, fusion, pruning, and Trace-Out optimizations are valid only
  when they preserve the accepted state semantics.
- Backend lowering must not redefine the language or silently discard a
  worldline.

See [runtime execution model](../staqex-runtime-execution-model.md),
[backend targets](../staqex-backend-targets.md), and the
[language specification](../../specs/staqex-language-specification.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0019, ADR 0022, ADR 0028, ADR 0031, ADR 0032, ADR 0033, ADR 0041, ADR 0042, ADR 0043, ADR 0046, ADR 0047, ADR 0048, ADR 0049, ADR 0050, ADR 0051, ADR 0061, ADR 0062, ADR 0069, ADR 0078, ADR 0079, ADR 0080, ADR 0081, ADR 0082, ADR 0093, ADR 0094, ADR 0096, ADR 0098, ADR 0100, ADR 0137, ADR 0138, ADR 0139, ADR 0140, ADR 0141, ADR 0142, ADR 0143, ADR 0157, ADR 0158, ADR 0159
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set must be reviewed for duplicate, superseded, unique, and unresolved decisions before this document is promoted to the current normative reading surface. Existing ADRs remain authoritative until that review is accepted.
