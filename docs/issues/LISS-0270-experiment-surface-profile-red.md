# LISS-0270: Kernel Red — experiment surface profile (ADR 0176)

## Metadata

- Local issue ID: LISS-0270
- GitHub issue: https://github.com/nn0cl/staqex/issues/283
- Status: **open** — Architecture Accept done; **Phase 1 Red authorized** (Adjudicator「承認」Wave B Accept)
- Type: Feature Path
- Priority: P0
- ADR: [0176](../architecture/adr/0176-experiment-surface-profile.md) (**Accepted**)
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Parent umbrella: [LISS-0269](LISS-0269-kernel-wave-b-green-followups.md)

## Intent

Ship ADR 0176: `// staqex-profile: experiment` enables optional package omission
(default `staqex.experiment`) and optional bare top-level desugar to
`pub fn main() -> Unit`. Existing packages remain valid.

## Exit

- [ ] Phase 1 Red tests
- [ ] Phase 2 Green minimal
- [ ] Phase 3 Refactor
- [ ] B01 or B08 sample can use short profile
- [ ] SV / pytest green

## Non-goals

- Breaking S01 multi-package trees
- Changing measure/NLTS
