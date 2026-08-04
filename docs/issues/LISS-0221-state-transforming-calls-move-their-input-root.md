# LISS-0221: State-transforming calls must move their input root

## Metadata

- Local issue ID: LISS-0221
- Status: **complete** — 2026-08-01 (WP-0073 Wave 1)
- Phase: phase-3-refactor
- Type: bug
- Priority: P1
- Planning size: M
- Program: [WP-0073](../work-plans/WP-0073-linear-transform-move.md)
- Related: [ADR 0168](../architecture/decision-themes/dec-0002-state-first-semantics-and-measurement.md);
  [ADR 0167](../architecture/decision-themes/dec-0002-state-first-semantics-and-measurement.md);
  LISS-0133 (amended); LISS-0114 lineage
- Unblocks: residual of [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Adjudicator ruling (2026-08-01)

**A transformation consumes what it transforms.** After

```
DensityState<Qubit> evolved = lindblad(rho, H, jumps, t)
measure evolved
```

the old `rho` no longer exists; its linear obligation transports to `evolved`.
Today `rho` is reported as `LINEAR_IMPLICIT_DISCARD`, because LISS-0133 decided
that builtin calls do not move quantum arguments.

The chosen rule is type-driven rather than a hand-kept builtin table: **a call
whose result is a linear carrier moves the linear carriers among its
arguments.** `expect` and `inner` return a `Classical` scalar, so they keep
leaving their argument live and still requiring discharge — the existing
non-destructive-read behavior is unchanged.

This subsumes the current hard-coded `_CONSUMING_BUILTINS = {"apply",
"hadamard"}` in `compiler/staqex/hir.py`.

## Why this is not a local edit — two blockers found 2026-08-01

A direct implementation was attempted and **reverted**; it moved the suite from
193/32 to 190/35 while still not discharging `rho`. Two obstacles:

**1. `TypeChecker.typed` does not cover the density path.** For

```
DensityState<Qubit> rho = DensityState(Ensemble([(1.0, |0>)]))
DensityState<Qubit> evolved = lindblad(rho, H, jumps, t)
```

`typed[id(expr)]` is `None` for *both* `Call` nodes — the density binding has
its own checker path that never records an inferred type. So the result type
is unavailable exactly where the rule needs it. (The linear obligation itself
still lands correctly, via the declared Type-First head — ADR 0167 decision 2.)

Using the *binding's* declared carrier instead of the call's result type is the
obvious workaround, which leads straight to blocker 2.

**2. It collides with same-name rebind.** For

```
State<Int> q = coin()
State<Int> q = hadamard(q)
```

with no `measure`, `test_linear_hardening_slice_b_red.py` asserts
`LINEAR_IMPLICIT_DISCARD` — and it is currently **not** emitted, which is a
separate under-report in the same family. Adding transport makes it worse: the
`hadamard(q)` call consumes `q`, and because the rebind reuses the root, the
new binding is born already-consumed and the discard is still not reported.

A correct implementation must let a same-name rebind **retire the old
obligation and open a fresh one**, rather than treating the root as a single
lifetime. That is a change to the root/alias model, not a predicate tweak.

## Exit

- [x] Result-type availability fixed for the density path, or the rule keyed on
      a source the density path does provide (Type-First bind head fallback)
- [x] Same-name rebind opens a fresh obligation after transport
- [x] `test_linear_hardening_slice_b_red.py` green **because the discard is now
      emitted**, not because it was silenced
- [x] The 5 density/Lindblad suites green without adding an artificial
      uncompute of a value the transformation already consumed
- [x] `expect` / `inner` still leave their argument live
- [x] ADR amending the LISS-0133 "builtins do not move" decision — [ADR 0168](../architecture/decision-themes/dec-0002-state-first-semantics-and-measurement.md)
- [x] Full suite no worse than 193/32 — measured **207 pass / 25 fail** after Green

## Non-goals

Re-opening ADR 0167 (the carrier-type rule stands); a per-builtin move table
(rejected in favour of the type-driven rule); changing `inspect`.

## Work Notes

- 2026-08-01: Implemented in `compiler/staqex/hir.py` under WP-0073; Red
  `tests/test_liss_0221_state_transforming_calls_move_red.py`.
