# Staqex phase-separated scientific scopes

Status: **accepted for LISS-0034 Phase 3 sealed scope contracts**. Full
body-level scientific AST resolution remains a later refinement.

## 1. Purpose

Staqex must allow theoretical physicists and engineers to describe one study
without placing Hamiltonians, shots, retries, and provider settings in the same
semantic scope. The source declaration order may be flexible; dependency
direction is not.

## 2. Scope kinds

```text
theory      mathematical laws, states, operators, observables
experiment  concrete system, preparation, observation plan
workflow    host-controlled parameter/result feedback
execution   backend, shots, seed, resource and Job policy
report      result presentation/analysis after execution
```

The normative dependency direction is:

```text
execution -> workflow -> experiment -> theory
report -> execution result
```

## 3. Declarative Builder/Resolver boundary

Each scope collects declarations without making source order part of the
meaning. A resolver performs, in order:

1. name resolution;
2. scope visibility checks;
3. type and Hilbert-domain checks;
4. dependency graph construction and cycle detection;
5. completeness checks;
6. immutable scope contract generation.

The Builder/Resolver may be an implementation mechanism or an explicit surface
API, but it must not turn mathematical expressions into imperative method-call
boilerplate. Formula bodies remain formula-like.

Phase 2 established the declaration boundary, reference collection,
source-order independence, upward-dependency rejection, and cycle detection.
Phase 3 seals the collected declarations into immutable contracts exposed by
the compiler result. The contract map is read-only, and each contract has
immutable kind, name, references, symbols, and `sealed` fields. Existing
Type-First declarations such as `Operator H = …` are preserved in the scope
AST. Execution assignments remain boundary metadata until their phase-specific
syntax is accepted separately.

## 4. Visibility rules

| Symbol | Theory | Experiment | Workflow | Execution |
|---|---:|---:|---:|---:|
| `Operator`, `State`, observable | yes | yes | through contract | through contract |
| `ShotCount`, `Backend`, `RetryPolicy` | no | no | yes | yes |
| `Host<T>` | no | no | yes | yes |
| provider SDK object | no | no | no | adapter only |
| `measure` result | no | result contract | yes | yes |

An invalid upward dependency is a hard compile error. No implicit import or
closure capture may make an Execution symbol visible in Theory.

## 5. Acceptance scenarios

1. Theory can define an indexed Hamiltonian without seeing `shots` or `backend`.
2. Experiment can refer to a Theory contract but cannot mutate its internals.
3. Workflow can consume a measurement-result DTO and bind a `Param<T>`.
4. Execution can configure a Job without changing the Theory AST.
5. Declarations resolve successfully regardless of source block order.
6. A cycle or upward dependency produces a diagnostic before lowering.

## 6. Non-goals

- no provider SDK or cloud submission;
- no VQE/QAOA optimizer implementation (LISS-0035);
- no implicit mid-program measurement;
- no general mutable classical language inside the Theory scope.
