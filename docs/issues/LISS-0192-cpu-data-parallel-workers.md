# LISS-0192: CPU pool over independent Joint worlds

## Metadata

- Local issue ID: LISS-0192
- Status: **complete**
- ADR: [0159](../architecture/adr/0159-cpu-data-parallel-workers.md)
- Program: [WP-0065](../work-plans/WP-0065-data-parallel-workers.md)
- Tests: `tests/test_data_parallel_workers_red.py`

## Exit

- [x] Opt-in workers via Evaluator / run_source / CLI flag / env
- [x] Multi-world pushforward denotation matches sequential under fixed seed
- [x] Default `workers=1` unchanged; no language Thread surface
- [x] `EvalResult.data_parallel_workers` records configured N
