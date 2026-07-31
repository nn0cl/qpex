# LISS-0202: Linear-discipline hard-fail breaks 21 pre-existing suites

## Metadata

- Local issue ID: LISS-0202
- Status: **proposed** (investigation intake — no Red authorized)
- Phase: phase-0-design
- Type: bug
- Priority: P0
- Planning size: L
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: ADR 0114 / LISS-0114 / LISS-0121 (linear hardening lineage)
- Blocked by: [LISS-0208](LISS-0208-test-harness-hygiene.md) — the suite must be
  runnable before its failures can be judged
- Blocks: [LISS-0203](LISS-0203-qudit-local-dimension-typing-regression.md),
  [LISS-0204](LISS-0204-class-method-return-type-regression.md),
  [LISS-0205](LISS-0205-dirac-block-result-parse-regression.md),
  [LISS-0206](LISS-0206-si-conversion-diagnostic-regression.md),
  [LISS-0207](LISS-0207-residual-regression-cluster.md)

## Intent

`LINEAR_IMPLICIT_DISCARD` / `LINEAR_DUPLICATE_USE` became hard diagnostics
during the linear-hardening lineage. 21 suites written before that change
construct a `State` and never measure or uncompute it, so `compiled.ok` is now
`False` and their `assert compiled.ok` fails.

This is the largest of the six regression clusters found by the 2026-08-01
full-suite sweep (**50 of 224 test files fail on a clean `main`**). CI does not
run tests ([LISS-0209](LISS-0209-ci-runs-test-suite.md)), which is why the
breakage accumulated undetected.

## Evidence (reproduced 2026-08-01)

Representative — `tests/test_dirac_slice_a_red.py`:

```
AssertionError: [{'code': 'LINEAR_IMPLICIT_DISCARD', 'line': 4, 'col': 13,
  'message': 'quantum state `bra` is discarded without measure or uncomputation'}, …]
```

Affected files (21):

```
tests/test_density_cptp_lindblad_numeric_red.py
tests/test_density_cptp_lindblad_red.py
tests/test_density_cptp_lindblad_source_red.py
tests/test_density_cptp_lindblad_symbolic_red.py
tests/test_dirac_slice_a_red.py
tests/test_dirac_slice_b_red.py
tests/test_dirac_slice_c_red.py
tests/test_dirac_slice_d_red.py
tests/test_dirac_slice_e_red.py
tests/test_evolve_until_red.py
tests/test_lindblad_jump_inputs_red.py
tests/test_linear_hardening_slice_b_red.py
tests/test_liss0055_execution_acceptance.py
tests/test_liss0056_empty_domain_identity_red.py
tests/test_liss0057_periodic_boundary_red.py
tests/test_pipeline_currying_red.py
tests/test_qasm3_codegen.py
tests/test_symbolic_expression_ir_red.py
tests/test_symbolic_lindblad_jump_lowering_red.py
tests/test_trait_impl_system_red.py
tests/test_unicode_math_source_red.py
```

`tests/test_linear_hardening_slice_b_red.py` is notable: it is a suite *of the
linear feature itself*, and its `test_gate_rebind_does_not_consume` now fails
because the expected `LINEAR_IMPLICIT_DISCARD` is **not** emitted. So the
cluster is not uniformly "tests are stale" — at least one case points at the
Kernel.

## Adjudicator decision points

**This is the hard-stop of the batch. Do not resolve it by editing tests until
it is decided.**

For each affected suite the question is which side is wrong:

1. **The test is stale** — it predates the linear axiom and should add a
   terminal `measure` or an uncompute witness. Cost: 20 mechanical edits, but
   it silently changes what each suite was written to prove.
2. **The Kernel is over-strict** — e.g. a bare `bra` in Dirac algebra position,
   or a density/Lindblad carrier, is not a linear quantum resource and should
   not require discharge. Cost: a diagnostic-scope change, needs an ADR
   amendment to the ADR 0114 lineage.
3. **Mixed** — most likely. The split must be decided per sub-family
   (Dirac algebra / density-Lindblad / symbolic IR / pipeline / trait).

`tests/test_linear_hardening_slice_b_red.py` must be resolved first: it is the
only suite whose failure asserts a *missing* linear diagnostic, so it names a
genuine behavior gap independent of the stale-test question.

## Exit

- [ ] Per-sub-family ruling recorded (test stale vs Kernel over-strict)
- [ ] ADR amendment raised if any Kernel-side change is chosen
- [ ] All 21 suites green with their original intent preserved
- [ ] No suite made to pass by weakening what it asserts

## Non-goals

The other five regression clusters (LISS-0203…LISS-0207); enabling CI
(LISS-0209); revisiting the Never-Leave-the-State or linear axioms themselves.
