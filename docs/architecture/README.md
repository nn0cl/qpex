# Staqex architecture

This page is the architecture index. It records current boundaries and points
to the canonical decision and work registers; it is not a second copy of every
ADR or work-plan narrative.

## Start here

- [Current decision register](current-decision-register.md) — compressed
  current rules.
- [Decision theme register](decision-theme-register.md) — accepted `DEC-*`
  theme-based current reading surface and ADR migration matrix.
- [Open-work register](open-work-register.md) — canonical open/deferred work.
- [Language specification](../specs/staqex-language-specification.md) —
  normative language contract and grammar.
- [Adjudicator language vision](adjudicator-language-vision.md) —
  physicist-first design priority.
- [Documentation policy](documentation-canonicalization-policy.md) — current
  versus source-record rules.

## Implementation generations

- **Shipping Kernel:** Python 3 package under `compiler/staqex/`; run with
  `python3 -m compiler.staqex`.
- **Long-term target:** Rust edition 2021+ Cargo workspace for the VM and
  simulator.
- **Backends:** QPU and OpenQASM integrations remain ports/adapters; provider
  SDKs and credentials are not part of the Kernel.
- Both generations implement one Staqex language semantics. Rust-only wording
  in historical documents does not define a second language.

## Clean Architecture boundary

- **Domain:** pure language semantics and state transformations; no project-
  specific infrastructure dependencies.
- **UseCase:** coordinates domain behavior through ports.
- **Ports:** define external resources such as `RngPort`, `SourcePort`, and
  `MeasureSinkPort`.
- **Adapters:** implement ports and framework integrations; they do not define
  business or language policy.
- **Delivery:** CLI/library entry points call application contracts only.

The MVP has no application datastore, cloud database, LLM provider, or live QPU
provider inside the runtime.

## Required operating documents

- [Agent quickstart](agent-quickstart.md)
- [Implementation readiness](implementation-readiness.md)
- [Project structure](project-structure.md)
- [Testing strategy](testing-strategy.md)
- [Dependency policy](dependency-policy.md)
- [AI request routing](ai-request-routing.md)
- [AI I/O and reasoning contracts](io-reasoning-contracts.md)
- [Collaboration scheme](../collaboration/ai-human-scheme.md)
- [Definition of Done](../collaboration/definition-of-done.md)

## Detailed source records

- [Retained policy ADRs](adr/)
- [Archived decision recovery map](documentation-compression-map.md)
- [Language and runtime architecture pages](.)
- [Specifications](../specs/)
- [Research](../research/)

Read a source record only when the task requires its exact decision, acceptance
boundary, or review evidence. Current implementation work starts from the
decision register and open-work register.
