# ADR 0095: Design horizon — ideal form first, not shortest working path

## Status

Accepted (Adjudicator, 2026-07-26).

## Context

QPex's documents are written in the vocabulary of incremental delivery: the
word "MVP" appears across ~78 files, slices are scoped as "the first
accepted boundary", and deferrals are recorded as "remains deferred". That
vocabulary is a faithful record of how the project was built, but it does
not state what the project is *aiming at*, and agents have been reading it
as if shortest-path-to-working were the goal.

It is not. The Adjudicator's stated intent (2026-07-26) is that QPex is a
language for **generalized quantum computers on a hundred-year horizon**.
The target is the correct final form of the language, judged the way
engineers judge a language as well-made: the notation expresses the
physicist's *experiment* directly, rather than the machine's convenience,
and it is internally consistent enough that learning one part predicts the
rest.

A concrete measurement prompted this. Probing the accepted finite-binder
surface (LISS-0030/LISS-0043) against the Hamiltonians physicists actually
write found:

| Written form | Result |
|---|---|
| `sum (i in ...) { -1.0 * Z[i] * Z[next(i)] }` | lowers, but is **not executable** — `run` and `emit-qasm` both fail with `cannot compile sparse Pauli for OpBinder` |
| `sum (i in ...) { X[i]*X[next(i)] + Y[i]*Y[next(i)] }` (Heisenberg) | `BINDER_DOMAIN_ERROR` — `+` rejected inside a binder body |
| `sum (i in ...) { J * Z[i] * Z[next(i)] }` (named coefficient) | `BINDER_DOMAIN_ERROR` — scalar variable rejected, though `J * Z(0) * Z(1)` is fine outside a binder |
| `sum {...} + sum {...}` (full transverse-field Ising) | **silently produces no lowering**, no diagnostic |
| `product (i in ...) { ... }` | **silently produces no lowering**, no diagnostic |
| `Z(k)` vs `Z[k]` | two notations for one concept; `Z(k)` works only outside a binder, `Z[k]` only inside — neither works in both |

Every one of these is individually defensible as "a first slice". Together
they describe a language in which the single most canonical many-body
Hamiltonian cannot be written at all, and in which the notation for
"Pauli on site k" depends on syntactic context. That is the accumulated
cost of optimizing each decision for shortest-path rather than for the
final form.

## Decision

The design horizon for QPex is the **ideal final form of the language**, not
the shortest path to something that runs. This is a project-level design
principle and applies to every agent and human working on the language
surface, semantics, and diagnostics.

Operationally, when scoping or reviewing any language-affecting change:

1. **The scoping question is not "what is the least that works" but "what
   is the correct final design, and is this slice a faithful step toward
   it?"** A slice that works but points away from the intended final form
   is rejected, not accepted-and-revisited.

2. **A deferral is acceptable only when adopting the deferred thing later
   does not require a breaking change.** If choosing to defer now would
   force a migration, a re-spelling, or a compatibility alias later, decide
   it now instead. Cost of deciding now is paid once; cost of deciding
   wrong is paid by every program written in between.

3. **Surface and notation decisions are settled early and correctly**,
   because they accrue legacy fastest. Two spellings of one concept, or a
   spelling whose validity depends on syntactic context, is a defect
   regardless of whether each spelling individually works.

4. **"It runs" is not acceptance.** The acceptance question is whether this
   is the form the project would still choose with unlimited implementation
   budget. If not, record why the difference is acceptable — do not let the
   gap go unrecorded.

5. **Machine convenience never shapes the surface.** Term counts, circuit
   depth, compile time, and simulation cost are never grounds to restrict
   what a physicist may write. This generalizes the decision already
   recorded in [ADR 0093](0093-jordan-wigner-numerical-mapping.md) §4 for
   two-body fermionic terms, and in
   [ADR 0094](0094-explicit-trotter-step-policy.md) for Trotter step
   policy. Optimization is separate, later work.

### How to read existing "MVP" language

The ~78 files using "MVP", "first slice", and "remains deferred" are **not**
retroactively invalidated and are **not** to be mass-edited: they are an
accurate historical record of what was built when, and rewriting them would
produce a large, risky diff with no behavioral value.

Read them as *historical scope*, never as *target end-state*. When an
existing document says a capability is "deferred", that records where the
implementation stopped — it does not assert that stopping there was the
intended final design. Where this ADR and an older "MVP" framing appear to
disagree about what QPex should eventually be, this ADR governs.

### Relationship to Phase 2 Green

`AGENTS.md` and `CLAUDE.md` both instruct, under Phase 2 Green: "Write the
smallest implementation that satisfies reviewed tests." That instruction is
unchanged and does not conflict with this ADR. The two operate at different
levels:

- **Phase 2 Green** governs implementation *within* an already-approved
  slice: do not gold-plate, do not add speculative machinery, write the
  least code that satisfies the reviewed Red tests.
- **This ADR** governs how a slice is *chosen and designed* in the first
  place: aim the slice at the correct final form rather than at the
  smallest thing that could work.

Minimal implementation of a well-aimed slice is correct. Minimal *ambition*
in choosing the slice is what this ADR rejects.

## Consequences

Positive:

- Language-surface decisions get made once, correctly, instead of
  accumulating spellings and special cases that later need migration.
- Deferral becomes an explicit judgment ("this can be added without
  breaking anything") rather than a default.
- Silent partial support — a construct that compiles but does nothing, as
  `sum {...} + sum {...}` and `product` currently do — is recognizable as a
  defect against the stated horizon, not as an acceptable intermediate
  state.

Negative:

- Slices become larger and slower to land. Design review before Phase 1 Red
  carries more weight, and more decisions must be made before the first
  test is written.
- Some already-shipped surfaces will be found to point away from the ideal
  form and will need rework that pure shortest-path development would have
  avoided. The binder surface measured above is the first such case.
- "Correct final form" is a judgment, not a test. It cannot be enforced by
  CI, and it will occasionally be wrong; the mitigation is that Decision 4
  requires the gap to be recorded rather than silently accepted.

## Verification contract

This ADR governs design review, not runtime behavior, so it has no test
assertions. Its observable effects are:

- A design intake or Issue that defers a capability states, explicitly,
  whether adopting it later would be a breaking change (Decision 2).
- A change introducing a second spelling of an existing concept, or a
  context-dependent spelling, is rejected in review (Decision 3).
- A resource or performance limit proposed as a constraint on what may be
  written is rejected, and re-proposed as separate optimization work if it
  is genuinely needed (Decision 5).
