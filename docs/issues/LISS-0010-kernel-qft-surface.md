# LISS-0010: Kernel QFT surface (future; honesty gate)

## Metadata

- Local issue ID: LISS-0010
- GitHub issue: none
- Status: **proposed** (deferred — no fake QFT)
- Phase: Architecture Path first
- Type: feature + architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

If/when QPex grows a real **quantum Fourier transform** surface (e.g. `qft` /
`iqft` on an Int / qubit register), add a dedicated official example under a
honest folder name. Until then, **do not** reintroduce QFT claims into
`08_gauge_symmetry` (LISS-0006).

## Acceptance Notes

- [ ] ADR for `qft` / `iqft` semantics (unitarity, register typing).
- [ ] Kernel + SV cases.
- [ ] New example folder (not a rename of gauge demo).
- [ ] Honesty table: educational scale only.

## Dependencies

- Related: LISS-0006, ADR 0053 surface purification
- Blocks: none today

## Adjudicator Decision Points

- [ ] Whether QFT is near-term Kernel work or research Hold.

## Work Notes

- 2026-07-23: placeholder so the gap is ISSUE-tracked, not silent.

## Verification

- n/a until Accept
