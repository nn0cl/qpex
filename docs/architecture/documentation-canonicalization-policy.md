# Documentation canonicalization policy

This policy keeps the current documentation small without destroying the
project's decision history. The normative compaction rule is
[ADR 0187](adr/0187-documentation-source-record-compaction.md).

## Four layers

1. **Entry:** a small set of pages linked from [`docs/README.md`](../README.md).
2. **Current canonical pages:** one current narrative per theme. These contain
   rules, accepted constraints, current status, and next actions.
3. **Source records:** ADRs, Issues, Work Plans, and Traces that still carry an
   independent decision, obligation, acceptance boundary, or review evidence.
4. **Git recovery:** superseded or low-value records deleted from the current
   tree remain recoverable through the immutable baseline tag and full source
   commit recorded in the compression map.

## Classification

| Class | Current-tree treatment | Required source pointer |
|---|---|---|
| `retain-canonical` | Keep as the current normative or operational page | Not required when it is the canonical destination |
| `retain-evidence` | Keep because it carries a live decision, open obligation, acceptance boundary, or required review evidence | Link to the canonical page |
| `index-pointer` | Delete a historical narrative and retain its recovery pointer in the central map | Baseline tag, full commit, original path, destination, reason |
| `unresolved-review` | Do not modify until a human decides | Add to the review list |

## Rules for ADR, Issue, Work Plan, and Trace compression

- ADR numbers and titles are immutable identifiers. An ADR remains in the
  current tree when it is the unique source of an accepted or pending decision;
  its narrative may be summarized in the current decision register.
- Closed or superseded Issues are deleted when their outcome is represented by
  the accepted ADR, current specification, or open-work register and no active
  obligation remains. Unresolved Issues remain full.
- Completed Work Plans are deleted when they contain only execution
  history already represented by the Issue/ADR and no current process rule or
  completion packet depends on their full body.
- Historical Traces are deleted when they contain only a completed
  execution log and no current approval, completion, or unresolved-risk
  evidence refers to their full body.
- A source record is never deleted merely because it is old. It is deleted only
  when its independent current meaning is absent and its useful facts are
  represented by a canonical destination.
- No identifier is reused, no published commit history is rewritten, and no
  accepted decision is silently changed.

## Source pointer format

Every deleted record is represented in
[`documentation-compression-map.md`](documentation-compression-map.md) with:

```text
source_tag    = docs/pre-canonicalization-2026-08-03
source_commit = <full commit hash containing the original file>
source_path   = docs/<original path>
destination   = docs/<canonical destination>
classification= index-pointer
reason        = <why the source has no independent current meaning>
```

Recovery is deterministic:

```text
git show <source_tag>:<source_path>
```

## Review gates

- The compression map must be complete before compaction or removal.
- All source commits must be verified with `git cat-file`.
- Current-document links and the spec-verification suite must pass.
- `unresolved-review` entries must be listed in the PR and must not be
  silently compressed. In particular, unresolved Issues remain full.
