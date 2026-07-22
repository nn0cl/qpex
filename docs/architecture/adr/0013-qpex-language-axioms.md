# ADR 0013: QPex language axioms (distribution-first semantics)

## Status

Accepted

Adjudicator architecture approval: 2026-07-22 (chat decision).
Follow-up issue: `docs/issues/LISS-0001-language-axioms-mvp-spec.md`.




> **Historical / superseded surface note:** This document records earlier
> decisions. Current normative surface (`measure`, `when`, `fun`, `class`,
> `project`, `interfer`, packages, no exceptions) is in
> [`docs/architecture/qpex-language-spec.md`](../qpex-language-spec.md)
> and ADRs **0021–0026**. Do not copy retired spellings (`observe`, `span`,
> `fn`, `filter`, `fold`, keyword `system`) into new examples.

## Context

QPex rejects deterministic scalar programming as the default. Without a
written axiom set, agents and contributors tend to reintroduce classical
`i64` / `bool` thinking, classical `if`, and early collapse.

The Adjudicator approved documenting the five core principles as durable
architecture law, with MVP implementation limited to arithmetic + `observe`.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. The five axioms in `docs/architecture/qpex-language-axioms.md` are
   normative for all QPex design and implementation work.
2. No first-class classical scalar runtime value exists; literals denote
   distributions.
3. Arithmetic is distribution algebra (convolution / pushforward).
4. Collapse / sampling is allowed only at an explicit observation boundary
   (`observe` in MVP).
5. Probabilistic `if` and loops remain axiomatic even when unimplemented;
   classical control-flow must not be smuggled in as a temporary shortcut
   without a superseding ADR and accepted specification.

## Consequences

Positive:

- Shared invariant for specs, tests, and reviews.
- Clear rejection criteria for scalar-first patches.

Negative:

- Early MVP cannot reuse classical interpreter patterns without adaptation.
- Contributors must learn distribution semantics before coding.

## Enforcement

Code review should reject:

- Domain types that represent “the” value as a bare scalar without a
  distribution wrapper.
- Arithmetic that collapses operands before operating, unless a reviewed
  spec requires that path.
- Classical `if` / loop control in the language surface before an accepted
  probabilistic-control specification.
- Silent collapse outside `observe` (or a future named observation form).
