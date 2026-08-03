# Adjudicator review request — LISS-0196 trait / effect surface examples

## Review Target

- Artifact: [staqex-v1-trait-effect-surface-examples.md](../../specs/staqex-v1-trait-effect-surface-examples.md)
  + [LISS-0196](../../issues/LISS-0196-trait-specialization-surface-design.md)
- Current phase: Architecture Path — design only
- Requested approval: **review of surface-example draft** (not ship ADR Accept)
- Approval type: architecture (draft alignment only)
- Approved scope: docs design under LISS-0196
- Implementation allowed: **no**
- Post-review required: yes — direction on §5 open questions in the draft
- Execution batch ID: none

## What Changed

- Concrete shipped / proposed / rejected surface examples for:
  - trait specialization (recommend: none; optional pure interface defaults later)
  - effect rows (recommend: keep fixed set; no provider rows)
- Interaction with free-fn / selective-import face (WP-0089 residuals)
- Explicit recommendation: **no Kernel ship ADR now**

## Why It Matters

ADR 0128 blocks Red until surface examples exist. This draft closes that
documentation gate without inventing Kernel semantics.

## Adjudicator Checklist

- [ ] The phase is correct (design only).
- [ ] The included context is sufficient.
- [ ] The omitted context is acceptable (no Kernel).
- [ ] Assumptions are visible.
- [ ] Open decisions (§5 of the draft) are answered or deferred.
- [ ] Deterministic verification: docs-only; no runtime.
- [ ] The approval type and scope are explicit.
- [ ] Implementation permission is **no**.
- [ ] Post-review: choose whether to file a ship ADR or park LISS-0196 as
      “examples accepted, no ship”.

## Decision

- [ ] Approved (examples accepted; no ship ADR)
- [ ] Approved with comments
- [ ] Request ship ADR for pure interface defaults only
- [ ] Rejected / revise draft
