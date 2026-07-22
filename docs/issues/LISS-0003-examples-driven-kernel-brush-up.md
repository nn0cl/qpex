# LISS-0003: Examples-driven Kernel brush-up (parent)

## Metadata

- Local issue ID: LISS-0003
- GitHub issue: none (local-only)
- Status: **proposed** (planning ledger; Kernel work gated on ADR Accept)
- Phase: Architecture Path → Feature Path (children)
- Type: epic / planning
- Priority: P0 (umbrella)
- Initial planning size: L
- Current planning size: L
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: docs/language-axioms-mvp-spec lineage (no feature branch yet)

## Summary

Cross-review of `examples/01`–`15` exposed systematic DX holes: Joint
coordinate loss under `grover_diffuse`, classical config not linker-harvested,
literal-only `evolve times N`, and dream-skinned demos that duplicate Grover /
DTQW without new Kernel surface.

This issue is the **parent ledger**. Implementation is split:

| Child | Focus | Priority |
|-------|--------|----------|
| [LISS-0004](LISS-0004-joint-preservation-classical-env.md) | Joint preserve + classical `phase`/`times` | P0 |
| [LISS-0005](LISS-0005-classical-module-config-harvest.md) | Extend ADR 0054 classical harvest | P0 |
| [LISS-0006](LISS-0006-examples-catalog-honesty.md) | Catalog / SV-09 / QFT honesty / π | P1 |

Work plan: [WP-0003](../work-plans/WP-0003-examples-driven-brush-up.md).  
Intake: [inbox/2026-07-23-examples-driven-brush-up.md](inbox/2026-07-23-examples-driven-brush-up.md).

## Acceptance Notes

- [x] Examples 01–15 friction review recorded (inbox + this issue Context).
- [x] Child LISS issues filed with acceptance criteria.
- [x] ADR 0060 / 0061 filed as **Proposed** (not authorizing implement yet).
- [x] Catalog conventions doc under `docs/collaboration/`.
- [ ] Adjudicator Accepts ADR 0060 and/or 0061 (or rejects with rationale).
- [ ] Children closed or explicitly deferred.
- [ ] SV suite remains green after any Kernel change.

## Dependencies

- Parent: none
- Depends on: shipping Kernel (ADR 0054/0053/0042), examples 09–15 multi-file
- Blocks: honest multi-file Grover oracles (12/14), step-count from struct (09/15)
- Related: LISS-0001, LISS-0002, ADR 0054, ADR 0030 (`inspect`)

## Adjudicator Decision Points

- [ ] Accept ADR 0060 (Joint coordinate preservation) before Feature Path Red.
- [ ] Accept ADR 0061 (classical harvest) or prefer narrower `pub const` surface.
- [ ] Whether 12/14/15 stay as narrative skins or require new Kernel surface
      before more dream examples.
- [ ] Whether `08` is renamed or gains a real QFT example (LISS-0006).

## Context

### Included (review highlights)

1. **P0 — `diffuse_copy` rebuilds `{dest: v}` only** → classical Floats and
   sibling wires vanish; `inspect(target)` after Grover → `KeyError`
   (`compiler/qpex/runtime/joint.py`). Worked around in 12/14 by omitting
   post-diffuse Float inspect.
2. **P0 — `phase(…, only)` evaluates `only` with empty assign** → cannot pass
   `Float target` / harvested notes as mark value.
3. **P0 — linker harvests `Operator` + class fields only** → 11/12/14 operator
   files are comment-synced Float notes (`Float bodies are not linker-harvested`).
4. **P0 — `evolve times N` parser requires integer literal** → harvested
   `n_steps` / `MeshParams.n_steps` unused; hardcoded `times 50` / `times 20`.
5. **P1 — catalog honesty** — `08` folder says QFT but only gauge; 04≈12≈14;
   07/09≈15; SV-09 dual allowlists; `portable_bell_qpu` / `ket_evolve_expect`
   on disk but not in SV-09.

### Omitted (do not “fix”)

- Nested `when` ban (ADR 0039) — correct; index via `b0*2+b1` stays.
- Honesty tables in 11–15 READMEs — keep; do not inflate claims.
- Real RSA / metro / NGS / Mars modem — forever out of scope for toys.

### Assumptions

- Project continues local-only issue management (`docs/issues/`).
- Kernel honesty > narrative skin count.

## AI Planning Records

### AIP-0003-001

- Status: proposed
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path (ADR Proposed) then Feature Path
  per child after Accept
- Intended scope: issue ledger + ADRs + collaboration conventions + work plan;
  **no Kernel code in this planning unit**
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: documentation / planning only
- Assumptions: Adjudicator reviews ADR 0060/0061 before implement
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: n/a

## References

- `examples/README.md`, `examples/11`–`15` READMEs (Honesty tables)
- `compiler/qpex/modules.py` (`merge_modules` Operator harvest)
- `compiler/qpex/runtime/joint.py` (`diffuse_copy`)
- ADR 0054, 0030, 0042, 0039
- SV-09: `tests/spec_verification/suites/sv09_examples.py`

## Work Notes

- 2026-07-23: full examples pass review; parent + children + WP-0003 filed.

## Verification

- Planning-only: files exist and cross-link.
- Post-implement (children): SV suite green; example comments about “not
  harvested” / Float KeyError removed where fixed.
