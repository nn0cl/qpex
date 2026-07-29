# ADR 0018: Runtime values are `State<T>`; classical `T` only via lift or measure

## Status

Accepted (design baseline 2026-07-22; Architecture Path).
Follow-up design note: `docs/architecture/staqex-type-system.md`.

## Context

Design discussion introduced a two-layer picture (classical vs superposed).
Without a hard boundary, agents may reintroduce mid-program classical scalars
and classical short-circuit control, violating Never Leave the State and the
joint-store semantics (ADR 0013–0014, formal semantics sketch).

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **Object-language runtime values** bound by `state` are always of the form
   `State<T>` for some carrier `T`, and live as coordinates of one joint.
2. **Classical `T`** is not a mid-program first-class runtime island. It may
   appear as:
   - source literals / compile-time constants / type parameters that
     **lift** to $\delta_c : \mathsf{State}\langle T\rangle$;
   - results **after** terminal `measure` (host / sink / post-collapse binding).
3. **Operations** on `State<T>` (arithmetic, string concat, etc.) are
   pushforwards on the joint; they must not sample or short-circuit-discard.
4. **MVP Kernel** implements `State<Int>` with `+`, `-`, `*` only.
   `State<String>` concat and richer ops are design-accepted but out of Kernel
   PoC A/B until fixtures exist.
5. **Deferred:** `/`, `%`, bitwise, `Float` analytics, short-circuit boolean
   connectives — require a later ADR or explicit semantics section.

## Consequences

Positive:

- One evaluation ontology: $\mathsf{Joint}\to\mathsf{Joint}$.
- Clear story for researchers: labels and numbers are basis atoms under
  superposition until `measure`.

Negative:

- Rich classical-style typing UX must be sugar over `State<T>`.
- Open carriers (`String`, `Float`) need finite-support discipline in
  implementations.

## Enforcement

Code review / design review should reject:

- Runtime classical binders used to drive control before `measure`.
- Ops that collapse or independently resample operands.
- Kernel scope creep into `/` or `Float` without ADR.
- Docs that claim “classical layer” as a parallel live store during
  uncollapsed execution.
