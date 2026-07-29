# ADR 0110: Optimistic quantum capacity horizon

## Status

**Proposed** (2026-07-30). Requires Adjudicator architecture approval.

The values are architecture stress envelopes, not delivery forecasts, language
limits, provider commitments, or implementation permission.

Companions:

- [Capacity horizon scenarios](../quantum-capacity-horizon-scenarios.md)
- [ADR 0109](0109-quantum-machine-scale-and-model-envelope.md) (**Proposed**)
- [ADR 0111](0111-current-hardware-first-delivery-horizon.md) (**Proposed**)
- [Machine scale/model research](../../research/2026-07-30-quantum-machine-scale-and-model-horizon.md)

## Context

The facility-to-household transition in classical computing took roughly 35
years to the IBM PC milestone, but that interval includes historical
recognition, capital, manufacturing, and distribution delays. Reusing it for
quantum computing would ignore the modern technology ecosystem and the
importance already assigned to quantum computing.

The scenario clock therefore starts only after a capability-defined useful
quantum-computing breakthrough (`BQ-0`), not at a roadmap date or first
facility machine. Literal conversion between classical FLOPS and quantum
operations remains invalid; the curve is an optimistic architecture stress
model.

The long-run 2.2-year average also hides the semiconductor golden window:
Moore's original projection and the following decade were approximately annual
doubling, before the 1975 revision toward a two-year cadence. The optimistic
quantum scenario therefore models a bounded post-breakthrough acceleration
window rather than a century-scale average.

## Dependency adoption evidence

No dependency is adopted. Public historical records, product specifications,
and roadmaps are evidence inputs. The scenario arithmetic is deterministic and
recorded in the companion document.

## Proposed decision

1. Adopt three non-normative architecture stress profiles:
   - QP-1 early personal workstation, `BQ+3–5` years;
   - QP-2 mature household quantum computer, `BQ+7–10` years;
   - QS-2 quantum supercomputer in the QP-2 world.
2. `BQ-0` is a capability gate requiring reproducible useful advantage, stable
   compiler/runtime contracts, and a credible modular manufacturing path. It
   is not a calendar date or vendor announcement.
3. For the first ten years after `BQ-0`, use a 12–18-month doubling interval as
   the golden-window stress envelope. Do not continue it automatically after
   BQ+10.
4. QP-2 stresses the compiler at `10^4–10^7` logical carriers and
   `10^11–10^15` sustainable logical operations per job.
5. QS-2 stresses it at `10^8–10^12` logical carriers and `10^15–10^20`
   logical operations per campaign.
6. These values are test/profile fixtures, never language maxima, guaranteed
   hardware availability, or default resource reservations.
7. No core semantic or planning structure may require one object, ID, or
   diagnostic per expanded operation.
8. Hierarchical templates, callable regions, symbolic multiplicity, aggregate
   provenance, and bounded/streamed materialization are required.
9. Resource magnitudes support exact values beyond unsigned 64-bit range
   through an abstract exact/symbolic contract. Concrete Rust numeric
   technology remains a separate decision.
10. Failure budgets are compositional and record assumptions; ordinary
    per-operation floating-point multiplication is not sufficient evidence.
11. QP-2 and QS-2 share versioned semantic and plan-fragment formats. Capability
    and deployment differ; source meaning does not.
12. Synthetic QP-1/QP-2/QS-2 profiles may be used for deterministic compiler
    tests without claiming corresponding hardware exists.

## Consequences

Positive:

- integer overflow, flat-IR explosion, and provenance explosion are prevented
  before implementation commits to them;
- the household vision becomes quantitatively testable;
- the supercomputer tier is derived from the same future world rather than
  designed as an unrelated backend;
- compiler complexity can be reviewed against compact plan size;
- capability rejection can be tested long before hardware exists.

Negative:

- exact/symbolic resource arithmetic and compositional failure evidence add
  design and implementation work;
- the scenario dates and values will need periodic revision;
- developers must distinguish compact-plan size from expanded-work estimates;
- optimistic numbers may be mistaken for forecasts unless consistently
  labelled.

## Rejected alternatives

- **Multiply logical qubits directly by the classical operation-rate ratio:**
  category error and physically ungrounded.
- **Start the household clock at a late-2020s roadmap machine:** confuses a
  planned facility milestone with the useful, repeatable, manufacturable
  breakthrough that triggers accelerated adoption.
- **Reuse ENIAC's 35-year social diffusion delay:** ignores the modern
  technology ecosystem and understates the requested optimistic horizon.
- **Use the 79-year 2.2-year average after breakthrough:** smooths away the
  semiconductor golden window and delays the household stress point.
- **Continue annual doubling indefinitely:** turns a bounded stress window
  into an unsupported physical forecast.
- **Avoid quantitative scenarios:** permits hidden 64-bit, flat-list, and
  single-machine assumptions.
- **Make scenario values normative limits:** future hardware could exceed or
  miss them; source semantics must remain scale-free.
- **Create separate household and supercomputer languages:** forks semantics
  and breaks portable scientific provenance.

## Follow-on if accepted

1. Add hierarchy-capable identity/root Red tests to LISS-0082 Slice A.
2. Add exact/symbolic resource and no-eager-expansion scenarios to LISS-0083,
   LISS-0087, LISS-0091, and LISS-0099.
3. Let LISS-0120 use QP-2/QS-2 synthetic profiles when reviewing Noether Forge.
4. Revisit scenario values through a new ADR revision; do not silently edit
   Accepted figures.
