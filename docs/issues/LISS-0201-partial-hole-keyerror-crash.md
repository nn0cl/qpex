# LISS-0201: Partial-hole binding raises a raw `KeyError` traceback instead of a diagnostic

## Metadata

- Local issue ID: LISS-0201
- Status: **complete** — 2026-08-01 (WP-0074)
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Code: `compiler/staqex/runtime/evaluator.py`, `compiler/staqex/runtime/joint.py`
- Tests: `tests/test_function_partial_holes_red.py`

## Intent

The evaluator lets an unhandled Python `KeyError` escape to the user. A Kernel
program must fail with a Staqex diagnostic, never a Python traceback.

## Evidence (reproduced 2026-08-01)

`python3 tests/test_function_partial_holes_red.py`:

```
File ".../compiler/staqex/runtime/evaluator.py", line 2663, in _bind_user_fun
    joint = joint.bind_pushforward(
        param.name, lambda a, s=src: a[s]
    )
File ".../compiler/staqex/runtime/joint.py", line 156, in bind_pushforward
    name: _coerce_joint_atom(f(w.assign)),
File ".../compiler/staqex/runtime/evaluator.py", line 2664, in <lambda>
    param.name, lambda a, s=src: a[s]
KeyError: 'z'
```

`_bind_user_fun` closes over a source variable name `src` and indexes the Joint
world assignment with it unguarded. When the name is absent from the world, the
lookup raises instead of producing a diagnostic.

The suite is one of the 50 currently failing on `main`
(see [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md) for the
sweep), but this one is a crash, not an assertion mismatch, so it is tracked
separately.

## Adjudicator decision points

1. Is an absent binding name a *user* error (needs a named diagnostic code and
   a catalog entry) or an *internal invariant violation* (means the typechecker
   should have rejected it earlier and the evaluator may assert)?
2. If it is a user error, the diagnostic code is new and belongs in
   [`staqex-v1-diagnostic-catalog.md`](../specs/staqex-v1-diagnostic-catalog.md).

## Exit

- [x] No Python traceback reaches the user for this input
- [x] Root cause named: typecheck gap vs evaluator gap
- [x] Red test asserts a diagnostic (or a clean typecheck rejection), not an exception
- [x] `tests/test_function_partial_holes_red.py` green

## Work Notes

- 2026-08-01 (WP-0074): Root cause was evaluator gap — interprocedural Trace-Out
  after Partial formation (`second(z, _)`) dropped closed-over `z` because
  `_is_library_user_call` treated hole Calls as executed library Calls. Fix:
  skip Trace-Out for Calls containing `_` holes; Pipe State binds move linear
  Vars; unused linear params in the sample uncompute via `state x = |0>`;
  KeyError→`KernelError` guard remains as fail-closed.
