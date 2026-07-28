# QPex v1 conformance scenario catalog (LISS-0071 Slice B)

| Field | Value |
|---|---|
| Status | **Slice B+C published** (2026-07-28); Normative catalog live; E-05 gap closed |
| Authority | [`qpex-v1-conformance-plan.md`](qpex-v1-conformance-plan.md); [`qpex-v1-acceptance-envelopes.md`](qpex-v1-acceptance-envelopes.md) |
| Depends on | LISS-0071 Slice A **complete** |
| Last updated | 2026-07-28 |

Filling remaining deferred Host/Dynamic rows is out of LISS-0071 Slice C.
E-05 Static Hilbert gap is **closed** (E05-001…E05-003 covered).

## 1. Goals

1. Give every acceptance envelope `E-01`–`E-14` at least one stable
   `scenario_id` row (or an explicit `gap` / `deferred`).
2. Classify each row with the Slice A taxonomy:
   valid / invalid / semantic / numerical / provenance / backend.
3. Point each covered row at a Python-reference oracle location (SV suite/case
   or reviewed Red module path).
4. Make envelope vs suite title conflicts resolve in favor of the **envelope**.

## 2. Row schema (Normative for Slice B)

| Column | Required | Notes |
|---|---|---|
| `scenario_id` | yes | Stable id: `E##-###` (e.g. `E01-001`) |
| `envelope` | yes | `E-01` … `E-14` |
| `class` | yes | taxonomy class from conformance plan §2 |
| `oracle` | yes | `SV-NN/case-id` or `tests/…_red.py` or `examples/…` |
| `status` | yes | `covered` / `gap` / `deferred` |
| `notes` | no | Deferral owner Issue, ε override, lane caveat |

### Status meanings

- **covered** — Python-reference run can pass/fail the claim today.
- **gap** — claim is normative but no stable scenario yet (Slice C candidate).
- **deferred** — intentionally out of Kernel conformance (Host/Dynamic/north-star).

## Catalog (Normative)

One primary row per envelope. Additional rows may be added in Slice C without
renumbering existing `scenario_id` values.

| scenario_id | envelope | class | oracle | status | notes |
|---|---|---|---|---|---|
| E01-001 | E-01 | semantic | SV-01; SV-07 | covered | Lit-Lift + joint/measure path |
| E02-001 | E-02 | invalid | SV-06 | covered | Forbidden / Retired surface |
| E03-001 | E-03 | semantic | SV-02; SV-13; tests/test_evolve_until_runtime_red.py | covered | when + evolve; until covered by evolve-until Red |
| E04-001 | E-04 | semantic | SV-16 | covered | structured main / explicit returns |
| E05-001 | E-05 | semantic | docs/specs/qpex-static-hilbert-kernel.md; tests/test_static_hilbert_migration_red.py | covered | primary Static Hilbert surface |
| E05-002 | E-05 | invalid | tests/test_kernel_classical_boundary_red.py | covered | FOR_EACH_DYNAMIC_BOUND_ERROR |
| E05-003 | E-05 | invalid | tests/test_static_hilbert_migration_red.py | covered | STATIC_HILBERT_RESOURCE_ERROR |
| E06-001 | E-06 | backend | tests/test_parametric_circuit_runtime_red.py | covered | Parametric lane |
| E07-001 | E-07 | backend | docs/issues/LISS-0028-dynamic-qpu-lane.md | deferred | Dynamic lane capability; not Kernel Static oracle |
| E08-001 | E-08 | numerical | SV-19; SV-23; SV-30 | covered | operator Hamiltonian / unitarity cluster |
| E09-001 | E-09 | numerical | tests/test_continuous_discretization_red.py; tests/test_continuous_lowering_red.py | covered | continuous discretization MVP |
| E10-001 | E-10 | semantic | tests/test_multi_register_acting_space_red.py | covered | multi-register acting space |
| E11-001 | E-11 | semantic | SV-19; tests/test_finite_binder_lowering_red.py | covered | finite binder lowering |
| E12-001 | E-12 | semantic | SV-31 | covered | modules / visibility |
| E13-001 | E-13 | provenance | examples/basics/B13_host_job_api | deferred | Host Job boundary; Host lane |
| E14-001 | E-14 | provenance | docs/specs/qpex-scientific-scopes.md | deferred | scientific scopes / workflow; not Static Kernel gate |

## 3. Verification

- Red: `tests/test_conformance_slice_b_red.py`, `tests/test_conformance_slice_c_red.py`
- Green: Normative table (E-05 gap closed in Slice C)
- Deferred: E-07 / E-13 / E-14 remain Host/Dynamic out of Kernel Static gate

## 4. Explicit non-goals

- Changing SV suite assertions.
- Filling all `gap` rows in Slice B (Slice C).
- Rust differential (Slice D / LISS-0070).
- Report-write policy (Slice A, already shipped).
