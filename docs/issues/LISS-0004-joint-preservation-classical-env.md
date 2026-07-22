# LISS-0004: Joint coordinate preservation + classical env for phase/times

## Metadata

- Local issue ID: LISS-0004
- GitHub issue: none
- Status: **proposed** (blocked on ADR 0060 Accept)
- Phase: Architecture Path → Feature Path
- Type: bug + language semantics
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD after ADR Accept
- Related branch: TBD `feature/joint-preserve-diffuse`

## Summary

Amplitude remarginalization ops (`grover_diffuse` / `diffuse`) rebuild Joint
worlds as `{dest: value}` only, discarding classical Floats and other wires.
Separately, `phase(…, θ, only)` and `evolve … times N` cannot consume classical
bindings (`Float` / struct fields / harvested notes).

Examples 12/14 already omit post-diffuse `inspect` of config Floats to avoid
`KeyError`. Examples 09/15 hardcode `times 50` / `times 20` despite `n_steps`
fields.

Normative design: **[ADR 0060](../architecture/adr/0060-joint-coordinate-preservation.md)**
(Proposed).

## Acceptance Notes

- [ ] ADR 0060 **Accepted** by Adjudicator (or rejected with alt design).
- [ ] `diffuse_copy` / `grover_diffuse` preserve unrelated `assign` keys;
      only rewrite amplitude marginal for `src`→`dest`.
- [ ] SV / unit tests: bind `Float cfg = 2.0` → Grover → `inspect(cfg)` succeeds.
- [ ] Multi-wire: coin wires or sibling names survive diffuse when not the dest.
- [ ] `phase(state, θ, only)` resolves `only` (and preferably `θ`) against
      classical env ∪ current world assign (documented rule).
- [ ] `evolve … times <expr>` accepts closed classical `Int` (or truncatable
      Float) expression — not only integer literals.
- [ ] Examples 12/14 can inspect corridor/motif size after amplify; 09/15 can
      use `n_steps` / `mesh.n_steps` (or document remaining limit).
- [ ] Full SV suite green.

## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Depends on: ADR 0060 Accept
- Blocks: honest post-Grover classical inspect in dream examples; step-count
  from domain structs
- Related: ADR 0030 (`inspect`), ADR 0018 (State vs classical boundary)

## Adjudicator Decision Points

- [ ] Confirm: remarginalization must be **coordinate-preserving** (0060).
- [ ] Confirm: classical env for `only`/`times` is evaluator scalars + closed
      Attr on objects — not a second Joint.
- [ ] Whether `times` Float truncation is Allowed or Int-only.

## Context

- Included: `joint.py` `diffuse_copy`; evaluator `_eval_value(only, {})`;
  parser `evolve times` literal check; examples 09, 12, 14, 15.
- Omitted: full QFT; oracle combinators (LISS-0006 / later).
- Assumptions: Born weights remain on preserved worlds; vacuum still vacuum.

## AI Planning Records

### AIP-0004-001

- Status: proposed
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-23
- Planning size: M
- Intended execution route: Architecture (ADR) then Feature Path AT-TDD
- Intended scope: Joint + evaluator + parser/`EvolveExpr`; tests; touch examples
  that currently work around the bug
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: medium Kernel change, localized files
- Assumptions: no change to nested-when ban
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: n/a

## References

- Evidence: `examples/12_city_route_search/main_city_route.qpex` (no Float
  inspect after diffuse)
- `compiler/qpex/runtime/joint.py` — `diffuse_copy`
- Parent review: LISS-0003 Context

## Work Notes

- Discovered while shipping 12/14 (SV-09 `UNEXPECTED_EXCEPTION` / `KeyError`).

## Verification

- New SV or unit cases for preserve + `times` expr + `phase` with Float `only`.
- Re-run `tests/spec_verification/run_all.py`.
