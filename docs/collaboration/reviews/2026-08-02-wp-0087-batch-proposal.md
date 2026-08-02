# WP-0087 bounded-batch proposal (draft)

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Work plan | [WP-0087](../../work-plans/WP-0087-s01-expressiveness-brushup.md) |
| Batch record | [execution-batch-wp-0087.json](execution-batch-wp-0087.json) |
| Status | **draft** — not `approved_for_execution` |
| Requested approval | bounded-batch (optional) **or** per-Issue Plan approval |
| Implementation allowed by this doc alone | **no** |

```markdown
[DESIGN CHECK]
- Scope: file a manageable draft batch for S01 expressiveness brush-up Issues
  LISS-0255–0260; document order, paths, invalidators, and approval recipe.
- Not in scope: Red/Green source edits; Kernel; live QPU; ADR Accept.
- Inputs: 2026-08-02 re-review; LISS-0243–0254 complete wave; minimal dialect.
- Verification: JSON schema_version 1 fields; links resolve; status remains draft
  until Adjudicator promotes.
```

## 1. Why a batch

After dialect / seats / `tracing_out` / field units / Host ticket, residual work is
mostly **examples + docs + Host**, with one Architecture ADR draft. A single
bounded batch keeps path and phase gates explicit without implying Kernel work.

## 2. Issue set and order

| Order | ID | Role |
|---|---|---|
| 1 | LISS-0255 | Docs hygiene (0254 complete sync) |
| 2 | LISS-0258 | Failure glossary ADR draft (parallel OK) |
| 3 | LISS-0256 | **P0** spine causal domain→Joint |
| 4 | LISS-0257 | Chapter story arcs |
| 5 | LISS-0259 | TonightTicket thin ops meaning |
| 6 | LISS-0260 | FQN / inspect polish |

## 3. Path boundary (summary)

**In:** `examples/showcase/S01_quantum_disaster_response/**`, WP-0087 / LISS-0255–0260
docs, S01 specs, ADR tree for 0258, collaboration reviews, related tests.

**Out:** `compiler/staqex/**` (by default), live QPU, non-S01 examples, secrets.

If 0256 discovers a Kernel gap: **stop**; do not expand this batch silently.

## 4. Approval recipe (Adjudicator)

1. Review WP-0087 + Issues + this proposal + JSON draft.
2. Optionally amend `issue_ids`, `allowed_paths`, or drop 0258/0260 from batch.
3. On execution branch tip, set in `execution-batch-wp-0087.json`:
   - `status`: `approved_for_execution`
   - `approved_by`, `approved_at`, `expires_at` (~14d)
   - `approval_commit`: that commit SHA
   - `approved_scope`: copy or edit `proposed_scope`
4. Agents may then run Issues in `issue_order` within path/phase gates.
5. After batch complete: `post_reviewed_*` + merge discipline per branch policy.

**Partial approval:** Adjudicator may approve only `{0255}` or `{0255,0256}` by
editing `issue_ids` before status promotion.

## 5. Success / post-review checklist

- [ ] 0255 scorecard/review no longer contradict shipped 0173/0174/0254
- [ ] 0256 mapping table + ≥3 causal domain→Joint hooks; seed-0 spine + ticket
- [ ] 0257 CH arcs documented; all chapter mains seed-0
- [ ] 0258 ADR filed (Accept may lag post-review)
- [ ] 0259 ticket meaning/honesty; no invented KPIs
- [ ] 0260 no new inspect museum; multi-file evidence intact
- [ ] Scorecard A+B rows retained
- [ ] No `compiler/staqex` edits unless batch amended

## 6. Explicit non-authorization

This proposal and the JSON `status: draft` **do not** grant:

- Phase 1/2/3 on any Issue
- Architecture Accept of a failure glossary ADR
- Technology selection
- Mutation on `main`

## 7. Agent payload (after approval only)

```text
Execute approved batch execution-batch-wp-0087.json only if status is
approved_for_execution and approval_commit matches current batch branch base.
Follow issue_order; stay in allowed_paths; stop on invalidating_triggers.
Start LISS-0255 docs-only; do not touch compiler/staqex.
Report Red/Green/Refactor per Issue; keep scorecard A+B.
```
