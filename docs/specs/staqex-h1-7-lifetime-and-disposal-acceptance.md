# Staqex H1-7 Lifetime and Disposal

| Field | Value |
|---|---|
| Status | **Draft for Final Review** |
| Parent | [H1-6 Operation Characteristics](staqex-h1-6-operation-characteristics-acceptance.md) |
| Scope approval | Adjudicator, 2026-08-03 |
| Phase | Phase 3 — Refactor complete |
| Out of scope | Automatic uncompute synthesis, optimizer lifetime shortening, QPU-specific disposal, new effect rows |

## 1. Objective

Make state lifetime and disposal explicit in the H1 State Transformer boundary.
The language must not teach `trace_out` as if it were reversible uncomputation.

- `uncompute`: restores an ancilla/value through a reversible witness and keeps
  the operation distinct from disposal.
- `trace_out`: performs an irreversible partial trace/disposal of a coordinate.
- implicit leftover State: remains a linear-use error.

The existing `LINEAR_IMPLICIT_DISCARD`, `UNCOMPUTE_WITNESS_MISSING`, and
`UncomputeObligation` contracts remain authoritative.

## 2. Acceptance scenarios

### H1-7-01 — `trace_out` is irreversible disposal

```gherkin
Given an H1 experiment that terminally measures a state while tracing out an ancilla
When the source is compiled
Then the plan records a TraceOut disposal step
And the step is not classified as Uncompute
And the operation has no Adj or Unitary characteristic
```

### H1-7-02 — `uncompute` is a separate reversible lifetime operation

```gherkin
Given an H1 experiment with an explicit uncompute witness
When the source is compiled
Then the plan records an Uncompute step
And the semantic artifact contains an UncomputeObligation
And the step is not classified as TraceOut
```

### H1-7-03 — Missing uncompute witness is rejected

```gherkin
Given an H1 experiment that requests uncompute without a witness
When the source is compiled
Then compilation emits UNCOMPUTE_WITNESS_MISSING
And no executable H1 plan is produced
```

## 3. Trial spellings

These are design-time spellings only and are not normative grammar:

```text
uncompute ancilla witness |0>
measure probe tracing_out ancilla
```

`trace_out` must retain its partial-trace meaning. It must not be silently
rewritten into `uncompute`, reset, or a basis-state assertion.

## 4. Phase 3 closeout

The lifetime step shape, witness boundary, and mapping to the existing
`UncomputeObligation` are implemented without changing the Red tests. Automatic
uncompute synthesis, optimizer lifetime shortening, QPU-specific disposal, and
new effect rows remain out of scope.
