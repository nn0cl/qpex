# LISS-0208: 10 test files are unrunnable by the documented invocation

## Metadata

- Local issue ID: LISS-0208
- Status: **complete** — 2026-08-01
- Phase: phase-0-design
- Type: bug
- Priority: P0
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: [`testing-strategy.md`](../architecture/testing-strategy.md)
- Blocks: [LISS-0209](LISS-0209-ci-runs-test-suite.md)

## Intent

[`testing-strategy.md`](../architecture/testing-strategy.md) states that suites
run as plain scripts and that "the repository has no pytest configuration; do
not assume a pytest-only invocation". Ten suites contradict that: five import
`pytest`, five omit the `sys.path` bootstrap every other suite carries. All ten
fail before executing a single assertion.

## Evidence (reproduced 2026-08-01)

**`ModuleNotFoundError: No module named 'pytest'`** (5):

```
tests/test_host_qpu_submit_orchestration_red.py
tests/test_liss0058_acting_space_typing_red.py
tests/test_multi_register_acting_space_red.py
tests/test_qpu_observation_result_integration_red.py
tests/test_simulator_resource_execution_wiring_red.py
```

**`ModuleNotFoundError: No module named 'compiler'`** — missing the
`sys.path.insert(0, _REPO)` prologue used by the other 216 suites (5):

```
tests/test_higher_order_suzuki_green.py
tests/test_liss_0125_hir_binop_expr_children_red.py
tests/test_qft_basic_gate_lowering_red.py
tests/test_qpu_ir_lowering_green.py
tests/test_qpu_ir_lowering_red.py
```

These ten are part of the 50 failing files in the 2026-08-01 sweep, but unlike
the regression clusters they prove nothing about the Kernel — they never ran.

### Correction: the `sv12` gap is not a defect

The intake claimed `sv12` was missing with no record explaining it. That was
**wrong**, and is withdrawn. The absence is deliberate, documented, and tested:

- `docs/testing/staqex-spec-verification-protocol.md` lists the harness as
  "SV-01–11, SV-13–31; **SV-12 absent**"
- `tests/test_conformance_slice_a_red.py::test_protocol_explicitly_marks_sv12_absent`
  asserts the protocol says so
- [`staqex-v1-conformance-plan.md`](../specs/staqex-v1-conformance-plan.md)
  requires the absence to be documented

`sv12` never existed in git history. No action is needed and none was taken.

## Adjudicator decision points

1. Is `pytest` being adopted as a dependency, or must those five suites be
   rewritten as plain scripts to match the stated strategy? The dependency
   choice is a technology selection and needs its own approval
   ([`dependency-policy.md`](../architecture/dependency-policy.md),
   [`external-resource-adoption-contract.md`](../architecture/external-resource-adoption-contract.md)).
2. Should the bootstrap prologue be factored into a shared helper rather than
   copied into 220+ files? (Left as-is for now — 220 files already carry it and
   changing them all is a larger refactor than this Issue.)

## Exit

- [x] All ten suites execute under the documented invocation
- [x] pytest question answered explicitly, not by drift — Adjudicator ruled
      2026-08-01: rewrite as plain scripts, adopt no new dependency
- [x] `sv12` claim withdrawn as incorrect (see correction above)
- [x] Whatever the ten suites then assert is triaged — nine pass;
      `test_liss0058_acting_space_typing_red.py` reveals a genuine
      `LINEAR_IMPLICIT_DISCARD` and joins
      [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Non-goals

Fixing the assertions those suites make once runnable — that is triage output,
tracked against the regression Issues; enabling CI (LISS-0209).
