# QPex Spec Compliance Report

- Generated: `2026-07-22T16:09:02.741047+00:00`
- Spec Compliance Rate: **100.0%**
- Gate: **PASS** (31/31 passed)

| Suite | Case | Result | Assertions |
|-------|------|--------|------------|
| SV-01 | sv01-int-lift | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-01 | sv01-float-lift | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-01 | sv01-add-state | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-01 | sv01-dirac | PASS | assertTypeIsState, assertNormEquals |
| SV-01 | sv01-compiler-lit-lift | PASS | assertTypeIsState (compiler) |
| SV-02 | sv02-when-coin | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-02 | sv02-when-nested | PASS | assertNormEquals, assertSuperposition |
| SV-03 | sv03-div-by-zero | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-03 | sv03-div-ok | PASS | assertTypeIsState, assertNormEquals, assertSuperposition |
| SV-04 | sv04-early-collapse-bad | PASS | assertCompileError(EARLY_COLLAPSE_ERROR) |
| SV-04 | sv04-early-collapse-ok | PASS | assertCompileError(absent) |
| SV-05 | sv05-vacuum-project | PASS | assertVacuum, assertNormEquals |
| SV-05 | sv05-compare-state-bool | PASS | assertTypeIsState<Bool>, assertNormEquals, assertSuperposition |
| SV-05 | sv05-vacuum-ctor | PASS | assertVacuum |
| SV-05 | sv05-compiler-compare-bool | PASS | assertTypeIsState<Bool> (compiler) |
| SV-06 | sv06-package-tensor | PASS | namespace resolve, tensor_compose |
| SV-06 | sv06-forbidden-if | PASS | assertCompileError(FORBIDDEN_KEYWORD) |
| SV-06 | sv06-forbidden-null-throw | PASS | assertCompileError(FORBIDDEN_KEYWORD) |
| SV-06 | sv06-retired-observe-span | PASS | assertCompileError(RETIRED_KEYWORD) |
| SV-07 | sv07-correlated-self-sum | PASS | assertSuperposition, assertNormEquals |
| SV-07 | sv07-when-mixture | PASS | assertSuperposition, assertNormEquals |
| SV-07 | sv07-project-vacuum | PASS | assertVacuum |
| SV-07 | sv07-map | PASS | assertSuperposition |
| SV-07 | sv07-interfer | PASS | assertSuperposition, assertNormEquals |
| SV-07 | sv07-measure-stdout | PASS | measure output |
| SV-08 | sv08-prelude | PASS | prelude |
| SV-08 | sv08-math-sin | PASS | assertSuperposition, Math.sin |
| SV-08 | sv08-inspect | PASS | inspect |
| SV-08 | sv08-snapshot | PASS | snapshot |
| SV-08 | sv08-cli-check | PASS | cli check |
| SV-08 | sv08-dag-ir | PASS | dag ir |

