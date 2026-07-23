# Work Plan: Function signatures and measure-free returns

## Goal

Make ordinary QPex functions and class methods composable value-producing
boundaries while preserving terminal-only measurement.

## Scope

- In: LISS-0021, its acceptance specification, grammar, AST, parser,
  typechecker, evaluator, module linker, relevant tests, and language docs.
- Out: new measurement semantics, `return`, currying, traits, `until`, QPU
  provider submission, and unrelated example redesign.

## Issue Graph

| Issue | Status | Size | Depends on | Phase |
|---|---|---:|---|---|
| LISS-0021 | Phase 2 Green complete | XL | ADR 0018/0021/0027/0037/0044/0054/0056/0058 | Architecture → Feature |

## Recommended Order

1. Review LISS-0021 and its acceptance scenarios.
2. Resolve return annotation, explicit `main -> Unit`, final-expression,
   classical-result, and QASM boundary decisions.
3. Phase 1 Red: add failing parser/typechecker/runtime/module-link tests only.
4. Obtain explicit Phase 2 Green approval.
5. Implement the minimum signature and return model.
6. Phase 3 Refactor and migrate examples without changing measurement laws.
7. Run full SV, QASM, module-link, class-method, and example regressions.

## Current Next Issue

- Issue: LISS-0021 Architecture Path review.
- Reason: the change crosses the language contract and several Kernel layers.
- Adjudicator approval needed: scope, `Unit` representation, explicit
  `main -> Unit`, return type policy, and Phase 1 Red.

## Risks

- Existing implicit last-bind methods may be source-compatible only under a
  deliberate migration rule.
- Function calls inside `evolve` must preserve joint coordinates rather than
  accidentally duplicate or discard them.
- QASM lowering may support only an accepted subset of returned functions.
- Allowing classical results too broadly could reintroduce hidden collapse.

## Verification Plan

- Phase 1 acceptance tests for zero/one/multi-argument returns and terminal
  measurement.
- Parser and AST inspection for explicit return metadata.
- Typechecker diagnostics for arity, carrier, product, and dimension mismatch.
- Runtime tests for joint preservation and class receiver immutability.
- Existing SV, QASM, module-link, and all official example regressions.
- `git diff --check` and documentation cross-reference checks.

## Execution Notes

- Phase 1 Red: completed; reviewed tests initially failed on the missing
  `-> Type` grammar and result evaluation.
- Phase 2 Green: completed for the accepted minimum slice. Production changes
  are limited to parser/AST/typechecker/runtime/pipeline diagnostics and
  synchronized language documentation.
- Phase 3 Refactor: the earlier Observatory slice is complete; the strict
  annotation migration is the current Phase 2 Green boundary. Further
  cleanup remains a separate Phase 3 review.

## Phase 2 Green evidence

Phase 1 Red coverage is in `tests/test_missing_return_annotations_red.py`.
Phase 2 Green adds `MISSING_RETURN_TYPE`, preserves the untyped `init`
exception, migrates all official examples, and removes the legacy
compatibility path. Official examples report zero missing non-`init` return
annotations.
