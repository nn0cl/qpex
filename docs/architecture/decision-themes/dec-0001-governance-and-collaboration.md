# DEC-0001: Governance and collaboration

## Status

**Accepted current surface — ADR 0188**

## Current rules

- Every substantial change starts with design intake and an explicit operating
  path.
- Scope, Architecture, technology selection, phase, and implementation
  approvals are distinct and must not be inferred from one another.
- Branches, commits, PRs, and merges are reviewable units; `main` is never
  modified directly for agent work.
- Source code and documentation stay readable and deterministic; adapters do
  not contain hidden business policy.
- AI context is minimal, source-grounded, and never includes secrets or
  unrelated private data.

See the [agent quickstart](../agent-quickstart.md),
[AI-human collaboration scheme](../../collaboration/ai-human-scheme.md), and
[definition of done](../../collaboration/definition-of-done.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0001, ADR 0002, ADR 0003, ADR 0004, ADR 0005, ADR 0006, ADR 0007, ADR 0008, ADR 0009, ADR 0010, ADR 0011, ADR 0012, ADR 0112, ADR 0113
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set has been reviewed for duplicate, superseded, unique, and
unresolved decisions. This document is the current thematic reading surface;
the listed ADRs are archived source records.
