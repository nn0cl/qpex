# LISS-0241: CI runs spec-verification

## Metadata

- Local issue ID: LISS-0241
- Status: **complete**
- Type: infrastructure
- Priority: P1
- Program: [WP-0086](../work-plans/WP-0086-spec-verification-ci.md)
- Follows: [LISS-0209](LISS-0209-ci-runs-test-suite.md) (SV deferred there)

## Intent

Add a blocking GitHub Actions job for
`python3 tests/spec_verification/run_all.py`. Do not commit
`reports/latest.*` from CI.

## Exit

- [x] `spec-verification` job in `.github/workflows/ci.yml`
- [x] Local SV gate 161/161 before merge
- [x] testing-strategy updated
