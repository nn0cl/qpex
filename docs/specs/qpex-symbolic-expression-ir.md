# QPex symbolic expression IR and lowering provenance

Status: **accepted for the LISS-0033 traceable source IR boundary**.
Resolved/executable IR and lowering provenance remain out of scope.

## 1. Purpose

QPex must preserve the physicist's expression long enough to type-check,
diagnose, optimize, and explain lowering. A Pauli list or gate sequence alone
is not sufficient provenance for a source formula containing domains, operator
algebra, mappings, discretization, or approximation policy.

## 2. IR stages

```text
Source AST
  -> Symbolic IR
  -> Resolved IR
  -> Executable/QPU IR
```

### Symbolic IR

Retains source-shaped nodes including:

- finite binders and domains;
- indexed operator access;
- operator algebra;
- second-quantized families;
- source `Span` and declaration identity.

### Resolved IR

Adds:

- carrier and Hilbert-space domains;
- resolved index bounds and boundary policy;
- operator algebra laws;
- mapping and discretization choices;
- resource estimates and approximation metadata.

### Executable/QPU IR

Contains a finite simulator/QPU representation. It must retain a stable link to
the resolved and symbolic ancestors.

## 3. Provenance contract

Every lowering pass that changes representation must append a record:

```text
pass name
input node identity
output node identity
parameters
approximation/error metadata
source span
```

No pass may silently discard a domain, mapping, discretization, Trotter order,
or error budget. Provider-specific details remain outside the Kernel IR.

The source projection provides deterministic source node IDs, a resolved-link
surface marked `unresolved`, and explicit empty mapping/approximation slots.
Those slots do not claim that a lowering pass has occurred.

## 4. Acceptance scenarios

1. A finite `sum` remains identifiable as a binder before expansion.
2. `commutator(A, B)` remains identifiable before algebraic rewriting.
3. A future fermion-to-qubit mapping records its mapping name and input/output
   node identities.
4. Trotter/Suzuki lowering records order, step count, and error policy.
5. A diagnostic can point from a lowered node to its source `Span`.
6. Provider SDK objects do not appear in the Kernel IR.

## 5. Non-goals

- no backend/provider selection;
- no serialized file format lock beyond a stable inspectable contract;
- no automatic approximation policy selection;
- no implementation of second quantization (LISS-0032).
