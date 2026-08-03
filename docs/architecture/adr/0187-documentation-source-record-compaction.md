# ADR 0187: Issue, Work Plan, and Trace source-record compaction

## Status

**Accepted** (2026-08-03) — documentation architecture decision for WP-0090.

## Context

Completed Issues, Work Plans, and AI work Traces contain useful history but often repeat
the same outcome, status, and decision already captured by an ADR, normative
specification, or the open-work register. Keeping every execution narrative in
full makes the current project surface difficult to navigate.

## Decision

1. **ADR and normative specifications are the source of truth for decisions.**
   An Issue, Work Plan, or Trace must not be the only place where a language rule,
   acceptance boundary, or current architectural constraint is recorded.
2. **Historical Issues, Work Plans, and Traces are compact pointer records.**
   When a record is completed, closed, superseded, or otherwise historical, its
   current-tree body is reduced to its identifier, status, canonical destination,
   baseline tag, full source commit, and original path. The original path is
   retained so inbound links and stable identifiers continue to resolve.
3. **The pointer uses the immutable baseline**
   `docs/pre-canonicalization-2026-08-03` at commit
   `8663ba72295964069ac275b93c350e762a0844d8`. The original body is recovered
   with:

   ```text
   git show docs/pre-canonicalization-2026-08-03:<source_path>
   ```

4. **Keep unresolved records full.** Issues, Work Plans, or Traces that are
   open, blocked, proposed, deferred, awaiting approval, part of a current
   completion packet, or needed as current review evidence remain full. An
   unresolved Issue is never compacted merely because it is old.
5. **Stable paths and identifiers remain.** Compaction does not renumber ADRs,
   Issues, Work Plans, or Traces, and it does not rewrite Git history.
6. **Canonical destination is explicit.** Each pointer names the ADR, spec,
   open-work register, or documentation policy that now carries the useful
   current meaning.

## Consequences

- Developers read ADRs and normative specs for rules, not execution logs.
- Unresolved Issues remain actionable and readable in place; historical Issues
  retain their stable links without duplicating settled narrative.
- Historical paths remain linkable and recoverable without retaining duplicate
  narratives in the working tree.
- A future decision must update an ADR/spec first; a Work Plan/Trace can then
  link to it rather than restating it.
- The baseline tag is a recovery dependency and must not be deleted or moved.

## Scope

This ADR governs documentation records only. It does not change Staqex
language semantics, compiler behavior, tests, or runtime architecture.
