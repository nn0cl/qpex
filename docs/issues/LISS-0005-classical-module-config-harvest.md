# LISS-0005: Classical module config harvest (extend ADR 0054)

## Metadata

- Local issue ID: LISS-0005
- GitHub issue: none
- Status: **proposed** (blocked on ADR 0061 Accept)
- Phase: Architecture Path → Feature Path
- Type: feature + architecture
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD after ADR Accept
- Related branch: TBD `feature/classical-config-harvest`

## Summary

ADR 0054 linker harvests `Operator` binds from `public fun` bodies and class
fields into entry `main`. Classical `Float` / `Int` binds in library funs are
**not** harvested, so multi-file “oracle” / “hints” modules force duplicated
literals and sync comments (11, 12, 13, 14).

Normative design: **[ADR 0061](../architecture/adr/0061-classical-module-config-harvest.md)**
(Proposed) — amend/companion to ADR 0054.

## Acceptance Notes

- [ ] ADR 0061 **Accepted** (surface chosen: harvest typed classical binds
      and/or `pub const` / struct defaults — per ADR Decision).
- [ ] Path-linked compile prepends harvested classical binds into entry main
      (or equivalent env) without requiring comment-sync.
- [ ] Visibility rules (ADR 0058): only `pub` / allowed module visibility.
- [ ] Name collision policy documented (entry wins vs error).
- [ ] Examples 11/12/14 operator comments about “not harvested” removed or
      updated; mains use harvested / imported config.
- [ ] SV-31 extended or new cases for classical harvest.
- [ ] Full SV suite green.

## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Depends on: ADR 0061 Accept; preferably LISS-0004 if harvested Floats are
  inspected after Grover
- Blocks: non-decorative multi-file oracles; SSH params → `Hssh` (P2 follow-on)
- Related: ADR 0054, 0058, 0055

## Adjudicator Decision Points

- [ ] Harvest **all** closed Type-First classical binds from `pub fun`, or
      introduce explicit `pub const` / `pub val` only?
- [ ] Should harvested classicals live in Joint assign, evaluator `scalars`,
      or both?
- [ ] Interaction with namespace-qualified names (`Shor.Hints.r` vs `r`).

## Context

- Included: `modules.py` `merge_modules` harvest loop; examples 11–14 operator
  files; 10 SSH params vs hardcoded `Hssh` (follow-on after harvest).
- Omitted: full parameterised Operator builder DSL.
- Assumptions: Operator harvest behavior unchanged.

## AI Planning Records

### AIP-0005-001

- Status: proposed
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: n/a
  - N/A reason: n/a
- Created at: 2026-07-23
- Planning size: M
- Intended execution route: Architecture then Feature Path
- Intended scope: `modules.py` + visibility + SV-31 + example cleanup
- Estimated token range: n/a
- Estimated token midpoint: n/a
- Token metric: n/a
- Estimation basis: linker-focused change
- Assumptions: ADR 0061 picks one surface; no GitHub Issue
- Confidence: high
- Revises: none
- Revision reason: n/a
- Superseded by: n/a

## References

- `examples/11_shor_rsa_toy/operators/period_hints.qpex`
- `examples/12_city_route_search/operators/route_oracle.qpex`
- ADR 0054 Decision §2 (Operator-only harvest today)

## Work Notes

- 2026-07-23: filed from examples review.

## Verification

- Compile_path probe: `pub fun` Float appears in main env; `inspect` works
  (with LISS-0004 if after diffuse).
