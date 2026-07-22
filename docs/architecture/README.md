# Architecture Overview

The project uses Clean Architecture with **local-first** runtime assumptions
(CLI and library on the developer machine).

The selected stack is **Rust (edition 2021+), Cargo workspace**. The
application core owns distribution semantics, AST evaluation, and measure
collapse rules. Delivery is a local CLI (and library API); there is no UI
framework in MVP.

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

- Runtime/shell: local CLI.
- Application language: Rust (Cargo workspace).
- UI framework: none (MVP).
- Package manager: Cargo.
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
- `qpex-syntax-vocabulary.md`: Surface lexicon (`state` / `when` / `evolve` / `measure`).
- `qpex-token-specification.md`: Lexer/Parser tokens (ADR 0035).
- `qpex-ast-design.md`: AST nodes and $\mathsf{Joint}\to\mathsf{Joint}$ eval axis.
- `qpex-type-system.md`: `State<T>`, lift, classical boundary (ADR 0018).
- `qpex-abstraction-model.md`: generics, traits, `system` (ADR 0019).
- `qpex-stdlib-combinators.md`: `map` / `project` / `interfer` / `System` (ADR 0021).
- `qpex-stdlib-packages.md`: math/io/state/collection/debug (ADR 0031).
- `qpex-language-spec.md`: umbrella language spec — laws / packages / Kotlin DX (ADR 0024).
- Doc audit snapshot: `docs/collaboration/doc-audit-2026-07-23.md`.
- Language-spec re-audit: `docs/collaboration/doc-audit-language-spec-2026-07-23.md`.
- 10-criteria completeness audit: `docs/collaboration/audit-10-criteria-language-spec-2026-07-23.md`.
- Spelling cheat sheet: `docs/collaboration/spelling-cheat-sheet.md`.
- Entry-point addendum: `docs/collaboration/agent-sync-entry-point.md`.
- No-threads addendum: `docs/collaboration/agent-sync-no-threads.md`.
- Host I/O addendum: `docs/collaboration/agent-sync-host-io.md`.
- Inspect addendum: `docs/collaboration/agent-sync-inspect.md`.
- Stdlib packages addendum: `docs/collaboration/agent-sync-stdlib-packages.md`.
- Runtime execution addendum: `docs/collaboration/agent-sync-runtime-execution.md`.
- Immutable class addendum: `docs/collaboration/agent-sync-immutable-class.md`.
- P1 final + Hold unseal: `docs/collaboration/agent-sync-p1-final-unseal.md`.
- Token spec addendum: `docs/collaboration/agent-sync-token-specification.md`.
- `qpex-compiler-optimizations.md`: quantum-native IR / engine passes (ADR 0022).
- `qpex-runtime-execution-model.md`: DAG + data-parallel runtime (ADR 0032).
- `qpex-backend-targets.md`: `--target cpu|gpu|qpu:*` + OpenQASM path (ADR 0036).
- Style guide: `docs/style-guide/naming-conventions.md` (ADR 0023).
- Agent sync handoff: `docs/collaboration/agent-sync-qpex-baseline.md`.
- Stdlib naming addendum: `docs/collaboration/agent-sync-project-interfer-system.md`.
- Optimizer addendum: `docs/collaboration/agent-sync-quantum-native-opts.md`.
- Naming addendum: `docs/collaboration/agent-sync-naming-conventions.md`.
- Language-spec DX addendum: `docs/collaboration/agent-sync-language-spec-dx.md`.
- No-exceptions addendum: `docs/collaboration/agent-sync-no-exceptions.md`.
- Prior-art intake: `docs/research/2026-07-22-prior-art-and-differentiation.md`.
- Formal semantics sketch: `docs/specs/qpex-formal-semantics-sketch.md`
  (includes §Span / §Block / §Evolve / §Tuple / §Project / §Interfer).
- Kernel PoC fixtures: `tests/fixtures/poc/`.

## Accepted Decisions

- `adr/0001-design-first-ai-request-routing.md`
- `adr/0002-input-output-reasoning-contracts.md`
- `adr/0003-ai-human-collaboration-governance.md`
- `adr/0004-human-readable-source-code-quality.md`
- `adr/0005-local-issue-planning.md`
- `adr/0006-prompt-instruction-change-control.md`
- `adr/0007-trunk-oriented-branching.md`
- `adr/0008-template-update-propagation.md`
- `adr/0009-bug-planning-and-ai-usage-records.md`
- `adr/0010-ai-failure-recovery-and-runner-cli-contract.md`
- `adr/0011-external-resource-adoption-contract.md`
- `adr/0012-rename-referee-to-adjudicator.md`
- `adr/0013-qpex-language-axioms.md`
- `adr/0014-mvp-discrete-pmf-representation.md`
- `adr/0015-local-first-runtime-and-ports.md`
- `adr/0016-pmf-mvp-amplitude-lift.md`
- `adr/0017-surface-vocabulary.md`
- `adr/0018-state-t-lift-and-classical-boundary.md`
- `adr/0019-generics-traits-system.md`
- `adr/0020-map-given-fold-conditioning.md` (superseded naming → 0021)
- `adr/0021-project-interfer-system-naming.md`
- `adr/0022-quantum-native-optimizations.md`
- `adr/0023-naming-conventions.md`
- `adr/0024-kotlin-dx-packages-when-class.md`
- `adr/0025-failure-as-superposition-no-exceptions.md`
- `adr/0026-p1-locks-fun-result-project-vacuum-packages.md`
- `adr/0027-entry-point-main-measure.md`
- `adr/0028-no-threads-concurrency-is-superposition.md`
- `adr/0029-host-io-boundary-measure-sink.md`
- `adr/0030-inspect-non-destructive-debug.md`
- `adr/0031-stdlib-packages-math-state.md`
- `adr/0032-runtime-dag-data-parallel.md`
- `adr/0033-immutable-class-reentrancy.md`
- `adr/0034-vacuum-state-compare-prelude.md` (**Hold unseal**)
- `adr/0035-token-specification-lexer-parser.md`

## Remaining Technology Evaluation

- `evolve` repetition grammar (`times` / `until`).
- Specs for pipeline `|>` and currying (enables Operator Fusion surface).
- Trait `impl` surface; `system` as Expr vs decl-only.
- Effect marking for measure-capable vs pure `fun`.
- Method call sugar (`x.project(p)` vs `project(x, p)`).
- `project` on joints inside `class`; null-event UX; Result carrier name lock.
- Amplitude `interfer` vs PMF shadow tests (ADR 0016).
- Fusion algebra for non-polynomial carriers; prune epsilon vs exact 0.
- Deferred vs eager engine profiles; IR opcode set.
- Naming linter enforcement (style Hold); Unicode identifiers; `s_` default.
- `Vacuum` encoding mini-spec; package path strictness; extension orphan rules.
- `Symbol` vs `String`; `State<Float>` representation; `/` on `State<Int>`.
- Typed AST / inference surface (`state x: State<Int>`).
- Amplitude reinterpretation of `when` / §Span (ADR 0016 lift).
- Continuous PDF / Monte Carlo sample representation.
- Exact rational vs `f64` probability masses.
- Parser library choice.
- Concrete amplitude / QPU IR design (lift after ADR 0016).
- Discrete support domain beyond `i64`.
- Whether numeric literals are sugar for `dirac`.
