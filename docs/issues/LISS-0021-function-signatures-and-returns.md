# LISS-0021: Function signatures and measure-free returns

## Metadata

- Local issue ID: LISS-0021
- GitHub issue: none
- Status: Superseded for return syntax by LISS-0025 / ADR 0068
- Phase: Architecture Path → Feature Path
- Type: language architecture / type system
- Priority: P0
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: cross-cutting grammar, AST, typechecker, evaluator,
  module linking, and specification change
- Owner/agent: TBD
- Related branch: none yet

## Summary

Define ordinary function and class-method signatures so that a function may
accept any supported number of inputs and return an explicitly typed value
without weakening QPex's terminal-measure rule.

`main` remains a special no-result entry point. It owns the terminal
`measure`; ordinary functions, methods, and `init` remain measure-free.

## Problem statement

The current grammar parses `fn name(params) { ... }` but has no return-type
annotation. The original implementation used an implicit final expression and
class methods used the last Type-First bind as an implicit return. LISS-0025
replaces that convention with an explicit terminal `return` and lexical scope.

The intended physical invariant is different:

```text
measure-free function:  (State<A>, State<B>, ...) -> State<R>
main:                   program -> Unit, with terminal measurement as an effect
```

Returning an unmeasured state does not violate “Never Leave the State”; only
`measure` crosses the observation boundary.

## Proposed acceptance scope

- [ ] Ordinary `fn` declarations support an explicit return annotation, such
      as `fn f(x: State<Int>) -> State<Int> { ... }`.
- [ ] Omitted return annotations are rejected with `MISSING_RETURN_TYPE` for
      ordinary functions, methods, and `main`.
- [ ] Class methods use the same signature rules, with an implicit `this`
      receiver; methods may accept zero or more explicit arguments.
- [ ] `init` is a constructor-only exception and has no return value.
- [x] A function body returns an explicit terminal `return` expression; early
      early return remains forbidden
      so control flow cannot bypass the joint-state pipeline.
- [ ] The final expression may be a state-preserving transform, a supported
      classical/domain value, or a product value according to the accepted
      type rules; implicit State-to-classical collapse is forbidden.
- [ ] Return type, argument types, product arity, and dimensions are checked
      statically where the Kernel already has those checks.
- [ ] `measure` and `snapshot` remain forbidden inside ordinary functions and
      methods; `main` remains the only terminal observation owner.
- [ ] Zero-, one-, and multi-argument functions have deterministic acceptance
      tests, including a State return and a class-method return.
- [ ] Existing state-transformer modules and examples remain source-compatible
      or receive an explicit migration note.
- [ ] `main` declares explicit `-> Unit`; bare `pub fn main(...)` is
      rejected and removed from official examples.
- [ ] The observer contract is explicit: `RngPort` samples, `MeasureSinkPort`
      emits, and the user/host consumes; no QPex function receives the sample.

## Impact inventory

| Area | Current behavior | Required decision/change |
|---|---|---|
| Grammar | `fn` has params and block only; no `->` | Add return annotation and final-expression form |
| AST | `FunDecl` stores name, params, body only | Store return type and distinguish constructor/main |
| Parser | Blocks contain binds/measure/snapshot only | Parse a terminal expression without reintroducing `return` |
| Typechecker | Method assignment checks are partial; no function result check | Infer/check function result and call arity/types |
| Runtime | Explicit terminal return is evaluated without collapse | Preserve result binding without implicit local leakage |
| Module linker | Collects and merges function bodies | Preserve return metadata and call resolution across imports |
| Physical rules | `measure` is terminal in `main` | Keep measure-free function boundary and add regression tests |
| QASM lowering | Primarily lowers executable `main` circuit | Define whether called pure functions inline, lower, or stay CPU-only |
| Tests | Existing methods rely on implicit last-bind convention | Add Red cases, then migrate compatibility cases deliberately |
| Documentation | Formal semantics says blocks are expressions, grammar does not | Synchronize grammar, language spec, and abstraction model |

## Non-goals

- No mid-program measurement or classical branching.
- No `return` keyword, early exit, exceptions, or classical escape from State.
- No generic trait `impl`, currying, pipeline semantics, or `until` in this
  issue; those remain LISS-0012 through LISS-0015.
- No QPU provider submission or new external dependency.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0021, ADR 0027, ADR 0037, ADR 0044, ADR 0054,
  ADR 0056, ADR 0058, proposed ADR 0064
- Related: LISS-0013 pipeline/currying, LISS-0014 trait `impl`, LISS-0015
  effect marking
- Blocks: expressive modular examples, future trait methods, and reliable
  function composition

## Adjudicator Decision Points

- [ ] Accept `-> Type` as the explicit return annotation spelling.
- [ ] Accept final-expression returns while retaining the ban on `return`.
- [ ] Reject omitted return annotations for all ordinary functions and methods;
      retain a compatibility window only in the implementation, not the
      language specification.
- [ ] Accept ADR-0064's explicit `main -> Unit` entry-point contract.
- [ ] Decide whether functions may return classical/domain values, or only
      `State<T>` and immutable product values.
- [ ] Define the QASM boundary for function calls whose bodies can be lowered.
- [ ] Approve Architecture Path design before Phase 1 Red tests.

## Context

- Included: `compiler/qpex/parser.py`, `ast_nodes.py`, `typecheck.py`,
  `runtime/evaluator.py`, `modules.py`, function/method tests, grammar,
  `docs/architecture/qpex-language-spec.md`,
  `docs/architecture/qpex-abstraction-model.md`, and language/semantics
  documents.
- Omitted: open LISS implementations, cloud/QPU submit, new numerical
  representations, and provider SDKs.
- Assumption: `measure` remains a terminal effect owned by `main`; a returned
  `State<T>` is not a measurement.
- Ambiguity boundary: exact return-type inference, classical/domain return
  policy, and QASM function inlining require Adjudicator decisions.

## AI Planning Records

### AIP-0021-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: XL
- Intended execution route: Architecture Path design/spec review, then
  Feature Path Phase 1 Red → Phase 2 Green → Phase 3 Refactor.
- Intended scope: function grammar/signatures, terminal-expression returns,
  type checking, runtime evaluation, module linking, tests, and docs.
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Token metric: N/A
- Estimation basis: cross-cutting language change with compatibility and QASM
  boundary decisions.
- Assumptions: no external dependency and one language semantics across Kernel
  generations.
- Confidence: medium until return-type and QASM decisions are accepted.
- Revises: none
- Revision reason: n/a
- Superseded by: none

## Verification

- Architecture review of this issue and the companion acceptance spec first.
- Phase 1 Red tests must fail before any production implementation.
- Existing full SV, QASM, module-link, and example suites must remain green
  after migration.

## Work Notes

- 2026-07-23: Phase 1 Red added acceptance tests for zero-argument returns,
  multi-argument State returns, class-method returns, and the measure-free
  boundary.
- 2026-07-23: Phase 2 Green implemented explicit `-> Type` metadata, terminal
  result expressions, typed result lookup, and runtime result binding. Legacy
  last-bind methods remain compatible; migration policy is still open.
- 2026-07-23: Phase 3 Refactor added the explicit-return idiom to the Quantum
  Observatory domain model and synchronized the teaching README. Assertions
  and terminal-measure semantics were unchanged.
