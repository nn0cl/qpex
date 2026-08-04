# LISS-0028: Dynamic QPU lane

## Metadata

- Local issue ID: LISS-0028
- Status: **Phase 3 reviewed** for the rejection/capability boundary; follow-up open
- Phase: Architecture Path → Feature Path boundary slice complete
- Type: language semantics / dynamic circuit boundary
- Priority: P1
- Related: ADR 0065, ADR 0069, ADR 0071, [ADR 0193](../architecture/adr/0193-dynamic-qpu-timing-region-intent.md) (Accepted 2026-08-05), LISS-0016, LISS-0019

## Acceptance specification

- [ ] Mid-circuit measurement and classical feed-forward have explicit
      semantics distinct from terminal `measure`.
- [x] Dynamic control is syntactically and semantically separate from static
      `forEach`.
- [x] A target capability profile is required before submission.
- [x] Unsupported dynamic features fail explicitly; no hidden Host fallback.
- [ ] Timing, qubit reuse, controller values, and JobResult composition are
      specified. **Partial:** timing's grammar/IR shape (`dynamic qpu
      within <name>`, a `TimingRegion` witness) is Accepted via ADR 0193;
      not yet implemented, and qubit reuse / controller values / JobResult
      composition remain fully open.
- [ ] CPU simulator and QPU lowering share an observable semantic contract.

## Non-goals

- Selecting IBM, Amazon Braket, IQM, or another provider.
- Implementing error correction or a provider-specific control dialect.
- Relaxing the Static Hilbert Kernel's terminal-measure baseline.

## Phase 1 record

- Status: **Red complete; awaiting Phase 2 Green approval**.
- Test file: `tests/test_static_parametric_dynamic_boundaries_red.py`.
- The test uses provisional `dynamic qpu { … }` syntax to make the required
  capability boundary observable; syntax and effect markers remain reviewable.

## Phase 2 record

- Status: **Green complete; awaiting Phase 3 Refactor approval**.
- Explicit dynamic blocks are parsed and rejected with capability/unsupported
  diagnostics; no dynamic execution or Host fallback was added.
- Verification: all unit tests and SV 165/165 passed.

## Phase 3 record

- Status: **Complete for the rejection/capability boundary; follow-up open**.
- Added explicit dynamic-lane teaching documentation and preserved the
  terminal-measure/static-Kernel separation.
- Remaining: mid-circuit semantics, timing, qubit reuse, capability DTO, and
  observable JobResult contract.

## Phase 3 review record

- The current boundary accepts the explicit `dynamic qpu { ... }` marker only
  as a capability/rejection surface; it does not execute mid-circuit control.
- Unsupported dynamic features fail with stable diagnostics and never fall
  back to Host execution or static `forEach` elaboration.
- Static Kernel programs retain terminal `measure` semantics independently of
  this lane.
- Reviewer empathy: the completed rejection boundary is now clearly separated
  from the still-undecided dynamic measurement type/effect model.
- Status: **Phase 3 reviewed; rejection/capability boundary complete**.
