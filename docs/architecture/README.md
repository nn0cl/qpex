# Architecture Overview

The project uses Clean Architecture with **local-first** runtime assumptions
(CLI and library on the developer machine).

**Honesty:** the shipping Kernel that runs `examples/` today is the **Python**
tree under `compiler/qpex/`. The long-term application core is still specified
toward a **Rust** VM / simulator with QPU backends as ports — not a second
semantics. Agents must not invent a second language meaning for “Rust-only”
phrases in older ADRs.

**Design horizon:** QPex targets the *ideal final form* of a language for
generalized quantum computers on a hundred-year horizon — not the shortest
path to something that runs. See
[ADR 0095](adr/0095-design-horizon-ideal-form-first.md), which governs how
slices are scoped, when a deferral is acceptable, and how the pervasive
“MVP” vocabulary in older documents is to be read (historical scope, never
target end-state).

## Layers

### Domain

Pure QPex language semantics: probability distributions (Discrete PMF in
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

- Parse and evaluate a QPex program fragment under MVP scope A.
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

- Runtime/shell: local CLI (`python3 -m compiler.qpex` today; Rust CLI later).
- Kernel language (shipping): Python 3 (`compiler/qpex/`).
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
- `qpex-language-axioms.md`: immutable QPex language axioms.
- `qpex-positioning.md`: Accepted manifesto (never leave the state; joint store).
- **`physicist-dx-harmony.md`**: physicist mental model × programmer DX
  (`enum` / `struct` / `class` / `pub` / `_`; no `protected` / no required
  `module-info`).
- **`qpex-design-philosophy.md`**: 設計思想アーカイブ（数式↔コード直体感・Type-First・物理公理コンパイラ）。
- `qpex-syntax-vocabulary.md`: Surface lexicon (`state` / `when` / `evolve` / `measure`).
- `qpex-token-specification.md`: Lexer/Parser tokens (ADR 0035).
- `qpex-ast-design.md`: AST nodes and $\mathsf{Joint}\to\mathsf{Joint}$ eval axis.
- `qpex-type-system.md`: `State<T>`, lift, classical boundary (ADR 0018).
- `qpex-dimensional-types.md`: Type-First + $(L,M,T)$ algebra (ADR **0037**).
- `qpex-abstraction-model.md`: generics, traits, `system` (ADR 0019).
- `qpex-stdlib-combinators.md`: `map` / `project` / `interfer` / `System` (ADR 0021).
- `qpex-stdlib-packages.md`: math/io/state/collection/debug (ADR 0031).
- **Normative Language Spec:** `docs/specs/qpex-language-specification.md`
  (v0.1) + grammar `docs/specs/grammar/qpex.ebnf`.
- **Proposed v1 north star:** [`qpex-v1-language-north-star.md`](../specs/qpex-v1-language-north-star.md)
  + [ADR 0106](adr/0106-qpex-v1-north-star-language-and-compiler.md) +
  [`qpex-v1-compiler-blueprint.md`](qpex-v1-compiler-blueprint.md). These are
  Architecture Path proposals; v0.1 remains normative until LISS-0068 is
  reviewed and accepted. Rebaseline progress:
  [`qpex-v1-normative-rebaseline-register.md`](../specs/qpex-v1-normative-rebaseline-register.md).
- **North-star implementation roadmap:** [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md)
  and the supporting
  [language/compiler landscape research](../research/2026-07-27-quantum-language-compiler-landscape.md).
- `qpex-language-spec.md`: architecture umbrella + ADR lock index (points to
  the normative spec; ADR 0024–0058).
- Spec verification: `docs/testing/qpex-spec-verification-protocol.md`
  (SV-01–SV-31; Language Spec Conformance).
- Kernel entry for humans: repo `QUICKSTART.md` / `QUICKSTART.ja.md`.
- Kernel PoC fixtures: `tests/fixtures/poc/`.
- Compiler tree: `compiler/README.md`.
- `open-work-register.md`: canonical register for open/deferred capabilities
  and items not yet assigned a dedicated Issue.

## Accepted Decisions (collaboration template)

- `adr/0001-design-first-ai-request-routing.md` … `adr/0012-rename-referee-to-adjudicator.md`

## Accepted Decisions (QPex language / Kernel)

- `adr/0013-qpex-language-axioms.md` … `adr/0040-physical-axiom-typechecking.md`
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

- ADR **0057** Lindblad / density matrix is Phase 3 reviewed for the current
  numeric and one-qubit symbolic boundary; general lowering remains open.
- `evolve` **`until`** runtime repetition (`times` / `for` locked in ADR 0037;
  grammar/type boundary reviewed under LISS-0012).
- Pipeline `|>` and currying implementation (semantic boundary accepted by
  ADR 0080; Phase 1 Red remains).
- Trait `impl` surface; `system` as Expr vs decl-only.
- Effect marking for measure-capable vs pure `fn`.
- Provider-neutral Job/Task lifecycle and opaque host result contract are
  reviewed; real QPU submission remains outside the Kernel.
- Rust-aligned `fn` function keyword migration (ADR 0066 / LISS-0023).
- Rust-aligned `pub`-only visibility migration (ADR 0067 / LISS-0024).
- QASM function-call lowering (LISS-0049): correct gate output for
  function-call programs (Option A, inlining) — deferred, not scheduled;
  the honest-rejection boundary (Option B) is closed, see Done above.
- QPU Kernel classical boundary and static `forEach` (Accepted ADR 0069 /
  LISS-0026); revised as Static Hilbert Kernel with follow-up LISS-0029.
- Parametric Circuit (`Param<T>`, ADR 0070 / LISS-0027); type boundary is reviewed,
  while QPU IR preservation and Host binding remain open.
- Dynamic QPU lane (ADR 0071 / LISS-0028); rejection/capability boundary is
  reviewed, while mid-circuit execution remains open.
- SI scale conversion beyond $(L,M,T)$ tags (ADR 0037).
- Continuous PDF / Monte Carlo sample representation.
- Exact rational vs `f64` probability masses.
- Concrete QPU IR lowering and target capability profiles (inspection boundary
  is reviewed under LISS-0019).
- Whether numeric literals are sugar for `dirac`.
