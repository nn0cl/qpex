# LISS-0260: S01 FQN noise + residual chapter inspect hygiene

## Metadata

- Local issue ID: LISS-0260
- Status: **complete** (2026-08-02) — waive package rename; inspect not increased
- Type: Fast Path / Feature (docs + limited `.sqx` renames if safe)
- Priority: P2
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Soft after: [LISS-0257](LISS-0257-s01-chapter-story-arcs.md)
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Intent

Pedagogy polish only:

1. Reduce **package / FQN noise** in S01 where legal without breaking multi-file
   import evidence (shorten showcase package segments or use local aliases if
   language allows; if not, document import style in README)
2. Push remaining **decorative `inspect`** on chapters toward Host logs (SE-01);
   keep at most sparse scorecard peeks already justified

## Exit

- [x] Documented decision: **waive package rename** in this wave
  - Rationale: multi-file `package` / import evidence is scorecard A-row; global
    FQN shorten needs Kernel or mass import rewrites; cognitive win is small vs
    churn. Residual remains Class E pedagogy (expressiveness review P2).
- [x] Chapter `inspect` count not increased in WP-0087 (0257 headers only;
  spine remains inspect-free post-0246)
- [x] Spine + ticket + chapter smoke remain green on this branch
- [x] Scorecard multi-file import evidence unchanged

## Non-goals

- Causal spine (0256)
- ADR work
- Global Kernel package system redesign

## Verification

- Diff review: no new inspect museum
- Optional later Issue if package alias sugar ships