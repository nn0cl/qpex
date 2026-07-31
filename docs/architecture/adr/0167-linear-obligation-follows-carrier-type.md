# ADR 0167: Linear obligation follows the carrier type, not the binding keyword

## Status

**Accepted** (2026-08-01) — Adjudicator ruling during the WP-0069 operations
review. Amends the ADR 0114 linear lineage; supersedes nothing.
Implements [LISS-0202](../../issues/LISS-0202-linear-discipline-regression-cluster.md).

## Context

Staqex enforces a linear discipline on quantum resources: a value that carries
quantum state must be measured or uncomputed, never silently dropped. Dropping
one is physically a partial trace, and permitting it silently would put a hole
in Never Leave the State.

`compiler/staqex/hir.py` already carried the correct predicate:

```python
def is_linear_carrier_ty(ty: Ty) -> bool:
    if ty.kind == "State":
        return True
    return ty.kind == "Object" and ty.payload == "DensityState"
```

but `_stmt_binds_state` never reached it for the common case. It decided the
obligation from **syntax**:

```python
if stmt.via_state_keyword:
    if isinstance(stmt.expr, Inspect):
        return False
    return True
```

so any `state x = …` binding was a linear quantum resource regardless of what
`x` actually held. The in-code comment records why — `fn`-local names are absent
from `TypeChecker.env` after `check_unit`, so the keyword was used as a stand-in
for type information that was believed unavailable.

The consequence was a category error, reproduced 2026-08-01:

| Source | Inferred type | Reported |
|---|---|---|
| `state overlap = ⟨0\|1⟩` | `Classical<Float>` | "quantum state `overlap` is discarded" |
| `state m = ⟨0\|X\|1⟩` | `Classical<Float>` | "quantum state `m` is discarded" |
| `state a = adjoint(X)` | `Operator<Qubit>` | "quantum state `a` is discarded" |

An inner product is a complex amplitude and a matrix element is a number:
there is nothing to collapse, so demanding `measure` is meaningless. An
operator is a classical description of a transformation, freely copyable, and
outside what no-cloning restricts.

The type information was in fact available. `TypeChecker.typed`
(`id(expr) → Ty`, written by every `_infer` call) covers `fn`-local bindings,
and `build_hir` already passed it into the HIR as `HirModule.typed`.

## Dependency Adoption Evidence

Not applicable. No dependency is selected.

## Decision

1. **The carrier type decides the linear obligation.** Only `State` and
   `DensityState` carry one. `Classical`, `Operator`, `Register`, `Param`,
   `Struct` and every other kind do not.

2. **A declared Type-First head is the authoritative carrier evidence.**
   `State<T> x = …` / `DensityState x = …` carry an obligation; a declared
   `Operator`, `Classical` or register head does not.

3. **Raw expression inference is consulted only for inference-only `state x = …`
   binds, and never overrides a declaration.** Some builtin calls infer
   coarsely — `qft(reg)` infers `State` while it is declared and used as
   `Operator` — so inference is a fallback, not the primary oracle.

4. **The `state` keyword remains the last-resort fallback** when neither a
   declaration nor an inferred type is available. It is no longer the first
   test.

5. **Bras keep their linear obligation.** `⟨ψ|` is the adjoint of `|ψ⟩` — the
   same physical resource viewed dually — and ADR 0087 types both operands of
   `inner` as `State<V>`. Exempting bras would let
   `state escape = adjoint(psi)` discharge nothing while `psi`'s register is
   still live. `⟨0|` is a basis-label constant exactly as `|0⟩` is, and `|0⟩`
   uncontroversially carries an obligation.

6. **`inspect` still yields a non-destructive view** and binds no obligation
   (LISS-0114 Slice E, unchanged).

## Consequences

Positive:

- Scalars and operators stop being reported as discarded quantum state.
- The obligation is now derived from the type system rather than from a
  syntactic proxy, so it stays correct as the surface grows.
- `fn`-local coverage is preserved: `HirModule.typed` reaches inside `fn`
  bodies where `TypeChecker.env` does not.

Negative:

- Correctness now depends on inference quality for inference-only binds. The
  `qft(reg) → State` mis-inference is real and is why declarations win; it is
  worth its own Issue.
- Suites that bound a genuine `State` and never discharged it were passing only
  because the diagnostic was noisy in a different direction; they now have to
  state their intent.

Measured on the full suite: 174 → 176 passing, 50 → 48 failing, no suite that
passed before now fails.

## Enforcement

Code review should reject:

- A new linear decision keyed on the `state` keyword, a binding form, or any
  other syntax rather than on the carrier type.
- Exempting `State` or `DensityState` from the obligation to widen what
  compiles.
- Treating `Classical` or `Operator` as a linear resource.
- Using raw `typed` inference to override a declared Type-First head.
