# LISS-0260: S01 FQN noise + residual chapter inspect hygiene

## Metadata

- Local issue ID: LISS-0260
- Status: **open**
- Type: Fast Path / Feature (docs + limited `.sqx` renames if safe)
- Priority: P2
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Soft after: [LISS-0257](LISS-0257-s01-chapter-story-arcs.md)
- Branch (suggested): `feature/liss-0260-s01-fqn-inspect-hygiene`

## Intent

Pedagogy polish only:

1. Reduce **package / FQN noise** in S01 where legal without breaking multi-file
   import evidence (shorten showcase package segments or use local aliases if
   language allows; if not, document import style in README)
2. Push remaining **decorative `inspect`** on chapters toward Host logs (SE-01);
   keep at most sparse scorecard peeks already justified

## Exit

- [ ] Documented decision: rename packages **or** waive with rationale (parser limits)
- [ ] Chapter `inspect` count does not increase; preferably decreases vs post-R3 baseline
- [ ] All mains + host scripts still run seed 0 paths used by WP-0087 verification
- [ ] Scorecard multi-file import row still has evidence

## Non-goals

- Causal spine (0256)
- ADR work
- Global Kernel package system redesign

## Verification

- WP-0087 verification command block (subset OK if documented)
- Diff review: no new inspect museum
