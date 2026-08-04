# LISS-0013: Pipeline and currying surface

## Metadata

- Local issue ID: LISS-0013
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path complete for the pipeline MVP boundary
- Type: language architecture
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Specify the reserved `|>` pipeline and currying/partial-application surface
for composable state transformers and future Operator Fusion.

## Acceptance Notes

- [x] Pipeline direction and associativity are normative.
- [ ] Call-chain and partial-application grammar is normative.
- [ ] State/classical type lifting and error cases are specified.
- [x] Purity, joint preservation, and Operator Fusion boundaries are specified.
- [x] Phase 1 Red cases are approved before implementation.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0021, ADR 0032
- Blocks: pipeline/currying implementation and fusion work
- Related: `staqex-ast-design.md`, `staqex-syntax-vocabulary.md`

## Adjudicator Decision Points

- [ ] Choose `lhs |> f` expansion and composition order.
- [ ] Decide whether currying is function-only or supports Operators.
- [ ] Decide whether partial application creates a first-class value.

## Context

- Included: `Pipe` AST placeholder, call chains, pure state transformers.
- Omitted: optimizer implementation and external provider IR.
- Assumptions: no classical escape from State values.

## AI Planning Records

### AIP-0013-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only until syntax is accepted.
- Intended scope: syntax and semantics specification.
- Estimation basis: grammar, type system, and optimizer boundary.
- Assumptions: existing `Pipe` node is provisional.
- Confidence: medium

## Verification

- Architecture examples first; parser/typechecker tests only after acceptance.

## Architecture design intake

### Recommended MVP semantics

- `lhs |> f` expands to `f(lhs)` and is left-associative:
  `x |> f |> g` means `g(f(x))`.
- The pipeline accepts named `fn` values and calls whose first parameter is
  compatible with the left-hand value. It does not introduce a new runtime
  loop or Host escape.
- Currying/partial application is function-only in the MVP. It produces an
  immutable first-class function value with the remaining parameter types;
  Operators are not silently treated as functions.
- State transformers preserve `State<T>` / Joint semantics. A pipeline cannot
  measure, consume RNG, mutate outer bindings, or call provider/Job APIs.
- Arity, type, effect, and missing-argument errors are hard diagnostics before
  lowering. Operator Fusion remains an optimizer concern, not pipeline
  semantics.

### Proposed examples for review

```staqex
state result = psi |> phase(theta) |> evolve_under(H, 1.0.s)
fn add_bias(x: State<Float>, bias: Float) -> State<Float> { ... }
let shifted = add_bias(0.5)
```

The examples are illustrative and do not authorize parser/runtime changes.

### Decisions required before Phase 1 Red

1. Confirm left-associative `lhs |> f` expansion and function-only MVP;
2. decide whether partial application uses `let` or a dedicated `curry` form;
3. define closure capture/effect restrictions;
4. define whether named `fn` references and method values share one callable
   type;
5. define diagnostics for arity/type/effect violations.

Architecture Approval is required before parser/typechecker tests are added.

## Architecture decision record

- [ADR 0080](../architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md) accepts
  left-associative State-preserving pipelines and function-only partial
  application.
- Phase 1 Red must lock the exact grammar, callable representation, closure
  restrictions, and stable diagnostics.

## Phase 1 Red record

- Added [`test_pipeline_currying_red.py`](../../tests/test_pipeline_currying_red.py).
- The Red contract covers left-associative `|>`, State-preserving stages,
  measurement/effect rejection, and rejection of implicit Operator-to-function
  conversion.
- Partial application is constrained to function values in this slice; its
  final `let`/`curry` spelling remains a follow-up grammar decision.

## Phase 2 Green record

- Reused the existing `Pipe` AST node and parser associativity; no new surface
  grammar was introduced.
- Implemented the minimal lowering `lhs |> f(args)` → `f(lhs, args)` for
  callable function calls, preserving left-to-right State/Joint evaluation.
- Added hard diagnostics `PIPE_EFFECT_ERROR` for terminal `measure` stages and
  `PIPE_CALLABLE_ERROR` for implicit Operator-to-function use or non-call
  right-hand sides.
- Runtime binding now applies the left-hand expression as the first function
  argument. General partial-application values, closure capture, and method
  value support remain deferred and are not part of this Green slice.

Verification: `python3 tests/test_pipeline_currying_red.py` passes; the next
phase is Refactor after review of the minimal callable boundary.

## Phase 3 Refactor record

- Extracted construction of the desugared call into dedicated helpers in the
  type checker and evaluator; pipeline binding and type checking now share the
  same explicit `lhs`-as-first-argument rule.
- No acceptance assertions or pipeline semantics were changed. Partial
  application values, closure capture, method values, and Operator Fusion
  remain deferred.

Reviewer empathy summary: a reviewer can now locate the surface lowering rule
in one helper per layer, while the surrounding pipeline branches read as
effect/callability checks rather than duplicated AST construction.

Verification: all standalone `tests/test_*.py` scripts, the pipeline Red
contract, spec verification (165/165), bytecode compilation, and
`git diff --check` pass.
