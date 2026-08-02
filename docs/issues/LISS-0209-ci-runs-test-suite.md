# LISS-0209: CI executes no tests

## Metadata

- Local issue ID: LISS-0209
- Status: **complete** — 2026-08-02 (WP-0080)
- Phase: docs-only + infrastructure
- Type: infrastructure
- Priority: P0
- Planning size: M
- Program: [WP-0080](../work-plans/WP-0080-ci-runs-test-suite.md)
- Code: `.github/workflows/ci.yml`
- Unblocked by: [LISS-0233](LISS-0233-green-floor-residual-suites.md) / WP-0079
  (0-fail floor)

## Intent

`.github/workflows/ci.yml` had one job, `repository-sanity`, which checks that
documents exist, that scripts parse, that batch records validate, and that no
conflict markers remain. It ran **zero** tests. Add a blocking root-suite job.

## Locked rulings (WP-0080)

1. **Gate scope:** root suites only — `python3 -m pytest tests/ -q`.
2. **Spec-verification:** deferred (not in this WP); `run_all.py` stays manual /
   separate.
3. **Mode:** blocking (fail the build on any failure), not advisory.
4. **Runtime:** full root sweep (~minutes worst case; ~6s observed locally) is
   acceptable.
5. **pytest:** ephemeral CI install only — not a Kernel/runtime dependency
   (consistent with LISS-0208 “no project pytest dependency” for the language
   runtime).

## Exit

- [x] CI executes the root suites and fails the build on any failure
- [x] Spec-verification decision recorded (deferred at WP-0080; **shipped**
  WP-0086 / LISS-0241)
- [x] Landed only against a green tree (WP-0079: 1062 passed / 0 failed)
- [x] Template placeholder block removed

## Non-goals

Repairing failing suites; adding lint, type-check, or coverage jobs; changing
the existing `repository-sanity` job beyond coexistence; committing
spec-verification reports from CI.
