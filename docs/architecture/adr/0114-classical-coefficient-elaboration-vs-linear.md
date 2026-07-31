# ADR 0114: Classical coefficient elaboration vs linear quantum resources

## Status

**Accepted** (Adjudicator, 2026-07-31).

Architecture approval only. **Not** Phase 1 / implementation authorization —
execute via [LISS-0121](../../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md)
after explicit phase approval.

## Context

Staqex is a language **for physicists**. When physicist spelling and programmer
convenience conflict, the physicist mental model wins
([physicist-dx-harmony](../physicist-dx-harmony.md); ADR 0095).

ADR 0096 / LISS-0053 already require **named coefficients** in binder bodies
(e.g. `Float J = 1.0` then `J * Z[i] * Z[next(i)]`) to resolve like literals.
Probes on 2026-07-31 show that spelling still fails with
`LINEAR_IMPLICIT_DISCARD` on `J`, while literal `1.0 * Z[i] * …` works.

Root cause (Kernel evidence, not speculation):

1. Literals lift to `State<…>` (axioms / typecheck `LitFloat` → `Ty("State","Float")`).
2. Type-First `Float J = 1.0` is stored in the type environment as a **State**
   carrier and asserted as state.
3. Linear analysis (`hir.is_linear_carrier_ty`) treats every `State` as a
   linear quantum resource.
4. Using `J` only inside an `Operator` tree does not count as measure/uncompute
   consumption → false `LINEAR_IMPLICIT_DISCARD`.
5. Separately, Operator/Hamiltonian elaboration must substitute coefficient
   names like compile-time constants (evaluator already has a partial
   “Type-First classical scalars for H coefficients” path).

So this is a **bug / boundary misclassification**, not an open philosopher’s
conflict — **provided** the fix does not let programmers misread classical
coefficients as mid-program classical *control islands*, or treat quantum
`State<Float>` as free classical ALU.

Adjudicator constraint (2026-07-31): fix is welcome only with a
programmer-non-misrecognition condition analogous to C language design —
after preprocessor / constant folding / optimization, expanded constants must
still be well-defined and must not introduce surprising errors or silent
semantic changes.

Related friction rows: F-02, F-05 in
[physicist-source-friction-ledger.md](../physicist-source-friction-ledger.md).
Prior acceptance intent: [LISS-0053](../../issues/LISS-0053-binder-composition-and-honest-deferral.md)
named-scalar bullet (still must hold under LINEAR).

## Decision

### D1 — Two coefficient roles (normative distinction)

| Role | Surface cue | Ontology | LINEAR? |
|---|---|---|---|
| **Elaboration coefficient** | Type-First quantity (`Float`, dimful Type-First) used **only** as Operator / binder coefficient / theory parameter pack field feeding Operator AST | Compile-time / elaboration scalar (Classical-kind or equivalent elaboration carrier) | **No** |
| **Quantum float state** | `state` binding or inferred `State<Float>` used as Joint coordinate | Linear quantum resource | **Yes** |

Physicist priority: `Float J = …` in Hamiltonian formulas is the **elaboration
coefficient** role by default when the name’s uses are confined to Operator
elaboration. Programmers must not invent a third “secret classical store” for
`if` / short-circuit control (still forbidden; F-01).

### D2 — Elaboration-after-fold invariant (C analogy)

At every stage after which a coefficient may be substituted or folded —

1. parse / typecheck  
2. binder expansion / Operator tree rewrite  
3. Hamiltonian / Suzuki / QASM lowering  
4. any future optimization that constant-folds coefficients  

— the following must hold:

1. **Semantic identity:** a program using named coefficient `J` has the same
   Operator meaning as the program with `J` textually replaced by its
   elaboration value (for closed, pure coefficient expressions).
2. **Diagnostic honesty:** that substitution must not create a new false
   `LINEAR_*` on the coefficient name, nor silence a true LINEAR error on a
   quantum `state`.
3. **No classical-control smuggling:** elaboration coefficients must not become
   mid-program branch predicates or short-circuit conditions.
4. **Fail-closed on open coefficients:** if a name cannot be elaborated to a
   closed coefficient (depends on unmeasured quantum state, host I/O, etc.),
   emit an explicit diagnostic — never silently treat it as `0` or drop terms.

This is the Staqex analogue of “after the C preprocessor expands a macro /
after const folding, the program remains well-defined and does not spuriously
error.”

### D3 — Programmer recognition rules (must be teachable)

Document in harmony / QUICKSTART / diagnostics text:

- **Write couplings as Type-First quantities** (`Float J = 1.0`, struct fields)
  and use them in `Operator` formulas — that is the physicist spelling.
- **Do not** use `state j = …` for a coupling constant; `state` means Joint
  quantum (or probabilistic) resource and is LINEAR.
- **`inspect` / `measure` on a coupling** is a programmer smell: couplings are
  not measurement subjects (align ADR 0053: cannot measure classical value).
- Diagnostics should say **coefficient** vs **quantum state** explicitly when
  misused (e.g. `COEFFICIENT_IN_QUANTUM_POSITION` / reuse existing codes where
  accurate).

### D4 — Struct / field sugar (same decision family)

`params.h_x * X` and `Float hx = params.h_x; … hx * X` must obey D1–D2.
Field projection used as elaboration coefficient is not LINEAR discard of a
quantum resource. Parse/`Attr` in Operator position is in scope for the
implementing Issue (may slice after scalar names if needed, but same ADR).

### D5 — Out of scope

- Restoring classical `if` / `&&`.
- User operator overloading.
- Changing axiom “literals denote distributions” for Joint evaluation of
  `state` values — only the **Operator elaboration** boundary is refined.
- Showcase / LISS-0120 reclaim.

## Consequences

Positive:

- Paper Hamiltonians with named `J`, `h`, struct couplings become honest again.
- LINEAR remains strict for true quantum resources.
- Programmer/physicist boundary is named, not vibes.

Negative / residual risk:

- Agents may over-widen “Classical” and reintroduce classical islands —
  mitigated by D2.3 and forbidden-keyword surface.
- Dimensional Type-First coefficients need the same elaboration path as
  dimensionless `Float`.

## Verification

- Named `J` in binder body: no `LINEAR_IMPLICIT_DISCARD`; run/QASM match literal
  coefficient program (revive LISS-0053 acceptance).
- `state j = dirac(1.0)` (or equivalent State float) still LINEAR if discarded.
- After binder expansion, diagnostics unchanged under coefficient fold (D2).
- Negative: coefficient used as `when` control / measure subject → explicit error.
- Probe suite recorded in friction ledger F-02/F-05.

## Issue

Implementation: [LISS-0121](../../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md)
(after this ADR is Accepted).
