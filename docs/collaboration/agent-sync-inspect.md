# Agent sync addendum: inspect (ADR 0030)

Date: 2026-07-23.

## Lock

| Form | Collapse? | Role |
|------|-----------|------|
| `measure` | Yes | Terminal sample |
| `snapshot` | No | Checkpoint file log |
| `inspect` | No | Debug passthrough of distribution table |

Console text is **host String only** — not a `State` fed back into the joint.
Dirac and mixtures share one ket/`prob` format family (ADR 0030).

Never use `measure` just to print a PMF.
