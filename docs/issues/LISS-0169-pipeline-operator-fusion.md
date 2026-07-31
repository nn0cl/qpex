# LISS-0169: Thin pipeline Operator Fusion MVP

## Metadata

- Local issue ID: LISS-0169
- Status: **complete**
- ADR: [0137](../architecture/adr/0137-pipeline-operator-fusion-mvp.md)
- Program: [WP-0043](../work-plans/WP-0043-pipeline-operator-fusion.md)
- Tests: `tests/test_pipeline_operator_fusion_red.py`

## Exit

- [x] `x |> double |> inc` measures same as sequential nested calls
- [x] Effectful / non-unary stages are not fused (sequential or hard error)
