# Trace: WP-0069 operations and implementation review intake

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| Agent | Claude Code (Opus 5) |
| Branch | `docs/wp-0069-operations-review-intake` |
| Operating path | Architecture Path — work-plan investigation (`CLAUDE.md` §Claude Code Issue-Level and Work-Plan Autonomy) |
| Phase | investigation / docs-only |
| Issues filed | LISS-0199 … LISS-0219 (21) |
| ADRs filed | 0164, 0165 — both **Proposed** |
| Instruction change | **none** — `CLAUDE.md` and the other agent contracts untouched |

## Request

Adjudicator, 2026-08-01: review the existing operating rules and the
implementation state; produce Issues for implementation expansion, bug fixes,
and items needing design; work in the worktree and merge to `main`. Issue
execution happens after the `main` distribution.

Adjudicator answers during planning: (a) split the failing-test work by root
cause cluster; (b) file Proposed ADRs alongside the design Issues; (c) open a
PR and merge it.

Adjudicator correction mid-work: user-defined operator overloading is not
permitted by policy. Verified against
[ADR 0114 §D5](../../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md),
which lists it under Out of scope. The planned design Issue and its ADR were
dropped; only the documentation gap (friction ledger F-08 does not cite that
decision) was filed, inside LISS-0215.

## Scope boundary held

Investigation and documents only. No test, no implementation, no status
promotion on existing Issues, no ADR acceptance, no batch record set to
`approved_for_execution`.

## Evidence gathered (all reproduced, not inferred)

- Full root suite sweep: **PASS=174, FAIL=50** of 224 files on a clean tree.
  Classified by primary cause: linear-discipline 21, qudit typing 6,
  class-method return type 5, harness 10, Dirac parse 2, SI conversion 2,
  residual 3, crash 1.
- `staqex check` returns 0 and prints `ok` for a program with
  `EFFECT_VIOLATION_ERROR` while `compile_source(...).ok` is `False`. Executed
  `cli.cmd_check` in-process to confirm.
- `run.run_source` executed the same rejected program with `compile_ok=True`
  and returned a `MeasureResult`. Set difference computed in-process:
  72 codes hard in `pipeline._HARD_CODES` but absent from `run.HARD_CODES`;
  `CONFIG_HARVEST_COLLISION_ERROR` absent the other way.
- `KeyError: 'z'` traceback from `evaluator._bind_user_fun` →
  `joint.bind_pushforward`.
- `.github/workflows/ci.yml` contains no test invocation; the template
  placeholder block is still present.
- 5 suites import `pytest` (not installed, and `testing-strategy.md` says it is
  not used); 5 suites lack the `sys.path` prologue. `sv12` missing from the SV
  suite sequence.
- `CLAUDE.md` says batch records are `schema_version: 2`;
  `scripts/check-execution-batch-reviews.py` fails anything but `1`.
- No `RngPort` / `SourcePort` / `MeasureSinkPort` in the tree, against
  `CLAUDE.md` §External Resources Must Be Ports.
- `LISS-0070` referenced by 6 documents; no Issue file exists.
- ADRs 0065 / 0075 / 0076 / 0097 `Proposed` with complete dependent Issues.
- All 26 example programs run through the CLI: **OK=26, FAIL=0**.

## Context Ledger

- Included: `CLAUDE.md`, `local-issue-planning.md`,
  `branch-commit-pr-discipline.md`, `definition-of-done.md`,
  `execution-batch-review.md` + validator, ADR index, open-work register,
  friction ledger, open-topics specs, QPU capability honesty, coverage ledger,
  `compiler/staqex/` structure, `tests/`, `.github/workflows/ci.yml`.
- Omitted: the 162 ADR bodies individually (only status lines scanned plus the
  four flagged); most spec bodies; git history beyond the recent commits.
- Assumptions: recent lean Issue shape (LISS-0193…0197) is the accepted form,
  not `docs/templates/local-issue.md`'s long form; recorded in WP-0069 rather
  than silently.

## Deliberate deviation

`CLAUDE.md` §work-plan investigation asks for "the proposed
`docs/collaboration/reviews/execution-batch-<id>.json`". A `.json` file cannot
be proposed: CI validates every `execution-batch-*.json`, requires
`approval_commit` to be a real ancestor SHA, and offers no draft status. The
proposal is therefore
[`2026-08-01-wp-0069-batch-proposal.md`](../reviews/2026-08-01-wp-0069-batch-proposal.md),
carrying the exact JSON to paste on approval. This matches existing practice —
the other three records in that directory are Markdown and no
`execution-batch-*.json` has ever existed here.

## Mid-work renumbering

The intake was first drafted against `15c7ef0` as LISS-0198+, WP-0068, and
ADR 0164/0165. PR #223 (`feat(wp-0068): Host MC inject consumption seam`) merged
to `main` during this work and claimed `LISS-0198`, `WP-0068`, and `ADR 0164`.
The branch was reset onto `179bb29` and everything renumbered to LISS-0199+,
WP-0069, ADR 0165/0166. Pre-existing references (ADR 0087/0095/0114/0115/0116,
LISS-0070/0114/0129/0133/0195…0197, WP-0062…0068) were verified unchanged by
the shift.

Findings were re-verified against the new `main` rather than carried over:
`CLAUDE.md` still specifies `schema_version: 2`, and the full sweep is now
**PASS=174 / FAIL=50 of 224** — the one test PR #223 added passes, so the 50
failures are unchanged.

## Adjudicator decisions still needed

1. Investigation approval for this intake.
2. Batch approval for BATCH-0001 (LISS-0212…0215) if the proposed scope is right.
3. LISS-0202's semantic ruling — the hard stop of the whole plan.
4. LISS-0211: is `schema_version` 1 or 2 authoritative?
5. LISS-0208: adopt `pytest` or rewrite five suites?
6. Architecture approval for ADR 0165 / 0165 before LISS-0217 / 0217 move.

## Verification

- `python3 scripts/check-execution-batch-reviews.py --branch docs/wp-0069-operations-review-intake`
- `python3 scripts/check-coverage-ledger-consistency.py`
- `git grep -n -E '^(<<<<<<<|=======|>>>>>>>)'`
- Relative-link resolution across the new Issues, ADRs, work plan, and proposal
- `git diff --stat` confined to `docs/`

## Changed files

New: `docs/issues/LISS-0199…0218` (21), `docs/architecture/adr/0164`, `0165`,
`docs/work-plans/WP-0069-operations-review-intake.md`,
`docs/collaboration/reviews/2026-08-01-wp-0069-batch-proposal.md`, this trace.

Modified: `docs/collaboration/local-issue-planning.md` (ID claims + next-free),
`docs/architecture/README.md` (ADR index), `docs/architecture/open-work-register.md`
(open evaluations + repository health).

## Next safe action

Stop. Await investigation approval. Do not begin Red on any filed Issue.
