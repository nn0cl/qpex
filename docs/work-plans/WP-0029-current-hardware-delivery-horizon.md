# WP-0029: Current-hardware delivery horizon

## Status

**Proposed Architecture Path plan. Documentation only; no implementation or
technology-selection permission.**

- Parent roadmap: [WP-0025](WP-0025-staqex-v1-north-star.md)
- Proposed authority:
  [ADR 0111](../architecture/adr/0111-current-hardware-first-delivery-horizon.md)
- Detailed contract:
  [current-hardware delivery envelope](../architecture/current-hardware-delivery-envelope.md)
- Research:
  [current hardware delivery evidence](../research/2026-07-30-current-quantum-hardware-delivery-envelope.md)
- Planning size: XL across many independently gated Issues
- Branch: `codex/p0-p1-delivery-horizon-review`
- Implementation permission: **none**

## Objective

Deliver one future-safe language/compiler through small, meaningful programs
that run on current simulators and current quantum computers.

The plan does not create a second “NISQ language.” Current-machine execution is
a bounded realization of the same source and semantic meaning.

## Execution-document rule

Every P0/P1 ID in this plan has a dedicated local Issue document linked from
[WP-0025](WP-0025-staqex-v1-north-star.md). Its Slice and phase may be executed
only through the
[bounded feature execution packet](../architecture/bounded-feature-execution-packet.md).
Roadmap prose alone is never implementation authority.

## P0 review result — executable foundation

### P0-A — accept and build semantic spine

Order:

1. Accept ADR 0108–0111.
2. LISS-0082 Slices A–E, optional F only if separately approved.
3. LISS-0083 bounded Algorithm Plan slices.
4. LISS-0087 verified pass manager.

Current evidence:

- Bell/GHZ and a 4–8-site finite spin witness remain recognizable from source
  through Semantic IR and Algorithm Plan;
- `SIM0_EXACT` provides deterministic probabilities/expectations;
- `CH0_COMMON_PHYSICAL` either produces a validated portable artifact or a
  named capability rejection;
- QP-2/QS-2 use the same compact contracts without expansion.

### P0-B — current execution exits

Order after the relevant P0-A contracts:

1. LISS-0094 simulator port and fake capability profiles.
2. LISS-0099 target capability snapshot/port.
3. LISS-0097 static OpenQASM subset first; dynamic/timing completion follows
   LISS-0077 capability slices.
4. LISS-0077 semantic/controller safety, then bounded dynamic simulator and
   current-target witness.

P0 does not select a simulator engine or live provider SDK. It makes those
choices replaceable and testable. The P0 physical smoke may use a
human-authorized manual submission of the validated portable artifact; it must
not be represented as an integrated adapter.

Every P0-B artifact is also validated against the four NH5 synthetic
capability profiles so planned 2026–2031 systems do not force a new flat IR or
provider-specific semantic fork.

### P0-C — programming-language review

LISS-0120 remains P0. Noether Forge keeps its ambitious 1,000–3,000-line source
scope, but physical execution uses reduced experiment configurations:

- 2–5-qubit smoke mission;
- 4–16-qubit digital research mission after P1 routing/resource support;
- 16–64-site native analog mission only after the analog planner/profile exists;
- full-size source remains inspectable even when a selected target rejects it.

## P1 plan — useful current quantum workflows

### P1-A — deterministic local truth and target feasibility

| Order | Issues | Outcome |
|---|---|---|
| 1 | LISS-0078, LISS-0079, LISS-0101 | coherent effects and validated scientific inputs |
| 2 | LISS-0095 | select exact initial simulator engines through technology review |
| 3 | LISS-0089, LISS-0090, LISS-0091 | exact optimization, measurement plans, resource/feasibility evidence |
| 4 | LISS-0092 | topology/native routing and scheduling against snapshots |
| 5 | LISS-0102, LISS-0103, LISS-0104 | lifecycle, results/uncertainty, debugging and evidence dossier |

Exit: one current digital program is exact-simulated, planned, routed, emitted,
and represented as a complete provider-neutral job/result lifecycle.

### P1-B — bounded scientific breadth

| Order | Issues | Current-machine slice | Deferred breadth |
|---|---|---|---|
| 1 | LISS-0086 | small spin/fermion mappings, normally <=12 active qubits | large chemistry and external adapters |
| 2 | LISS-0088 | Suzuki/QDrift and hardware-efficient preparation first | qubitization/large LCU fault-tolerant paths |
| 3 | LISS-0085 | explicit small grids mapped within `SIM0_EXACT`/`CH1_DIGITAL_RESEARCH` | high-resolution continuous workloads |
| 4 | LISS-0084, LISS-0096 | <=10-qubit mixed/channel/dynamic simulator oracle; bounded current dynamic witness | general large open-system execution |

Exit: at least one finite quantum-matter, one mapped second-quantized, and one
dynamic or mixed protocol has an honest current-profile result or named
rejection.

### P1-C — physical evidence endcap

Order:

1. LISS-0093 bounded readout mitigation, symmetry verification, and carefully
   reviewed ZNE slice; raw results always retained.
2. LISS-0100 technology selection and one live provider adapter.
3. Re-run selected Noether Forge reduced missions through the physical path.

Exit:

- at least one `CH1_DIGITAL_RESEARCH` physical run;
- analog artifact/execution evidence when analog support is claimed;
- source/compiler/plan/capability/calibration/artifact/result provenance;
- raw and mitigated uncertainty reported separately;
- no provider type in Domain, Semantic IR, or Algorithm Plan.

## P2 plan — broaden and harden

- delivered NH5 target enablement for megaquop/gigaquop fault-tolerant and
  large-native machines through separately selected adapters;
- LISS-0098 QIR profile/toolchain after Rust/toolchain need becomes concrete.
- LISS-0105 LSP/notebook and deeper physicist authoring tools.
- advanced LISS-0088 qubitization/LCU and fault-tolerant preparation slices;
- broader LISS-0093 PEC and high-overhead mitigation;
- second provider, production credential isolation, quota/cost operations;
- larger open-system, continuous, chemistry, and analog profile coverage;
- release-scale differential, resource, and performance suites.

## P3 / horizon plan

- BQ-0 qualification and logical-resource evidence;
- QP-1 personal workstation realization;
- QP-2 household appliance workflows;
- QS-2 partitioned campaign planning and fault-tolerant network execution.

P3 realization is not required to accept the scale-free contracts used by P0
and P1.

## Cross-priority acceptance laws

1. Every executable feature names its supported delivery profiles.
2. Every unsupported profile produces a stable rejection.
3. Simulator, emulator, and physical evidence are never conflated.
4. Current profile numbers are fixtures, not semantic maxima.
5. QP-2/QS-2 compact-plan tests remain present where scale is relevant.
6. NH5 profiles remain synthetic until a matching machine is independently
   capability-checked; roadmap publication alone is not execution evidence.
7. Physical evidence records calibration, attempts, shots, raw results,
   uncertainty, and mitigation.
8. Provider/SDK decisions occur only in adapter technology Issues.
9. Each Issue retains independent Red/Green/Refactor approvals.

## Next safe action

With the Adjudicator's P0/Slice A Refactor approval:

1. review the complete LISS-0082 Slice A implementation and evidence;
2. authorize LISS-0082 Slice B Phase 1 Red separately;
3. do not start LISS-0083, a simulator selection, or provider selection from
   this plan alone.
