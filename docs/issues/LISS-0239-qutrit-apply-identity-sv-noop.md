# LISS-0239: Qutrit `apply(I)` Identity SV no-op (multi-wire path)

## Metadata

- Local issue ID: LISS-0239
- Status: **complete**
- Phase: phase-3-refactor
- Type: bug
- Priority: P1
- Planning size: S
- Program: [WP-0085](../work-plans/WP-0085-deferred-kernel-gaps.md)
- Parent ship: [LISS-0112](LISS-0112-qutrit-qudit-d3-statevector-mvp.md) Slice B
- Recorded on: [LISS-0233](LISS-0233-green-floor-residual-suites.md) deferred Kernel

## Intent

`state out = apply(I, s)` on `State<Qutrit>` must Identity-no-op at runtime
(including when bind name ≠ wire name via `_bind_apply_multi`).

## Exit

- [x] `apply(I)` on `State<Qutrit>` `|2⟩` runs and measures `2`
- [x] Non-Identity / `Qudit<4>` stay unsupported
- [x] Qubit `apply(I)` unchanged
- [x] Full `pytest tests/` green

## Non-goals

Clock/shift gates; registers; QASM D=3; non-Identity D=3 operators.
