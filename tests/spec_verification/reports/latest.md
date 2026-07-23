# QPex Spec Compliance Report

- Generated: `2026-07-22T23:52:11.979857+00:00`
- Spec Compliance Rate: **100.0%**
- Gate: **PASS** (163/163 passed)

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
| SV-06 | sv06-nested-when | PASS | assertCompileError(NESTED_WHEN_ERROR) |
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
| SV-09 | sv09-01-phase_space | PASS | qpex check, qpex run |
| SV-09 | sv09-02-double_slit | PASS | qpex check, qpex run |
| SV-09 | sv09-02-ket_evolve_expect | PASS | qpex check, qpex run |
| SV-09 | sv09-03-bell_state | PASS | qpex check, qpex run |
| SV-09 | sv09-03-controlled_unitary | PASS | qpex check, qpex run |
| SV-09 | sv09-03-toffoli | PASS | qpex check, qpex run |
| SV-09 | sv09-03-open_control | PASS | qpex check, qpex run |
| SV-09 | sv09-03-mixed_control | PASS | qpex check, qpex run |
| SV-09 | sv09-03-portable_bell_qpu | PASS | qpex check, qpex run |
| SV-09 | sv09-04-grover_search | PASS | qpex check, qpex run |
| SV-09 | sv09-05-classical_oscillator | PASS | qpex check, qpex run |
| SV-09 | sv09-05-quantum_oscillator | PASS | qpex check, qpex run |
| SV-09 | sv09-05-xp_oscillator | PASS | qpex check, qpex run |
| SV-09 | sv09-05-grid_oscillator | PASS | qpex check, qpex run |
| SV-09 | sv09-06-ising_model | PASS | qpex check, qpex run |
| SV-09 | sv09-06-quantum_ising | PASS | qpex check, qpex run |
| SV-09 | sv09-06-quantum_ising_4 | PASS | qpex check, qpex run |
| SV-09 | sv09-07-quantum_vs_classical_walk | PASS | qpex check, qpex run |
| SV-09 | sv09-07-dtqw | PASS | qpex check, qpex run |
| SV-09 | sv09-07-classical_walk | PASS | qpex check, qpex run |
| SV-09 | sv09-08-gauge_symmetry | PASS | qpex check, qpex run |
| SV-09 | sv09-09-main_quantum_walk | PASS | qpex check, qpex run |
| SV-09 | sv09-10-main_ssh_topological | PASS | qpex check, qpex run |
| SV-09 | sv09-11-main_shor_period | PASS | qpex check, qpex run |
| SV-09 | sv09-12-main_city_route | PASS | qpex check, qpex run |
| SV-09 | sv09-13-main_deep_space_qkd | PASS | qpex check, qpex run |
| SV-09 | sv09-14-main_genome_motif | PASS | qpex check, qpex run |
| SV-09 | sv09-15-main_orbital_mesh | PASS | qpex check, qpex run |
| SV-09 | sv09-docs | PASS | docs |
| SV-10 | sv10-openqasm-bell | PASS | emit_openqasm3 |
| SV-10 | sv10-cli-emit-qasm | PASS | cli |
| SV-10 | sv10-target-cpu | PASS | --target cpu |
| SV-10 | sv10-target-qpu-emit | PASS | --target qpu |
| SV-10 | sv10-docs | PASS | docs |
| SV-11 | sv11-qasm3-syntax | PASS | QASM3Emitter |
| SV-11 | sv11-gate-map | PASS | lower |
| SV-11 | sv11-swap-route | PASS | router |
| SV-11 | sv11-cli-openqasm3 | PASS | cli |
| SV-13 | sv13-evolve-parse | PASS | parser |
| SV-13 | sv13-evolve-correlated | PASS | assertSuperposition, joint |
| SV-13 | sv13-evolve-times2 | PASS | evolve |
| SV-13 | sv13-examples-evolve | PASS | examples |
| SV-14 | sv14-destructive-vacuum | PASS | assertVacuum |
| SV-14 | sv14-constructive-dirac | PASS | assertSuperposition, assertNormEquals |
| SV-14 | sv14-cis-prelude | PASS | cis, Complex.cis |
| SV-14 | sv14-double-slit-cancel | PASS | assertSuperposition |
| SV-14 | sv14-grover-amplify | PASS | assertSuperposition |
| SV-15 | sv15-type-first-parse | PASS | Type-First, unit literal |
| SV-15 | sv15-dim-ok-evolve | PASS | dimensional analysis |
| SV-15 | sv15-dim-reject-add | PASS | assertCompileError(DIMENSION_MISMATCH_ERROR) |
| SV-15 | sv15-phase-space-example | PASS | example |
| SV-16 | sv16-main-ok | PASS | main, Type-First |
| SV-16 | sv16-toplevel-reject | PASS | assertCompileError(TOPLEVEL_EXECUTION_ERROR) |
| SV-16 | sv16-package-import | PASS | unit.package, unit.main |
| SV-17 | sv17-ket-literals | PASS | KetLit |
| SV-17 | sv17-evolve-under-x | PASS | hamiltonian |
| SV-17 | sv17-expect-z | PASS | expect |
| SV-17 | sv17-cnot-zz | PASS | cnot, ZZ |
| SV-17 | sv17-dim-pretty | PASS | DIMENSION_MISMATCH_ERROR |
| SV-18 | sv18-h-evolve-length | PASS | DIMENSION_MISMATCH_ERROR |
| SV-18 | sv18-interfer-independent | PASS | INTERFER_INDEPENDENT_STATE_ERROR |
| SV-18 | sv18-expect-mix | PASS | EXPECT_CLASSICAL_ONLY_ERROR |
| SV-18 | sv18-evolve-tuple-swap | PASS | DIMENSION_MISMATCH_ERROR |
| SV-18 | sv18-length-eq-float | PASS | DIMENSION_MISMATCH_ERROR |
| SV-18 | sv18-when-in-ctrl | PASS | NESTED_WHEN_ERROR |
| SV-18 | sv18-coin-in-evolve | PASS | COIN_IN_EVOLVE_ERROR |
| SV-18 | sv18-interfer-shared-ok | PASS | ok |
| SV-19 | sv19-fock-ho-unitary | PASS | Operator, expm |
| SV-19 | sv19-ising-unitary | PASS | Operator, Z(i), Float coeff |
| SV-19 | sv19-expm-unitary-matrix | PASS | matrix.expm_ih |
| SV-19 | sv19-tensor-trace-out | PASS | TensorExpr, trace_out |
| SV-19 | sv19-energy-eigenstate | PASS | expect, evolve under H |
| SV-19 | sv19-example-files | PASS | examples |
| SV-20 | sv20-hadamard | PASS | hadamard |
| SV-20 | sv20-apply-x | PASS | apply |
| SV-20 | sv20-dtqw-one-step | PASS | apply, shift, *|* |
| SV-20 | sv20-dtqw-two-step | PASS | DTQW |
| SV-20 | sv20-apply-hadamard-name | PASS | Hadamard |
| SV-20 | sv20-example-files | PASS | examples |
| SV-21 | sv21-capply-x-bell | PASS | capply, X |
| SV-21 | sv21-cnot-equiv-capply-x | PASS | cnot, capply |
| SV-21 | sv21-capply-z-phase | PASS | CZ |
| SV-21 | sv21-capply-ctrl0-id | PASS | controlled-I |
| SV-21 | sv21-example-file | PASS | examples |
| SV-22 | sv22-typed-product-bind | PASS | TypeRef Tuple, *|* |
| SV-22 | sv22-product-single-name | PASS | PRODUCT_BIND_ERROR |
| SV-22 | sv22-product-arity | PASS | PRODUCT_ARITY_ERROR |
| SV-22 | sv22-product-payload-mismatch | PASS | PRODUCT_TYPE_MISMATCH |
| SV-22 | sv22-trace-out-typed | PASS | trace_out |
| SV-22 | sv22-dtqw-typed-example | PASS | examples |
| SV-23 | sv23-project-predicate | PASS | PREDICATE_PROJECTOR_ERROR |
| SV-23 | sv23-map-constant | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-23 | sv23-when-collapse | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-23 | sv23-apply-non-unitary | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-23 | sv23-apply-hadamard-ok | PASS | ok |
| SV-23 | sv23-hilbert-project-ok | PASS | ok |
| SV-23 | sv23-coin-project-banned | PASS | PREDICATE_PROJECTOR_ERROR |
| SV-23 | sv23-gauge-u1-ok | PASS | examples |
| SV-24 | sv24-ccx-flip | PASS | CCX |
| SV-24 | sv24-toffoli-idle | PASS | toffoli |
| SV-24 | sv24-single-ctrl-compat | PASS | compat |
| SV-24 | sv24-example | PASS | examples |
| SV-25 | sv25-ocx-on-zero | PASS | ocapply |
| SV-25 | sv25-ocx-idle-on-one | PASS | open |
| SV-25 | sv25-dual-open | PASS | multi-open |
| SV-25 | sv25-example | PASS | examples |
| SV-26 | sv26-mixed-fire | PASS | ! |
| SV-26 | sv26-mixed-idle | PASS | polarity |
| SV-26 | sv26-double-bang-eq-ocapply | PASS | ocapply |
| SV-26 | sv26-example | PASS | examples |
| SV-27 | sv27-hermitian-e0 | PASS | Q, P |
| SV-27 | sv27-evolve-ground | PASS | evolve |
| SV-27 | sv27-example | PASS | examples |
| SV-28 | sv28-sparse-eq-dense-h | PASS | sparse |
| SV-28 | sv28-taylor-eq-dense-u | PASS | expm |
| SV-28 | sv28-ising4-norm | PASS | n=4 |
| SV-28 | sv28-example | PASS | examples |
| SV-29 | sv29-grid-hermitian | PASS | X, P |
| SV-29 | sv29-evolve-norm-mean | PASS | wavepacket |
| SV-29 | sv29-example | PASS | examples |
| SV-30 | sv30-apply-fock | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-30 | sv30-apply-grid | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-30 | sv30-map-bit-collapse | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-30 | sv30-map-flip-ok | PASS | ok |
| SV-30 | sv30-capply-non-unitary | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-30 | sv30-evolve-non-hermitian | PASS | NON_UNITARY_TRANSFORM_ERROR |
| SV-30 | sv30-evolve-grid-ok | PASS | ok |
| SV-31 | sv31-link-symbols | PASS | compile_path, merge |
| SV-31 | sv31-linked-run | PASS | run_path, step_quantum_walk |
| SV-31 | sv31-missing-import | PASS | MODULE_NOT_FOUND_ERROR |
| SV-31 | sv31-class-fields | PASS | class, Type-First |

