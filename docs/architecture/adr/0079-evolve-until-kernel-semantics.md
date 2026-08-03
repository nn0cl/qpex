# ADR 0079: Bounded pure `evolve ... until` Kernel semantics

## Status

Accepted (2026-07-24). This ADR accepts the semantic boundary only; grammar,
parser, evaluator, and QPU lowering require a later AT-TDD slice.

Companion: [LISS-0012](../documentation-compression-map.md).

## Decision

1. Kernel `evolve ... until` is a pure State-preserving repetition construct,
   distinct from Host workflow `until`.
2. Its predicate may inspect only current `State<T>`/joint-preserving values.
   `measure`, RNG, `Host<T>`, Job/Task, provider values, and mutation are not
   permitted.
3. The source form requires an explicit positive `max` bound. No implicit
   language-wide default is selected.
4. The predicate is evaluated after each pure evolution step and consumes no
   RNG. If it succeeds, the current State result is returned.
5. Reaching `max` before success produces hard diagnostic
   `EVOLVE_UNTIL_MAX_STEPS_ERROR`. The implementation must not silently return
   a partial state, collapse the state, or fall back to a Host loop.
6. The predicate must be deterministic over the current state and cannot
   mutate an outer binding.
7. Kernel compilation and static type checking accept the bounded construct
   independently of backend lowering. A QPU/OpenQASM emission request that
   cannot represent runtime repetition rejects explicitly with
   `E_QPU_UNSUPPORTED_CAPABILITY`; it must not make the language construct
   appear syntactically or semantically invalid, and it must not silently
   replace the repetition with a fixed circuit.

## Boundary

```text
Kernel evolve-until -> pure State-preserving repetition
Workflow until      -> completed JobResult projection / Host policy
```

The two constructs may use similar English vocabulary but have different
ownership, timing, and observation semantics.

## Consequences

Positive:

- Termination is explicit and bounded without weakening `Never Leave the State`.
- Nontermination is diagnosable and reproducible.
- Host workflow convergence cannot leak into Kernel execution.

Deferred:

- exact grammar and predicate vocabulary;
- static versus runtime validation of the `max` bound;
- QPU lowering and capability checks for bounded repetition;
- richer convergence/error reporting.

The QPU capability check belongs to the emission boundary. It is not a
compile/typecheck rejection for a program that is otherwise valid in the
Kernel lane.

## Enforcement

- No implicit sampling or measurement occurs during predicate evaluation.
- No classical `while`, unbounded loop, or Host fallback is introduced.
- Phase 1 Red must cover valid bounded repetition, forbidden effects, missing or
  invalid bounds, RNG preservation, and max-step diagnostics.
