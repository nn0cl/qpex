# LISS-0048: Operator-typed return typecheck gap

## Metadata

- Local issue ID: LISS-0048
- GitHub issue: none
- Status: Phase 3 complete
- Phase: Feature Path — Phase 3 complete; Adjudicator final review pending
- Type: bug / typechecker soundness gap
- Priority: P1
- Initial planning size: S
- Current planning size: S
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

A function whose body binds an `Operator`-typed local and returns it under a
declared return type that is not `Operator` (e.g. `-> State<Int>`) produces
no typecheck diagnostic and crashes at runtime with an unhandled Python
`KeyError` instead of a `RETURN_TYPE_MISMATCH` diagnostic.

Discovered during the LISS-0021 Architecture Path re-scope review
(2026-07-25) while probing the shipped return-type-checking boundary; it is
not a new design question, it is a defect in already-shipped Phase 2 Green
code (LISS-0021 / WP-0017).

## Reproduction

```qpex
fn bad() -> State<Int> {
    Operator k = X
    return k
}

pub fn main() -> Unit {
    State<Int> r = bad()
    measure r
}
```

- `python3 -m compiler.qpex check <file>` reports "ok — no vocabulary /
  collapse / parse issues" (expected: `check` only lints
  Forbidden/Retired/Early-Collapse vocabulary, so no typecheck diagnostic is
  expected here regardless).
- `python3 -m compiler.qpex run <file>` raises an unhandled Python traceback
  ending in `KeyError: 'k'` from `runtime/joint.py:118`
  (`bind_pushforward`), reached via `runtime/evaluator.py:1120` and
  `_bind_user_fun` at `runtime/evaluator.py:1608`.

## Root cause and fix

In `compiler/qpex/typecheck.py`, the per-function body-checking loop that
registers local bindings into `self.env` has:

```python
elif isinstance(stmt, StateBind):
    if stmt.ty is not None and stmt.ty.name == "Operator":
        for name in stmt.names:
            self.env[name] = self._ty_from_ref(stmt.ty)
        continue
    ...
    for name in stmt.names:
        self.env[name] = ty
```

An `Operator`-typed `StateBind` is skipped entirely — it is never added to
`self.env`. When the function's terminal `return` expression references that
name, `_infer` cannot resolve it against the declared return type, so no
`RETURN_TYPE_MISMATCH` is raised before evaluation. The mismatch only
surfaces later, in the runtime evaluator, as a raw `KeyError` rather than a
diagnostic.

## Acceptance notes

- [x] An `Operator`-typed local is registered in the typechecker's function
      environment (with `Ty("Operator", ...)`), consistent with how it is
      already handled when the declared return type is itself `Operator`.
- [x] Returning an `Operator`-typed local under a non-`Operator` declared
      return type produces `RETURN_TYPE_MISMATCH` at typecheck time, not a
      runtime crash.
- [x] Returning an `Operator`-typed local under a declared `Operator` return
      type continues to work exactly as today (no behavior regression for
      the already-shipped `fn make_coin() -> Operator { ... return k }`
      pattern).
- [x] A regression test reproduces the crash before the fix (Phase 1 Red)
      and asserts a clean diagnostic after the fix (Phase 2 Green).
- [x] No other `StateBind`/typecheck path is affected; this is scoped to the
      `Operator`-typed local skip only.

## Dependencies

- Parent: none
- Depends on: none (independent of LISS-0021's remaining scope; LISS-0021
  itself is Complete)
- Related: [LISS-0021](LISS-0021-function-signatures-and-returns.md) (found
  during its re-scope review), ADR 0068 (return-type checking boundary)
- Blocks: nothing known; this is a soundness/DX gap, not a blocker for other
  issues

## Adjudicator Decision Points

- [x] Approve Phase 1 Red (regression test reproducing the `KeyError`) before
      any production code change.
- [x] Confirm the fix should register `Operator`-typed locals in the
      typechecker environment rather than special-casing the return-site
      check only (the more general fix; avoids similar gaps elsewhere an
      `Operator` local might be referenced).

## Context

- Included: `compiler/qpex/typecheck.py` (function-body checking loop),
  `compiler/qpex/runtime/evaluator.py` / `runtime/joint.py` (crash site, for
  understanding only — no runtime change is expected once typecheck catches
  the mismatch earlier).
- Omitted: QASM lowering, module linking, unrelated LISS-0021 scope.
- Assumption: the correct fix is a typecheck-time diagnostic
  (`RETURN_TYPE_MISMATCH`), not a runtime behavior change; the runtime should
  simply never receive an ill-typed program once this is fixed.

## Verification

- Phase 1 Red: a new test reproduces today's `KeyError` (or, once the
  typechecker is fixed to reach `_infer`, reproduces the missing
  `RETURN_TYPE_MISMATCH`) via `compile_source`/`run_source`, matching the
  house style of `tests/test_function_signatures_red.py`.
- Phase 2 Green: the same test asserts a clean `RETURN_TYPE_MISMATCH`
  diagnostic and no unhandled exception.
- Existing SV suite, `tests/test_function_signatures_red.py`,
  `tests/test_missing_return_annotations_red.py`, and QASM/example
  regressions must remain green.

## Work Notes

- 2026-07-25: Issue opened from LISS-0021 Architecture Path re-scope review.
  Root cause read and recorded above.
- 2026-07-25: Phase 1 Red added and reviewed; Phase 2 Green registered
  Operator-typed locals in the function type environment. Phase 3 preserved
  behavior while clarifying the intent and acceptance-test label.
