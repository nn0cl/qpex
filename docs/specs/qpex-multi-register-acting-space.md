# QPex Multi-register Acting-space Contract

Status: Phase 1 Red acceptance specification for LISS-0067 / ADR 0105.

This contract defines the first language slice for statically sized named
registers. It is intentionally limited to semantic shape and logical mapping;
it does not define physical routing, provider submission, or dynamic register
allocation.

## Observable requirements

### Named registers form one explicit tensor-product space

```gherkin
Feature: named multi-register acting spaces

  Scenario: declare a static system shape
    Given a system named BellPair
    And it declares data as QubitRegister<2>
    And it declares ancilla as QubitRegister<1>
    When the source is compiled
    Then compilation succeeds
    And the acting space is RegisterSet<BellPair>
    And the total logical width is 3
    And the Hilbert dimension is 8
```

The source declaration order (`data`, then `ancilla`) is the tensor-product
order. No hash order or provider order may replace it.

### Register-qualified sites are required for multi-register expressions

```gherkin
  Scenario: compose an operator over named registers
    Given BellPair has data : QubitRegister<2>
    And BellPair has ancilla : QubitRegister<1>
    When an operator is declared as Operator<RegisterSet<BellPair>>
    And its terms reference data[0] and ancilla[0]
    Then the operator retains RegisterSet<BellPair> as its acting space
    And no one-register lift or implicit register merge occurs
```

### Logical identity survives QPU IR lowering

```gherkin
  Scenario: preserve logical and derived identities
    Given BellPair is ordered as data : QubitRegister<2>, ancilla : QubitRegister<1>
    When the operator is lowered to provider-neutral QPU IR
    Then each logical reference retains its register name and local index
    And the IR records a derived flat index
    And the IR records the source tensor-order provenance
```

The first slice does not choose a physical qubit, coupling map, or routing
algorithm. Those are Host/provider responsibilities.

### Ambiguous and incompatible expressions fail explicitly

```gherkin
  Scenario: reject an unqualified site in a multi-register context
    Given BellPair has more than one named register
    When an operator uses an unqualified site such as Z[0]
    Then compilation fails with MULTI_REGISTER_INDEX_AMBIGUOUS

  Scenario: reject an incompatible acting space without an implicit lift
    Given an operator acts on QubitRegister<2>
    When it is used where RegisterSet<BellPair> is required
    Then compilation fails with ACTING_SPACE_MISMATCH
```

Unknown register identity, non-positive or dynamic register width, and
inconsistent derived flat mappings are hard errors. No silent truncation,
normalization, state reduction, or one-register fallback is allowed.

## Explicitly deferred

- physical routing and device capacity checks;
- provider SDKs, authentication, and network submission;
- dynamic register allocation;
- explicit embedding/covariance operations;
- new operator algebra, POVM, or mid-circuit measurement syntax;
- implementation of the accepted surface syntax.
