# QPex conformance Slice C — E-05 gap fill (LISS-0071)

| Field | Value |
|---|---|
| Status | **Slice C Phase 2 Green** (2026-07-28); E-05 gap closed |
| Authority | [`qpex-v1-conformance-scenario-catalog.md`](qpex-v1-conformance-scenario-catalog.md); [`qpex-v1-acceptance-envelopes.md`](qpex-v1-acceptance-envelopes.md) E-05; [`qpex-static-hilbert-kernel.md`](qpex-static-hilbert-kernel.md) |
| Depends on | LISS-0071 Slice B **complete** |
| Last updated | 2026-07-28 |

This companion freezes **Slice C** scope: close the sole catalog `gap` row
(`E05-001`) by binding E-05 Gherkin to existing Python-reference oracles.
It does not authorize Phase 1 Red until plan approval.

## 1. Goals

1. Change `E05-001` from `gap` → `covered` with precise oracle pointers.
2. Add fine-grained scenario rows for E-05 Gherkin (without renumbering
   `E05-001`):
   - dynamic `forEach` bound → `FOR_EACH_DYNAMIC_BOUND_ERROR`
   - static Hilbert resource overflow → `STATIC_HILBERT_RESOURCE_ERROR`
3. Prefer **existing** Red modules / compile paths; do not invent new language
   semantics.
4. Leave `deferred` Host/Dynamic rows (E-07/E-13/E-14) untouched.

## 2. Why E-05 (only gap)

Catalog Normative table currently has exactly one `gap`:

| scenario_id | notes |
|---|---|
| E05-001 | tighten QubitRegister-typed scenarios in Slice C |

SV-26 is **mixed control** (`!c`), not Static Hilbert — the provisional
`SV-26` oracle was a mis-map and must be replaced.

## 3. Proposed Normative rows (draft for Green)

| scenario_id | envelope | class | oracle (proposed) | status | notes |
|---|---|---|---|---|---|
| E05-001 | E-05 | semantic | `docs/specs/qpex-static-hilbert-kernel.md`; `tests/test_static_hilbert_migration_red.py` | covered | primary Static Hilbert surface |
| E05-002 | E-05 | invalid | `tests/test_kernel_classical_boundary_red.py` | covered | `FOR_EACH_DYNAMIC_BOUND_ERROR` |
| E05-003 | E-05 | invalid | `tests/test_static_hilbert_migration_red.py` | covered | `STATIC_HILBERT_RESOURCE_ERROR` |

Optional later (out of Slice C unless Adjudicator expands): measure-shape /
acting-space reject as `E05-004` if a dedicated Red case is selected.

## 4. Acceptance envelopes (Slice C)

### EARS

When Slice C completes, envelope E-05 shall have no `gap` rows in the
Normative catalog.

When a new E-05 scenario row is `covered`, its `oracle` shall name an existing
test path or reviewed spec under the Shipping Kernel tree.

### Gherkin

```gherkin
Feature: E-05 gap closed

  Scenario: Catalog has no E-05 gap
    Given the Normative catalog
    When E-05 rows are listed
    Then no row has status gap

  Scenario: Dynamic forEach oracle exists
    Given scenario E05-002
    When its oracle path is resolved
    Then tests/test_kernel_classical_boundary_red.py exists
```

## 5. Verification plan

- Phase 1 Red: `tests/test_conformance_slice_c_red.py`
  - no `gap` status for envelope E-05
  - E05-002 / E05-003 present with required diagnostics named in notes or oracle
  - listed oracle files exist on disk
- Phase 2 Green: update Normative catalog rows only (and Status/notes); **no**
  new compiler behavior unless Red proves a missing diagnostic (stop and ask).
- Phase 3 Refactor: readability only.
- Full SV 160/160 remains PASS; Slice A/B Red suites remain PASS.

## 6. Explicit non-goals

- Filling deferred E-07 / E-13 / E-14.
- Splitting all covered clusters (E-08 etc.) into finer rows.
- Changing SV-26 semantics or adding a new SV suite number.
- Rust differential / CST / NFC.
