# Trace: LISS-0069 plan intake (Slice A)

- Date: 2026-07-28
- Task: Open LISS-0069 and propose Slice A plan (Unicode math dual-accept)
- Agent: Cursor (Auto)
- Phase: Feature Path / Phase 0 Design Intake
- Branch: `feature/liss-0069-unicode-math-source`

## Delivered

- `docs/issues/LISS-0069-canonical-mathematical-source-and-migration.md`
- `docs/specs/qpex-unicode-math-source.md` (Slice A surface contract)
- open-work-register + migration matrix pointers

## Requested approval

**Plan approval** for Slice A only:

- lexer dual-accept for Unicode ket / tensor / postfix dagger;
- bra: prefer wiring to existing nodes, or allow deferral;
- no Pauli ASCII removal; no `state` sugar migration;
- Phase 1 Red after approval; Green not implied unless batch autonomy granted.

## Explicitly not authorized yet

- Phase 1 Red tests
- lexer/parser production changes
- migrator CLI / golden corpus (Slices B/C)
- formatter emit (LISS-0072 overlap)

## Next safe action

Adjudicator plan approval → Phase 1 Red on this branch.
