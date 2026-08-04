# DEC-0006: Host, QPU, and external ports

## Status

**Accepted current surface — ADR 0189**

## Current rules

- The Kernel is local-first and provider-neutral.
- Entropy, source loading, measurement sinks, settings, and QPU submission
  cross boundaries through ports; concrete providers belong in adapters.
- QPU and OpenQASM targets are compilation/submission targets, not alternate
  language semantics.
- Host workflows, jobs, sweeps, credentials, and provider SDKs stay outside
  the Kernel unless a dedicated boundary is accepted.
- Capability limits and unsupported dynamic behavior are reported explicitly;
  they are not hidden behind permissive fallback behavior.
- Observation meaning is defined independently from target capability. Host
  `JobResult` is a classical execution envelope, not the semantic quantum
  state; repeated protocols such as tomography remain Host/protocol concerns.

See [backend targets](../staqex-backend-targets.md),
[runtime model](../staqex-runtime-execution-model.md), and the
[external resource port rules](../dependency-policy.md). The observation and
boundary direction is defined by [ADR 0189](../adr/0189-quantum-mental-model-and-observation-contract.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0015, ADR 0029, ADR 0036, ADR 0059, ADR 0063, ADR 0065, ADR 0070, ADR 0071, ADR 0072, ADR 0073, ADR 0077, ADR 0083, ADR 0084, ADR 0085, ADR 0086, ADR 0091, ADR 0092, ADR 0103, ADR 0104, ADR 0105, ADR 0108, ADR 0109, ADR 0110, ADR 0111, ADR 0119, ADR 0126, ADR 0127, ADR 0161, ADR 0162, ADR 0163, ADR 0164, ADR 0166, ADR 0169, ADR 0170, ADR 0171, ADR 0172
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set has been reviewed for duplicate, superseded, unique, and
unresolved decisions. This document is the current thematic reading surface;
the listed ADRs are archived source records.
