# WP-0069: Operations and implementation review intake

| Field | Value |
|---|---|
| Status | **investigation — awaiting Adjudicator approval** (2026-08-01) |
| Branch | `docs/wp-0069-operations-review-intake` |
| Parent | Adjudicator request 2026-08-01: review operating rules + implementation, file Issues |
| Scope | investigation and documents only — no test, no implementation, no status promotion, no ADR acceptance |

## Goal

Record what the 2026-08-01 review of the operating rules and the shipping
Kernel found, as reviewable Issues with reproduction evidence, and propose an
execution order. **This work plan authorizes nothing.** Issue execution begins
only after the Adjudicator approves a bounded execution batch, per
`CLAUDE.md` §Claude Code Issue-Level and Work-Plan Autonomy.

## Scope

**In:** `docs/issues/LISS-0199`…`LISS-0219`, ADR 0165 / 0165 (both `Proposed`),
this work plan, the draft batch record, registry synchronization, AI work trace.

**Out:** any change under `compiler/` or `tests/`; edits to `CLAUDE.md`,
`AGENTS.md`, `.github/copilot-instructions.md`, `.grok/rules/*`,
`.cursor/rules/*`; status changes to existing Issues; edits to
`staqex-v1-language-coverage-ledger.md` or `staqex-v1-open-topics-permanent-out.md`.

## Findings that produced these Issues

All reproduced on a clean `main` on 2026-08-01.

| # | Finding | Issue |
|---|---|---|
| 1 | `staqex check` prints `ok` and exits 0 on hard compile errors | LISS-0199 |
| 2 | Two diverged hard-code sets; 72 codes bypass the execution gate | LISS-0200 |
| 3 | Raw `KeyError` traceback escapes the evaluator | LISS-0201 |
| 4 | **50 of 224 test files fail** on a clean tree | LISS-0202…0206, 0200, 0207 |
| 5 | **CI executes zero tests** — root cause of #4 | LISS-0209 |
| 6 | 10 suites unrunnable by the documented invocation | LISS-0208 |
| 7 | `CLAUDE.md` batch `schema_version: 2` vs validator `1` | LISS-0211 |
| 8 | `RngPort` / `SourcePort` / `MeasureSinkPort` required by contract, absent | LISS-0218 / ADR 0166 |
| 9 | Dangling `LISS-0070`; Proposed-but-shipped ADRs; stale catalog and READMEs | LISS-0212…0215 |

Healthy and needing no Issue: all 26 example programs run correctly through the
CLI (`OK=26 / FAIL=0`).

## Issue rows

| ID | Topic | Mode | Size | Status | Depends on |
|---|---|---|---|---|---|
| LISS-0199 | `check` false-OK | bug | S | proposed | — |
| LISS-0200 | hard-code set divergence | bug | M | proposed | — |
| LISS-0201 | partial-hole `KeyError` crash | bug | S | proposed | — |
| LISS-0202 | linear-discipline cluster (21 suites) | bug | L | proposed | LISS-0208 |
| LISS-0203 | qudit local-dimension typing (6) | bug | M | proposed | LISS-0202 |
| LISS-0204 | class-method return type (5) | bug | M | proposed | LISS-0202 |
| LISS-0205 | Dirac block-result parse (2) | bug | S | proposed | LISS-0202 |
| LISS-0206 | SI conversion diagnostics (2) | bug | S | proposed | LISS-0202 |
| LISS-0207 | residual cluster (3) | bug | M | proposed | LISS-0202 |
| LISS-0208 | test harness hygiene (10) | bug | S | proposed | LISS-0211 |
| LISS-0209 | CI runs the test suite | infra | M | proposed | LISS-0202…0207 |
| LISS-0210 | duplicated Kernel constants | refactor | S | proposed | — |
| LISS-0211 | batch `schema_version` contradiction | bug | S | proposed | — |
| LISS-0212 | dangling `LISS-0070` | bug | S | proposed | — |
| LISS-0213 | Proposed ADRs with shipped Issues | process | S | proposed | — |
| LISS-0214 | broken documented commands / names | bug | S | proposed | — |
| LISS-0215 | settled decisions shown as open | process | S | proposed | — |
| LISS-0216 | Issue-planning doc drift | process | S | proposed | — |
| LISS-0217 | Dirac paper spelling sugar (design) | design | M | open | ADR 0165 accept |
| LISS-0218 | Kernel external-resource ports (design) | design | M | open | ADR 0166 accept |
| LISS-0219 | `inspect` / lane-choice guidance (design) | docs | S | open | — |

## Issue granularity rationale

**Why the Kernel/CLI bugs are three Issues, not one.** LISS-0199, 0199 and 0200
touch three different seams (the CLI verb, the gating contract, the evaluator).
LISS-0200 changes a diagnostic contract and deserves its own review; folding it
into a "CLI fixes" Issue would bury that.

**Why the 50 failures are six Issues, not one and not fifty.** One umbrella
Issue is not reviewable — it would mix a parser question, a carrier-inference
question, and a unit-table question in one diff. Fifty Issues would relitigate
one shared root cause 21 times. The chosen unit is *one semantic ruling per
Issue*: each cluster asks a single question of the form "is the test stale or
is the Kernel wrong". LISS-0207 holds the three suites that share no cause with
the others and may split once triaged.

**Why harness defects are separate from regressions.** The 10 suites in
LISS-0208 fail before running an assertion — 5 import `pytest` (which the
testing strategy says is not used) and 5 lack the `sys.path` prologue. They
prove nothing about the Kernel, and mixing them into a regression Issue would
inflate its apparent size and hide a technology-selection question.

**Why CI is its own Issue and last.** LISS-0209 is the root cause of the
accumulation, but landing it against a red tree pins `main` red and blocks every
later PR. It is P0 in importance and last in order.

**What was deliberately left out of this batch:**

- The 13 existing `proposed` Issues (LISS-0078/0079/0084/0085/0086/0093/0095/
  0096/0100/0101/0102/0103/0104) — each needs its own Architecture or
  technology-selection approval.
- Reopened backlog rows: CUDA GPU Deferred workers, Kernel `Continuous`, Joint
  rational mode, live QPU provider SDK. All are ADR topics (ADR 0125/0126/0127),
  not intake items.
- **User-defined operator overloading.** Not an open question:
  [ADR 0114 §D5](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md)
  lists it under Out of scope. Only the documentation gap — friction ledger F-08
  not citing that decision — is filed, as part of LISS-0215.
- The ~15 re-implemented `_diagnostic` helpers with four different return
  shapes. Real, but a larger refactor than LISS-0210 should carry.

## Recommended order

```
1.  LISS-0211   batch schema contradiction — unblocks Claude's own batch workflow
2.  LISS-0208   test harness — the suite must be runnable before it is judged
3.  LISS-0202   largest cluster; its ruling propagates to 0202-0206
4.  LISS-0203 / 0203 / 0204 / 0205 / 0206   independent of each other
5.  LISS-0199 / 0199 / 0200   0199 tightens gating, so it needs a green baseline
6.  LISS-0209   CI gate — last, against a green tree
7.  LISS-0210   refactor
--- independent track, any time ---
    LISS-0212 / 0212 / 0213 / 0214 / 0215
--- separate approval track (Architecture Path) ---
    LISS-0217 (ADR 0165) / LISS-0218 (ADR 0166) / LISS-0219
```

Why LISS-0211 is first: until the contract and the validator agree, no bounded
execution batch record Claude Code writes can pass CI, so every later step in
this plan is blocked on it.

Why LISS-0200 is not first despite being the sharpest correctness bug:
tightening the execution gate will newly fail programs and suites. Against the
current 50 failures the delta would be unreadable; against a green tree it is
exactly measurable.

## Current Next Issue

- **Issue:** none — this plan is at investigation stage.
- **Reason it is not unblocked:** investigation approval is a distinct approval
  type and authorizes neither a phase nor implementation. Execution begins only
  when the Adjudicator sets a batch record to `approved_for_execution`.
- **Adjudicator approval needed:** (1) investigation approval for this intake;
  (2) a bounded execution batch naming the Issues to execute; (3) separate
  Architecture approval for ADR 0165 / 0165 before LISS-0217 / 0217 move.

## Risks

- **LISS-0202 is a hard stop, not a chore.** "Make the tests pass" is the wrong
  reflex: at least one suite (`test_linear_hardening_slice_b_red.py`) fails
  because a linear diagnostic is *missing*, which points at the Kernel. The
  Issue forbids resolving the cluster by weakening assertions.
- **LISS-0204 may be a physics-law issue, not a typing issue.** If method bodies
  now yield `Classical<Float>` where `State<Float>` was declared, the state was
  left. That must be confirmed either way before any repair.
- **LISS-0218 risks perturbing seeded outputs**, which would invalidate
  published SV reports and example expectations. ADR 0166 makes bit-identical
  seeded output the binding constraint.
- **Ordering risk:** landing LISS-0209 early pins `main` red.
- **LISS-0208 hides a technology selection** (adopt `pytest` or not) that must
  not be settled by drift.

## Verification plan

Documentation-only batch, so verification is structural:

```bash
python3 scripts/check-execution-batch-reviews.py --branch docs/wp-0069-operations-review-intake
```

```bash
python3 scripts/check-coverage-ledger-consistency.py
```

- `git diff --stat` shows changes under `docs/` only; no `compiler/`, no `tests/`.
- Every relative link in the new Issues, ADRs, and this plan resolves.
- New Issue IDs are unique and contiguous (LISS-0199…LISS-0219).
- GitHub Actions `repository-sanity` green on the PR.
