# LISS-0270: Kernel Red — experiment surface profile (ADR 0176)

## Metadata

- Local issue ID: LISS-0270
- GitHub issue: https://github.com/nn0cl/staqex/issues/283
- Status: **complete** (2026-08-02) — Red → Green
- Type: Feature Path
- Priority: P0
- ADR: [0176](../architecture/adr/0176-experiment-surface-profile.md) (**Accepted**)
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Parent umbrella: [LISS-0269](LISS-0269-kernel-wave-b-green-followups.md)

## Intent

Ship ADR 0176: `// staqex-profile: experiment` enables optional package omission
(default `staqex.experiment`) and optional bare top-level desugar to
`pub fn main() -> Unit`. Existing packages remain valid.

## Exit

- [x] Phase 1 Red tests (`tests/test_liss_0270_experiment_surface_profile_red.py`)
- [x] Phase 2 Green: `experiment_profile.py` + Parser/pipeline/modules
- [x] B08 uses `// staqex-profile: experiment` short face
- [x] pytest 0270 + qasm codegen green

## Non-goals

- Breaking S01 multi-package trees
- Changing measure/NLTS
