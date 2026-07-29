# LISS-0100: First live QPU provider adapter

## Metadata

- Local issue ID: LISS-0100
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: research, provider selection, live execution
- Status/phase: **proposed — technology decision required** /
  `phase-0-design`
- Type/priority/size: external adapter / P1 / XL
- Depends on: LISS-0097, LISS-0099 and LISS-0102
- Branch: `docs/liss-0100-provider-selection`; implementation: **none**

## Acceptance scenarios

1. candidates are compared by contract coverage, testability, current
   availability, OpenQASM/subset fit, calibration evidence and operational
   constraints—not brand preference.
2. credentials, network, SDK types, retries, quotas and costs remain in the
   adapter/Host boundary.
3. core tests use fakes; live tests are opt-in, budgeted, redacted and never
   required for deterministic CI.
4. one `CH1_DIGITAL_RESEARCH` run records complete source-to-result evidence
   without implicit fallback.

## Decision slices

| Slice | Scope |
|---|---|
| A | provider-neutral evaluation matrix and consent/security requirements |
| B | official SDK/API/version and vulnerability research |
| C | isolated credential-free/fake POCs |
| D | technology ADR and Adjudicator selection |
| E | adapter Red/Green/Refactor under separate approvals |
| F | human-authorized bounded live acceptance |

No agent may choose a provider, install an SDK, use credentials, submit a job
or spend quota before the corresponding explicit approval. Apply the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0100-001: proposed; XL; strong reasoning/human selection; code assistant
  only for approved adapter slices.
