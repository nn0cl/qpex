# LISS-0077: Dynamic QPU controller and feed-forward

## Metadata

- Local issue ID: LISS-0077
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: architecture contract; each Slice and phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: language + execution contract / P0 / XL
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: LISS-0075 and LISS-0076 **complete**; LISS-0082 Slice D
- Blocks: LISS-0096; dynamic portions of LISS-0097
- Branch: `feature/liss-0077-dynamic-qpu`
- Implementation permission: **none**

## Summary

Define `dynamic qpu fn`, finite measurement feedback, reset/reuse, and
controller lifetime without weakening Static Kernel terminal measurement.

## Acceptance scenarios

1. Given a Static Kernel function, dynamic tokens and post-measure operations
   are rejected without changing existing terminal-measure behavior.
2. Given a dynamic measurement, its finite outcome token remains paired with
   the correlated post-measurement Joint state and is consumed by one merge.
3. Controller values cannot escape their phase, alter shape, enter Theory, or
   select deployment/provider behavior.
4. Supported supplied outcomes are deterministic; unsupported feedback,
   latency, reset, or reuse capabilities produce stable rejection.

## Slices

| Slice | Scope | Profile |
|---|---|---|
| A | lane/type markers and escape diagnostics | `SIM0_EXACT` |
| B | finite match, correlation, and one-merge verifier | `SIM0_EXACT` |
| C | reset/reuse and capability obligations | `CH1_DIGITAL_RESEARCH` |
| D | simulator execution under supplied outcomes | `SIM0_EXACT` |
| E | target metadata and portable dynamic artifact contract | `CH1_DIGITAL_RESEARCH`, NH5 |

## Boundaries and execution

- Candidate writes: new `dynamic_qpu.py`; approved tests
  `tests/test_dynamic_qpu_*.py`.
- Read-only by default: `quantum_semantic_ir.py`, evaluator, QASM backend.
- Forbidden: provider SDKs, implicit measurement, Static Kernel relaxation,
  credentials/network, runtime-dependent shape.
- Apply the [bounded execution packet](../architecture/bounded-feature-execution-packet.md);
  one Slice and one phase per approval.

## Decisions and verification

Architecture approval must fix token operations, merge law, reset semantics,
and diagnostic codes before Red. Verify type/linearity suites, deterministic
outcome fixtures, and unchanged Static terminal-measure suites.

## AI planning record

- AIP-0077-001: proposed; XL; strong reasoning for architecture, code assistant
  only for an approved bounded Slice; token estimate N/A because the executing
  environment supplies the metric.
