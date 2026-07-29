# Trace: WP-0027 pre–north-star Kernel bump (v0.2 closure)

- Date: 2026-07-27
- Task: Close deferred Kernel slices and Basics B13–B15 before LISS-0068
- Agent: Cursor (Auto)
- Planning size: XL (WP-0027 / LISS-0110)

## Waves delivered

| Wave | Slice | Verification |
| --- | --- | --- |
| 1 | LISS-0012 `evolve until` runtime | `tests/test_evolve_until_runtime_red.py` |
| 1 | LISS-0027 parametric QPU IR + Host binding | `tests/test_parametric_circuit_runtime_red.py` |
| 2 | B13–B15 Basics examples | SV-09 registration |
| 3 | LISS-0111 continuous lowering MVP | `tests/test_continuous_lowering_red.py` |

## Exit gate

- SV: **160/160** (`python3 tests/spec_verification/run_all.py`)
- Provider physical routing: **not claimed** (ADR 0105 D6)
- Next recommended step: [LISS-0068](../../issues/LISS-0068-staqex-v1-normative-rebaseline.md) Architecture Path

## Related artifacts

- Work plan: `docs/work-plans/WP-0027-pre-north-star-kernel-bump.md`
- Parent Issue: `docs/issues/LISS-0110-pre-north-star-kernel-bump.md`
- Branch: `docs/wp-0027-pre-north-star-kernel-bump`
