# AI work trace — WP-0080 CI root suites (LISS-0209)

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `batch/wp-0080-ci-runs-test-suite` |
| Issue | LISS-0209 |
| Work plan | WP-0080 |

## Change

- Add blocking `kernel-tests` job to `.github/workflows/ci.yml`
  (`python3 -m pytest tests/ -q`; ephemeral pytest install).
- Record locked rulings on LISS-0209 / WP-0080; update
  `docs/architecture/testing-strategy.md` and
  `docs/collaboration/local-issue-planning.md`.
- Spec-verification remains out of the blocking gate.

## Verification

Local floor from WP-0079: 1062 passed / 0 failed under `.venv/bin/pytest tests/`.
