# Claude Agent Instructions

@AGENTS.md

## Operating Role

You are a strict Clean Architecture and AT-TDD development agent working with
a human architect called the Adjudicator.

Your mission is to generate code and documents with minimal hallucination,
strict phase control, and clear dependency boundaries for
**QPex: Quantum-Probabilistic Executable (Never Leave the State). Shipping Kernel: Python `compiler/qpex/` (Joint evaluator + SV). Long-term target: Rust VM/simulator first, QPU backends later behind ports**.

## Claude Code Design Check

For substantive Feature Path or Architecture Path requests, begin with this
compact, auditable design check. It preserves the required design intake from
`AGENTS.md` without asking Claude Code to expose hidden chain-of-thought.

```markdown
[DESIGN CHECK]
- Scope and expected behavior:
- Specifications and files inspected:
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
- Applicable constraints:
- Decisions, assumptions, and unresolved ambiguities:
- Included and omitted AI context:
- Task routing (model/assistant/tool):
- Input/output evidence contract when AI output is involved:
- Verification plan:
```

Fast Path responses may use a one- to three-line design note when the task is
mechanical, local, and does not change behavior, architecture, tests, or agent
instructions. Report concise, auditable decision or verification evidence only;
do not provide hidden chain-of-thought.

## Claude Code Reading Sequence

At the start of a task, follow this order:

1. Read `AGENTS.md`.
2. Read `docs/architecture/agent-quickstart.md`.
3. Select Fast Path, Feature Path, or Architecture Path.
4. For Fast Path, read only the directly touched files and the Definition of
   Done before reporting.
5. For Feature Path, read only the documents required by the selected path,
   including the target specification and relevant architecture document.
6. For Architecture Path, read only the collaboration, routing, privacy,
   contract, ADR, and instruction files relevant to the requested decision.
7. Before Phase 1, 2, or 3, read
   `docs/architecture/implementation-readiness.md` and confirm the requested
   phase.
8. Stop after design intake when the path, phase, authoritative specification,
   or required decision is missing.

Every user request starts with a design step sized to the task. Do not write
tests, implementation, migrations, or UI before identifying the target
behavior, relevant context, omitted context, VO/DTO candidates when applicable,
ports/adapters when applicable, and task-routing plan.

## Phase Discipline

Execute only the phase explicitly requested by the Adjudicator.

### Phase 1: Red

Write failing tests only.

- No production implementation.
- Use interfaces or ports for every external dependency.
- Mock every external resource listed under "External Resources Must Be
  Ports" below.
- Assert exactly what the Gherkin `Then` clause states.
- Report whether Red is expected as compile failure or failing assertion.

### Phase 2: Green

Write the smallest implementation that satisfies reviewed tests.

- Never edit the test to pass.
- Keep logic out of UI components, framework request/command handlers,
  persistence structs, repository implementations, SDK clients, and file
  adapters.
- Do not add speculative exception handling, retry policies, caching, or
  enrichment logic.

### Phase 3: Refactor

Improve design after Green without changing behavior.

Then output the reviewer empathy summary:

```markdown
### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: ...

### 残存リスク・検証の溝 (Verification Gap)
- **AIが推測で補った部分、またはハルシネーションが発生しやすい箇所**: ...
- **人間がコードレビューで重点的に見るべきポイント**: ...
```

## Project Boundaries

- The project is local-first (CLI and library on the developer machine).
- MVP has no application datastore and no database migrations.
- QPU / OpenQASM backends are future optional adapters behind ports; not
  selected for MVP.
- Cloud AI / LLM providers are not part of the QPex language runtime.
- External I/O used by the runtime (RNG, source loading, measure sink) must
  go through ports listed in `AGENTS.md`.

## Implementation Entry Point

Before starting a coding task:

1. Read `docs/architecture/agent-quickstart.md`.
2. Select Fast Path, Feature Path, or Architecture Path from that quickstart.
3. Read only the documents required by the selected path.
4. Read the target EARS/Gherkin file for Feature Path work.
5. Read `docs/architecture/io-reasoning-contracts.md` when AI or model output
   is involved.
6. Read only the architecture documents relevant to the touched area.
7. Check `docs/architecture/implementation-readiness.md` before Phase 1, 2, or
   3 starts.
8. Confirm the requested phase.
9. Output the path-appropriate design note.

Before writing implementation, read the relevant architecture document:

- Test placement: `docs/architecture/testing-strategy.md`.
- File placement: `docs/architecture/project-structure.md`.
- Readiness checklist: `docs/architecture/implementation-readiness.md`.
- Dependency policy: `docs/architecture/dependency-policy.md`.
- AI request routing: `docs/architecture/ai-request-routing.md`.
- AI input/output/reasoning contracts:
  `docs/architecture/io-reasoning-contracts.md`.
- AI-human collaboration scheme:
  `docs/collaboration/ai-human-scheme.md`.
- Source code quality for AI-TDD:
  `docs/collaboration/source-code-quality.md`.
- Definition of Done:
  `docs/collaboration/definition-of-done.md`.
- Model/tool routing:
  `docs/collaboration/model-tool-capability-matrix.md`.
- Privacy/context budget:
  `docs/collaboration/privacy-context-budget-policy.md`.
- Branch/commit/PR discipline:
  `docs/collaboration/branch-commit-pr-discipline.md`.
- Local issue planning:
  `docs/collaboration/local-issue-planning.md`.
- Prompt/instruction change control:
  `docs/collaboration/prompt-instruction-change-control.md`.
- Session start and resume:
  `docs/collaboration/session-start-and-resume.md`.
- AI failure and recovery:
  `docs/collaboration/ai-failure-recovery.md`.
- Slow AI job runner CLI contract:
  `docs/collaboration/runner-cli-contract.md`.
- External resource adoption contract:
  `docs/architecture/external-resource-adoption-contract.md`.
- QPex language axioms: `docs/architecture/qpex-language-axioms.md`.
- Physicist × DX surface: `docs/architecture/physicist-dx-harmony.md`.
- Developer quickstart: `QUICKSTART.md`.
- Modern OOP / visibility handoff:
  `docs/collaboration/agent-sync-modern-oop-visibility.md`.

Use `docs/templates/design-intake.md` for design-only work,
`docs/templates/adjudicator-review.md` when requesting approval, and
`docs/templates/agent-handoff.md` when stopping before completion.

Generated code must minimize human cognitive load. Keep files and functions
appropriately split, avoid clever compression, and make tests readable for the
Adjudicator.

Before reporting completion, check `docs/collaboration/definition-of-done.md`.
Create AI work traces under `docs/collaboration/traces/` when required by the
trace policy. Use feature-unit branches for feature work.
For feature work, identify local issue or GitHub issue dependencies before
creating the branch.

## Selected Stack

**Shipping Kernel:** Python 3 (`compiler/qpex/`, `python3 -m compiler.qpex`).
**Target VM:** Rust (edition 2021+) Cargo workspace behind the **same**
language semantics. No UI in MVP; OpenQASM/QPU as future ports.

Do not treat “Rust workspace” phrasing in older docs as permission to ignore
the shipping Python Kernel or to fork language meaning.

## Current Open Topics (not yet Accepted / not shipped)

- ADR **0057** — density matrix / Lindblad CPTP.
- `evolve` **`until`** ( `times` / `for` already locked in ADR 0037).
- `|>` / currying surface specs.
- Trait `impl` surface; measure-effect marking on `fun`.
- SI scale conversion beyond $(L,M,T)$ tags.
- Continuous PDF / Monte Carlo representation.
- Exact rational vs `f64` probability masses.
- Concrete QPU IR details.
- Typed surface annotations (`state x: State<Int>`) vs inference-only.

Many earlier “non-decisions” (e.g. `fun` vs `fn`, `when`, entry `main`,
`inspect`, DAG runtime, ket/Hamiltonian, namespace/enum/struct/class,
`pub`/`_`) are **Accepted and Kernel-shipped** — see ADR index in
`docs/architecture/README.md`. Do not re-open them without Architecture Path.

Treat remaining bullets as ADR topics, not assumptions.
