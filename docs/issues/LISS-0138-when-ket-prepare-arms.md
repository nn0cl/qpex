# LISS-0138: `when` arms with ket / prepare literals

## Metadata

- Local issue ID: LISS-0138
- Status: **complete** — 2026-07-31 (PR pending)
- Phase: Feature Path Red → Green → Refactor
- Type: Kernel residual / language
- Priority: P1 (language surface growth)
- Depends on: none hard; discovered by [LISS-0134](LISS-0134-showcase-s1-thin-slice.md)
- Implementation permission: **yes** (Adjudicator 承認 — language first)
- Branch: `feature/liss-0138-when-ket-prepare-arms`
- Tests: `tests/test_when_ket_prepare_arms_red.py`

## Summary

Physicist-legible prepare branching:

```text
state prep = when (bit) {
  0 -> |0>,
  else -> |+>,
}
```

`_bind_when` expands `KetLit` arms via `ket_support` (same as bare ket bind),
preserving mixture amplitudes. Spec §3.4 documents ket arms.

## Exit

- [x] Red suite for ket prepare arms
- [x] Green: prepare branching without classical label indirection
- [x] B02 + showcase teach ket-`when`
- [x] Spec §3.4 note
- [ ] Adjudicator PR merge review
