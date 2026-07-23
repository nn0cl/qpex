# LISS-0023: Migrate function declarations from `fun` to `fn`

## Metadata

- Local issue ID: LISS-0023
- Status: Complete
- Phase: Architecture Path → Feature Path
- Type: language surface migration
- Priority: P1
- Initial planning size: L
- Related: ADR-0024, ADR-0026, ADR-0035, ADR-0056, ADR-0066, LISS-0021

## Acceptance criteria

- [x] `fn` is accepted for top-level functions, methods, constructors, and `main`.
- [x] `fun` is rejected as a retired keyword; it is not an alias.
- [x] `pub fn main(...) -> Unit` remains the only runnable entry spelling.
- [x] All official examples contain no function declaration using `fun`.
- [x] All tests, fixtures, grammar, normative specifications, and current ADR indexes use `fn`.
- [x] Existing return-type rules from LISS-0021 are unchanged.
- [x] Full SV, QASM, CLI, and example tests pass.

## Non-goals

- Rust ownership, lifetimes, macros, or implementation syntax.
- Backward compatibility or an automatic source rewrite layer.
- Trait `impl` semantics, currying, `until`, or QPU provider work.

## AT-TDD sequence

1. Phase 1 Red: tests for `fn` acceptance, `fun` rejection, and source inventory.
2. Phase 2 Green: lexer/parser migration and all source/doc migration.
3. Phase 3: refactor terminology and reviewer-empathy pass.

## Verification record

- Phase 1 Red: `tests/test_fn_keyword_red.py` established acceptance and
  rejection cases.
- Phase 2 Green: Python Kernel, all 164 specification-verification cases,
  OpenQASM 3 code generation, and official examples pass.
- Phase 3: current specifications, ADR cross-references, teaching material,
  diagnostics, and audit-facing terminology were aligned with `fn`; historical
  records retain `fun` only where they document the retired spelling.
