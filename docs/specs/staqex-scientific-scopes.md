# Staqex phase-separated scientific scopes

Status: **accepted** — LISS-0034 Phase 3 sealed scope contracts **and**
LISS-0076 body-level phase visibility (Slices A–D; Slice E closeout).

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

Linked programs (`compile_path`) merge scientific scope declarations across
the import graph so body-level phase visibility applies at the module
boundary (LISS-0076 Slice C).

## 4. Visibility rules

| Symbol | Theory | Experiment | Workflow | Execution |
|---|---:|---:|---:|---:|
| `Operator`, `State`, observable | yes | yes | through contract | through contract |
| `ShotCount`, `Backend`, `RetryPolicy` | no | no | yes | yes |
| `Host<T>` | no | no | yes | yes |
| provider SDK object | no | no | no | adapter only |
| `measure` result | no | result contract | yes | yes |

An invalid upward dependency is a hard compile error. No implicit import or
closure capture may make an Execution symbol visible in Theory,
Experiment, or Workflow expression bodies.

### 4.1 Body-level Execution / Report symbol visibility (LISS-0076 / 0118)

| Rule | Diagnostic |
|---|---|
| Theory/Experiment/Workflow body names an Execution-bound symbol (not lexeme) | `PHASE_TYPE_VISIBILITY_ERROR` |
| Theory body names lexeme `shots` / `backend` / `retry` / `Host` | `PHASE_SCOPE_DEPENDENCY_ERROR` (parser) |
| Theory Call args name an Execution symbol | `PHASE_TYPE_VISIBILITY_ERROR` |
| Theory calls a fn/method whose body (transitively) names an Execution symbol | `PHASE_TYPE_VISIBILITY_ERROR` |
| Report body may name Execution-bound symbols | allowed (`report -> execution`) |
| Theory/Experiment/Workflow body names a Report-bound symbol | `PHASE_TYPE_VISIBILITY_ERROR` |
| Qualified clean method call (`Pure().k()`) despite a tainted peer `S.k` | allowed (precise `Class.method` key) |
| Bare short name `k()` when any FunDecl `k` or `*.k` is execution-tainted | `PHASE_TYPE_VISIBILITY_ERROR` (fail closed) |
| Execution / `main` may reference Theory symbols or call such fns | allowed (downward / Kernel) |

## 5. Acceptance scenarios

1. Theory can define an indexed Hamiltonian without seeing `shots` or `backend`.
2. Experiment can refer to a Theory contract but cannot mutate its internals.
3. Workflow can consume a measurement-result DTO and bind a `Param<T>`.
4. Execution can configure a Job without changing the Theory AST.
5. Declarations resolve successfully regardless of source block order.
6. A cycle or upward dependency produces a diagnostic before lowering.
7. Theory/Experiment/Workflow bodies that name Execution-bound symbols fail
   with `PHASE_TYPE_VISIBILITY_ERROR` (not unresolved-name alone).
8. Imported Execution symbols remain invisible to entry Theory; imported
   Theory remains usable by entry Experiment.
9. Theory must not call fn/methods that close over Execution symbols; `main`
   may.

### 5.1 Gherkin (LISS-0076 / 0118)

Automated coverage:
`tests/test_body_phase_slice_{a,b,c,d}_red.py` and
`tests/test_body_phase_slice_{a,b,c}_0118_red.py`.

```gherkin
Feature: Body-level scientific phase typing

  Scenario: Theory body must not see Execution symbols
    Given an execution scope that binds a classical name n
    And a theory scope whose Operator body references n
    And the reference is not a forbidden lexeme (shots/backend/retry/Host)
    When compile_source runs
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Experiment and Workflow bodies must not see Execution symbols
    Given an execution scope that binds a classical name n
    And an experiment or workflow body that references n
    When compile_source runs
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Imported Execution symbols stay invisible to entry Theory
    Given an imported module that binds execution symbol n
    And the entry theory body references n
    When compile_path runs
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Theory must not call execution-tainted fn or method
    Given a fn or method whose body names execution symbol n
    And a theory body that calls that fn or method
    When compile_source runs
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Transitive helper taint is rejected
    Given mid calls leak and leak names execution symbol n
    And a theory body that calls mid
    When compile_source runs
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Report may see Execution; Theory must not see Report symbols
    Given a report scope that binds a classical name r
    And an execution scope that binds n
    When a report body references n
    Then compilation succeeds for that reference
    When a theory body references r
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR

  Scenario: Bare short name fails closed; qualified clean method stays precise
    Given tainted method S.k and clean method Pure.k
    When a theory body calls Pure().k()
    Then diagnostics do not include PHASE_TYPE_VISIBILITY_ERROR for that call
    When a theory body calls bare k() while any peer *.k is tainted
    Then diagnostics include PHASE_TYPE_VISIBILITY_ERROR
```

## 6. Non-goals

- no provider SDK or cloud submission;
- no VQE/QAOA optimizer implementation (LISS-0035);
- no implicit mid-program measurement;
- no general mutable classical language inside the Theory scope;
- LISS-0076 deferred residuals (Report matrix, transitive taint, short-name
  policy) are **closed** by
  [LISS-0118](../issues/LISS-0118-body-phase-typing-residuals.md)
  (**not** LISS-0116). Bare short-name fail-closed remains an intentional
  over-approx; use qualified `Receiver.method` for precision.
