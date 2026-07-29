# LISS-0120 representative-program review gate intake

- Date: 2026-07-30
- Branch: `codex/liss-0082-design-deepening`
- Operating path: Architecture Path
- Current phase: Phase 0 design intake
- Scope approval: create a local Issue and estimate the point at which a
  1,000–3,000-line representative Staqex program can honestly review the
  language
- Implementation permission: **none**
- Post-review required: Issue/scope approval, then Slice A docs approval;
  implementation phases remain separate

## Findings

- LISS-0020 is a broad showcase/kitchen-sink precedent, not a maintainability-
  scale language review gate.
- A10 currently has 124 physical `.sqx` lines; the complete official catalog
  has 857 physical / 662 non-blank `.sqx` lines. A 1,000-line minimum exceeds
  the current catalog and is therefore XL integration/review work.
- A large sample built now could review the shipping evaluator but not the new
  Quantum Semantic IR architecture.
- Control, measurement, and resource contracts become stable enough for a
  small vertical prototype after LISS-0082 Slice D.
- The full representative sample becomes an honest source-to-Semantic review
  only after finite lowering and a reviewed inspection path exist (LISS-0082 E
  plus F or equivalent).
- Algorithm Plan and simulator-port work improve realization/backend review but
  are not prerequisites for the first programming-language review.

## Decision recorded

- Claim LISS-0120.
- Leave LISS-0119 available because existing Physics IR documentation already
  points to 0119+ for deferred public-oracle work.
- Use **Noether Forge**, a finite quantum-matter discovery mission, as the
  default candidate. Its scientific spine is model families, symmetry,
  initial-state protocols, quench/spectroscopy, observables, and a
  provenance-rich phase evidence dossier. It remains finite so the first
  sample does not hide a discretization decision.
- Treat 30-line methods and 300-line files as sample-review constraints, not
  language or repository-wide laws.

## Verification plan

- local Issue field completeness;
- ID collision and active-claim check;
- WP/open-register synchronization;
- local Markdown link and whitespace checks;
- docs-only diff verification.

## Stop condition

Stop after documentation verification. No `.sqx`, tests, compiler, runtime,
pipeline, or provider changes.
