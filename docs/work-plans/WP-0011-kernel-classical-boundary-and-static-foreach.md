# WP-0011: Kernel classical boundary and static `forEach`

## [DESIGN CHECK]

- Scope and expected behavior: define a QPU Kernel lane without ordinary
  classical runtime control, with deterministic static `forEach` expansion and
  an explicit Host API boundary.
- Specifications and files inspected: AGENTS.md, agent quickstart,
  implementation readiness, ADR 0065, ADR 0059, ADR 0054/0068, language spec,
  open-work register, LISS-0016/0019/0022.
- Component boundaries, ports/adapters, and VO/DTO candidates: Kernel
  element-handle and static-collection concepts; Host-side `Host<T>` boundary
  and Job/JobResult remain outside Kernel. No new provider adapter or port is
  selected by this work.
- Applicable constraints: Never Leave the State, terminal `measure`, one
  language semantics for Python/Rust, no hidden host fallback, no provider SDK
  in `compiler/staqex/`.
- Decisions, assumptions, unresolved ambiguities: opaque element handles are
  preferred over exposed indices; register syntax, parameter types, expansion
  limits, and dynamic circuits remain open.
- Included and omitted AI context: included only decision-relevant language,
  QPU, Host, and Job documents; omitted unrelated examples, providers, and
  private context.
- Task routing: strong reasoning agent for ADR/spec review; deterministic tools
  for document link/search checks; later code assistant for reviewed Phase 1.
- Input/output/reasoning evidence contract: input is the selected ADR/spec
  excerpts; output is the four reviewable markdown artifacts plus index links;
  evidence is file references and explicit assumptions, not hidden reasoning.
- Verification plan: markdown link/path checks and search for register/index
  consistency; no implementation or runtime tests in this design-only batch.

## Planned phases

1. Phase 0 / Architecture review: complete; ADR 0069 accepted and the open
   questions in LISS-0026 retained for implementation review.
2. Phase 1 Red: add only conformance tests for static expansion and forbidden
   dynamic/classical control.
3. Phase 2 Green: implement the smallest accepted static elaboration boundary.
4. Phase 3 Refactor: examples, diagnostics, OpenQASM lowering, and full SV.

## Current status

- Design artifacts accepted.
- Phase 1 Red tests added: `tests/test_kernel_classical_boundary_red.py`.
- Expected Red state: the current Kernel has no static `forEach` elaborator or
  QPU-lane boundary diagnostics.
- Phase 1 Red verification: 4/4 tests fail as intended.
- Phase 2 Green: complete; reviewed Red assertions remain unchanged in
  meaning, with only a mechanical regular-expression escaping correction.
- Phase 3 Refactor: complete for the bounded `register(N)` slice; example 17,
  lowering helpers, and documentation are synchronized.
- Final review: accepted by the Adjudicator on 2026-07-23.
- Remaining open decisions are recorded in ADR 0069/LISS-0026; no provider or
  dynamic-circuit implementation is implied.
