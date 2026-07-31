# LISS-0155: Function partial `_` holes

## Metadata

- Local issue ID: LISS-0155
- Status: **complete**
- ADR: [0123](../architecture/adr/0123-function-partial-holes.md)
- Program: [WP-0038](../work-plans/WP-0038-partial-si-scale-design.md)
- Tests: `tests/test_function_partial_holes_red.py`

## Exit

- [x] `f(a, _)` typechecks as Partial; strict `f(a)` still arity error
- [x] Unary remaining hole usable as pipe stage
