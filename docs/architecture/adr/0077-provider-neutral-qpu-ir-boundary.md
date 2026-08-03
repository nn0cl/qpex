# ADR 0077: Provider-neutral internal QPU IR boundary

## Status

Accepted (2026-07-24). This ADR accepts the internal boundary only; it does
not authorize an opcode implementation, provider SDK, or public source syntax.

Companion: [LISS-0019](../documentation-compression-map.md).

## Context

Staqex already has source/resolved contracts, DAG/symbolic provenance, and an
OpenQASM 3 emitter. OpenQASM is a useful backend artifact, but it is not a
sufficient ownership boundary for symbolic parameters, future dynamic
capabilities, discretization provenance, and multiple backend forms.

Adding provider concepts to the Kernel would violate the source/backend
separation. Keeping every future concern in OpenQASM text would instead lose
typed boundaries and make non-OpenQASM lowering provider-specific.

## Decision

1. Staqex retains an internal, provider-neutral QPU IR between resolved/symbolic
   IR and backend adapters.
2. The QPU IR is not a public Staqex source language and does not add `Job`,
   `Task`, provider objects, credentials, or submission syntax to the Kernel.
3. The IR must preserve links to source/resolved nodes and retain, when
   applicable, Hilbert shape, symbolic parameters, measurement semantics,
   approximation/discretization provenance, and resource estimates.
4. OpenQASM emission is an adapter from this boundary. Provider SDKs and cloud
   submission remain Host-side ports/adapters.
5. A backend must reject unsupported dynamic, parametric, or resource features
   explicitly. It must not silently emulate them on the Host or weaken
   `State<T>` and terminal `measure` semantics.
6. The CPU Kernel remains authoritative for language meaning; QPU IR is a
   lowering representation, not a second language semantics.

## Ownership and lifecycle

```text
Staqex source
  -> resolved/symbolic IR
  -> provider-neutral QPU IR
  -> backend adapter (OpenQASM, future backend)
  -> Host Job adapter
```

The compiler owns the in-process IR contract. Backend adapters consume it via
ports. Serialization format, opcode inventory, optimization policy, and
provider capability DTOs are follow-up decisions and are not selected here.

## Consequences

Positive:

- `Param<T>`, static Hilbert shape, and provenance have a shared lowering home.
- OpenQASM remains portable output without becoming the public semantic model.
- Future backends can be added without importing provider SDKs into the
  compiler core.

Negative / deferred:

- A second intermediate representation adds lifecycle and verification cost.
- Opcode set, serialization, target capability negotiation, and concrete
  lowering passes require separate acceptance slices.

## Enforcement

- No provider SDK imports under `compiler/staqex/`.
- No Staqex source-level QPU IR syntax.
- No lowering pass may discard terminal-measure, Hilbert-domain, parameter, or
  approximation provenance without an explicit diagnostic.
