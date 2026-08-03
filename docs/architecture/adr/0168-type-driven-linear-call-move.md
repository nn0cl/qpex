# ADR 0168: Type-driven linear move on transforming Calls

## Status

**Accepted** (2026-08-01) — Adjudicator Wave 1 of WP-0073 / plan confirmation.
Amends the LISS-0133 residual that treated most builtins as non-moving.
Implements [LISS-0221](../documentation-compression-map.md);
unblocks the residual of [LISS-0202](../../issues/LISS-0202-linear-discipline-regression-cluster.md).

## Context

After ADR 0167, the linear obligation follows the carrier type (`State` /
`DensityState`). Consumption of Call arguments was still mostly a hand-kept
table: user `fn` names plus `_CONSUMING_BUILTINS = {"apply", "hadamard"}`.
LISS-0133 had left other builtins non-moving, so

```
DensityState evolved = lindblad(rho, H, jumps, t)
measure evolved
```

still reported `LINEAR_IMPLICIT_DISCARD` on `rho` even though the
transformation already consumed that carrier.

Same-name rebinds such as `State q = hadamard(q)` without a later `measure`
were also under-reporting discard: the call consumed the root and the rebind
reused that root, so the new value was born already-consumed and no discard
fired.

## Dependency Adoption Evidence

Not applicable. No dependency is selected.

## Decision

1. **A Call whose result is a linear carrier moves the linear carriers among
   its arguments.** Result evidence is `HirModule.typed[id(call)]` when
   present; otherwise a Type-First `State` / `DensityState` bind whose RHS is
   that Call. This retires `_CONSUMING_BUILTINS`.

2. **Classical-result Calls do not move.** `expect`, `inner`, and other Calls
   whose result is not a linear carrier leave argument obligations live
   (non-destructive read). `inspect` remains a use-not-transform path
   (LISS-0114 Slice E, unchanged).

3. **Same-name rebind opens a fresh obligation.** After a transforming Call
   consumes the old root of `Name`, binding `Name = …` re-introduces `Name`
   and clears it from `consumed` so the new value is a live obligation until
   `measure` / uncompute. Multi-wire in-place `apply` revive (LISS-0228)
   remains compatible.

4. **User `fn` Calls continue to move** when they are in the move-name set
   (return / argument transport), independently of this builtin rule.

## Consequences

Positive:

- Density / Lindblad transforms discharge their input carriers.
- Gate rebinds correctly require a later discharge of the *new* value.
- The rule scales with new builtins without a per-name table.

Negative:

- Programs that reuse a carrier after a transforming Call become
  `LINEAR_DUPLICATE_USE` (correct). Sample/test programs that double-used a
  density root must be repaired without weakening assertions.
- Correctness still depends on result-type evidence for inference-only binds;
  Type-First heads remain the fallback (ADR 0167).

## Enforcement

Code review should reject:

- Reintroducing a hard-coded builtin consume table as the primary rule.
- Treating Classical-result Calls as moves.
- Same-name rebind that leaves the new value already-consumed with no path
  to emit `LINEAR_IMPLICIT_DISCARD`.
- Editing assertions solely to silence linear diagnostics.
