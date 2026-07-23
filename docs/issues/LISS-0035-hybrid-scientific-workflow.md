# LISS-0035: Hybrid scientific workflow contract

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0022, LISS-0016, LISS-0015, LISS-0034, ADR 0070/0071
- Blocks: VQE/QAOA-style iterative execution language surface

## Summary

Define an explicit host/workflow layer for VQE/QAOA-like loops around a closed
experiment specification. The layer may bind parameters, submit Jobs, consume
typed measurement results, update a classical optimizer, and schedule another
run, while keeping provider policy outside the Kernel.

## Acceptance questions

- What are the parameter-binding, measurement-result, convergence, and
  cancellation DTOs?
- How are shots, seeds, retries, and reproducibility reported?
- Which feedback is host workflow, and which is Dynamic QPU feed-forward?
- How does a workflow compose Job/Task handles without exposing provider SDKs?

## Non-goals

No provider SDK, credentials, cloud submission, or optimizer implementation is
authorized by this design issue.
