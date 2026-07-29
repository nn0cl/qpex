# ADR 0097: Numeric representation horizon — `f64` is provisional, not permanent

## Status

**Proposed.** Split out of [ADR 0096](0096-indexed-operator-and-binder-surface.md)
during its design review (2026-07-26), because the question is independent of
the binder/indexed-operator surface and must not block it.

This ADR does **not** change any runtime behaviour. It records a horizon
decision and a constraint on future work. [ADR 0076](0076-numeric-representation-policy.md)
remains in force for everything it currently decides.

## Context

[ADR 0076](0076-numeric-representation-policy.md) decided that the Kernel's
runtime numeric representation is `f64` for real scalars and probabilities
and complex pairs of `f64` for amplitudes and finite matrices, that "exact
rational arithmetic is not a Kernel runtime mode", and that tolerances are
per-contract (`1e-9` for probability normalisation, `1e-12` for density
trace/positivity, Kraus and POVM completeness, Lindblad trace guard) and
never authorise silent normalisation or repair.

[ADR 0095](0095-design-horizon-ideal-form-first.md) then established that
Staqex targets the ideal final form of the language on a hundred-year horizon.
That raises a question ADR 0076 did not answer: **is `f64` the permanent
answer, or a provisional one?**

The design review that produced this split established three things that
narrow the question:

1. **Exact rationals would not make Staqex exact.** The coefficients that
   dominate quantum computing are $1/\sqrt{2}$, $e^{i\theta}$, Trotter time
   steps, and molecular integrals $h_{pq}$. Rationals capture $1/2$ and
   little else that matters. "Rationals instead of `f64`" is not the shape
   of a correct answer.
2. **Frontend representation and Kernel execution representation are
   different axes.** A language can carry exact or symbolic values in its
   front end and lower them to `f64` at the point of state-vector or QPU
   execution. ADR 0076's "no exact rationals as a Kernel runtime mode" does
   not, by itself, forbid exact values earlier in the pipeline. Both
   positions in the review had partly conflated these.
3. **Exact commutativity checking does not require exact coefficients.**
   Commutation of Pauli words and similar operator structures is decidable
   symbolically from operator structure, independently of how coefficients
   are represented.

## Decision

1. **`f64` remains the Kernel's concrete runtime representation.** No change
   to ADR 0076's decisions 1–6.

2. **`f64` is recorded as provisional, not as the permanent answer for every
   future language layer.** A future exact, arbitrary-precision, or symbolic
   layer is anticipated and is not foreclosed by ADR 0076.

3. **The coefficient type is not genericised now.** No generic numeric
   trait, no type parameter over coefficients, no rational implementation is
   added in anticipation. Reasons:

   - It is speculative abstraction, which the project's own Phase 2 Green
     rule forbids ("no speculative machinery").
   - The shape the abstraction would need is genuinely unknown. Candidates
     include arbitrary-precision floats, algebraic numbers, parameterised
     angles, symbolic expressions, interval arithmetic, and
     measurement-derived uncertainties. A premature "numeric type `T`" is
     unlikely to express the expression simplification, precision tracking,
     explicit degradation, and backend-capability checking a real answer
     needs.

4. **What is required now instead is that the `f64` boundary be explicit and
   documented.** It is not sufficient merely to keep `f64` out of surface
   semantics: literal parsing and rounding, constant folding, equality
   comparison, and serialisation are all observable, and a later change to
   any of them would change the meaning of existing programs. Therefore:

   - The point at which a source literal or a computed coefficient becomes
     `f64` is a documented boundary, not an implementation accident.
   - Rounding rules at that boundary are documented.
   - Literal parsing, constant folding, coefficient serialisation, and
     lowering into the Kernel stay separable rather than intermixed, so a
     future layer can be inserted at the boundary instead of threaded
     through everything.

5. **Any future numeric mode is additive and explicit.** Introducing one
   must not silently change the rounding behaviour of existing `f64` code.
   It arrives behind an explicit type, mode, or conversion boundary. This is
   what keeps this deferral legitimate under ADR 0095 Decision 2.

## Non-goals

- No change to any tolerance value or to the "validate, never repair"
  posture of ADR 0076 Decision 3.
- No selection of a specific future numeric tower, precision policy, or
  dependency. That is the subject of a future ADR, when there is a concrete
  requirement to design against.
- No new dependency (`NumPy`/`SciPy` remain non-required, per ADR 0076
  Decision 1).

## Consequences

Positive:

- Removes the standing ambiguity about whether `f64` is a permanent
  commitment, without paying for an abstraction whose shape is unknown.
- Documenting the `f64` conversion boundary and rounding rules is useful
  immediately — it is the part of this question that is observable today.
- Keeps the binder/indexed-operator work (ADR 0096) unblocked.

Negative:

- Records an intention without implementing it, which carries the usual risk
  that the intention is not honoured when the time comes. The mitigation is
  Decision 4: the boundary work is concrete and checkable now, so the future
  insertion point exists in the code rather than only in this document.
- Programs written against `f64` semantics in the meantime may need review
  if an exact layer is later adopted, even though Decision 5 forbids silently
  changing their behaviour.

## Verification contract

This ADR governs design review and documentation, not runtime behaviour, so
it has no behavioural test assertions. Its observable effects are:

- A proposal to genericise the coefficient type, or to add a rational or
  symbolic numeric mode, is rejected in review unless it comes with the
  concrete requirement and semantics ADR 0076/0097 say such a change needs.
- The `f64` conversion boundary and its rounding rules are documented where
  literal parsing and Kernel lowering meet.
- A future numeric mode arrives behind an explicit type, mode, or conversion
  boundary, and existing `f64` results are unchanged by its introduction.
