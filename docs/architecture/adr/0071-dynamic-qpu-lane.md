# ADR 0071: Dynamic QPU lane

## Status

**Accepted** (2026-07-23). Architecture approval recorded. No implementation
or provider selection is authorized.

Companions: [LISS-0028](../../issues/LISS-0028-dynamic-qpu-lane.md),
[ADR 0069](0069-kernel-static-hilbert-space.md), [ADR 0065](0065-job-based-host-execution.md).

## Context

OpenQASM 3 and current QPU toolchains can express some classical control after
mid-circuit measurement, but support is backend-dependent. IBM documents
dynamic `if`, `switch`, `for`, and `while` constructs; Amazon Braket exposes
dynamic circuits experimentally on selected devices. This is materially
different from Static Hilbert Kernel elaboration.

## Decision proposal

1. Dynamic circuits are a separate Staqex lane, not an extension of static
   `forEach`.
2. The lane may introduce explicit mid-circuit measurement, classical
   feed-forward, qubit reuse, timing, and capability requirements.
3. A dynamic program must declare or select a target capability profile. If a
   target cannot support the required feature, submission fails explicitly; no
   host-side emulation is silently substituted.
4. Dynamic measurement semantics must define the boundary between `State<T>`
   evolution and classical controller values. It may require an effect marker
   or a new result/control type, but this ADR does not choose that syntax.
5. Static Kernel programs remain valid without dynamic support and preserve the
   terminal-measure law.

## Rejected alternatives

- Treating measurement-dependent `forEach` as static elaboration: impossible
  before execution and semantically misleading.
- Adding provider-specific `Job`/polling syntax to Staqex: violates the Host
  boundary in ADR 0065.
- Emulating unsupported dynamic circuits on the Host without an explicit
  semantic marker: changes latency and execution meaning invisibly.

## Open decisions

- dynamic syntax and effect/type marker;
- supported classical operations and timing model;
- capability profile/negotiation DTO;
- how dynamic results compose with terminal `measure` and JobResult;
- simulator conformance model for dynamic circuits.
