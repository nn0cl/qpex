# LISS-0102: Job, Session, Batch, cancellation, and retry orchestration

## Metadata

- Local issue ID: LISS-0102
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: state machine/consent/budget; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: Host use case / P1 / XL
- Depends on: LISS-0065, LISS-0066 and LISS-0099
- Blocks: LISS-0100 and LISS-0103
- Branch: `feature/liss-0102-job-orchestration`; implementation: **none**

## Acceptance scenarios

1. provider-neutral Job/Attempt/Session/Batch states and transitions are
   deterministic and idempotency is explicit.
2. cancellation, retry and partial/complete result policy produce stable Host
   outcomes for adapter failures and duplicate events.
3. local insufficiency never triggers implicit remote or simulator fallback;
   remote execution requires explicit consent and budget.
4. Kernel and semantic IR remain unchanged and unaware of lifecycle details.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | lifecycle VOs/state machine and illegal transitions |
| B | attempts, idempotency and retry policy |
| C | cancellation and partial-result policy |
| D | Session/Batch and budget/consent |
| E | fake adapter event conformance |

Candidate writes: Host/use-case lifecycle modules, ports, fakes and
`tests/test_job_orchestration_*.py`. Provider SDKs, implicit fallback,
credentials and Kernel changes are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0102-001: proposed; XL; strong state-machine review, code assistant per
  reviewed transition Slice.
