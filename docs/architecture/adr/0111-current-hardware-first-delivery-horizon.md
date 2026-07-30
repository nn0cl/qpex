# ADR 0111: Current-hardware-first delivery horizon

## Status

**Accepted** (2026-07-30) — Adjudicator Architecture approval.

Acceptance does **not** authorize: provider/SDK selection, account use,
network adapters, live execution, or treating CH*/NH5 profile numbers as
language limits or delivery promises.

Companions:

- [Current-hardware delivery envelope](../current-hardware-delivery-envelope.md)
- [P0/P1 delivery work plan](../../work-plans/WP-0029-current-hardware-delivery-horizon.md)
- [Current hardware research](../../research/2026-07-30-current-quantum-hardware-delivery-envelope.md)
- [ADR 0109](0109-quantum-machine-scale-and-model-envelope.md) (**Accepted**)
- [ADR 0110](0110-optimistic-quantum-capacity-horizon.md) (**Accepted**)

## Context

ADR 0109 and ADR 0110 protect Staqex from small-machine assumptions, but a
future-facing design could postpone useful execution indefinitely. Current
machines already span small on-premises systems, high-fidelity dynamic digital
systems, large topology-constrained processors, and analog neutral-atom
systems.

P0 and P1 should therefore be ambitious in semantics and scientific intent
while maintaining deliberately bounded instances that can run now.

## Proposed decision

1. Every open P0/P1 capability is reviewed against both future scale and
   current execution evidence.
2. Adopt non-normative acceptance profiles:
   `CH0_COMMON_PHYSICAL`, `CH1_DIGITAL_RESEARCH`,
   `CH1_ANALOG_RESEARCH`, `SIM0_EXACT`, and `SIM1_MIXED`.
3. Adopt 2026–2031 roadmap stress profiles: `NH5_NISQ_MODULAR`,
   `NH5_FT_MEGA`, `NH5_FT_GIGA`, and `NH5_NATIVE_LARGE`. They are neither
   current acceptance requirements nor delivery promises.
4. P0 integration includes a 2–5-qubit common physical smoke path and exact
   small simulation, without requiring a provider account for each component
   slice.
5. P1 integration includes at least one target-resolved current digital
   physical execution and one analog artifact/execution witness when analog
   support is claimed.
6. Profile values are test fixtures and never semantic limits. Target
   capability and calibration snapshots may tighten them.
7. `ExecutionEvidence` distinguishes simulator, emulator, and physical runs
   and records source/compiler/plan/target/artifact/result provenance.
8. OpenQASM syntax validity is insufficient; the emitted subset and target
   capability match are explicit.
9. Promote LISS-0100 first live provider adapter from P2 to the P1 integration
   endcap. Provider/SDK selection still requires separate technology approval.
10. Promote bounded error-mitigation work in LISS-0093 from P2 to P1 because
   current-machine interpretation requires raw-versus-mitigated evidence.
11. Move LISS-0098 QIR profile/toolchain from P1 to P2 while Rust
    infrastructure is deferred and OpenQASM provides the first current-hardware
    path.
12. Advanced fault-tolerant planner methods may be sliced to P2 even when
    their common planner contracts begin in P1.
13. NH5 profiles bridge current and BQ horizons: P0/P1 plans must validate
    compactness/capability rejection against them, but need no nonexistent
    hardware.
14. QP-1/QP-2/QS-2 remain required compact-plan stress profiles and do not
    block current-hardware delivery.

## Consequences

Positive:

- P0 produces an executable foundation rather than only DTOs;
- P1 culminates in a useful, evidence-rich physical workflow;
- current machines provide feedback on language and IR design early;
- future scale remains protected by the same contracts;
- noisy physical results cannot be confused with exact semantics.

Negative:

- live integration and mitigation enter P1 earlier;
- current-hardware evidence can be slow, quota-limited, or calibration-sensitive;
- separate digital, analog, exact, and mixed profiles add fixtures and review;
- provider selection remains a blocking human decision near the P1 endcap.

## Rejected alternatives

- **Future profiles only:** permits an elegant compiler with no useful current
  execution.
- **Current qubit count as a language maximum:** couples semantics to volatile
  products.
- **One universal current-hardware profile:** hides topology, modality,
  fidelity, control, and measurement differences.
- **Require live hardware in every P0 slice:** makes core progress dependent on
  credentials, queues, and external availability.
- **Keep the first live adapter in P2:** leaves P1 “current hardware” support
  unproved.
- **Require QIR before current execution:** conflicts with deferred Rust work
  and duplicates the earlier OpenQASM route.

## Follow-on if accepted

1. Keep WP-0029 as the delivery-horizon work-plan companion; rebaseline
   individual P0/P1 Issue acceptance scenarios when those Issues open Red.
2. Select the first simulator and provider only through named Technology
   selection Issues — never from this ADR alone.
3. Keep QP-1/QP-2/QS-2 (ADR 0110) as compact-plan stress profiles that do not
   block current-hardware delivery.
