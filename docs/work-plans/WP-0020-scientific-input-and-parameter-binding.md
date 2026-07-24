# WP-0020: Scientific input and parameter binding

## Planning record

- Issue: [LISS-0045](../issues/LISS-0045-scientific-input-and-parameter-binding.md)
- ADR: [ADR 0090](../architecture/adr/0090-scientific-input-and-parameter-binding.md)
- Size: L
- Current phase: Phase 2 Green complete
- Branch scope: scalar Host input and parameter-binding contract

## Goal

Give a physicist a typed path from a scalar experimental/model value to a
`Param<T>` binding, a finite sweep, and a provenance-bearing provider-neutral
result without making file formats or provider SDKs part of QPex semantics.

## Dependencies

- Existing `Param<T>` and Job/JobResult boundaries.
- Existing Host/Kernel isolation diagnostics.
- LISS-0027, LISS-0022, LISS-0032, LISS-0033, and LISS-0035.
- No new external dependency.

## Phase plan

### Phase 0 — design intake

Completed by the research note and ADR 0090 acceptance. Representative
workloads include H2, Ising/material, Rabi sweeps, and open-system runs.

### Phase 1 — Red

Add only acceptance tests for:

1. scalar typed input and mandatory provenance;
2. binding name and dimension validation;
3. immutable non-empty parameter sweeps;
4. provenance retention at the JobResult boundary;
5. rejection of generic data/file-format values in Kernel scope.

The expected state is Red because the new Host contract module is not yet
implemented. No production module, adapter, provider, or network call may be
added in this phase.

### Phase 2 — Green

After Adjudicator review of the Red tests, add the smallest dependency-free
Host value objects and validation needed to pass them. Reuse existing
`ParamBinding` and `JobResult` boundaries where their contracts fit; do not
introduce a provider SDK.

Completed with `compiler/qpex/scientific_input.py` and public package exports.
The reviewed tests pass; result-envelope integration and provider adapters
remain deferred.

### Phase 3 — Refactor

Review names and boundaries for physicist readability, confirm result
provenance is not hidden in an adapter, and keep file/provider concerns behind
ports.

## Verification and exit gates

- Phase 1: each acceptance test fails for the missing contract, while the
  existing test suite remains untouched.
- Phase 2: reviewed tests pass without modifying their assertions.
- Phase 3: full deterministic verification and reviewer empathy summary.
- Phase 1 exit requires explicit Adjudicator approval before Green.
