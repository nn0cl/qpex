# Architecture Overview

The project uses Clean Architecture with **local-first** runtime assumptions
(CLI and library on the developer machine).

The selected stack is **Rust (edition 2021+), Cargo workspace**. The
application core owns distribution semantics, AST evaluation, and observe
collapse rules. Delivery is a local CLI (and library API); there is no UI
framework in MVP.

## Layers

### Domain

Pure QPex language semantics: probability distributions (Discrete PMF in
MVP), convolution / pushforward arithmetic, and collapse rules for
`observe`.

Must not depend on:

- any UI framework.
- SQL schemas, ORM structs, vector DB SDKs, or file-system APIs.
- LLM SDKs, cloud AI SDKs, or third-party provider APIs.
- concrete RNG or I/O implementations (those are ports/adapters).

### UseCase

Coordinates domain behavior through ports.

Examples:

- Parse and evaluate a QPex program fragment under MVP scope A.
- Execute `observe` by sampling through `RngPort` and reporting via
  `ObserveSinkPort`.

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

## Remaining Technology Evaluation

- Continuous PDF / Monte Carlo sample representation.
- Probabilistic `if` / loop implementation strategy.
- Exact rational vs `f64` probability masses.
- Parser library choice.
- QPU / OpenQASM backend details.
- Discrete support domain beyond `i64`.
