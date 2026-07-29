# Trace: LISS-0068 normative rebaseline slice 5 (E0 completion)

- Date: 2026-07-27
- Task: Migration/removal matrix for breaking v1 surfaces
- Agent: Cursor (Auto)
- Phase: Architecture Path / LISS-0068 slice 5 — **E0 batch complete**

## Delivered

- `docs/specs/staqex-v1-migration-matrix.md`
  - Completed migrations M-C01–M-C08 (fn, pub, measure, etc.)
  - Planned migrations M-P01–M-P07 with staged dual-accept / deprecate / remove gates
  - Documentation reconciliation rows D-R01–D-R08
  - Version bump gates and LISS-0068 E0 exit checklist

## E0 artifact set (slices 1–5)

| # | Document |
|---|---|
| 1 | `staqex-v1-normative-rebaseline-register.md` |
| 2 | `staqex-v1-normative-outline-s12.md` |
| 3 | `staqex-v1-diagnostic-catalog.md` |
| 4 | `staqex-v1-acceptance-envelopes.md` |
| 5 | `staqex-v1-migration-matrix.md` |

## Verification

- Documentation-only; no compiler or test changes.

## Next safe actions

1. Adjudicator review of LISS-0068 E0 package.
2. LISS-0069 — Unicode/Dirac migrator (M-P01–M-P04 dual-accept).
3. Spec promotion PR merging E0 artifacts into v1 normative text.
4. LISS-0071 — conformance harness sync (DR-011).
