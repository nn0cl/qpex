# ADR 0095: Design horizon — ideal form first, not shortest working path

## Status

Accepted (Adjudicator, 2026-07-26).

## Context

Staqex's documents are written in the vocabulary of incremental delivery: the
word "MVP" appears across ~78 files, slices are scoped as "the first
accepted boundary", and deferrals are recorded as "remains deferred". That
vocabulary is a faithful record of how the project was built, but it does
not state what the project is *aiming at*, and agents have been reading it
as if shortest-path-to-working were the goal.

It is not. The Adjudicator's stated intent (2026-07-26) is that Staqex is a
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

The observable effect is that the single most canonical many-body
Hamiltonian cannot be written at all, and that the notation for "Pauli on
site k" depends on syntactic context. That is what prompted this ADR.

### Correction to this ADR's original evidence

The table above was originally presented as "the accumulated cost of
optimizing each decision for shortest-path rather than for the final form".
On re-examination (2026-07-26, prompted by the Adjudicator asking whether
some findings were bugs being over-read) **that framing overstated the
case**, and the table is corrected here rather than left standing:

| Row | Actually |
|---|---|
| binder lowering not executable | **Bug.** [ADR 0088](0088-finite-binder-lowering.md) Decision 3 already promises "a concrete Pauli `Operator` tree suitable for the existing Hamiltonian/Suzuki path"; the implementation produces an inspection `dict` and leaves the bound AST as `OpBinder`. The spec was not followed. |
| `sum {...} + sum {...}` silent | **Bug.** Named nowhere — not in ADR 0088's decisions and not in its deferred list. The lowering pass only inspects a top-level binder. |
| named coefficient `J *` rejected | **Bug.** ADR 0088 Decision 3 writes `coefficient * Pauli[i] * Pauli[next(i)]` without restricting *coefficient* to a literal, and `J * Z(0) * Z(1)` is accepted outside a binder. |
| `Z[k]` failing outside a binder | **Bug.** `compile_sparse_pauli` has no `OpIndexed` handler; nothing decided against it. |
| `product` silent | **Documented deferral** — `product` is named in ADR 0088's deferred list. Only its *expression* is defective: it is silent rather than diagnosed. |
| Heisenberg (`+` in body) | **Documented deferral**, ADR 0088 Decision 3 restricts the body to a Pauli nearest-neighbour term. The design-level observation that the accepted scope was too narrow to write canonical models does stand. |
| `Z(k)` vs `Z[k]` as *which is canonical* | **Genuine design gap.** A real decision, unmade. |

So the table mixed four implementation bugs, two documented deferrals, and
one genuine design gap. Bugs are not evidence about design philosophy, and
presenting them as such both overstated this ADR's argument and obscured
defects that should simply have been fixed. Decision 6 below exists so this
does not recur.

This correction does **not** weaken the decision itself: the design horizon
recorded here is the Adjudicator's stated intent for the project, which
stands independently of how well the original evidence supported it. The
genuinely design-level findings — an accepted scope too narrow for canonical
models, an unmade notation decision, and (found later, during
[ADR 0096](0096-indexed-operator-and-binder-surface.md)) the total absence of
multi-index and constrained sums — remain valid motivation.

## Decision

The design horizon for Staqex is the **ideal final form of the language**, not
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

6. **Classify evidence before using it as design evidence.** A finding that
   a program does not work is, before anything else, one of three different
   things, and they call for different responses:

   | Kind | Test | Response |
   |---|---|---|
   | **Implementation bug** | An accepted ADR/spec already promises this behaviour, or nothing anywhere decided against it | Fix it. It is not evidence about design philosophy. |
   | **Documented deferral** | A deferred list explicitly names it | The deferral may be legitimate; check only whether it is *expressed* honestly (a diagnostic, not silence) |
   | **Genuine design gap** | No document decided it either way, and the ideal form requires it | Design it — this is the evidence that belongs in an ADR |

   Marshalling bugs as evidence for a design principle does two kinds of
   harm: it overstates the argument, and it hides a defect that should
   simply have been fixed. This rule was added retroactively after the
   evidence table in this ADR's own Context was found to mix all three
   kinds; see "Correction to this ADR's original evidence" below.

### How to read existing "MVP" language

The ~78 files using "MVP", "first slice", and "remains deferred" are **not**
retroactively invalidated and are **not** to be mass-edited: they are an
accurate historical record of what was built when, and rewriting them would
produce a large, risky diff with no behavioral value.

Read them as *historical scope*, never as *target end-state*. When an
existing document says a capability is "deferred", that records where the
implementation stopped — it does not assert that stopping there was the
intended final design. Where this ADR and an older "MVP" framing appear to
disagree about what Staqex should eventually be, this ADR governs.

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
