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

Canonical open-work register: [open-work-register](../architecture/open-work-register.md).

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

## AI Planning Records

### AIP-0010-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only until the QFT surface ADR
  is accepted; no Kernel code or example work in this planning unit.
- Included context: current Kernel gate/operator surface, examples catalog
  honesty rules, ADR 0053, and the open-work register.
- Omitted context: vendor QPU APIs, full Shor implementation, and density
  matrix/Lindblad semantics.
- Assumptions: `qft` / `iqft` are one language surface across the Python
  shipping Kernel and future Rust generation.
- Confidence: medium; register typing and target scale are unresolved.

## Verification

- n/a until Accept
