# LISS-0209: CI executes no tests

## Metadata

- Local issue ID: LISS-0209
- Status: **proposed** (investigation intake — no Red authorized)
- Phase: phase-0-design
- Type: infrastructure
- Priority: P0
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Code: `.github/workflows/ci.yml`
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md) …
  [LISS-0208](LISS-0208-test-harness-hygiene.md) (must land **last**)

## Intent

`.github/workflows/ci.yml` has one job, `repository-sanity`, which checks that
documents exist, that scripts parse, that batch records validate, and that no
conflict markers remain. It runs **zero** tests. The file still carries the
collaboration-template placeholder:

```yaml
  # Add stack-specific jobs here once the implementation exists, for example:
  #
  # backend:
  #   name: Backend checks
  #     - name: Run tests
  #       run: <your test command>
```

## Evidence (reproduced 2026-08-01)

- No `pytest`, no `python3 tests/…` invocation anywhere in the workflow.
- 224 root suites and 30 spec-verification suites are never executed by CI.
- Consequence, measured: **50 of 224 root test files fail on a clean `main`**
  (21 linear-discipline, 6 qudit, 5 return-type, 2 Dirac parse, 2 SI, 3
  residual, 1 crash, 10 harness). Every merge that introduced one of these was
  green.

This is the root cause that let the other regression Issues accumulate, which
is why it is P0 — but it must be the **last** of them to land. Turning the gate
on while 50 suites are red pins `main` red and blocks every subsequent PR.

## Adjudicator decision points

1. Scope of the gate: root suites only, or root suites + `tests/spec_verification/run_all.py`?
2. `run_all.py` writes `tests/spec_verification/reports/latest.{json,md}`.
   Should CI run it read-only, or commit refreshed reports? A CI job that
   mutates tracked files needs an explicit ruling.
3. Blocking vs advisory on first landing. Recommendation: land blocking, but
   only after LISS-0202…LISS-0208 are green, so it never runs against a known-red tree.
4. Runtime budget — the full sweep takes minutes locally; confirm acceptable.

## Exit

- [ ] CI executes the root suites and fails the build on any failure
- [ ] Spec-verification decision recorded and implemented
- [ ] Landed only against a green tree
- [ ] Template placeholder block removed

## Non-goals

Repairing any failing suite (LISS-0202…LISS-0208); adding lint, type-check, or
coverage jobs; changing the existing `repository-sanity` job.
