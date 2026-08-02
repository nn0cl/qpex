# LISS-0272: Kernel Red — lane annotation (ADR 0178)

## Metadata

- Local issue ID: LISS-0272
- GitHub issue: https://github.com/nn0cl/staqex/issues/285
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: P1
- ADR: [0178](../architecture/adr/0178-lane-annotation.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Parse/recognize `// staqex-lane: experiment|circuit|open`; soft diagnostics when
circuit constructs appear under experiment lane (phase 1 soft only).

## Exit

- [x] `// staqex-lane:` detection + soft `LANE_SOFT_CIRCUIT_IN_EXPERIMENT`
- [x] Tests in `tests/test_liss_0271_0272_import_lane_red.py`
- [x] B10/B11/S01 burst/A01/A10 marked circuit
