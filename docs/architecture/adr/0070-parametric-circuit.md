# ADR 0070: Parametric Circuit boundary

## Status

**Accepted** (2026-07-23). Architecture approval recorded. No implementation
or technology selection is authorized.

Companions: [LISS-0027](../../issues/LISS-0027-parametric-circuit.md),
[ADR 0069](0069-kernel-static-hilbert-space.md).

## Decision proposal

1. Introduce a symbolic `Param<T>` family for circuit parameters, beginning
   with `Param<Angle>` for parameterized unitary gates.
2. A `Param<T>` is neither a `Host<T>` value nor a `State<T>` coordinate. It is
   a symbolic circuit node that survives into QPU IR/OpenQASM parameter binding.
3. Parameters may appear only in explicitly parameterized gate/operator
   arguments. They may not control `forEach`, register shape, measurement,
   classical branching, or circuit termination.
4. Host submission binds concrete values to declared parameters. The binding
   is validated before Job submission and is opaque to the Kernel semantics.
5. VQE/QAOA, parameter-shift gradients, differentiability, and batch binding
   are follow-up concerns; this ADR only defines the boundary and purity rule.

## Rejected alternatives

- Using `Host<T>` directly in gate expressions: mixes submission data with
  symbolic circuit structure.
- Treating parameters as `State<T>`: confuses a symbolic coefficient with a
  superposed physical coordinate.
- Allowing parameter-dependent loop bounds or branches: makes circuit shape
  depend on Host control and belongs to a separate dynamic lane.

## Open decisions

- parameter declaration syntax and naming;
- allowed physical parameter domains and dimensional types;
- OpenQASM binding representation and provider capability negotiation;
- whether parameter expressions are symbolic ASTs or a dedicated QPU IR node.
