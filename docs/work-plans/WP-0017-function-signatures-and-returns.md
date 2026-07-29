# WP-0017: Function signatures and measure-free returns

## Goal

Make ordinary Staqex functions and class methods composable value-producing
boundaries while preserving terminal-only measurement.

## Scope

- In: LISS-0021, its acceptance specification, grammar, AST, parser,
  typechecker, evaluator, module linker, relevant tests, and language docs.
- Out: new measurement semantics, early/branch-local `return`, currying, traits, `until`, QPU
  provider submission, unrelated example redesign, QASM function-call
  lowering (LISS-0049), and the Operator-return typecheck gap (LISS-0048).

## Issue Graph

| Issue | Status | Size | Depends on | Phase |
|---|---|---:|---|---|
| LISS-0021 | **Complete** (2026-07-25) | XL | ADR 0018/0021/0027/0037/0044/0054/0056/0058/0064/0068 | Architecture → Feature → Phase 3 reviewed complete |

## Recommended Order

1. Review LISS-0021 and its acceptance scenarios.
2. Resolve return annotation, explicit `main -> Unit`, terminal `return`,
   classical-result, and QASM boundary decisions.
3. Phase 1 Red: add failing parser/typechecker/runtime/module-link tests only.
4. Obtain explicit Phase 2 Green approval.
5. Implement the minimum signature and return model.
6. Phase 3 Refactor and migrate examples without changing measurement laws.
7. Run full SV, QASM, module-link, class-method, and example regressions.

## Current Next Issue

- Issue: none under WP-0017/LISS-0021. Resolved 2026-07-25: LISS-0021 is
  Complete for function signatures and typed returns. Follow-on work
  continues under [LISS-0048](../issues/LISS-0048-operator-return-typecheck-gap.md)
  (Operator-return typecheck gap) and
  [LISS-0049](../issues/LISS-0049-qasm-function-call-lowering.md) (QASM
  function-call lowering), tracked as separate work plans/issues.
- Reason (historical): the change crossed the language contract and several
  Kernel layers; scope, `Unit` representation, explicit `main -> Unit`, and
  return type policy were resolved during Phase 1–3 execution recorded below.

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
- Phase 3 Refactor: the Observatory slice and strict annotation migration are
  complete; the remaining Operator-return correction is tracked separately
  under LISS-0048.
- 2026-07-25: Architecture Path re-scope review closed this work plan's
  original scope as Complete. QASM function-call lowering and the
  Operator-return typecheck gap found during review are split to
  LISS-0049 and LISS-0048 respectively (see LISS-0021 Work Notes for detail).
- 2026-07-25: LISS-0048 completed its Phase 1 Red, Phase 2 Green, and Phase 3
  review as a separate follow-up slice. The typechecker now registers
  Operator-typed locals before checking terminal returns.

## Phase 2 Green evidence

Phase 1 Red coverage is in `tests/test_missing_return_annotations_red.py`.
Phase 2 Green adds `MISSING_RETURN_TYPE`, preserves the untyped `init`
exception, migrates all official examples, and removes the legacy
compatibility path. Official examples report zero missing non-`init` return
annotations.
