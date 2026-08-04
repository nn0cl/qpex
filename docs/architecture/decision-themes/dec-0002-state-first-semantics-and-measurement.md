# DEC-0002: State-first semantics and measurement

## Status

**Accepted current surface — ADR 0188**

## Current rules

- Mid-program values remain `State<T>`; classical collapse occurs only at
  terminal `measure`.
- `when` preserves all worldlines and replaces classical `if` branching.
- Failure is represented as a state/worldline outcome, not an exception path.
- `inspect` and `snapshot` are non-destructive diagnostics and must not
  collapse a state.
- `project`, `map`, `interfer`, `evolve`, and `trace_out` operate within the
  accepted state semantics; unsupported or non-unitary operations reject
  explicitly.
- Linear uncompute checks use the physical amplitude tolerance `1e-12`.
- The language surface is governed by the language axioms and normative
  specification, not by a backend's implementation convenience.

See [language axioms](../staqex-language-axioms.md), the
[language specification](../../specs/staqex-language-specification.md), and
[physicist-first vision](../adjudicator-language-vision.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0013, ADR 0014, ADR 0016, ADR 0018, ADR 0020, ADR 0021, ADR 0025, ADR 0026, ADR 0027, ADR 0030, ADR 0034, ADR 0038, ADR 0039, ADR 0040, ADR 0044, ADR 0045, ADR 0052, ADR 0060, ADR 0064, ADR 0075, ADR 0087, ADR 0088, ADR 0089, ADR 0102, ADR 0107, ADR 0114, ADR 0115, ADR 0117, ADR 0120, ADR 0122, ADR 0123, ADR 0167, ADR 0168, ADR 0173
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set has been reviewed for duplicate, superseded, unique, and
unresolved decisions. This document is the current thematic reading surface;
the listed ADRs are archived source records.
