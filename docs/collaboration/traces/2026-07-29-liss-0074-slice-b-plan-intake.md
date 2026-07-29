# Trace: LISS-0074 Slice A completion + Slice B plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0074 |
| Path | Feature Path — Slice A closeout + Slice B plan (docs) |
| Phase | slice-a done; slice-b phase-0-design |
| Branch | `feature/liss-0074-slice-a-red` |
| Implementation | **forbidden** for Slice B until plan approval |

## [DESIGN CHECK]

- Scope: close Slice A after Green approval; propose Slice B only — numeric
  ket/bra labels must satisfy `0 ≤ k < D` for `Qutrit`/`Qudit<D>`; reuse
  `LOCAL_DIMENSION_TYPE_ERROR`; exclude C/D/E.
- Specs: north-star §5.2; Slice A surface; probe `|3⟩` on `Qutrit` still ok.
- Decisions pending: label code name; alone-ket without declared carrier;
  Red authorization.
- Verification: land Slice A PR; docs for B plan; no B Green yet.

## Slice A completion evidence

- `tests/test_qudit_slice_a_red.py` PASS
- Commits: plan → Red → Green on this branch

## Slice B requested approval

**Plan approval** for Slice B only with recommended label policy above.

## Next safe action

Land Slice A PR; Adjudicator Slice B plan approval → Phase 1 Red.
