# WP-0010: Explicit returns and lexical function scope

## [DESIGN CHECK]

- Scope and expected behavior: require terminal explicit `return` in ordinary
  functions/methods and prevent function-local bindings from escaping.
- Specifications and files inspected: LISS-0021, ADR 0054/0056/0061/0068,
  function-signature specification, module linker, evaluator, examples 09–16.
- Component boundaries, ports/adapters, and VO/DTO candidates: lexer/parser,
  AST `ReturnStmt`, typechecker, evaluator call frames, linker declarations;
  no new port or DTO.
- Applicable constraints: no early return, no return from `main`/`init`, no
  mid-program measure, no implicit module-local harvest.
- Decisions, assumptions, unresolved ambiguities: `Operator` values cross
  boundaries through explicit parameters or terminal returns; module constants
  remain a separate future design.
- Included and omitted AI context: included QPex function/module semantics and
  official examples; omitted QPU providers and unrelated deferred features.
- Verification plan: Red test, full unit tests, SV 164/164, QASM, CLI runs,
  example execution, and diff check.

## Execution status

- Phase 1 Red: complete.
- Phase 2 Green: complete.
- Phase 3 Refactor: complete for current examples and documentation.
