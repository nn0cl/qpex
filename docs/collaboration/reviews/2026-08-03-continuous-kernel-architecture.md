# Adjudicator review: Continuous Kernel value (P3 reopen)

## Review Target

- Artifact: [ADR 0185 Proposed](../../architecture/adr/0185-kernel-continuous-value.md);
  [LISS-0312](../../issues/LISS-0312-continuous-kernel-architecture.md)
- Current phase: Architecture Path design intake (complete)
- Requested approval: **Architecture** — choose Lane A / B / C
- Approval type: architecture
- Approved scope: design artifacts for Continuous reopen only
- Implementation allowed: **no**
- Post-review required: yes (record Accept/Reject on ADR 0185)
- Execution batch ID: not applicable

## [DESIGN CHECK]

- **Scope and expected behavior:** Reopen Continuous for Architecture Path;
  produce Proposed ship ADR with three lanes; stop before Kernel Red.
- **Specifications and files inspected:** ADR 0126, 0162, 0163, 0164;
  LISS-0195/0198; re-review P3 table; permanent-out reopen; Host MC module;
  continuous_lowering / discretization lineage.
- **Component boundaries:** Continuous stays outside Joint mid-program unless
  Lane B; finiteize reuses HostMonteCarloPort / FiniteStateInject; Theory
  continuous_operator remains behind ADR 0074 contracts.
- **Applicable constraints:** NLTS; terminal measure only on finite State;
  no silent truncation; no inventing cloud MC SDK; physicist-first ideal form.
- **Decisions, assumptions, ambiguities:** Host path is complete enough to
  draft ship ADR (0162 §4). Lane choice is Adjudicator-only. Surface spelling
  for Lane A finiteize is open.
- **Included and omitted AI context:** boundary ADRs + Host inject; omitted full
  continuous_lowering implementation dump and cloud vendor catalogs.
- **Task routing:** deterministic Architecture Path docs (this agent).
- **I/O evidence contract:** N/A (no model-as-domain-output).
- **Verification plan:** docs-only PR; no pytest required for this Issue.

## What Changed

- Proposed ADR 0185 with Lanes A (finiteize surface MVP — recommended),
  B (mid-program Continuous + hard gates), C (repark).
- LISS-0312 investigation Issue + draft Feature Issue split (0313–0315).
- Re-review / permanent-out register notes Continuous Architecture reopen in
  progress (not shipped).

## Why It Matters

Continuous is the highest-impact remaining language-type question. Host MC is
shipped; without an explicit lane, agents either invent Kernel Continuous or
leave physicists on Python-only inject forever.

## Adjudicator Checklist

- [ ] The phase is correct (Architecture only).
- [ ] The included context is sufficient.
- [ ] The omitted context is acceptable.
- [ ] Assumptions are visible.
- [ ] Open decisions are either answered or intentionally deferred.
- [ ] Deterministic verification is adequate for this step.
- [ ] The approval type and scope are explicit.
- [ ] Implementation permission is **no** until a later Feature grant.
- [ ] Any post-review requirement is recorded.

## Decision (Adjudicator)

- [ ] **Lane A Accepted** — finiteize surface ship ADR; authorize LISS-0313 Plan
- [ ] **Lane B Accepted** — mid-program Continuous ship; authorize LISS-0315 Plan
- [ ] **Lane C** — repark; mark ADR 0185 Rejected
- [ ] **Amend** — comment changes required before Accept
- [ ] Implementation allowed: **no** (default) / yes after separate Phase grant

### Recommendation

**Accept Lane A.** Elevate Host finiteize to notebook surface; keep mid-program
`Continuous` for a later ADR after A proves demand.
