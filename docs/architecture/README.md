# Architecture Overview

The project uses Clean Architecture with **local-first** runtime assumptions
(CLI and library on the developer machine).

**Honesty:** the shipping Kernel that runs `examples/` today is the **Python**
tree under `compiler/staqex/`. The long-term application core is still specified
toward a **Rust** VM / simulator with QPU backends as ports — not a second
semantics. Agents must not invent a second language meaning for “Rust-only”
phrases in older ADRs.

**Design horizon:** Staqex targets the *ideal final form* of a language for
generalized quantum computers on a hundred-year horizon — not the shortest
path to something that runs. See
[ADR 0095](adr/0095-design-horizon-ideal-form-first.md), which governs how
slices are scoped, when a deferral is acceptable, and how the pervasive
“MVP” vocabulary in older documents is to be read (historical scope, never
target end-state).

## Layers

### Domain

Pure Staqex language semantics: probability distributions (Discrete PMF in
MVP), convolution / pushforward arithmetic, and collapse rules for
`measure`.

Must not depend on:

- any UI framework.
- SQL schemas, ORM structs, vector DB SDKs, or file-system APIs.
- LLM SDKs, cloud AI SDKs, or third-party provider APIs.
- concrete RNG or I/O implementations (those are ports/adapters).

### UseCase

Coordinates domain behavior through ports.

Examples:

- Parse and evaluate a Staqex program fragment under MVP scope A.
- Execute `measure` by sampling through `RngPort` and reporting via
  `MeasureSinkPort`.

### Ports

Interfaces owned by the application core.

Ports isolate every external resource named in `CLAUDE.md` / `AGENTS.md`
under "External Resources Must Be Ports".

### Adapters

Framework and infrastructure implementations (CLI I/O, OS RNG, file
loaders).

Adapters must not define language semantics (no ad-hoc scalar shortcuts).

### Front-End / Delivery

Local CLI (and library API) presents results and accepts source input.

It must not own distribution arithmetic or collapse policy.

## Runtime Direction

Runs locally as a CLI / library. QPU backends and cloud providers are future
optional adapters, not part of MVP.

## Selected Technology

- Runtime/shell: local CLI (`python3 -m compiler.staqex` today; Rust CLI later).
- Kernel language (shipping): Python 3 (`compiler/staqex/`).
- Application language (target): Rust (Cargo workspace) for VM / ports.
- UI framework: none (MVP).
- Distribution goal: MIT OR Apache-2.0 dual license; eventual QPU backend.

## Detailed Rules

- `project-structure.md`: where files belong.
- `testing-strategy.md`: AT-TDD test placement.
- `implementation-readiness.md`: checklist before coding.
- `dependency-policy.md`: package dependency checking policy.
- `ai-request-routing.md`: AI payload selection and task routing.
- `io-reasoning-contracts.md`: AI input/output/reasoning contracts.
- `external-resource-adoption-contract.md`: optional contract for adopting
  AI-generated or human-sourced external content/data resources.
- `staqex-language-axioms.md`: immutable Staqex language axioms.
- `staqex-positioning.md`: Accepted manifesto (never leave the state; joint store).
- **`adjudicator-language-vision.md`**: **Accepted** (2026-07-31) Adjudicator
  orientation — language for physicists; ideal form first; anti “equation →
  broken DSL → QPU”; writeable≠executable; Outer/Kernel/lane boundaries
  (binding for agents).
- **`physicist-dx-harmony.md`**: physicist mental model × programmer DX
  (physicist primary; `enum` / `struct` / `class` / `pub` / `_`; no
  `protected` / no required `module-info`); links the vision doc.
- **`surface-modernization-north-star.md`**: **Accepted** (2026-08-02) —
  de-enterprise surface look (WP-0088); not axiom rewrite; Wave A plan approved.
- **`physicist-minimal-dialect.md`**: **Accepted** (2026-08-02) ~10-line
  blackboard dialect (pedagogy / teaching law; not axiom or Kernel approval).
- **`staqex-destructive-simplification-sketch.md`**: **Accepted** (2026-08-02)
  cut/demote policy sketch (not Kernel-deletion approval).
- **`physicist-source-friction-ledger.md`**: honest gaps where source still
  drifts from research reading (feeds P1; not an ADR).
- **`staqex-design-philosophy.md`**: 設計思想アーカイブ（数式↔コード直体感・Type-First・物理公理コンパイラ）。
- `staqex-syntax-vocabulary.md`: Surface lexicon (`state` / `when` / `evolve` / `measure`).
- `staqex-token-specification.md`: Lexer/Parser tokens (ADR 0035).
- `staqex-ast-design.md`: AST nodes and $\mathsf{Joint}\to\mathsf{Joint}$ eval axis.
- `staqex-type-system.md`: `State<T>`, lift, classical boundary (ADR 0018).
- `staqex-dimensional-types.md`: Type-First + $(L,M,T)$ algebra (ADR **0037**).
- `staqex-abstraction-model.md`: generics, traits, `system` (ADR 0019).
- `staqex-stdlib-combinators.md`: `map` / `project` / `interfer` / `System` (ADR 0021).
- `staqex-stdlib-packages.md`: math/io/state/collection/debug (ADR 0031).
- **Normative Language Spec:** `docs/specs/staqex-language-specification.md`
  (**v1.0**, promoted 2026-07-28) + grammar `docs/specs/grammar/staqex.ebnf`
  (named inventory sync: LISS-0072 Slice D **complete**).
- **v1 north star:** [`staqex-v1-language-north-star.md`](../specs/staqex-v1-language-north-star.md)
  + [ADR 0106](adr/0106-staqex-v1-north-star-language-and-compiler.md) (**Accepted
  with conditions**, 2026-07-27) +
  [`staqex-v1-compiler-blueprint.md`](staqex-v1-compiler-blueprint.md).
  LISS-0068 rebaseline and promotion are **complete**; next implementation
  gate is LISS-0069. Register:
  [`staqex-v1-normative-rebaseline-register.md`](../specs/staqex-v1-normative-rebaseline-register.md).
- **North-star implementation roadmap:** [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
  and the supporting
  [language/compiler landscape research](../research/2026-07-27-quantum-language-compiler-landscape.md).
- **Quantum Semantic IR contract:**
  [`quantum-semantic-ir-contract.md`](quantum-semantic-ir-contract.md),
  [LISS-0082 plan](../specs/staqex-v1-quantum-semantic-ir-plan.md), and
  [ADR 0108](adr/0108-quantum-semantic-ir-value-region-contract.md)
  (**Accepted**, 2026-07-30). Soft `CompileResult.quantum_semantic_ir` wire
  (Slice F) is complete (PR #160).
- **Resource estimation and feasibility:**
  [LISS-0091](../issues/LISS-0091-resource-estimation-feasibility.md) and
  [resource-estimation plan](../specs/staqex-v1-resource-estimation-plan.md)
  (integrated package **complete**; Red/Green/Refactor). Distinct from
  host [ADR 0100](adr/0100-resource-budget-policy.md)
  `SimulationResourceEstimate`.
- **Target layout / routing / schedule:**
  [LISS-0092](../issues/LISS-0092-layout-routing-native-scheduling.md) and
  [target-routing plan](../specs/staqex-v1-target-routing-plan.md)
  (integrated package **complete**; Red/Green/Refactor). Synthetic
  `TargetSnapshot` fixtures; LISS-0099 live ports deferred.
- **Target capability profile / physical port:**
  [LISS-0099](../issues/LISS-0099-target-capability-physical-port.md) and
  [target-capability plan](../specs/staqex-v1-target-capability-plan.md)
  (integrated package **complete**, PR #165). Fake port + CH0/CH1/NH5
  fixtures; optional projection into LISS-0092 snapshots.
- **Simulator port / capability profiles:**
  [LISS-0094](../issues/LISS-0094-simulator-port-capability-profiles.md) and
  [simulator-port plan](../specs/staqex-v1-simulator-port-plan.md)
  (integrated package **complete**, PR #166). Fake `SIM0_EXACT` /
  `SIM1_MIXED`; no engine selection (LISS-0095).
- **OpenQASM static CH0 subset:**
  [LISS-0097](../issues/LISS-0097-openqasm-3-backend-completion.md) and
  [openqasm-ch0 plan](../specs/staqex-v1-openqasm-ch0-plan.md)
  (P0 package **complete**, PR #167). D/E/F deferred.
- **Dynamic QPU controller / feed-forward:**
  [LISS-0077](../issues/LISS-0077-dynamic-qpu-controller-feed-forward.md) and
  [dynamic-qpu plan](../specs/staqex-v1-dynamic-qpu-plan.md)
  (P0 package **complete**; Red/Green/Refactor). E deferred.
- **Representative program language review:**
  [LISS-0120](../issues/LISS-0120-representative-program-language-review-gate.md)
  (**rejected / deferred**) and
  [rebaseline plan](../specs/staqex-v1-representative-program-rebaseline.md)
  (P0 example health → P1 coverage ledger → Physicist × DX showcase).
- **Physicist source friction (working ledger):**
  [`physicist-source-friction-ledger.md`](physicist-source-friction-ledger.md)
  — where writing `.sqx` today still breaks equations or drifts from research
  reading (feeds P1; not an ADR).
- **Classical coefficient vs LINEAR:**
  [ADR 0114](adr/0114-classical-coefficient-elaboration-vs-linear.md)
  (**Accepted**, 2026-07-31) +
  [LISS-0121](../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md)
  (ready for Phase 1 pending phase approval) — named couplings as elaboration
  scalars; fold-invariant.
- **Future machine scale/model envelope:**
  [`quantum-machine-scale-and-model-envelope.md`](quantum-machine-scale-and-model-envelope.md)
  and [ADR 0109](adr/0109-quantum-machine-scale-and-model-envelope.md)
  (**Accepted**, 2026-07-30): Personal Quantum Appliance ↔ utility-scale FTQC,
  hierarchy-preserving plans, generalized target profiles, no cloud
  assumption.
- **Optimistic quantum capacity horizon:**
  [`quantum-capacity-horizon-scenarios.md`](quantum-capacity-horizon-scenarios.md)
  and [ADR 0110](adr/0110-optimistic-quantum-capacity-horizon.md)
  (**Accepted**, 2026-07-30): QP-1/QP-2/QS-2 stress profiles; never language
  maxima or delivery forecasts.
- **Current and five-year delivery horizon:**
  [`current-hardware-delivery-envelope.md`](current-hardware-delivery-envelope.md),
  [WP-0029](../work-plans/WP-0029-current-hardware-delivery-horizon.md), and
  [ADR 0111](adr/0111-current-hardware-first-delivery-horizon.md)
  (**Accepted**, 2026-07-30): runnable P0/P1 current profiles plus NH5 roadmap
  stress profiles, without turning hardware numbers into language limits.
  Provider selection remains a separate Technology approval.
- **Bounded feature execution:**
  [`bounded-feature-execution-packet.md`](bounded-feature-execution-packet.md):
  mandatory one-Issue/one-Slice/one-Phase request shape for code assistants,
  including stop and escalation conditions.
- `staqex-language-spec.md`: architecture umbrella + ADR lock index (points to
  the normative spec; ADR 0024–0058).
- Spec verification: `docs/testing/staqex-spec-verification-protocol.md`
  (SV-01–SV-31; Language Spec Conformance).
- Kernel entry for humans: repo `QUICKSTART.md` / `QUICKSTART.ja.md`.
- Kernel PoC fixtures: `tests/fixtures/poc/`.
- Compiler tree: `compiler/README.md`.
- `open-work-register.md`: canonical register for open/deferred capabilities
  and items not yet assigned a dedicated Issue.

## Accepted Decisions (collaboration template)

- `adr/0001-design-first-ai-request-routing.md` … `adr/0012-rename-referee-to-adjudicator.md`
- [ADR 0112](adr/0112-claude-code-contract-independence.md) (**Accepted**,
  2026-07-30): `CLAUDE.md` leaves the literal-full-mirror set and becomes the
  independently authoritative, self-sufficient contract for Claude Code, with
  precedence over `agent-quickstart.md` and `at-tdd/process.md`. Supersedes the
  `CLAUDE.md` mirror portion of ADR 0006.
- [ADR 0113](adr/0113-work-plan-level-approval-and-pr-granularity.md)
  (**Accepted**, 2026-07-30, **Claude Code only**): a mandatory work-plan
  investigation step (spec/ADR, Issues, granularity rationale, execution order,
  draft batch record) precedes a bounded execution batch; the batch is the
  work-plan-level approval unit; commit granularity is unchanged while branch,
  push, PR, and merge move to the work plan. The other agent families keep the
  Issue-level default and the per-phase gate.

## Accepted Decisions (Staqex language / Kernel)

- `adr/0013-staqex-language-axioms.md` … `adr/0040-physical-axiom-typechecking.md`
  (see full list in git / prior index commits; do not renumber).
- `adr/0041` … `adr/0053` — Hamiltonian / walk / controlled apply / unitarity /
  physicist surface purification (see files under `adr/`).
- `adr/0054-user-module-import.md` — multi-file `import` linker.
- `adr/0055-namespace-scope.md` — `namespace` / `enum` / dotted scope.
- `adr/0056-class-methods-this.md` — `struct` / `class` / `fn init` / `this`.
- `adr/0058-access-control-modules.md` — `pub` / module-private / `_`
  (**revised**; `protected` Forbidden; `module-info` optional).
- `adr/0059-openqasm3-zero-dependency-codegen.md` — OpenQASM 3 emit;
  Braket/IBM as **host** adapters (LISS-0002).
- `adr/0060-joint-coordinate-preservation.md` — **Accepted**; Joint coords
  under `grover_diffuse`; classical `phase`/`times` ([LISS-0004](../issues/LISS-0004-joint-preservation-classical-env.md)).
- `adr/0061-classical-module-config-harvest.md` — **Accepted**; extend ADR 0054
  classical harvest ([LISS-0005](../issues/LISS-0005-classical-module-config-harvest.md)).
- `adr/0062-prelude-pi-constant.md` — **Accepted**; prelude classical `pi` /
  `sqrt2` / `inv_sqrt2` ([LISS-0007](../issues/LISS-0007-prelude-pi-constant.md),
  [LISS-0009](../issues/LISS-0009-chalkboard-dx.md)).
- `adr/0063-pauli-trotter-qasm.md` — **Accepted**; first-order Pauli Trotter for
  QASM evolve ([LISS-0008](../issues/LISS-0008-trotter-evolve-qasm.md)).
- **Phase 3 reviewed (source/runtime MVP):** ADR 0057 density matrix / Lindblad
  CPTP validates constructors, lowers explicit one-qubit Hamiltonian/time
  inputs into dependency-free fixed-step RK4, and bridges source-level mixed
  values to opaque Host results; explicit numeric and one-qubit symbolic
  `JumpSet` lowering are shipped, while general operators and QPU execution
  remain pending.
- **Done (LISS-0008):** Trotterize `evolve under H` → QASM.
- **Done (LISS-0009):** chalkboard DX (`inv_sqrt2`, cull decorative binds).
- **Phase 3 reviewed boundary:** [LISS-0010](../issues/LISS-0010-kernel-qft-surface.md) real QFT/IQFT; gate lowering is shipped by [LISS-0042](../issues/LISS-0042-qft-basic-gate-lowering.md), and the official example path is covered by [LISS-0020](../issues/LISS-0020-capstone-quantum-observatory.md).
- The complete open/deferred register, including `until`, `|>` / currying,
  effects, host submit, bare `H`, and higher-order Suzuki, is in
  [`open-work-register.md`](open-work-register.md).
- [ADR 0114](adr/0114-classical-coefficient-elaboration-vs-linear.md)
  (**Accepted**, 2026-07-31): classical Hamiltonian coefficients vs LINEAR;
  fold-invariant; implement [LISS-0121](../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md).
- [ADR 0115](adr/0115-typed-state-surface-annotations.md) (**Accepted**):
  `state name: State<T> = …` ([LISS-0129](../issues/LISS-0129-typed-surface-annotations.md)).
- [ADR 0116](adr/0116-classical-quantity-state-arithmetic.md) (**Accepted**):
  Classical Type-First quantities ⊕ State ([LISS-0133](../issues/LISS-0133-expression-residuals.md)).
- [ADR 0117](adr/0117-binder-index-endpoints-and-rev.md) (**Accepted**,
  2026-07-31): static Index endpoints, dependent ranges, `rev(D)`
  ([WP-0034](../work-plans/WP-0034-binder-endpoint-guards.md)).
- [ADR 0118](adr/0118-basis-binder-and-partial-float.md) (**Accepted**,
  2026-07-31): `Basis<N>` binder expansion and classical partial Float indexing
  ([WP-0035](../work-plans/WP-0035-basis-and-partial-float.md)).
- [ADR 0119](adr/0119-host-coefficient-tensor-inject.md) (**Accepted**,
  2026-07-31): in-memory Host `CoefficientTensor` + `host("…")`
  ([WP-0036](../work-plans/WP-0036-host-tensor-cqft.md)).
- [ADR 0120](adr/0120-controlled-exact-qft.md) (**Accepted**,
  2026-07-31): exact `cqft` / `ciqft` ([WP-0036](../work-plans/WP-0036-host-tensor-cqft.md)).
- [ADR 0121](adr/0121-si-base-dims-current-temperature.md) (**Accepted**,
  2026-07-31): SI base dims $I$, $\Theta$ ([WP-0037](../work-plans/WP-0037-permanent-out-reopen.md)).
- [ADR 0122](adr/0122-pipeline-unary-bare-stage.md) (**Accepted**,
  2026-07-31): pipe unary bare `lhs \|\> f` ([WP-0037](../work-plans/WP-0037-permanent-out-reopen.md)).
- [ADR 0123](adr/0123-function-partial-holes.md) (**Accepted**,
  2026-07-31): function Partial `_` holes ([WP-0038](../work-plans/WP-0038-partial-si-scale-design.md)).
- [ADR 0124](adr/0124-si-scale-conversion-explicit.md) (**Accepted**,
  2026-07-31): explicit `expr to unit` SI scale ([WP-0038](../work-plans/WP-0038-partial-si-scale-design.md)).
- [ADR 0125](adr/0125-exact-rational-design-boundary.md) (**Accepted**,
  2026-07-31): exact rational design boundary (docs-only, WP-0038).
- [ADR 0126](adr/0126-continuous-pdf-design-boundary.md) (**Accepted**,
  2026-07-31): continuous PDF design boundary (docs-only, WP-0038).
- [ADR 0162](adr/0162-continuous-host-bridge-first.md) (**Accepted**,
  2026-07-31): Host/Bridge-first continuous→finite strategy; Kernel
  `Continuous` deferred ([LISS-0195](../issues/LISS-0195-host-mc-finite-state-design.md)).
- [ADR 0163](adr/0163-host-mc-finite-state-inject.md) (**Accepted**,
  2026-07-31): Host Monte Carlo → finite State inject MVP
  ([WP-0067](../work-plans/WP-0067-host-mc-finite-inject.md)).
- [ADR 0164](adr/0164-host-mc-inject-consumption-seam.md) (**Accepted**,
  2026-07-31): Host MC inject consumption seam (label modes + ADR 0074
  provenance + Host demo)
  ([WP-0068](../work-plans/WP-0068-host-mc-inject-seam.md);
  [LISS-0198](../issues/LISS-0198-host-mc-inject-consumption-seam.md)).
- [ADR 0165](adr/0165-dirac-paper-spelling-sugar.md) (**Accepted**,
  2026-08-01): Dirac paper spelling `⟨φ|ψ⟩` / `|ψ⟩⟨φ|` as sugar lowering to
  `inner`/`outer` Calls; design lock only — Red needs a separate ship ADR
  ([LISS-0217](../issues/LISS-0217-dirac-paper-spelling-sugar.md),
  [WP-0078](../work-plans/WP-0078-design-0217-0219.md)).
- [ADR 0166](adr/0166-kernel-external-resource-ports.md) (**Accepted**,
  2026-08-01): Kernel entropy / measure sink / source loading behind ports as
  `CLAUDE.md` §External Resources requires; design lock only — Red separate
  ([LISS-0218](../issues/LISS-0218-kernel-external-resource-ports.md),
  [WP-0078](../work-plans/WP-0078-design-0217-0219.md)).
- [ADR 0167](adr/0167-linear-obligation-follows-carrier-type.md) (**Accepted**,
  2026-08-01): the linear obligation follows the carrier type, not the
  `state` binding keyword; scalars and Operators are not quantum resources
  ([LISS-0202](../issues/LISS-0202-linear-discipline-regression-cluster.md),
  [WP-0069](../work-plans/WP-0069-operations-review-intake.md)).
- [ADR 0168](adr/0168-type-driven-linear-call-move.md) (**Accepted**,
  2026-08-01): Calls whose result is a linear carrier move linear argument
  carriers; same-name rebind opens a fresh obligation
  ([LISS-0221](../issues/LISS-0221-state-transforming-calls-move-their-input-root.md),
  [WP-0073](../work-plans/WP-0073-linear-transform-move.md)).
- [ADR 0169](adr/0169-ship-dirac-paper-spelling-sugar.md) (**Accepted**,
  2026-08-02): ship gate for Dirac paper sugar Red (implements ADR 0165)
  ([LISS-0234](../issues/LISS-0234-dirac-paper-spelling-sugar-red.md),
  [WP-0081](../work-plans/WP-0081-0165-0166-red-intake.md)).
- [ADR 0170](adr/0170-ship-kernel-rng-port.md) (**Accepted**,
  2026-08-02): ship gate for Kernel `RngPort` Red (first ADR 0166 slice)
  ([LISS-0235](../issues/LISS-0235-kernel-rng-port-red.md),
  [WP-0082](../work-plans/WP-0082-kernel-rng-port.md)).
- [ADR 0171](adr/0171-ship-kernel-measure-sink-port.md) (**Accepted**,
  2026-08-02): ship gate for Kernel `MeasureSinkPort` Red (second ADR 0166
  slice)
  ([LISS-0236](../issues/LISS-0236-kernel-measure-sink-port-red.md),
  [WP-0083](../work-plans/WP-0083-kernel-measure-sink-port.md)).
- [ADR 0172](adr/0172-ship-kernel-source-port.md) (**Accepted**,
  2026-08-02): ship gate for Kernel `SourcePort` Red (third ADR 0166 slice;
  below `load_module_graph`)
  ([LISS-0237](../issues/LISS-0237-kernel-source-port-red.md),
  [WP-0084](../work-plans/WP-0084-kernel-source-port.md)).
- [ADR 0173](adr/0173-measure-tracing-out-leftover-policy.md) (**Accepted**,
  2026-08-02): terminal `measure … tracing_out …` leftover LINEAR / Born
  partial-trace policy (pedagogy Class E kill; ≠ `|0>` uncompute)
  ([LISS-0249](../issues/LISS-0249-adr-0173-measure-tracing-out.md);
  Kernel Red [LISS-0250](../issues/LISS-0250-measure-tracing-out-red.md)).
- [ADR 0174](adr/0174-type-first-field-units.md) (**Accepted**,
  2026-08-02): Type-First dimful `class`/`struct` fields retain units
  (reject permanent sell demotion; dialect D5 **lifted** after Kernel + S01 heal)
  ([LISS-0253](../issues/LISS-0253-adr-0174-type-first-field-units.md);
  Kernel [LISS-0254](../issues/LISS-0254-type-first-field-units-red.md)).
- [ADR 0175](adr/0175-failure-glossary.md) (**Accepted**,
  2026-08-02): failure glossary — world-line vs Kernel diagnostic vs Host Job
  vs capability reject ([LISS-0258](../issues/LISS-0258-failure-glossary-adr.md),
  [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)).
- [ADR 0176](adr/0176-experiment-surface-profile.md) (**Accepted**,
  2026-08-02): experiment surface profile — short package/ceremony
  ([LISS-0264](../issues/LISS-0264-adr-experiment-surface-profile.md);
  Kernel [LISS-0270](../issues/LISS-0270-experiment-surface-profile-red.md)).
- [ADR 0177](adr/0177-import-use-ergonomics.md) (**Accepted**,
  2026-08-02): selective import / use ([LISS-0265](../issues/LISS-0265-adr-import-use-ergonomics.md);
  Kernel [LISS-0271](../issues/LISS-0271-import-use-ergonomics-red.md)).
- [ADR 0178](adr/0178-lane-annotation.md) (**Accepted**,
  2026-08-02): lane annotation experiment/circuit/open
  ([LISS-0266](../issues/LISS-0266-adr-lane-annotation.md);
  Kernel [LISS-0272](../issues/LISS-0272-lane-annotation-red.md)).
- [ADR 0179](adr/0179-classical-call-in-expr.md) (**Accepted**,
  2026-08-02): pure classical Call in expressions
  ([LISS-0267](../issues/LISS-0267-adr-classical-call-in-expr.md);
  Kernel [LISS-0273](../issues/LISS-0273-classical-call-in-expr-red.md)).
- [ADR 0180](adr/0180-local-type-inference.md) (**Accepted**,
  2026-08-03): local type inference
  ([LISS-0281](../issues/LISS-0281-adr-local-type-inference.md);
  Kernel child [LISS-0282](../issues/LISS-0282-kernel-local-type-inference.md);
  [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)).
- [ADR 0181](adr/0181-named-struct-construction.md) (**Accepted**,
  2026-08-03): named struct construction
  ([LISS-0283](../issues/LISS-0283-adr-named-struct-construction.md);
  Kernel [LISS-0284](../issues/LISS-0284-kernel-named-struct-construction.md); WP-0089).
- [ADR 0182](adr/0182-default-experiment-profile.md) (**Accepted**,
  2026-08-03): default experiment profile (marker optional)
  ([LISS-0285](../issues/LISS-0285-adr-default-experiment-profile.md);
  Kernel [LISS-0286](../issues/LISS-0286-kernel-default-experiment-profile.md); WP-0089).
- [ADR 0183](adr/0183-module-relative-import.md) (**Accepted**,
  2026-08-03): module-relative import
  ([LISS-0287](../issues/LISS-0287-adr-module-relative-import.md);
  Kernel [LISS-0288](../issues/LISS-0288-kernel-module-relative-import.md); WP-0089).
- [ADR 0184](adr/0184-classical-multi-bind.md) (**Accepted**,
  2026-08-03): classical multi-name bind `J, h = 1.0, 0.5`
  (Kernel [LISS-0305](../issues/LISS-0305-classical-multi-bind.md)).
- [ADR 0185](adr/0185-kernel-continuous-value.md) (**Accepted**,
  2026-08-03): **Lane A** finiteize surface (no mid-program `Continuous`);
  Kernel [LISS-0313](../issues/LISS-0313-finiteize-surface.md) **complete**;
  investigation [LISS-0312](../issues/LISS-0312-continuous-kernel-architecture.md).
- [ADR 0127](adr/0127-live-qpu-credentials-boundary.md) (**Accepted**,
  2026-07-31): live QPU credentials boundary (docs-only, WP-0038).
- [ADR 0128](adr/0128-trait-effect-expansion-boundary.md) (**Accepted**,
  2026-07-31): trait/effect expansion boundary (docs-only, WP-0038).
- [ADR 0129](adr/0129-si-scale-catalog-wave2.md) (**Accepted**,
  2026-07-31): SI scale catalog wave-2 ([WP-0039](../work-plans/WP-0039-si-catalog-ketlit-fn-args.md)).
- [ADR 0130](adr/0130-user-fn-state-forming-args.md) (**Accepted**,
  2026-07-31): user-fn State-forming Call args ([WP-0039](../work-plans/WP-0039-si-catalog-ketlit-fn-args.md)).
- [ADR 0131](adr/0131-stepwise-partial-fill.md) (**Accepted**,
  2026-07-31): stepwise Partial fill ([WP-0040](../work-plans/WP-0040-stepwise-partial-ev.md)).
- [ADR 0132](adr/0132-ev-joule-si-conversion.md) (**Accepted**,
  2026-07-31): exact SI `eV`↔`J` ([WP-0040](../work-plans/WP-0040-stepwise-partial-ev.md)).
- [ADR 0133](adr/0133-pipeline-leftmost-hole-fill.md) (**Accepted**,
  2026-07-31): pipe fills leftmost `_` ([WP-0041](../work-plans/WP-0041-pipe-hole-celsius.md)).
- [ADR 0134](adr/0134-celsius-kelvin-affine.md) (**Accepted**,
  2026-07-31): affine °C↔K ([WP-0041](../work-plans/WP-0041-pipe-hole-celsius.md)).
- [ADR 0135](adr/0135-fahrenheit-kelvin-affine.md) (**Accepted**,
  2026-07-31): affine °F↔K ([WP-0042](../work-plans/WP-0042-fahrenheit-gram.md)).
- [ADR 0136](adr/0136-gram-kilogram-scale.md) (**Accepted**,
  2026-07-31): mass `g`↔`kg` ([WP-0042](../work-plans/WP-0042-fahrenheit-gram.md)).
- [ADR 0137](adr/0137-pipeline-operator-fusion-mvp.md) (**Accepted**,
  2026-07-31): thin pipeline Operator Fusion MVP / Hold partial unseal
  ([WP-0043](../work-plans/WP-0043-pipeline-operator-fusion.md)).
- [ADR 0138](adr/0138-trace-out-gc-fn-scope.md) (**Accepted**,
  2026-07-31): Trace-Out GC MVP for library `fn` scopes
  ([WP-0044](../work-plans/WP-0044-trace-out-gc-mvp.md)).
- [ADR 0139](adr/0139-interference-prune-mvp.md) (**Accepted**,
  2026-07-31): Interference prune / support-merge MVP
  ([WP-0045](../work-plans/WP-0045-interference-prune-mvp.md)).
- [ADR 0140](adr/0140-deferred-pushforward-mvp.md) (**Accepted**,
  2026-07-31): Deferred Pushforward MVP / Hold partial unseal
  ([WP-0046](../work-plans/WP-0046-deferred-pushforward-mvp.md)).
- [ADR 0141](adr/0141-algebraic-operator-fusion-mvp.md) (**Accepted**,
  2026-07-31): Algebraic Operator Fusion MVP (affine carriers)
  ([WP-0047](../work-plans/WP-0047-algebraic-operator-fusion.md)).
- [ADR 0142](adr/0142-evolve-trace-out-gc.md) (**Accepted**,
  2026-07-31): Trace-Out GC for block `evolve`
  ([WP-0048](../work-plans/WP-0048-evolve-trace-out-gc.md)).
- [ADR 0143](adr/0143-call-partial-pipe-fusion-mvp.md) (**Accepted**,
  2026-07-31): Call / Partial pipe Fusion MVP
  ([WP-0049](../work-plans/WP-0049-call-partial-fusion.md)).
- [ADR 0144](adr/0144-rankine-kelvin-affine.md) (**Accepted**,
  2026-07-31): Affine °R ↔ K (Rankine)
  ([WP-0050](../work-plans/WP-0050-rankine-kelvin.md)).
- [ADR 0145](adr/0145-imperial-pound-mass.md) (**Accepted**,
  2026-07-31): Imperial mass `lb` ↔ `kg`
  ([WP-0051](../work-plans/WP-0051-imperial-pound-mass.md)).
- [ADR 0146](adr/0146-imperial-ounce-mass.md) (**Accepted**,
  2026-07-31): Imperial mass `oz` ↔ `kg` / `lb`
  ([WP-0052](../work-plans/WP-0052-imperial-ounce-mass.md)).
- [ADR 0147](adr/0147-imperial-stone-mass.md) (**Accepted**,
  2026-07-31): Imperial mass `st` ↔ `kg` / `lb` / `oz`
  ([WP-0053](../work-plans/WP-0053-imperial-stone-mass.md)).
- [ADR 0148](adr/0148-tonne-mass.md) (**Accepted**,
  2026-07-31): Metric tonne `t` ↔ `kg`
  ([WP-0054](../work-plans/WP-0054-tonne-mass.md)).
- [ADR 0149](adr/0149-multi-hole-partial-pipe.md) (**Accepted**,
  2026-07-31): Multi-hole Partial bare pipe fill
  ([WP-0055](../work-plans/WP-0055-multi-hole-partial-pipe.md)).
- [ADR 0150](adr/0150-us-uk-ton-mass.md) (**Accepted**,
  2026-07-31): US short ton / UK long ton mass scales
  ([WP-0056](../work-plans/WP-0056-us-uk-ton-mass.md)).
- [ADR 0151](adr/0151-troy-ounce-mass.md) (**Accepted**,
  2026-07-31): Troy ounce `oz_t` ↔ `kg` / `g`
  ([WP-0057](../work-plans/WP-0057-troy-ounce-mass.md)).
- [ADR 0152](adr/0152-tuple-multi-hole-fusion.md) (**Accepted**,
  2026-07-31): Tuple simultaneous multi-hole pipe / Fusion fill
  ([WP-0058](../work-plans/WP-0058-tuple-multi-hole-fusion.md)).
- [ADR 0153](adr/0153-bare-block-trace-out.md) (**Accepted**,
  2026-07-31): Bare-block Trace-Out GC
  ([WP-0059](../work-plans/WP-0059-bare-block-trace-out.md)).
- [ADR 0154](adr/0154-mixed-unit-reject.md) (**Superseded** by
  [ADR 0155](adr/0155-mixed-unit-canonical-promote.md), 2026-07-31):
  reject-only mixed-unit `+`/`-` (WP-0060).
- [ADR 0155](adr/0155-mixed-unit-canonical-promote.md) (**Accepted**,
  2026-07-31): Mixed-unit `+`/`-` promote to canonical
  ([WP-0061](../work-plans/WP-0061-mixed-unit-canonical-promote.md)).
- [ADR 0156](adr/0156-atomic-mass-and-ton-alias.md) (**Accepted**,
  2026-07-31): Atomic mass `.u` + bare `.ton` alias
  ([WP-0062](../work-plans/WP-0062-si-residuals.md)).
- [ADR 0157](adr/0157-polynomial-operator-fusion.md) (**Accepted**,
  2026-07-31): Polynomial ≥2 Operator Fusion
  ([WP-0063](../work-plans/WP-0063-poly2-fusion.md)).
- [ADR 0158](adr/0158-interprocedural-trace-out.md) (**Accepted**,
  2026-07-31): Interprocedural Trace-Out GC
  ([WP-0064](../work-plans/WP-0064-interprocedural-trace-out.md)).
- [ADR 0159](adr/0159-cpu-data-parallel-workers.md) (**Accepted**,
  2026-07-31): CPU data-parallel Joint world workers
  ([WP-0065](../work-plans/WP-0065-data-parallel-workers.md)).
- [ADR 0160](adr/0160-classical-rational-literals.md) (**Accepted**,
  2026-07-31): Classical Fraction literals → f64 at State
  ([WP-0066](../work-plans/WP-0066-classical-rational-credentials.md)).
- [ADR 0161](adr/0161-credential-port.md) (**Accepted**,
  2026-07-31): CredentialPort + Env adapter + mock submit
  ([WP-0066](../work-plans/WP-0066-classical-rational-credentials.md)).
- QPU honesty catalog:
  [`../specs/staqex-v1-qpu-capability-honesty.md`](../specs/staqex-v1-qpu-capability-honesty.md)
  ([LISS-0135](../issues/LISS-0135-qpu-capability-honesty.md)).
- Theory-to-QPU notation coverage (finite binders, operator algebra, typed
  second quantization, symbolic IR, phase-separated scopes, hybrid workflow,
  continuous notation, and POVM/channel contracts) is inventoried in the
  [`theory-to-qpu-feature-roadmap.md`](../research/2026-07-23-theory-to-qpu-feature-roadmap.md)
  and sequenced by [WP-0013](../work-plans/WP-0013-theory-to-qpu-feature-roadmap.md).
- Implementation backlog and dependency order: [WP-0004](../work-plans/WP-0004-open-architecture-backlog.md).
- Highest-priority capstone example: [LISS-0020](../issues/LISS-0020-capstone-quantum-observatory.md) / [WP-0016](../work-plans/WP-0016-quantum-observatory-capstone.md).
- **Done (LISS-0001, LISS-0003…0007):** axioms ledger closed; examples brush-up + `pi`.
- **Done (LISS-0021, LISS-0025; ADR 0064/0068 Accepted):** function
  signatures and typed returns — explicit `-> Type`, terminal `return`,
  lexical scope, no implicit `Operator` harvest, `main -> Unit`.
- **Done (LISS-0048, closed 2026-07-25):** Operator-typed return typecheck
  gap — a mismatched declared return type against an `Operator`-typed local
  now produces `RETURN_TYPE_MISMATCH` at typecheck time instead of crashing
  at runtime.
- **Done (LISS-0049, closed 2026-07-25; Option B scope):** QASM
  function-call lowering boundary — calling a user-defined `fn` from `main`
  rejects with `QASM_FUNCTION_CALL_UNSUPPORTED` instead of silently falling
  back to the empty-program sketch. Inlining for correct gate output
  (Option A) remains a possible future follow-up, not scheduled.

## Remaining Technology Evaluation

Do **not** maintain a second open-topics list here. Authoritative deferred /
open / shipped rows live in
[`open-work-register.md`](open-work-register.md). Agent entry points
(`CLAUDE.md` / `AGENTS.md` Current Open Topics) must stay aligned with that
register, not with a hand-copied bullet list.


## Project Rename History

### QPex → Staqex (2026-07-29, LISS-0113)

The project was renamed from **QPex** to **Staqex** on 2026-07-29.

**Reason:** The name `QPex` conflicted with at least one existing product in the
market. The rename was timed after LISS-0080 (phase-resolved typed HIR) — the
last major structural issue before linear analysis — to minimise the surface
area of the change.

**Name selection:** A broad conflict-investigation process checked software
products, PyPI/crates.io/npm packages, trademarks (USPTO/EU), GitHub orgs,
YouTube channels, SNS handles, and company registrations across three naming
directions (concept coinages, physicist-name coinages, Japanese-origin coinages).
`Staqex` was chosen as a pure concept coinage: **St**ate + **Q**uantum +
**Ex**ecution — with zero conflicts confirmed. File extension changed from
`.qpex` to `.sqx`.

**Domains acquired:** staqex.org, staqex.com

**Scope of change (PR #118, commits daf894f + 566395f):**

| Category | From | To |
|---|---|---|
| Python package | `compiler/qpex/` | `compiler/staqex/` |
| Python imports | `compiler.qpex` | `compiler.staqex` |
| CLI entry | `python3 -m compiler.qpex` | `python3 -m compiler.staqex` |
| Source extension | `.qpex` | `.sqx` |
| Compiler class | `QPexCompiler` | `StaqexCompiler` |
| Project name string | `QPex` | `Staqex` (~340 doc files) |
| GitHub repo | `nn0cl/qpex` | `nn0cl/staqex` |

**Language semantics, ADR content, and test logic were not changed.**
Historical traces under `docs/collaboration/traces/` retain the original
`QPex`/`.qpex` spelling as immutable execution records.

**Release tagging:** The last QPex-era Kernel commit is git tag **`v0.1.1`**
(`858beb4`, LISS-0080 complete). The Staqex rename and subsequent Kernel work
belong to the **`v0.2.0`** line.
