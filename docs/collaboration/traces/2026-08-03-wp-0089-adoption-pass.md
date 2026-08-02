# AI work trace: WP-0089 plan approval + adoption pass

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Agent | Grok (Grok Build) |
| Branch | `docs/wp-0089-surface-adoption-and-sugar` |
| Approval | Plan approval — [2026-08-03-wp-0089-plan-approval.md](../reviews/2026-08-03-wp-0089-plan-approval.md) |

## Done

- LISS-0274 program lock + approval record
- LISS-0275: basics B01–B08, B10–B15 → experiment profile (B09 multi-file kept)
- LISS-0276: S01 spine selective import + lane + short names (`Disaster.*` count 0)
- LISS-0277: partial — `RationTicket`, `FairnessReport` → struct + `fairness_score`
- LISS-0278: A06 no inspect museum + selective import
- LISS-0279: package root `examples.…` (not `com.staqex…`; not `staqex.examples` — stdlib collision)
- LISS-0280: QUICKSTART, basics README, B09 honesty, package-root-naming, friction ledger §5

## Verification

- Spec verification: **161/161 PASS**
- Seed-0: B01, B08, S01 spine, A06, B09, day2, morning

## Not done (still WP-0089)

- Sugar ADRs / Kernel LISS-0281–0288 (blocked on Architecture Accept)
- LISS-0289 post-sugar re-sync
- Full S01 chapter FQN cleanup; remaining domain `class` DTOs
