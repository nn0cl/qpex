# LISS-0203: Declared `State<Qutrit>` is rejected as `State<Qubit>`

## Metadata

- Local issue ID: LISS-0203
- Status: **complete** — 2026-08-01
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: ADR 0115 (typed `State<T>` annotations) / LISS-0129;
  [`staqex-v1-qudit-local-dimension-plan.md`](../specs/staqex-v1-qudit-local-dimension-plan.md),
  [`staqex-v1-qudit-d3-sv-plan.md`](../specs/staqex-v1-qudit-d3-sv-plan.md)
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Intent

Qudit local-dimension annotations no longer typecheck. A declaration annotated
`State<Qutrit>` is reported as carrying `State<Qubit>`.

## Evidence (reproduced 2026-08-01)

`tests/test_qudit_slice_a_red.py`:

```
AssertionError: ('Qutrit', [{'code': 'PRODUCT_TYPE_MISMATCH', 'line': 4, 'col': 17,
  'message': 'cannot assign State<Qubit> to declared State<Qutrit>'}, …])
```

Affected files (6):

```
tests/test_qudit_slice_a_red.py
tests/test_qudit_slice_b_red.py
tests/test_qudit_slice_c_red.py
tests/test_qudit_slice_d_red.py
tests/test_qudit_d3_sv_slice_a_red.py
tests/test_qudit_d3_sv_slice_b_red.py
```

`tests/test_qudit_slice_e_red.py` still passes — it asserts the *rejection* path
(`UNSUPPORTED_LOCAL_DIMENSION` is listed in `run.HARD_CODES`), not the
acceptance path. So the rejection boundary survives while the acceptance
boundary does not.

The message shape (`cannot assign … to declared …`) is the ADR 0115 typed
annotation check, which suggests the declared-vs-inferred comparison does not
carry the local dimension through from the initializer.

## Adjudicator decision points

1. Is the regression in the *initializer's* inferred local dimension (the
   constructor always yields `Qubit`) or in the *comparison* (dimension dropped
   when matching declared against inferred)? These need different fixes.
2. Qudit D≠2 is documented as writable-but-not-placeable in
   [`staqex-v1-qpu-capability-honesty.md`](../specs/staqex-v1-qpu-capability-honesty.md).
   Confirm the Kernel acceptance path is still in scope, i.e. this is a
   regression to repair, not a boundary that was deliberately tightened.

## Exit

- [x] Root cause named: neither inference nor the ADR 0115 comparison, but a
      redundant payload-name check running *after* the dedicated
      `_check_ket_bra_local_dimension` had already accepted the literal
- [x] Qudit typing fixed; `State<Qutrit> s = |0>` and `State<Qudit<3>> s = |2>`
      accepted, `|5>` in `Qutrit` still rejected (`LOCAL_DIMENSION_TYPE_ERROR`),
      `coin()` in `Qutrit` still rejected (no silent qubit embedding)
- [x] `tests/test_qudit_slice_e_red.py` still rejects unsupported dimensions
- [x] No ADR amendment needed — the intended design was already present; the
      payload check was double-judging what the dimension check had passed
- [ ] Residual: 4 qudit suites still fail on `LINEAR_IMPLICIT_DISCARD` only,
      tracked under [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Non-goals

Qudit QPU/QASM lowering (deferred by capability honesty); adding new local
dimensions; the other regression clusters.
