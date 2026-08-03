# LISS-0199: `staqex check` reports `ok` on hard compile errors

## Metadata

- Local issue ID: LISS-0199
- Status: **complete** — 2026-08-01 (WP-0074)
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Code: `compiler/staqex/cli.py`

## Intent

`staqex check` is the "does my program compile" verb. It currently filters the
compiler's diagnostics through a hard-coded seven-code allowlist and reports
success for everything else, including hard errors.

## Evidence (reproduced 2026-08-01)

[`cmd_check`](../../compiler/staqex/cli.py) narrows `compiled.diagnostics` to:

```
FORBIDDEN_KEYWORD, RETIRED_KEYWORD, EARLY_COLLAPSE_ERROR,
NESTED_WHEN_ERROR, PARSE_ERROR, LEX_ERROR, TYPE_NOT_STATE
```

Anything else is discarded before the `if not interesting:` success branch, so
`TYPE_MISMATCH`, `DIMENSION_MISMATCH_ERROR`, `EFFECT_VIOLATION_ERROR`,
`LINEAR_DUPLICATE_USE`, `ACCESS_CONTROL_VIOLATION_ERROR` and ~100 further hard
codes are invisible to `check`.

Reproduction — a program that the compiler rejects:

```
package t
fn inspect_state(x: State<Float>) -> State<Float> effects { Inspect } { return inspect(x) }
fn pure_wrapper(x: State<Float>) -> State<Float> { return inspect_state(x) }
pub fn main() -> Unit {
    state psi = dirac(0.0)
    state viewed = pure_wrapper(psi)
    measure viewed
}
```

- `compile_source(src).ok` → `False` (`EFFECT_VIOLATION_ERROR`)
- `cmd_check` → prints `ok — no vocabulary / collapse / parse issues`, returns `0`

The success message is also inaccurate on its own terms: it claims only
vocabulary / collapse / parse were checked, while users read `check` as the
typecheck gate (`QUICKSTART.md`, every `examples/*/README.md`).

## Adjudicator decision points

1. Should `check` gate on the full hard-code set, or keep a documented narrow
   "vocabulary lint" mode plus a separate full gate?
2. If `check` starts reporting all hard codes, its exit status changes for
   existing programs. Confirm this is the intended behavior change and not a
   compatibility break for downstream scripts.

## Exit

- [x] `check` exit status agrees with the compiler's own hard/soft judgement
- [x] Success message states what was actually verified
- [x] Red test asserts non-zero exit for a program with a non-allowlisted hard code
- [x] Related: [LISS-0200](LISS-0200-hard-code-set-divergence.md) (same root family)

## Non-goals

Changing which diagnostics *are* hard (that is LISS-0200); adding new
diagnostics; changing `run` semantics.
