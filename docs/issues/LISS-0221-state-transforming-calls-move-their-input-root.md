# LISS-0221: State-transforming calls must move their input root

## Metadata

- Local issue ID: LISS-0221
- Status: **proposed** — Adjudicator ruled the *semantics* 2026-08-01
  (option A); implementation is not started
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [ADR 0167](../architecture/adr/0167-linear-obligation-follows-carrier-type.md);
  LISS-0133 (builtins do not move quantum args); LISS-0114 lineage
- Blocks: 5 density/Lindblad suites and `test_linear_hardening_slice_b_red.py`
  in [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

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

- [ ] Result-type availability fixed for the density path, or the rule keyed on
      a source the density path does provide
- [ ] Same-name rebind opens a fresh obligation after transport
- [ ] `test_linear_hardening_slice_b_red.py` green **because the discard is now
      emitted**, not because it was silenced
- [ ] The 5 density/Lindblad suites green without adding an artificial
      uncompute of a value the transformation already consumed
- [ ] `expect` / `inner` still leave their argument live
- [ ] ADR amending the LISS-0133 "builtins do not move" decision
- [ ] Full suite no worse than 193/32

## Non-goals

Re-opening ADR 0167 (the carrier-type rule stands); a per-builtin move table
(rejected in favour of the type-driven rule); changing `inspect`.
