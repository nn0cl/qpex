# LISS-0109: Examples applied track migration

## Metadata

- Local issue ID: LISS-0109
- GitHub issue: not created
- Status: in-progress
- Phase: phase-2-green
- Type: examples / documentation / migration
- Priority: P1
- Initial planning size: XL
- Current planning size: XL
- Owner/agent: unassigned
- Parent: [LISS-0106](LISS-0106-examples-catalog-v2-refresh.md)
- Depends on:
  - [LISS-0107](LISS-0107-examples-linker-runtime-prerequisite.md) for linked entries
- Related branch: TBD

## Summary

Migrate Applied curriculum **A01–A10** into `examples/applied/` per
[`qpex-examples-catalog-v2.md`](../specs/qpex-examples-catalog-v2.md).
Each entry MUST include:

- README Honesty table
- Bibliography section with **verified** primary references only
- explicit toy scale and out-of-scope claims

## Acceptance Notes

- [ ] Folders `examples/applied/A01_*` … `A10_*` created per catalog spec priority
- [ ] Narrative clones (legacy 12/14/15) absorbed into A02/A04; not duplicated
- [x] A06, A09, A10 migrated from legacy 10/13/16 with updated READMEs
- [x] A08 demonstrates `RegisterSet` / multi-register surface (LISS-0067)
- [ ] A03 demonstrates `FermionOperator` + Jordan-Wigner at minimal scale
- [ ] A01 ships as attention-inspired toy with verified bibliography and explicit
      non-LLM-inference wording
- [ ] No claim of production LLM inference, clinical drug discovery, or real-time
      robot control in any README
- [ ] All applied entry points registered in SV-09 successor suite (P0 done: A06, A08–A10)

## Verification

- Full SV suite
- Per-example `qpex check`, `run --seed 0`, and QPU-lane `emit-qasm` where applicable
- Manual Honesty table + bibliography review
