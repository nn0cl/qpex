# LISS-0120: Representative program language review gate

## Metadata

- Local issue ID: LISS-0120
- Status: **proposed** — Phase 0 design intake only
- Phase: `phase-0-design`
- Type: representative application / language design review / integration gate
- Priority: P0
- Initial planning size: XL
- Current planning size: XL
- Owner/agent: TBD
- GitHub issue: none
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on:
  - architecture start gate: [ADR 0108](../architecture/adr/0108-quantum-semantic-ir-value-region-contract.md)
    **Accepted**;
  - machine-envelope gate:
    [ADR 0109](../architecture/adr/0109-quantum-machine-scale-and-model-envelope.md)
    **Accepted**;
  - capacity-horizon gate:
    [ADR 0110](../architecture/adr/0110-optimistic-quantum-capacity-horizon.md)
    **Accepted**;
  - delivery-horizon gate:
    [ADR 0111](../architecture/adr/0111-current-hardware-first-delivery-horizon.md)
    **Accepted**;
  - prototype start gate: [LISS-0082](LISS-0082-quantum-semantic-ir.md)
    Slice D complete and reviewed;
  - review-candidate gate: LISS-0082 Slice E complete plus Slice F or an
    equivalent reviewed Quantum Semantic IR inspection path;
  - planning/backend extension only: LISS-0083 and LISS-0094.
- Blocks: representative-program language review; follow-up language/DX Issues
  discovered by that review
- Related:
  - [Quantum Semantic IR contract](../architecture/quantum-semantic-ir-contract.md)
  - [machine scale/model envelope](../architecture/quantum-machine-scale-and-model-envelope.md)
  - [optimistic capacity horizon](../architecture/quantum-capacity-horizon-scenarios.md)
  - [current-hardware delivery envelope](../architecture/current-hardware-delivery-envelope.md)
  - [LISS-0020](LISS-0020-capstone-quantum-observatory.md) showcase precedent
  - [physicist × DX harmony](../architecture/physicist-dx-harmony.md)
  - [source code quality](../collaboration/source-code-quality.md)
- Related branch: later `feature/liss-0120-representative-program-*`
- Implementation permission: **none**
- Post-review requirement: every implementation slice requires separate
  Phase 1/2/3 approval

## Problem

Small examples are effective for conformance but can hide language-design
friction:

- repeated boilerplate appears only after several modules cooperate;
- visibility and ownership become difficult only at realistic file size;
- short demonstrations can bypass domain modelling, diagnostics, and error
  recovery;
- IR boundaries may look coherent in isolated tests while losing source
  traceability across a full application;
- a kitchen-sink showcase can maximize feature count without resembling code a
  user would maintain.

The project therefore needs a deliberate point at which Staqex is reviewed as
a programming language through one coherent, maintainable application rather
than through isolated syntax examples.

Repository baseline at intake:

- the current A10 Mission Observatory source is 124 physical `.sqx` lines;
- all current official `.sqx` examples together are 857 physical lines and 662
  non-blank lines.

The requested lower bound is therefore larger than the current complete
example catalog. This confirms XL scope and makes a staged vertical prototype
necessary; it must not be treated as a routine example addition.

## Objective

Build one finite, scientifically credible representative program of
approximately **1,000–3,000 Staqex source lines** and use it to review:

- whether the language expresses the domain directly;
- whether Never Leave the State and the Joint store remain understandable at
  application scale;
- whether module, visibility, type, phase, resource, and measurement rules
  produce maintainable code;
- whether HIR → Physics IR → Quantum Semantic IR preserves recognizable
  intent and useful diagnostics;
- whether implementation workarounds reveal language, standard-library,
  compiler, or documentation gaps.

This is a review gate, not a requirement to add features merely to make the
sample impressive.

## Candidate application

The default candidate is **Noether Forge — a finite quantum-matter discovery
mission**.

Noether Forge studies small, exactly specified quantum lattices and assembles
an evidence dossier for symmetry, phase structure, and non-equilibrium
response. Its first review candidate does not claim experimental material
discovery. It demonstrates how a physicist could define candidate models,
design quench/spectroscopy protocols, compare observables, and preserve the
reasoning path from source equations to executable finite semantics.

The scientific spine is:

- finite qubit/qudit lattices, avoiding unresolved continuous-discretization
  ordering;
- Ising/XY/Heisenberg-like model families expressed through typed couplings
  and explicit Hamiltonian terms;
- symmetry declarations and conservation checks;
- product, defect, domain-wall, and entangled initial-state protocols;
- sudden and scheduled quenches with typed duration/parameter contracts;
- magnetization, correlation, structure-factor, return-probability, and
  symmetry-sector observation intents;
- comparison of equilibrium-like and driven signatures without silently
  turning numerical evidence into a theorem;
- simulator and static-QPU-oriented entry points derived from one semantic
  model;
- a provenance-rich **phase evidence dossier** that separates exact facts,
  approximation obligations, observed results, and interpretation.

The application should answer an ambitious but honest question:

> Can Staqex express a reproducible search for signatures of quantum phases
> while keeping physical intent, Joint-state continuity, and compiler evidence
> visible from source to execution?

The candidate is narrower in semantics but larger in sustained responsibility
than LISS-0020's Quantum Observatory. It should read like one maintainable
scientific application, not a catalog of unrelated features or a fictional
claim of quantum advantage.

Optional future missions may add open-system sensing, adaptive protocols, or
larger realization planning only after LISS-0084, LISS-0077, and LISS-0083.

Changing the application domain requires Adjudicator scope approval but not a
new ADR unless it changes architecture or dependencies.

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: define and later build one coherent
  1,000–3,000-line Staqex program that exposes language and compiler friction
  at realistic maintenance scale.
- Specifications and files inspected: agent quickstart; local Issue planning;
  implementation readiness; WP-0025; LISS-0020; LISS-0082 and its proposed
  detailed contract; current examples catalog and Shipping Kernel layout.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  source modules own scientific domain concepts; runner/inspection glue stays
  thin; RNG/source/sinks remain existing ports. Candidate source VOs include
  lattice size, site identity, coupling, duration, observable identity, and
  experiment configuration; no provider DTOs.
- Applicable constraints: Never Leave the State; one Joint store; terminal
  Static Kernel measurement; provider neutrality; no hidden discretization or
  approximation; Clean Architecture; readable source and phase gates.
- Decisions, assumptions, and unresolved ambiguities: ADR 0108–0111 are not
  yet Accepted; the exact inspection surface is Slice F or an equivalent
  reviewed path; the first candidate excludes continuous, mixed, and dynamic
  semantics; current/NH5 execution uses reduced configurations.
- Included and omitted AI context: include accepted language/IR contracts,
  relevant examples, and only source/compiler paths needed by each slice; omit
  provider SDKs, credentials, unrelated examples, and unaccepted future
  syntax.
- Task routing (model/assistant/tool): language/application design by a capable
  coding agent; line-budget, import-graph, compilation, and golden checks by
  deterministic tools; human/Adjudicator review for readability and language
  judgement.
- Input/output evidence contract when AI output is involved: accepted
  specifications and named example requirements in; readable source,
  deterministic diagnostics/IR snapshots, and a finding ledger out; no hidden
  reasoning or unsupported scientific claims.
- Verification plan: line/size checks, compile/inspect/run lanes, source-to-IR
  provenance checks, deterministic terminal-measurement evidence, reviewer
  rubric, and full regression suite as separately approved.
```

## Source-size and readability contract

The review candidate must satisfy all of the following without artificial
padding:

| Measure | Contract |
|---|---|
| Total Staqex source | 1,000–3,000 non-blank physical lines across `.sqx` files |
| File size | target 80–220 lines; hard maximum 300 non-blank lines |
| Function/method body | preferred maximum 30 non-blank lines |
| Function exception | up to 45 lines only with a local responsibility rationale; no body over 60 lines |
| Module count | expected 8–20 `.sqx` files, adjusted only for coherent ownership |
| Generated content | forbidden from satisfying the line target |
| Tests, runner scripts, READMEs | excluded from the 1,000–3,000 source count |

Comments count as non-blank source because they affect reading cost. The
minimum must not be reached by duplicated declarations, repeated fixtures,
decorative comments, or speculative wrappers.

The limits are review constraints for this sample, not new language laws or
repository-wide lint rules.

## Proposed module responsibilities

Names are illustrative and may change during the accepted design slice.

```text
noether_forge/
  main_static.sqx
  domain/
    lattice.sqx
    site.sqx
    couplings.sqx
    experiment_config.sqx
  physics/
    model_families.sqx
    hamiltonian_builder.sqx
    initial_states.sqx
    observables.sqx
    symmetries.sqx
  application/
    quench_protocol.sqx
    spectroscopy_protocol.sqx
    phase_evidence.sqx
    result_contract.sqx
  presentation/
    evidence_dossier.sqx
```

The split is by responsibility, not by reaching a line quota. Business and
physical policy must not be hidden in runners, output adapters, or generated
fixtures.

## Acceptance scenarios

1. **Given** the representative program, **when** a reviewer reads any source
   file, **then** the file is at most 300 non-blank lines, responsibilities are
   coherent, and functions are normally at most 30 body lines.
2. **Given** the complete source tree, **when** the deterministic line counter
   runs, **then** `.sqx` source totals 1,000–3,000 non-blank lines without
   generated or duplicated padding.
3. **Given** the static experiment entry point, **when** it is compiled and
   executed, **then** all intermediate quantum values remain one Joint state
   lineage and classical observation occurs only at terminal measurement.
4. **Given** the same source, **when** HIR, Physics IR, and Quantum Semantic IR
   are inspected, **then** acting spaces, transformations, parameters,
   resources, exactness obligations, and source provenance remain
   recognizable across stages.
5. **Given** source-native finite carriers, **when** semantic lowering runs,
   **then** it does not invent discretization, mapping, gates, shots, target
   capabilities, or provider details.
6. **Given** an intentionally invalid variant for each major boundary, **when**
   it is checked, **then** diagnostics identify the relevant source and public
   rule rather than failing in a backend adapter.
7. **Given** simulator-oriented and static-QPU-oriented review lanes, **when**
   they derive from the program, **then** they share source and semantic
   meaning while honestly reporting unsupported downstream realization.
   The review distinguishes a local appliance profile from future
   utility-scale hierarchical planning without changing source semantics.
8. **Given** the completed review, **when** friction is classified, **then**
   every finding is recorded as one of: language semantics, standard library,
   compiler/diagnostics, architecture/IR, documentation, or sample-local
   design.
9. **Given** a finding that requires behavior or architecture change, **when**
   follow-up is proposed, **then** it receives a separate Issue/ADR and is not
   repaired silently inside the sample.
10. **Given** QP-2 and QS-2 synthetic target profiles, **when** the sample is
    inspected and planned, **then** the same source meaning survives and
    compiler evidence grows with compact hierarchy rather than expanded
    operation count.
11. **Given** reduced Noether Forge configurations, **when** current and NH5
    profiles are selected, **then** 2–5-qubit physical smoke, bounded digital
    and analog research missions, or explicit capability rejection use the
    same source model and evidence vocabulary.

## Review rubric

The Adjudicator review records evidence for:

| Dimension | Review question |
|---|---|
| Domain directness | Does the source resemble the scientific model rather than compiler plumbing? |
| State continuity | Is the Joint state lineage obvious without following hidden mutation? |
| Control clarity | Can coherent control, resolved static selection, and terminal measurement be distinguished by reading source and IR? |
| Type and unit friction | Do types reject physical mistakes while remaining writable? |
| Module/OOP scale | Do imports, visibility, structs/classes, and methods remain understandable across files? |
| Diagnostics | Do representative failures point to source intent and the violated rule? |
| IR traceability | Can a reviewer follow a source concept through HIR, Physics IR, and Quantum Semantic IR? |
| Backend honesty | Are simulator/QPU limitations explicit without changing semantics? |
| Cognitive load | Are names, functions, files, and abstractions proportionate to the problem? |

The review must include at least one physicist-oriented reading pass and one
maintainer-oriented reading pass. Automated checks support but do not replace
those judgements.

## Implementation-point estimate

This estimate is dependency-based, not a calendar commitment.

| Point | Earliest honest work | What can be learned | Limitation |
|---|---|---|---|
| **Now** | Issue, rubric, candidate architecture, fixture-free source outline | review scope and desired programming style | current large sample would test the old pipeline, not the proposed Semantic IR |
| **After LISS-0082 Slice D review** | 300–500-line vertical prototype under its own approved Red/Green/Refactor slices | source ergonomics, Joint state/control/measurement/resource shape | no complete Physics→Semantic lowering evidence |
| **After LISS-0082 Slice E + Slice F or equivalent inspection path** | full 1,000–3,000-line review candidate | recommended language review: source through Quantum Semantic IR with provenance | Algorithm Plan and standardized simulator ports are not yet reviewed |
| **After LISS-0083 + LISS-0094** | planning/backend extension of the same sample | realization-choice ledger and simulator/QPU plan parity | not required to perform the first programming-language review |
| **After LISS-0077/0084/0096** | optional dynamic/mixed extension | adaptive and open-system programming review | separate scope; must not delay the static first review |

### Recommended gate

Begin full sample implementation only after LISS-0082 Slice D is reviewed and
the Slice E/F interface is stable enough to avoid sample-owned compiler
workarounds. Declare the sample **reviewable** only after:

1. LISS-0082 Slice E is complete and reviewed;
2. a reviewed source-to-Quantum-Semantic inspection path exists;
3. all acceptance fixtures use source-native finite carriers;
4. ADR 0108 is Accepted;
5. ADR 0109 is Accepted;
6. ADR 0110 is Accepted;
7. ADR 0111 is Accepted;
8. the sample's Phase 1 tests and review rubric are separately approved.

This is the earliest point where a 1,000–3,000-line example can test the new
architecture rather than merely demonstrate the already-shipping evaluator.

## Proposed slices

| Slice | Scope | Gate |
|---|---|---|
| **A — review specification** | candidate domain, source ownership map, line metric, rubric, accepted syntax inventory | docs-only Architecture approval |
| **B — vertical prototype** | 300–500 source lines covering one state-preparation → evolve → observable → terminal-measure path | after LISS-0082 D; separate Phase 1 Red |
| **C — review candidate** | expand coherently to 1,000–3,000 source lines and 8–20 modules | after stable E/F inspection contract; separate phases |
| **D — source-to-IR evidence** | HIR/Physics/Semantic golden catalog and invalid-boundary diagnostics | after LISS-0082 E/F; separate phases |
| **E — human language review** | physicist and maintainer rubric results; friction ledger; follow-up Issues | post-implementation review; no silent fixes |
| **F (optional)** | Algorithm Plan/simulator-port or dynamic/mixed extension | only after named dependencies and new scope approval |

Every Slice must be delivered through the
[bounded feature execution packet](../architecture/bounded-feature-execution-packet.md).
The sample may expose a design defect but must not repair language semantics,
IR contracts, or provider behavior outside its approved Slice.

## Non-goals

- no new syntax or semantics hidden inside example implementation;
- no replacement for small conformance examples;
- no recreation or expansion of the LISS-0020 kitchen sink;
- no continuous discretization in the first candidate;
- no general channel, dynamic controller, live QPU, provider SDK, credential,
  network, cost, or calibration work;
- no generated code used to satisfy source-size targets;
- no repository-wide 30-line-method or 300-line-file mandate;
- no implementation before the named architecture and phase gates.

## Adjudicator decision points

- [ ] Approve LISS-0120 as the representative-program language review gate.
- [ ] Approve Noether Forge, the finite quantum-matter discovery mission, or
      select another ambitious finite application domain.
- [ ] Approve the line/readability metrics as sample review constraints.
- [ ] Confirm the recommended implementation point: prototype after LISS-0082
      D; full review candidate after E + F/equivalent inspection path.
- [ ] Approve Slice A review specification only.
- [ ] Later approve Slices B–F and each AT-TDD phase separately.

## AI planning record

### AIP-0120-001

- Status: proposed
- Authoring environment: Codex desktop coding agent
- Model/reasoning setting: N/A — exact UI setting not exposed in repository
  evidence
- Created at: 2026-07-30
- Planning size: XL
- Intended execution route: Architecture Path Slice A; then Feature Path
  Phase 1 Red → Phase 2 Green → Phase 3 Refactor for each implementation slice
- Intended scope: one maintainable finite scientific program, 1,000–3,000
  Staqex source lines, source-to-IR evidence, deterministic execution, and
  human language review
- Estimated token range: 120,000–300,000 aggregate across all separately
  approved slices
- Estimated token midpoint: 210,000
- Token metric: aggregate model input/output tokens across planning,
  implementation, verification, review, and revisions
- Estimation basis: XL multi-slice source application; 8–20 modules; line and
  responsibility constraints; three IR evidence layers; deterministic and
  human review; expected follow-up classification
- Assumptions: LISS-0082 contracts stabilize before full expansion; no new
  provider/dependency; no new syntax implemented in this Issue
- Confidence: low for aggregate token range before Slice A source inventory;
  medium for dependency-based implementation point
- Revises: none
- Revision reason: n/a
- Superseded by: none

## Next allowed operation

After Adjudicator Issue/scope approval, execute **Slice A documentation and
review specification only**. Do not create `.sqx` source, tests, compiler
changes, or runtime changes until the corresponding phase and dependency gates
are separately approved.
