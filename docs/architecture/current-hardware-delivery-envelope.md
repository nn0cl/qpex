# Current-hardware delivery envelope

## Status and authority

**Draft for Adjudicator architecture review. No implementation or technology
selection permission.**

This contract complements the future scale envelopes in ADR 0109 and ADR 0110.
It defines how P0 and P1 remain executable on current quantum computers without
making current hardware limits part of Staqex semantics.

Proposed decision: [ADR 0111](adr/0111-current-hardware-first-delivery-horizon.md).

Evidence:
[current hardware research](../research/2026-07-30-current-quantum-hardware-delivery-envelope.md).

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: rebaseline P0 and plan P1+ so foundational and
  scientific work retains a bounded simulator/current-QPU execution witness
  while future household and supercomputer profiles remain valid stress loads.
- Specifications and files inspected: ADR 0106/0108/0109/0110; WP-0025;
  LISS-0082/LISS-0120; current compiler resource/QASM boundaries; official
  current-system and OpenQASM sources.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  semantics remain scale-free; candidate downstream VOs are DeliveryProfileId,
  ExecutionEvidence, CapabilitySnapshotRef, CalibrationSnapshotRef,
  ArtifactSubset, and PhysicalWitnessResult. Provider SDKs remain adapters.
- Applicable constraints: Never Leave the State; terminal Static measurement;
  provider neutrality; no silent fallback; no fixed hardware maximum in
  semantic IR; explicit approximation and noisy-result provenance.
- Decisions, assumptions, and unresolved ambiguities: current profiles are
  conservative acceptance fixtures; first live provider remains a separate
  technology-selection decision; ADR 0108–0111 remain Proposed.
- Included and omitted AI context: include public architecture, affected plans,
  current source boundaries, and public primary hardware evidence; omit
  credentials, provider SDK internals, pricing, private calibration data, and
  unrelated compiler modules.
- Task routing (model/assistant/tool): architecture synthesis by strong
  reasoning agent; source/link/arithmetic validation by deterministic tools;
  later execution by approved adapters and human-reviewed evidence capture.
- Input/output evidence contract when AI output is involved: dated primary
  claims and repository contracts in; proposed priority waves, bounded
  profiles, assumptions, and citations out; no hidden reasoning.
- Verification plan: dependency/priority/link synchronization, docs-only path
  check, and `git diff --check`; no tests or implementation.
```

## 1. Two simultaneous obligations

Every open P0/P1 capability is reviewed against:

1. **scale-free correctness** — the semantic and planning model must remain
   valid for QP-1/QP-2/QS-2;
2. **current execution evidence** — at least one deliberately small instance
   must compile, plan, validate, and execute or explicitly reject against a
   current profile.

Future scalability cannot excuse the absence of a runnable vertical slice.
Current hardware constraints cannot redefine source meaning.

## 2. Delivery profiles

| Profile | Role | Default acceptance boundary |
|---|---|---|
| `CH0_COMMON_PHYSICAL` | P0 cross-device smoke | 2–5 qubits, shallow static circuit, terminal measurement |
| `CH1_DIGITAL_RESEARCH` | P1 digital execution | normally <=16 active qubits and <=200 entangling operations; target-resolved |
| `CH1_ANALOG_RESEARCH` | P1 native evolution | 16–64 sites with explicit geometry/Hamiltonian/schedule |
| `SIM0_EXACT` | P0 exact oracle | normally <=20 qubits under the current resource profile |
| `SIM1_MIXED` | P1 mixed/channel oracle | normally <=10 qubits with explicit memory estimate |
| `NH5_NISQ_MODULAR` | 2026–2031 mitigated/modular bridge | 100–1,000 physical carriers; `5e3–2e4` qualified operations |
| `NH5_FT_MEGA` | 2026–2031 first useful FTQC | 100–300 logical carriers; `1e6–1e8` logical operations |
| `NH5_FT_GIGA` | 2026–2031 upper roadmap stress | 1,000+ logical carriers; `1e9`-class logical operations |
| `NH5_NATIVE_LARGE` | 2026–2031 large native system | `1e3–1e4` sites with geometry/loss/reload/QEC profile |
| `QP1/QP2/QS2_REFERENCE` | future stress only | compact hierarchy and exact symbolic resources; no hardware claim |

All numeric boundaries are profile fixtures. A capability snapshot may allow
more or less, and rejection is valid.

The NH5 family is neither current acceptance nor a BQ-0 declaration. It keeps
P0/P1 artifacts ready for announced systems that may arrive before the
household acceleration scenario begins.

## 3. P0 completion rule

An open P0 item is not complete merely because its DTO or verifier exists.
Where the capability reaches execution, its reviewed slices provide:

- a `SIM0_EXACT` semantic oracle;
- a `CH0_COMMON_PHYSICAL` OpenQASM or target-plan witness when representable;
- a named rejection when no current physical profile can preserve meaning;
- a QP-2/QS-2 compact-plan stress case when scale affects the design.

P0 does not require a live provider account for every slice. It requires a
provider-neutral artifact, capability validation, and at least one maintained
physical smoke path at the P0 integration gate.

Before LISS-0100, that physical smoke may be a human-authorized manual
submission of the validated artifact with imported execution evidence. It
must be labelled manual and is not evidence that an automated adapter exists.

## 4. P1 completion rule

P1 turns the foundation into useful current-machine workflows:

- one exact/small scientific oracle;
- one target-resolved current digital witness;
- an analog witness when native evolution is claimed;
- raw and derived results with uncertainty and provenance;
- bounded routing, shots, retries, cost, and mitigation;
- one approved live provider adapter by the P1 integration gate.

Unsupported scientific families remain explicit. General channels, continuous
models, and second-quantized mappings need only provide bounded current
instances, not arbitrary large physical execution.

## 5. Priority interpretation

- **P0 — executable foundation:** semantic IR, algorithm plan, verified passes,
  simulator port, portable static backend, target capability profile, dynamic
  semantic boundary, and representative-language review.
- **P1 — useful current quantum workflows:** current-bounded scientific
  lowerings, optimization, measurement/resource/routing, simulator adoption,
  dynamic/mixed execution, Host lifecycle/results/debugging, mitigation, and a
  first live adapter.
- **P2 — broaden and harden:** QIR/Rust-dependent interchange, advanced
  fault-tolerant algorithms, multi-provider production hardening, and authoring
  tools not required for the first useful workflow. NH5 delivered-machine
  enablement may enter P1/P2 through separately approved target adapters.
- **P3 / horizon:** BQ-0, personal appliance, utility FTQC, and quantum
  supercomputer realization work. These profiles continuously stress P0/P1
  contracts but do not block current delivery.

Priority denotes dependency and delivery criticality, not architectural
importance or permanent exclusion.

## 6. Evidence acceptance

Physical execution evidence is accepted only when it records the fields named
in the research note. A screenshot, provider success badge, or raw histogram
alone is insufficient.

Simulator evidence must not be represented as physical execution. Physical
noise must not silently weaken exact semantic assertions. Comparison occurs
through declared statistical acceptance and uncertainty contracts.

## 7. Review decisions

Adjudicator architecture approval is required for:

1. dual future-scale/current-execution obligations;
2. the five current delivery profiles and their non-normative ranges;
3. the four NH5 planned-system profiles and their roadmap-only status;
4. the P0 and P1 completion rules;
5. promoting first live provider integration and mitigation to P1;
6. moving QIR/Rust-dependent delivery behind the current OpenQASM path;
7. proposed ADR 0111 and WP-0029.
