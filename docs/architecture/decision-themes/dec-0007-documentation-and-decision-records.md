# DEC-0007: Documentation and decision records

## Status

**Draft — source review required**

## Current rules

- Developers start from current normative pages and registers, not historical
  execution narratives.
- `DEC-*` documents are the proposed theme-level current reading surface;
  existing ADR numbers remain immutable source identifiers.
- The full source tag and commit are the recovery authority for compressed
  records. Every removed path must be present in the compression map.
- Unresolved Issues, active review evidence, unique accepted decisions, and
  current completion packets remain readable until their meaning is migrated.
- A source record is deleted only after canonical content, inbound links,
  recovery metadata, and deterministic checks are complete.

See [documentation policy](../documentation-canonicalization-policy.md),
[compression map](../documentation-compression-map.md), and
[decision theme register](../decision-theme-register.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0187
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set must be reviewed for duplicate, superseded, unique, and unresolved decisions before this document is promoted to the current normative reading surface. Existing ADRs remain authoritative until that review is accepted.
