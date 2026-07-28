# QPex v1 conformance scenario catalog (LISS-0071 Slice B)

| Field | Value |
|---|---|
| Status | **plan proposed** (2026-07-28); awaiting Adjudicator plan approval |
| Authority | [`qpex-v1-conformance-plan.md`](qpex-v1-conformance-plan.md); [`qpex-v1-acceptance-envelopes.md`](qpex-v1-acceptance-envelopes.md) |
| Depends on | LISS-0071 Slice A **complete** |
| Last updated | 2026-07-28 |

This companion freezes the **Slice B** catalog contract. It does not authorize
Phase 1 Red until plan approval. The initial inventory rows below are
**planning drafts** (not yet a Red/Green oracle).

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
| `oracle` | yes | `SV-NN/case-id` or `tests/…_red.py::test_…` or `examples/…` |
| `status` | yes | `covered` / `gap` / `deferred` |
| `notes` | no | Deferral owner Issue, ε override, lane caveat |

### Status meanings

- **covered** — Python-reference run can pass/fail the claim today.
- **gap** — claim is normative but no stable scenario yet (Slice C candidate).
- **deferred** — intentionally out of Kernel conformance (Host/Dynamic/north-star).

## 3. Acceptance envelopes (Slice B)

### EARS

When the catalog is published, every envelope `E-01`–`E-14` shall appear in at
least one row.

When a row is `covered`, its `oracle` field shall name an existing suite case
or reviewed test path under the Shipping Kernel tree.

When a row is `gap` or `deferred`, the `notes` field shall name why (and an
owner Issue when known).

### Gherkin

```gherkin
Feature: Conformance scenario catalog

  Scenario: Every envelope has a row
    Given docs/specs/qpex-v1-conformance-scenario-catalog.md
    When the catalog table is read
    Then each of E-01 through E-14 appears at least once

  Scenario: Covered rows cite a real oracle path
    Given a catalog row with status covered
    When the oracle field is resolved
    Then it names an existing SV case id or test path in the repo
```

## 4. Planning inventory (draft — not Red-locked)

Provisional one-row-per-envelope map from the promoted envelope index.
Statuses are Adjudicator-reviewable guesses for Slice B Green; Red only
locks the **schema + presence** rules above.

| scenario_id | envelope | class | oracle (draft) | status | notes |
|---|---|---|---|---|---|
| E01-001 | E-01 | semantic | SV-01 / SV-07 | covered | Lit-Lift + measure path |
| E02-001 | E-02 | invalid | SV-06 | covered | Forbidden/Retired |
| E03-001 | E-03 | semantic | SV-02 / SV-13; `test_evolve_until_*` | covered | when + evolve; until may need extra row |
| E04-001 | E-04 | semantic | SV-16 | covered | structured main / returns |
| E05-001 | E-05 | semantic | SV-26 area | gap | tighten register-typed scenarios |
| E06-001 | E-06 | backend | `test_parametric_circuit_*` | covered | Parametric lane |
| E07-001 | E-07 | backend | LISS-0028 Red | deferred | Dynamic lane capability |
| E08-001 | E-08 | numerical | SV-19–SV-30 | covered | operator / unitarity cluster |
| E09-001 | E-09 | numerical | `test_continuous_*` | covered | discretization MVP |
| E10-001 | E-10 | semantic | LISS-0067 Red | covered | multi-register |
| E11-001 | E-11 | semantic | SV-19+ / binder Reds | covered | finite binders |
| E12-001 | E-12 | semantic | SV-31 | covered | modules / visibility |
| E13-001 | E-13 | provenance | examples B13 / Host Reds | deferred | Host Job boundary |
| E14-001 | E-14 | provenance | scope / workflow Reds | deferred | scientific scopes |

## 5. Verification plan

- Phase 1 Red: catalog presence + schema + E-01…E-14 coverage tests
  (`tests/test_conformance_slice_b_red.py`); expect missing/incomplete catalog.
- Phase 2 Green: publish catalog markdown satisfying Red (refine draft rows;
  no language semantics change).
- Phase 3 Refactor: readability only.
- Slice C (later): fill highest `gap` rows Adjudicator selects.

## 6. Explicit non-goals

- Changing SV suite assertions.
- Filling all `gap` rows in Slice B Green (that is Slice C).
- Rust differential (Slice D / LISS-0070).
- Report-write policy (Slice A, already shipped).
