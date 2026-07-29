# ADR 0109: Quantum machine scale and model envelope

## Status

**Proposed** (2026-07-30). Requires Adjudicator architecture approval.

No implementation, provider selection, phase transition, or hardware forecast
is accepted by this draft.

Companions:

- [Quantum machine scale and model
  envelope](../quantum-machine-scale-and-model-envelope.md)
- [Research note](../../research/2026-07-30-quantum-machine-scale-and-model-horizon.md)
- [ADR 0106](0106-staqex-v1-north-star-language-and-compiler.md)
- [ADR 0108](0108-quantum-semantic-ir-value-region-contract.md) (**Proposed**)
- [ADR 0110](0110-optimistic-quantum-capacity-horizon.md) (**Proposed**)

## Context

Staqex must not optimize its architecture only for today's small cloud QPUs.
Published roadmaps point toward modular fault-tolerant machines with hundreds
of logical carriers and millions to hundreds of millions of logical
operations. At the other end, current on-premises, desktop educational,
room-temperature accelerator, and compact photonic systems suggest a future
local quantum appliance integrated with ordinary computing.

Hardware also differs by computation model. A gate-only source semantics would
prematurely exclude native evolution, measurement-based/photonic, qudit, and
specialized optimization targets.

## Dependency adoption evidence

No dependency is adopted. Hardware roadmaps and product pages are dated design
evidence only. No provider claim becomes a language limit or guaranteed
delivery assumption.

## Proposed decision

1. Staqex supports a bidirectional machine horizon from a **Personal Quantum
   Appliance** to modular utility-scale fault-tolerant systems through one
   source and semantic contract.
2. Personal Quantum Appliance means a local quantum co-processor with a
   classical host. Core compilation and local execution do not require cloud
   credentials, queues, network access, or implicit remote fallback.
3. Semantic IR is scale-free. It contains no fixed qubit, operation, depth,
   power, price, or deployment limit.
4. Semantic and downstream plans retain hierarchy, callable regions, symbolic
   repetition, and symbolic resource expressions. Eager flattening is
   forbidden unless a reviewed bounded materialization step proves the output
   fits its budget.
5. Resource contracts distinguish semantic, logical, and physical levels.
6. Computation-model families are explicit downstream capability profiles, not
   alternative source semantics. Unsupported model/meaning combinations are
   rejected.
7. Local, on-premises, remote, and modular-facility deployment are explicit
   workflow/target profiles. Remote fallback requires an explicit authorized
   host-workflow decision.
   Deployment-specific adapters implement common core-owned capability and
   execution ports; local and remote execution do not create competing core
   semantics.
8. Provider, firmware, calibration, QEC, decoder, routing, and physical
   allocation details remain in Target IR/adapters and never redefine source
   or Quantum Semantic meaning.
9. Quantum Semantic IR v1 remains finite. Native continuous-variable execution
   requires a future reviewed semantic profile or an explicit finite
   realization contract.

## Consequences

Positive:

- the compiler can target both local appliances and large fault-tolerant
  facilities without separate language semantics;
- enormous programs remain representable without allocating enormous flat IR
  lists;
- household/local use does not inherit a cloud-first privacy or availability
  assumption;
- hardware modalities compete through explicit capability and lowering
  contracts;
- resource estimates become scientifically meaningful across abstraction
  levels.

Negative:

- Algorithm Plan, Logical QPU IR, resource estimation, and capability profiles
  require more structure than flat instruction DTOs;
- not every target can execute every Staqex program;
- symbolic plans and bounded materialization add verifier and tooling work;
- household-scale general-purpose quantum computing remains a horizon rather
  than a validated current capability.

## Rejected alternatives

- **Use the largest published qubit count as the language target:** roadmap
  numbers are volatile and incomparable across physical/logical systems.
- **Optimize only for utility-scale FTQC:** would preserve cloud/facility
  assumptions and neglect local privacy, latency, and constrained execution.
- **Optimize only for personal devices:** would prevent hierarchical planning
  for very large fault-tolerant systems.
- **Use a flat circuit as universal IR:** cannot scale to very large programs
  and privileges one computation model.
- **Silently use cloud or simulation when local hardware is insufficient:**
  violates explicit execution, privacy, and result provenance.

## Follow-on if accepted

1. Make ADR 0109 a prerequisite for LISS-0082 Slice A Red review alongside ADR
   0108.
2. Add hierarchy/materialization acceptance tests to the relevant LISS-0082,
   0083, 0087, 0091, and 0099 slices.
3. Keep concrete hardware/provider adoption behind separately approved Issues.
