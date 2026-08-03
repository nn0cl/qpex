# ADR 0169: Ship Dirac paper spelling sugar (implements ADR 0165)

## Status

**Accepted** (2026-08-02) — WP-0081 / [LISS-0234](../documentation-compression-map.md)
Adjudicator lock (「推奨通り」— Accept 0169, Dirac-only first batch).

Authorizes Feature Path Red for LISS-0234 under the WP-0081 execution batch.

## Context

[ADR 0165](0165-dirac-paper-spelling-sugar.md) (**Accepted**) locked the design:
paper inner `⟨φ|ψ⟩` and outer `|ψ⟩⟨φ|` dual-accept as sugar lowering to
`inner` / `outer` Calls; named `|psi>` stays rejected; teaching default remains
Call form. ADR 0165 §Enforcement requires a **separate ship ADR** before Kernel
Red.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Authorize Feature Path AT-TDD for [LISS-0234](../documentation-compression-map.md)
   to implement ADR 0165 locks without changing `inner` / `outer` semantics.
2. Parser / lexer disambiguation tests **must** cover: ket literals, comparison
   `>` / `>=`, pipeline `|>`, anticommutator `{A,B}`, bare-block `{ let … }`,
   and both Unicode and already-legal ASCII bra/ket forms where dual-accept
   applies.
3. Formatter / CST round-trip and `migrate_unicode_math.py` (shared Dirac label
   classes per LISS-0210) are **in** the ship Issue exit.
4. No evaluator or typechecker semantic change beyond desugar-to-Call.

## Consequences

Positive: F-04 “sugar later” can land under an explicit ship gate.

Negative: Grammar blast radius; regressions show up as PARSE / wrong Call shape.

## Enforcement

Code review should reject Red that changes Call semantics, accepts named
`|psi>`, or omits the disambiguation suite named above.
