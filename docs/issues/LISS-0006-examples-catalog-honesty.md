# LISS-0006: Examples catalog honesty (SV-09, QFT naming, dedup, π)

## Metadata

- Local issue ID: LISS-0006
- GitHub issue: none
- Status: **proposed**
- Phase: Feature Path (mostly docs/tests/examples; optional Kernel `pi`)
- Type: chore + docs + test harness (+ optional small prelude)
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: TBD `docs/examples-catalog-honesty`

## Summary

The official examples catalog grew dream-skinned demos (12–15) on top of Grover /
Bell / DTQW. Several honesty and maintenance gaps remain independent of P0
Kernel fixes:

1. **`08_qft_and_fields`** ships gauge symmetry only — no QFT.
2. **Near-duplicates:** 04 ≈ 12 ≈ 14 (Grover N=4); 07/09 ≈ 15 (DTQW).
3. **SV-09** maintains dual allowlists (`EXAMPLES` + multi-file folder set);
   `portable_bell_qpu.qpex` and `ket_evolve_expect.qpex` exist but are not
   registered.
4. **π**: READMEs write `π`; sources use `3.141592653589793`.
5. **Layout drift:** `09` uses `models/`; `10–15` use `domain/` + `operators/`.

Catalog conventions: [examples-catalog-conventions.md](../collaboration/examples-catalog-conventions.md).

## Acceptance Notes

- [ ] Decide and implement **one** of: rename `08` to gauge-focused name, **or**
      add a real QFT toy under `08` (may depend on future Kernel `qft` — if so,
      spawn follow-on LISS; do not fake QFT with extra `phase` only).
- [ ] SV-09: auto-discover or single source of truth for path-link vs
      `compile_source`; register missing official files or document exclusion.
- [ ] Document narrative-skin policy (when 12/14/15 are Allowed vs require new
      surface) in collaboration conventions (done as draft; Adjudicator Accept).
- [ ] Optional: prelude `pi` / `Math.pi` (ADR 0031 follow-on) and migrate
      example literals.
- [ ] Optional: thin shared libs or README cross-links to reduce silent drift
      between 04/12/14 and 09/15.
- [ ] `examples/README.md` package↔folder note aligned with conventions.
- [ ] Full SV suite green after harness changes.

## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Depends on: none for docs/SV-09; QFT implementation may need new ADR
- Blocks: unbounded growth of dream examples without Kernel growth
- Related: LISS-0002 (portable Bell path note), ADR 0031

## Adjudicator Decision Points

- [ ] Rename `08` vs add QFT (defer Kernel QFT?).
- [ ] Cap narrative skins: require new Kernel primitive for new numbered
      folders after 15?
- [ ] Approve SV-09 auto-discovery approach.

## Context

- Included: catalog layout, SV-09, README honesty, optional `pi`.
- Omitted: implementing full Shor U_f + QFT (separate ADR if pursued).
- Assumptions: 11–15 Honesty tables remain normative for claims.

## AI Planning Records

### AIP-0006-001

- Status: proposed
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-23
- Planning size: M
- Intended execution route: Feature Path (docs/tests first); Architecture only
  if QFT surface is approved
- Intended scope: conventions doc (shipped with this issue filing), SV-09,
  optional rename/`pi`
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: mostly harness + docs
- Assumptions: P0 Kernel issues tracked separately
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: n/a

## References

- `tests/spec_verification/suites/sv09_examples.py`
- `examples/08_qft_and_fields/`, `examples/04` / `12` / `14`, `examples/09` / `15`
- `docs/collaboration/examples-catalog-conventions.md`

## Work Notes

- 2026-07-23: conventions doc drafted with this issue.

## Verification

- SV-09 discovers/runs agreed set; README claims match registry.
