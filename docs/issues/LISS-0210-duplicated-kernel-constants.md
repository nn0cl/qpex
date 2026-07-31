# LISS-0210: Kernel constants duplicated across modules

## Metadata

- Local issue ID: LISS-0210
- Status: **proposed** (investigation intake — no Red authorized)
- Phase: phase-0-design
- Type: refactor
- Priority: P3
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [`source-code-quality.md`](../collaboration/source-code-quality.md)

## Intent

Several Kernel constants are literal copies in two to four modules. Each is a
silent drift hazard: adding a member requires N synchronized edits with nothing
enforcing N.

## Evidence (reproduced 2026-08-01)

| Constant | Copies | Locations |
|---|---|---|
| `_SECOND_QUANTIZED_FAMILIES` | 4 | `symbolic_ir.py`, `typecheck.py`, `runtime/evaluator.py`, `backend/qasm/lower.py` |
| `RELATIONAL` operator set | 3 | `typecheck.py`, `runtime/evaluator.py`, and `_GUARD_OPERATORS` in `finite_binder.py` |
| `_DIRAC_LABEL_EXTRAS` | 2 | `lexer.py`, `migrate_unicode_math.py` |

The `_DIRAC_LABEL_EXTRAS` copy is the sharpest: the Unicode-math migrator
re-implements the lexer's character classes instead of importing them, so the
migrator and the real lexer can disagree about what a Dirac label is.

The diagnostic hard-code duplication is the same failure mode but has real
behavioral consequences, so it is tracked separately and with higher priority
as [LISS-0200](LISS-0200-hard-code-set-divergence.md).

## Adjudicator decision points

1. Placement of the shared definitions — a new small module, or an existing one?
   The Clean Architecture dependency rule must not be bent to make the import
   convenient (`backend/` and `runtime/` both need `_SECOND_QUANTIZED_FAMILIES`).

## Exit

- [ ] One definition per constant
- [ ] No behavior change; full sweep result identical before and after
- [ ] Dependency direction unchanged

## Non-goals

The hard-code sets (LISS-0200); the ~15 re-implemented `_diagnostic` helpers
with four different return shapes — worth doing, but a larger refactor that
should be its own Issue once these land.
