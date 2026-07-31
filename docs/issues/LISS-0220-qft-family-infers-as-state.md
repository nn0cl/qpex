# LISS-0220: `qft` / `iqft` / `cqft` / `ciqft` infer as `State` instead of `Operator`

## Metadata

- Local issue ID: LISS-0220
- Status: **proposed**
- Phase: phase-0-design
- Type: bug
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [ADR 0078](../architecture/adr/0078-kernel-qft-iqft-surface.md) (QFT/IQFT
  surface); [ADR 0120](../architecture/adr/0120-exact-controlled-qft.md) (`cqft`/`ciqft`);
  [ADR 0167](../architecture/adr/0167-linear-obligation-follows-carrier-type.md)
- Code: `compiler/staqex/typecheck.py`

## Intent

The QFT family is declared and used as an `Operator`, but the typechecker
infers its call result as `State`. Found while implementing ADR 0167, whose
first draft trusted raw inference and consequently mis-flagged `Operator`
bindings as linear quantum resources.

## Evidence (reproduced 2026-08-01)

```
name       declared    inferred
qft        Operator    State
iqft       Operator    State
adjoint    Operator    (typed via _check_algebra_call)
hadamard   State       State
```

`_infer_call` dispatches known builtins explicitly — `create`/`annihilate` →
`Operator`, `system` → `Register`, `expect` → `Classical`, and so on — and ends
with a catch-all:

```python
return Ty("State", "Any", DIMLESS)
```

`qft`, `iqft`, `cqft` and `ciqft` are absent from the dispatch, so they land on
that catch-all. The static helper `_is_qft_call` already enumerates all four,
and `_check_qft_call` already validates the register shape and resource budget
— only the return type is wrong.

## Why it matters

The declared type saves most programs today: `Operator F = qft(reg)` typechecks
because the declaration is authoritative. The mis-inference bites wherever
inference is the only evidence:

- inference-only binds (`state f = qft(reg)`)
- any analysis that consults `HirModule.typed`, which is exactly how ADR 0167's
  first draft regressed the suite from 50 to 58 failures before declarations
  were given priority
- future passes that reasonably assume `typed` is trustworthy

ADR 0167 documents the declaration-first ordering as a deliberate guard against
this class of mis-inference. That guard should not have to carry a defect that
can simply be fixed.

## Exit

- [ ] `qft` / `iqft` / `cqft` / `ciqft` infer as `Operator`
- [ ] Declared `Operator` binds still typecheck (no payload unification break)
- [ ] Full suite no worse than the ADR 0167 baseline (176 pass / 48 fail)
- [ ] Red test asserts the inferred kind directly, not only via a declaration

## Non-goals

Auditing every builtin that reaches the catch-all — worth doing, but a separate
Issue. Changing QFT semantics, the register shape check, or the resource
budget. Removing the catch-all itself.
