# Trace: LISS-0211 batch record `schema_version` contradiction

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Agent | Claude Code (Opus 5) |
| Branch | `fix/wp-0069-operations-review` |
| Issue | [LISS-0211](../../issues/LISS-0211-batch-record-schema-version-contradiction.md) |
| Instruction change | **yes** — `CLAUDE.md` §Claude Code Issue-Level and Work-Plan Autonomy |

## Reason for the contract change

`CLAUDE.md` specified `schema_version: 2` for bounded execution batch records.
Two independent sources disagreed:

- `docs/templates/execution-batch-review.md` documents `"schema_version": 1`
- `scripts/check-execution-batch-reviews.py` hard-fails anything else:
  `if data["schema_version"] != 1: fail(path, "schema_version must be 1")`

Consequence: a record written to the contract failed CI, and a record written
to pass CI violated the contract. Claude Code could not produce a valid batch
record at all — the first PR of WP-0069 had to ship its batch record as a
Markdown proposal for exactly this reason.

## Decision

**`1` is authoritative.** Adjudicator ruling, 2026-08-01.

Rationale presented and accepted: the validator and the template already agree,
and no v2 schema shape is defined anywhere in the repository — there is nothing
for a `2` to mean. Defining a v2 would have required first deciding what
changes in v2, which no open Issue or ADR asks for.

`CLAUDE.md` now reads `schema_version: 1`. The Claude-only obligation to set
`work_plan_id` is unchanged; it remains optional in the shared schema, as
`docs/templates/execution-batch-review.md` states.

## Scope

One line in `CLAUDE.md`. No change to what a batch approval authorizes, to the
approval model, or to the Claude-only autonomy boundary. Not ported to
`AGENTS.md`, `.github/copilot-instructions.md`, `.grok/rules/*`, or
`.cursor/rules/*` — those are the other agents' contracts and ADR 0112 forbids
porting this section.

## Verification

- `python3 scripts/check-execution-batch-reviews.py` — pass
- `python3 scripts/check-coverage-ledger-consistency.py` — pass (it asserts
  `CLAUDE.md` content; the edited line is not one of its fixtures)
- `grep -n schema_version CLAUDE.md docs/templates/execution-batch-review.md
  scripts/check-execution-batch-reviews.py` — all three now say 1

## Next safe action

A future batch record may be written as real JSON with `schema_version: 1`.
`approval_commit` and `approved_for_execution` remain Adjudicator-only.
