# LISS-0162: User-fn State-forming Call arguments

## Metadata

- Local issue ID: LISS-0162
- Status: **complete**
- ADR: [0130](../architecture/adr/0130-user-fn-state-forming-args.md)
- Program: [WP-0039](../work-plans/WP-0039-si-catalog-ketlit-fn-args.md)
- Tests: `tests/test_user_fn_ketlit_args_red.py`

## Exit

- [x] `fn id(x) { return x }; id(|1>)` measures 1
- [x] Partial with KetLit bound slot completes
