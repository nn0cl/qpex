# QPex Spec Verification (AT-TDD)

Protocol: [`docs/testing/qpex-spec-verification-protocol.md`](../../docs/testing/qpex-spec-verification-protocol.md)

```bash
# Local default — no report file write (avoids timestamp git drift)
python3 tests/spec_verification/run_all.py

# Explicit report artifacts (CI)
python3 tests/spec_verification/run_all.py --write-report
```

With `--write-report`, emits `reports/latest.json` and `reports/latest.md` with
**Spec Compliance Rate**.
