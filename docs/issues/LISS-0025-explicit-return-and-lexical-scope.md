# LISS-0025: Explicit returns and lexical function scope

## Metadata

- Local issue ID: LISS-0025
- Status: Complete
- Phase: Architecture Path → Feature Path
- Type: language semantics / scope / function model
- Priority: P0
- Related: LISS-0021, LISS-0005, ADR-0054, ADR-0061, proposed ADR-0068

## Acceptance specification

- [x] Ordinary `fn` and methods require a terminal `return expression`.
- [x] An explicit return expression is checked against the declared return
  type, including `Operator`, `State<T>`, products, and supported classical
  values.
- [x] Implicit final-expression returns are rejected or no longer required by
  the accepted grammar; no silent fallback remains.
- [x] Early, branch-local, and `main` returns are rejected.
- [x] `fn init` remains no-result and rejects `return`.
- [x] A function-local `Operator` is not visible in sibling functions or
  `main` unless passed explicitly as an argument or returned explicitly.
- [x] Function parameters and local bindings obey lexical scope; nested block
  names do not leak outward.
- [x] Cross-module access continues to require `pub` and imports.
- [x] ADR 0061 harvest behavior is removed or narrowed so it cannot export
  function locals implicitly.
- [x] Observatory and all affected examples demonstrate explicit value flow.
- [x] Full SV, QASM, CLI, examples, and unit tests pass.

## Non-goals

- Closures or captured outer locals.
- Module-level `const` or global mutable state.
- Early classical control flow or mid-program measurement.
- Rust ownership, lifetimes, or provider SDK integration.

## AT-TDD sequence

1. Phase 1 Red: tests for explicit return, rejected implicit return, lexical
   local isolation, and explicit Operator passing.
2. Phase 2 Green: parser/AST/typechecker/runtime/linker changes and example
   migration.
3. Phase 3 Refactor: diagnostics, scope documentation, and teaching examples.

## Ambiguity boundary

The accepted design must choose whether `return` is syntactically restricted
to the final statement by the parser or accepted then rejected by a dedicated
control-flow check. It must not permit an early return in either case.

## Verification record

- Phase 1 Red: `tests/test_explicit_return_scope_red.py` failed while `return`
  was still Forbidden and module locals were not checked.
- Phase 2 Green: parser, typechecker, runtime, linker, examples, SV 164/164,
  QASM 3, and all unit tests pass.
- Phase 3: current documentation and historical harvest ADR status aligned;
  `Operator` factory examples use explicit parameters and returns.
