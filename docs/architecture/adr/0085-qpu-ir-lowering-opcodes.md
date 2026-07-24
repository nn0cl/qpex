# ADR 0085: Provider-neutral QPU IR lowering and initial opcode vocabulary

## Status

Accepted (2026-07-24) for the LISS-0041 implementation slice.

Companion: [LISS-0041](../../issues/LISS-0041-qpu-ir-lowering.md).

## Decision

1. The first QPU IR vocabulary contains only the existing OpenQASM-supported
   basic gates (`H`, `X`, `Y`, `Z`, `CX`, `RX`, `RY`, `RZ`), symbolic parameter
   nodes, and terminal `Measure` nodes.
2. DAG IR to QPU IR lowering is a pure function. Every generated node copies
   the source/resolved provenance of its input DAG node.
3. The OpenQASM adapter consumes immutable in-memory QPU IR objects directly;
   no JSON or other serialization boundary is introduced.
4. Unsupported capabilities produce hard diagnostic `E_QPU_UNSUPPORTED_CAPABILITY`.
   Host fallback and silent emulation are forbidden.
5. The immutable root object retains Hilbert shape, parameter metadata,
   measurement semantics, and approximation provenance separately from the
   instruction sequence.
6. Serialization, provider SDK objects, dynamic control opcodes, and a public
   QPex QPU IR syntax remain deferred.

## Consequences

The first implementation is a small one-to-one bridge from the existing DAG
and OpenQASM gate surface. It does not define a complete provider ABI or
backend capability negotiation protocol. The CPU Kernel remains authoritative.
