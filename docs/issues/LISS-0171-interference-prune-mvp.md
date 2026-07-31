# LISS-0171: Interference prune / support-merge MVP

## Metadata

- Local issue ID: LISS-0171
- Status: **complete**
- ADR: [0139](../architecture/adr/0139-interference-prune-mvp.md)
- Program: [WP-0045](../work-plans/WP-0045-interference-prune-mvp.md)
- Tests: `tests/test_interference_prune_mvp_red.py`

## Exit

- [x] Colliding full assignments merge by amplitude sum
- [x] Exact cancellation prunes to vacuum
- [x] Correlation with distinct live axes is not falsely merged
- [x] After fn Trace-Out of dead ctrl, identical `when` arms are one atom
- [x] `interfer` destructive cancel is vacuum
