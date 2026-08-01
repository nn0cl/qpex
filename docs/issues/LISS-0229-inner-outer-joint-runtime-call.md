# LISS-0229: `inner` / `outer` Joint runtime Call

## Metadata

- Local issue ID: LISS-0229
- GitHub issue: (none yet)
- Status: **proposed**
- Phase: (none — intake)
- Type: feature
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: (unassigned)
- Related branch: (none yet)
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

ADR 0087 ships `inner` / `outer` as compile-surface vocabulary. S01
`main_fidelity_inner_check.sqx` is **`staqex check` only**; runnable fidelity
uses `expect(ZZ,…)`. Joint **runtime Call** for `inner`/`outer` is still NYI
(scorecard Honesty).

Paper sugar `⟨φ|ψ⟩` (LISS-0217) stays out of this Issue unless Adjudicator
folds it in.

## Acceptance Notes

- [ ] Spec for Joint evaluation of `inner(phi, psi)` / `outer(psi, phi)`
- [ ] Red: runnable main (not check-only) with terminal measure
- [ ] Green without editing tests to pass
- [ ] S01 fidelity lane can become runnable, or a dedicated main added
- [ ] Scorecard Honesty row updated

## Dependencies

- ADR 0087; related LISS-0217 (sugar — optional follow)
- Related: `main_fidelity_inner_check.sqx`

## Verification

- New Red test under `tests/`
- `python3 -m compiler.staqex run` fidelity (or new) main seed 0
