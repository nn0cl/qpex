# ADR 0030: `inspect` — non-destructive debug (not measure)

## Status

Accepted (2026-07-23).

Companions: `staqex-language-spec.md` §5.5, ADR 0029 (`snapshot` / sinks),
formal §9 / §9b.

## Context

Debugging a superposition requires seeing the full PMF / amplitude table.
Using `measure` for that would collapse the joint and make further evolution
useless. Engineers need a printf-like probe that does not leave the state.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. Normative debug probe is **`inspect`** (method or free function).
   Optional label: `e.inspect("msg")` / `inspect(e, "msg")`.
2. **Denotation on the joint:** identity — returns the same `State` / joint
   coordinates; **no** `RngPort`; **no** Dirac collapse.
3. **Host effect:** format the in-memory distribution / amplitude
   representation (support → mass or complex amplitude) to a debug sink
   (stderr / IDE / log). This is a read of the simulator’s data structure,
   analogous to reading classical memory in a debugger.
4. **Host text ≠ object-language value.** The rendered line is a **host
   `String` / log bytes** only. It is **not** a Staqex `State<String>` and must
   **not** re-enter the joint / computation graph. Universal `State<T>`
   (no mid-program scalars) is therefore compatible with rich debug UX.
5. **Unified display:** Dirac and mixtures use one format family, e.g.
   - Dirac: `State<Int> { |10⟩ (prob: 1.0) }`
   - Mixture: `State<Int> { |100⟩ : 50.0%, |200⟩ : 50.0% }`  
   Exact glyphs / precision are styler-configurable; narrative ket/`prob`
   style is the default design target.
6. **`inspect` ≠ `measure`.** Equating them is a language-law violation.
7. **`inspect` vs `snapshot`:** both are non-collapsing. Prefer **`inspect`**
   for interactive debug / labeled console; **`snapshot`** for evolve
   checkpoint files (ADR 0029). Implementations may share one
   `InspectSinkPort` / distribution-mode sink.
8. AST: `Inspect { expr, label? }` (Expr form that yields the same typed
   value — passthrough). May appear mid-`main` / inside `evolve`.
9. Stripping `inspect` in release builds must preserve denotation (optional
   optimizer); must not change measure outcomes under the same RNG stream.

## Consequences

Positive:

- Safe debugging of mixtures without Early Collapse.
- Clear triple: measure / snapshot / inspect.

Negative:

- Host logging is still a side effect (ordering / timing); not part of the
  mathematical Joint→Joint arrow except as identity + optional trace.

## Enforcement

Reject tutorials that use `measure` “just to print the distribution,” or that
treat inspect output as a `State` value fed back into arithmetic. Prefer
`inspect` for PMF visibility.
