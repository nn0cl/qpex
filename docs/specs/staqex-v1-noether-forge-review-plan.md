# Staqex v1 Noether Forge language-review plan (LISS-0120 Slice A)

| Field | Value |
|---|---|
| Status | **in_progress** — Slice A–D complete; Slice E human review pending |
| Authority | WP-0025 P0-C; WP-0029 P0-C; ADR 0108–0111 **Accepted**; LISS-0082 A–F complete |
| Depends on | LISS-0082 **complete** (E+F inspection path); ADR 0108–0111 Accepted |
| Extends (non-blocking) | LISS-0083, LISS-0094, LISS-0097 P0 (planning/backend honesty) |
| Issue | [LISS-0120](../issues/LISS-0120-representative-program-language-review-gate.md) |
| Intake | [2026-07-30](../collaboration/traces/2026-07-30-liss-0120-language-review-gate-intake.md); refresh [2026-07-31](../collaboration/traces/2026-07-31-liss-0120-slice-a-refresh.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: Slice A only — lock Noether Forge as the
  review candidate, ownership map, line/readability metrics, rubric, and
  accepted-syntax inventory for the first static language review.
- Specifications and files inspected: LISS-0120 Issue; prior 2026-07-30
  intake; WP-0025/0029 P0-C; ADR 0108–0111 Accepted; LISS-0082 complete;
  LISS-0094/0097/0077 P0 exits now available for honest backend lanes.
- Component boundaries: scientific policy stays in `.sqx` modules; runners
  and inspection glue stay thin; RNG/source/sinks remain existing ports; no
  provider DTOs in the sample.
- Applicable constraints: Never Leave the State; Joint lineage; terminal
  Static measurement; no continuous/mixed/dynamic in first candidate; no
  generated padding for line quotas; sample metrics ≠ repo-wide lint laws.
- Decisions: gates for full review candidate are now open (0082 E+F + ADR
  Accepted). Slice A remains docs-only. Implementation Slices B–E stay
  separately gated. Optional F (plan/simulator/dynamic) remains optional.
- Included/omitted context: include Issue rubric/module map and current
  foundation exits; omit provider SDKs, live QPU, new syntax invention.
- Task routing: Architecture Path docs synthesis; later Feature Path for B+.
- Verification: docs sync + link/whitespace checks; no source/compiler/tests.
```

## 1. Gate status (2026-07-31 refresh)

| Gate | Status |
|---|---|
| ADR 0108–0111 | **Accepted** |
| LISS-0082 Slice D | **complete** |
| LISS-0082 Slice E + F inspection path | **complete** |
| LISS-0083 / 0094 / 0097 P0 | **complete** (extend honesty; not blockers for first review) |
| LISS-0077 P0 controller | **complete** (dynamic extension still out of first candidate) |

Therefore Slice A may be approved now, and Slice B (300–500-line prototype)
may be authorized next without waiting for further architecture ADRs.

## 2. Candidate lock

**Noether Forge** — finite quantum-matter discovery mission (unchanged from
Issue default). Domain change still requires Adjudicator scope approval.

Scientific spine (static first candidate only):

- finite qubit/qudit lattices;
- Ising/XY/Heisenberg-like typed couplings and Hamiltonian terms;
- symmetry / conservation declarations;
- product / defect / domain-wall / entangled initial protocols;
- sudden/scheduled quenches with typed duration/parameter contracts;
- magnetization, correlation, structure-factor, return-probability,
  symmetry-sector observation intents;
- provenance-rich phase evidence dossier;
- `SIM0_EXACT` and static `CH0_COMMON_PHYSICAL` honesty lanes from one meaning.

Out of first candidate: continuous discretization, mixed/channel, dynamic
controller execution, live QPU, provider SDKs.

## 3. Source ownership map (illustrative names)

```text
noether_forge/
  main_static.sqx
  domain/          lattice, site, couplings, experiment_config
  physics/         model_families, hamiltonian_builder, initial_states,
                   observables, symmetries
  application/     quench_protocol, spectroscopy_protocol, phase_evidence,
                   result_contract
  presentation/    evidence_dossier
```

Split by responsibility, not line quota.

## 4. Line / readability metrics (sample constraints)

| Measure | Contract |
|---|---|
| Total `.sqx` | 1,000–3,000 non-blank physical lines (full candidate) |
| Slice B prototype | 300–500 non-blank `.sqx` lines |
| File size | target 80–220; hard max 300 non-blank |
| Function body | preferred ≤30; exception ≤45 with rationale; never >60 |
| Module count | expected 8–20 for full candidate |
| Generated / padded content | forbidden for quota |

## 5. Accepted syntax inventory (first candidate)

Allowed to exercise from already-Accepted / Kernel-shipped surface only:

- modules, visibility (`pub` / `_`), `struct` / `class` / `enum` / `namespace`
  as already shipped;
- typed finite carriers and Joint/`State` continuity;
- coherent evolve/apply paths and terminal `measure`;
- parameters/`Param` as already contracted;
- explicit Hamiltonian / operator construction patterns already expressible.

Forbidden in the sample:

- inventing new syntax or semantics;
- dynamic `Controller` execution paths (LISS-0077 may be referenced as
  non-goal commentary only);
- provider objects, credentials, network, Job APIs inside `.sqx`.

## 6. Rubric (human + automated support)

Physicist pass and maintainer pass must both record evidence for:

Domain directness · State continuity · Control clarity · Type/unit friction ·
Module/OOP scale · Diagnostics · IR traceability · Backend honesty ·
Cognitive load.

Findings classify as: language semantics | stdlib | compiler/diagnostics |
architecture/IR | documentation | sample-local design. Behavior/architecture
fixes become separate Issues/ADRs — never silent sample patches.

## 7. Slice approval unit (reduced gates)

| Step | Approval |
|---|---|
| A — this specification | Architecture / docs — **complete** |
| B — vertical prototype | Architecture + Red + Green + Refactor — **complete** (`8/8`) |
| C+D — full candidate + IR evidence | integrated Red+Green+Refactor — **complete** (`8/8`, 1017 lines) |
| E — human language review | Adjudicator review of rubric + friction ledger |
| F — optional extensions | new scope only |

This keeps Adjudicator stops few while preserving that Slice A cannot create
`.sqx` or compiler changes.

## 8. Explicit non-goals

Kitchen-sink expansion of LISS-0020; continuous/mixed/dynamic first candidate;
generated padding; repo-wide method/file lint mandates; silent language fixes
inside the sample.
