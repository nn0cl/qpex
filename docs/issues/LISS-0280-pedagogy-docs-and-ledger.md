# LISS-0280: Pedagogy docs + friction ledger refresh

## Metadata

- Local issue ID: LISS-0280
- GitHub issue: _(none yet)_
- Status: **proposed**
- Phase: docs-only
- Type: docs
- Priority: P1
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md)
- Paths (expected):
  - `QUICKSTART.md` / `QUICKSTART.ja.md`
  - `examples/basics/README.md`, B03 README / failure notes
  - Host / ticket docs referencing [ADR 0175](../architecture/adr/0175-failure-glossary.md)
  - `docs/architecture/physicist-source-friction-ledger.md`
  - S01 README notes: interface/capability physics reading; Host H-lane DTO honesty
  - Optional: short note on dual `state` keyword vs `State<T>` vocabulary

## Summary

Bundle all **documentation-only** residuals from the re-review into one Issue so
teaching surfaces stay consistent with WP-0089 without scattering micro-docs PRs.

## Covers (complete list for this Issue)

1. Recommend experiment profile as **default teaching face** for single-file physics
2. Link ADR 0175 failure glossary from B03 / Host ticket docs
3. Refresh friction ledger post–WP-0088 / toward WP-0089 (package, FQN, type-ann,
   adoption debt classes)
4. Dual vocabulary note: `state` binding vs `State<T>` type (learning cost; not a bug)
5. Host Python DTO / TonightTicket: **H-lane** enterprise is OK; must not be sold as E-lane chalk
6. S01 `interface` / `impl` capability: physics reading in README (not Java ceremony claim)
7. B09 multi-file: honest “modules ≠ notebook default”
8. Soft notes: LINEAR + `tracing_out`, `when`, circuit soft-in-experiment are **Keep**

## Exit

- [ ] QUICKSTART points at profile + B08 as first chalk
- [ ] 0175 linked from at least B03 and Host ticket path
- [ ] Friction ledger dated update with Class E adoption rows + open sugar rows
- [ ] S01 / basics README honesty bullets above
- [ ] No code behavior change required (docs-only)

## Non-goals

- Kernel changes
- Sample rewrites owned by 0275–0278 (may land in any order; this Issue links them)

## Verification

- Link check / Adjudicator doc review
- Ledger table includes WP-0089 Issue IDs for open B/C items
