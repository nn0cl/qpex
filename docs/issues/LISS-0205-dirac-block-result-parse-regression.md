# LISS-0205: Dirac algebra slices F/G rejected by the block-result parse rule

## Metadata

- Local issue ID: LISS-0205
- Status: **proposed** (investigation intake — no Red authorized)
- Phase: phase-0-design
- Type: bug
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: ADR 0087 (`inner` / `outer`);
  [`staqex-v1-dirac-algebra-ast-plan.md`](../specs/staqex-v1-dirac-algebra-ast-plan.md);
  [`staqex-explicit-return-and-scope.md`](../specs/staqex-explicit-return-and-scope.md)
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Intent

Two Dirac-algebra suites now fail at parse with
`function result expression must be the final item in a block`, on programs
their own assertions declare must parse.

## Evidence (reproduced 2026-08-01)

`tests/test_dirac_slice_f_red.py`:

```
AssertionError: [{'code': 'PARSE_ERROR', 'line': 4, 'col': 22,
  'message': 'function result expression must be the final item in a block'}]
```

Affected files (2):

```
tests/test_dirac_slice_f_red.py
tests/test_dirac_slice_g_red.py
```

Slices A–E fail for the unrelated linear-discipline reason
([LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)); F and G fail
earlier, at the parser, so they are a distinct cause.

## Adjudicator decision points

1. Did the explicit-return / block-result rule tighten after these slices
   shipped, or do F/G use a form that was never intended to be legal?
2. If the form should be legal, the fix touches the parser's block-result
   handling — confirm the blast radius against
   `staqex-explicit-return-and-scope.md` before any Red.

## Exit

- [ ] Ruling: parser over-strict vs suite using an illegal form
- [ ] Both suites green
- [ ] Spec text agrees with the shipped parser behavior

## Non-goals

Dirac paper-spelling sugar (that is [LISS-0217](LISS-0217-dirac-paper-spelling-sugar.md)
/ ADR 0165); the other regression clusters.
