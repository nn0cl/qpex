# LISS-0010: Kernel QFT surface (future; honesty gate)

## Metadata

- Local issue ID: LISS-0010
- GitHub issue: none
- Status: **Phase 3 reviewed; type and provenance boundary complete**
- Phase: Feature Path — Phase 3 review complete; lowering shipped, example
  coverage supplied by LISS-0020
- Type: feature + architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

Canonical open-work register: [open-work-register](../architecture/open-work-register.md).

## Summary

If/when Staqex grows a real **quantum Fourier transform** surface (e.g. `qft` /
`iqft` on an Int / qubit register), add a dedicated official example under a
honest folder name. Until then, **do not** reintroduce QFT claims into
`08_gauge_symmetry` (LISS-0006).

## Acceptance Notes

- [ ] ADR for `qft` / `iqft` semantics (unitarity, register typing).
- [ ] Kernel + SV cases.
- [x] Official example path supplied by `examples/basics/B11_qft_registers/` and
      `examples/applied/A10_mission_observatory/`
      under LISS-0020 (not a rename of the gauge demo).
- [ ] Honesty table: educational scale only.

## Dependencies

- Related: LISS-0006, ADR 0053 surface purification
- Blocks: none today

## Adjudicator Decision Points

- [ ] Whether QFT is near-term Kernel work or research Hold.

## Work Notes

- 2026-07-23: placeholder so the gap is ISSUE-tracked, not silent.
- 2026-07-27: LISS-0020 supplies the official QFT/IQFT example path; no new
  QFT example Issue is needed.

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

## Architecture decision record

- [ADR 0078](../architecture/adr/0078-kernel-qft-iqft-surface.md) accepts the
  register-typed exact QFT/IQFT MVP boundary.
- The decision excludes controlled/approximate QFT, provider-specific
  instructions, and official examples until Kernel/SV acceptance.
- Phase 1 Red must first lock the operator-call/application grammar, exact
  inverse expectations, wire-order metadata, and resource diagnostics.

## Phase 1 Red record

- Added [`test_qft_surface_red.py`](../../tests/test_qft_surface_red.py).
- The Red contract uses `Operator F = qft(reg)` and
  `Operator G = iqft(reg)` over `QubitRegister<N>`.
- It requires hard diagnostics for non-register inputs and unsupported static
  resource sizes, plus QFT/IQFT identity and logical wire-order metadata in the
  provider-neutral projection.
- No parser, evaluator, QPU IR lowering, or official example was changed.

## Phase 2 Green record

- Added type checking for `qft(reg)` / `iqft(reg)` Operator values over
  `QubitRegister<N>`.
- Added `QFT_REGISTER_TYPE_ERROR` for non-register inputs and
  `QFT_RESOURCE_ERROR` for shapes above the Static Hilbert MVP budget.
- Added QFT/IQFT logical wire-order and inverse provenance to the existing
  provider-neutral `qpu_ir` projection.
- No gate decomposition, runtime QFT execution, provider instruction, or
  official example was added.
- Verification: QFT tests, all standalone tests, and specification
  verification pass 165/165 (100%). Phase 3 review remains pending.

## Phase 3 review record

- QFT provenance construction now has a dedicated projection helper and a
  named logical wire-order policy constant.
- The projection remains metadata only; it does not claim gate decomposition,
  runtime execution, approximation, or provider support.
- Reviewer empathy: readers can distinguish the exact semantic identity and
  wire-order metadata from the future executable lowering pass.
- Status: **Phase 3 reviewed; QFT/IQFT type and provenance boundary complete**.
  Gate lowering, SV expansion, and the official educational example remain
  follow-up work.

## Architecture design intake

The prerequisite boundaries are now available: `QubitRegister<N>` is the
normative static Hilbert shape (LISS-0029/ADR 0069), and the internal
provider-neutral QPU IR boundary is accepted (LISS-0019/ADR 0077). A real QFT
slice can therefore be reviewed without introducing a runtime integer-sized
register or a provider-specific operation.

### Candidate MVP boundary

- Input: a statically typed `QubitRegister<N>` only;
- semantics: the exact unitary QFT and its mathematical inverse IQFT on the
  register Hilbert space;
- lowering: a traceable decomposition into the existing gate/QPU IR boundary;
- rejection: non-static registers, unsupported size/resource budgets, and
  ambiguous wire ordering are hard diagnostics;
- honesty: no claim of arbitrary-size or hardware-efficient QFT, and no example
  until the Kernel/SV contract is accepted.

### Decisions required before Phase 1 Red

1. Surface form: `qft(reg)` / `iqft(reg)` as operator values, or a dedicated
   statement form;
2. wire-order convention: logical index order versus reversed Fourier order;
3. exact inverse and global-phase expectations;
4. whether controlled-QFT is excluded from the MVP;
5. maximum educational register size and diagnostic ownership.

The recommended scope is a small, exact, register-typed QFT/IQFT with explicit
wire order and no controlled variant. This is a design recommendation only;
it does not authorize parser, runtime, QPU lowering, or example changes.
