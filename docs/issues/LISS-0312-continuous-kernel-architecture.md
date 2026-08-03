# LISS-0312: Continuous Kernel value — Architecture Path reopen

## Metadata

- Local issue ID: LISS-0312
- Status: **investigation complete — awaiting Architecture approval**
- Type: Architecture Path (design only)
- Priority: P3 reopen (Adjudicator chose Continuous Kernel value)
- Branch: `process/liss-0312-continuous-kernel-architecture`
- Proposed ADR: [0185](../architecture/adr/0185-kernel-continuous-value.md)
- Review: [2026-08-03-continuous-kernel-architecture.md](../collaboration/reviews/2026-08-03-continuous-kernel-architecture.md)
- Depends: ADR 0126, 0162, 0163, 0164 (Host path shipped)

## Intent

Reopen the permanent-out Continuous row for **Architecture Path only**: produce
a Proposed ship ADR and a reviewable lane choice (A finiteize surface /
B mid-program Continuous / C repark). No Kernel Red in this Issue.

## Deliverables

- [x] Proposed [ADR 0185](../architecture/adr/0185-kernel-continuous-value.md)
- [x] Design intake + Adjudicator review record
- [x] Issue granularity for post-Accept Feature Path (LISS-0313… below)
- [x] No Kernel / test implementation

## Post-Accept Feature Path (draft — not authorized)

| Issue | Scope | Depends |
|---|---|---|
| LISS-0313 | Feature Red/Green for **Lane A** finiteize surface (if A Accepted) | ADR 0185 Accepted as A |
| LISS-0314 | Official example pedagogy + Host demo alignment | LISS-0313 |
| LISS-0315 | **Lane B only** — mid-program Continuous type Red (if B Accepted instead/later) | separate ship ADR amend or 0185-B |

## Exit (this Issue)

- [x] Proposed ADR + review packet on branch
- [ ] Adjudicator Architecture decision: Lane A / B / C
- [ ] If A or B: mark ADR Accepted (or reject) in a follow-up docs commit
- [ ] If C: repark Continuous; close 0185 as Rejected

## Non-goals

Kernel code; Phase 1 Red; cloud MC SDK; Joint rational; QPU continuous.
