# Staqex Dynamic QPU lane specification

| Field | Value |
|---|---|
| Status | **Accepted rejection/capability boundary; timing-intent grammar/IR Accepted (ADR 0193); Kernel slice LISS-0381 complete; execution follow-up remains open** |
| Decision | [ADR 0071](../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md); timing intent [ADR 0193](../architecture/adr/0193-dynamic-qpu-timing-region-intent.md) |
| Issue | [LISS-0028](../issues/LISS-0028-dynamic-qpu-lane.md) (rejection boundary); [LISS-0381](../issues/LISS-0381-dynamic-qpu-timing-region-intent.md) (timing intent Kernel slice) |

This lane is intentionally separate from the Static Hilbert Kernel.

Required future contracts:

- explicit mid-circuit measurement semantics;
- classical feed-forward/control values;
- timing and qubit-reuse semantics — **partial:** timing *intent* as a
  Region attribute is Accepted in ADR 0193; Kernel implementation is
  LISS-0381; concrete per-backend timing meaning and qubit reuse remain
  open;
- target capability profile and explicit unsupported-feature errors
  (shipped for the rejection boundary);
- simulator/QPU equivalence at the observable JobResult boundary.

The dynamic lane remains non-executable until a real target adapter is
selected. ADR 0193 / LISS-0381 add a capturable grammar and IR witness
only; they do not authorize execution.

## Acceptance scenarios — timing intent (ADR 0193, LISS-0381)

Normative for Feature Path Phase 1–3 on LISS-0381. Assertions must match
these `Then` clauses exactly. Physicist-first: timing remains a named
intent on the lane region (`within <name>`), never backend `dt` literals
scattered between operations, and `dynamic qpu` stays a statement.

Composition stability (vision §2.2): expanding or combining well-formed
blackboard fragments must keep the timing intent attached and inspectable;
`within` must not steal ordinary identifiers outside the `dynamic qpu`
clause (contextual / soft keyword only in that position).

```gherkin
Feature: Dynamic QPU timing intent as a Region attribute

  Scenario: optional within clause is accepted on dynamic qpu
    Given source containing
      """
      dynamic qpu within coherent_window {
        apply H onto q0
      }
      """
    When the program is compiled
    Then parsing succeeds with DynamicQpuStmt.timing_intent == "coherent_window"
    And DynamicQpuStmt remains a statement (not an expression)
    And diagnostics include DYNAMIC_CAPABILITY_REQUIRED_ERROR
    And diagnostics include DYNAMIC_UNSUPPORTED_FEATURE_ERROR

  Scenario: dynamic qpu without within remains valid and unchanged
    Given source containing `dynamic qpu { … }` with no within clause
    When the program is compiled
    Then DynamicQpuStmt.timing_intent is None
    And no TimingRegion is present in Quantum Semantic IR
    And diagnostics include DYNAMIC_CAPABILITY_REQUIRED_ERROR
    And diagnostics include DYNAMIC_UNSUPPORTED_FEATURE_ERROR

  Scenario: TimingRegion carries the source-derived timing intent
    Given source containing `dynamic qpu within coherent_window { … }`
    When the program is compiled
    Then Quantum Semantic IR contains exactly one TimingRegion
    And that region's timing_intent equals "coherent_window"
    And the intent is not a hardcoded placeholder unrelated to the source

  Scenario: different timing names produce distinguishable TimingRegions
    Given one program with `within coherent_window`
    And another with `within idle_window`
    When both are compiled
    Then each TimingRegion.timing_intent equals its own source name
    And the two timing_intent values differ

  Scenario: malformed within clause fails closed
    Given source containing `dynamic qpu within` with no following identifier
      before `{`
    When the program is compiled
    Then diagnostics include DYNAMIC_TIMING_INTENT_MALFORMED
    And the clause is not silently accepted
    And the compiler does not crash

  Scenario: timing intent does not make the lane executable
    Given any well-formed `dynamic qpu` statement with or without within
    When the program is compiled
    Then DYNAMIC_CAPABILITY_REQUIRED_ERROR is still emitted
    And DYNAMIC_UNSUPPORTED_FEATURE_ERROR is still emitted
    And no Host/QPU execution path is taken for the dynamic block

  Scenario: evolve under/for inside within keeps timing intent (composition)
    Given source containing
      """
      dynamic qpu within coherent_window {
        state psi = |0>
        Operator H = X
        state psi = evolve psi under H for 1.0.s
        measure psi
      }
      """
    When the program is compiled
    Then DynamicQpuStmt.timing_intent == "coherent_window"
    And Quantum Semantic IR contains a TimingRegion with timing_intent
      "coherent_window"
    And diagnostics include DYNAMIC_CAPABILITY_REQUIRED_ERROR
    And diagnostics include DYNAMIC_UNSUPPORTED_FEATURE_ERROR
    And the enclosing within clause is not dropped because the body grew

  Scenario: multiple within blocks in one program yield multiple TimingRegions
    Given one main containing both
      `dynamic qpu within coherent_window { … }` and
      `dynamic qpu within idle_window { … }`
    When the program is compiled
    Then Quantum Semantic IR contains exactly two TimingRegions
    And their timing_intent values are {"coherent_window", "idle_window"}
    And both dynamic statements still emit the two dynamic rejection diagnostics

  Scenario: non-identifier timing intent fails closed
    Given source containing `dynamic qpu within 1 { … }`
      or `dynamic qpu within foo(bar) { … }`
    When the program is compiled
    Then diagnostics include DYNAMIC_TIMING_INTENT_MALFORMED
    And the clause is not silently accepted as a bare dynamic qpu block

  Scenario: within remains usable as an ordinary identifier outside the clause
    Given source that binds and measures a name `within` with no dynamic qpu
      timing clause
    When the program is compiled
    Then compilation does not emit DYNAMIC_TIMING_INTENT_MALFORMED
    And the program is not rejected solely because `within` is an identifier
    And (vision §2.2) introducing timing intent must not globally reserve
      `within` as a hard keyword

  Scenario: adjacent Static evolve and dynamic within do not corrupt each other
    Given one main with Static `evolve … under H for t` followed by
      `dynamic qpu within coherent_window { … }`
    When the program is compiled
    Then the dynamic statement's timing_intent == "coherent_window"
    And Quantum Semantic IR contains a TimingRegion with that intent
    And diagnostics include DYNAMIC_CAPABILITY_REQUIRED_ERROR
    And diagnostics include DYNAMIC_UNSUPPORTED_FEATURE_ERROR
    And the Static evolve form is not rewritten or dropped to accommodate
      the within clause
```
