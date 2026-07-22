# ADR 0015: Local-first runtime and external ports for MVP

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

Placeholder fields in agent contracts still described generic SaaS/datastore
shapes. QPex MVP is a local language runtime / simulator, not a persistence
product.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. MVP runtime is local-first: Rust library + CLI on the developer machine.
2. MVP has no application datastore and no migration tool.
3. External resources that must be ports:
   - `RngPort` — entropy for `observe` sampling.
   - `SourcePort` — load program text (file or stdin).
   - `ObserveSinkPort` — report observed outcomes / diagnostics.
   - Settings (CLI flags / environment) and reserved secret storage.
   - Dependency policy checks (process tooling).
4. QPU, cloud AI, and network APIs are not MVP runtime dependencies; they
   may appear later only behind new ports and ADRs.

## Consequences

Positive:

- Agent contracts match the real product shape.
- Domain stays free of I/O and RNG concretes.

Negative:

- Some template examples about DB/UI remain irrelevant and must be ignored.

## Enforcement

Code review should reject:

- Domain or UseCase code that opens files, prints, or seeds RNG directly.
- Inventing a database, cloud provider, or LLM client for MVP without ADR.
