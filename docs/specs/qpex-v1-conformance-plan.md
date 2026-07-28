# QPex versioned conformance plan (LISS-0071)

| Field | Value |
|---|---|
| Status | **Slice B plan proposed** (2026-07-28); Slice A complete |
| Authority | WP-0025; ADR 0106 D12; [`qpex-v1-acceptance-envelopes.md`](qpex-v1-acceptance-envelopes.md); [`qpex-spec-verification-protocol.md`](../testing/qpex-spec-verification-protocol.md) |
| Depends on | LISS-0068 **promoted**; LISS-0070 **deferred** (no Rust differential in this Issue) |
| Last updated | 2026-07-28 |

This companion freezes the **LISS-0071** design intake. It does not authorize
Phase 1 Red until plan approval.

## 1. Goals

1. Make every normative language claim **falsifiable** via a stable scenario id
   (or an explicit deferral).
2. Establish a **Python-reference oracle** (`compiler/qpex/` +
   `tests/spec_verification/`) as the sole differential target for this Issue.
3. Publish a suite taxonomy: valid / invalid / semantic / numerical /
   provenance / backend.
4. Close **DR-011**: verification protocol index matches the harness (SV-01–
   SV-31; note SV-12 gap if intentional).
5. Stop ordinary local runs from creating **uncommitted report drift**
   (`reports/latest.*` timestamp churn).

## 2. Suite taxonomy (Normative for planning)

| Class | Meaning | Primary oracle |
|---|---|---|
| **valid** | Program accepted; AST/IR/runtime behavior matches envelope | compile + run / inspect |
| **invalid** | Program rejected with a named diagnostic code | `assertCompileError` |
| **semantic** | Non-numerical language rules (NLTS, early collapse, visibility, …) | SV assertions / diagnostics |
| **numerical** | Amplitudes, norms, expectations within stated ε | `assertNormEquals`, `assertSuperposition`, expect |
| **provenance** | Inspection / observation metadata without hidden measure | inspect / JobResult fields |
| **backend** | Target/capability boundaries (cpu / qpu:openqasm3 / reject) | CLI `--target`, emit-qasm |

### Numerical policy (initial)

- Default absolute ε: `1e-12` (existing protocol).
- Suite may declare a wider ε only when the envelope documents why.
- Seeded RNG cases must pin `--seed` (or harness seed) for determinism.
- Nondeterministic Host/provider paths are **out of Kernel conformance**
  (Host lane envelopes stay separate).

### Oracle rule

- Public oracle = reviewed scenarios + Python Shipping Kernel behavior.
- Implementation-private dicts / ad-hoc fixtures are **not** oracles until
  promoted into the versioned catalog.

## 3. Mapping spine (existing artifacts)

```text
qpex-language-specification.md v1.0
  → qpex-v1-acceptance-envelopes.md  (E-01 … E-14)
  → tests/spec_verification/suites/svXX_*.py  (SV-01 … SV-31)
  → reports (CI-gated; see Slice A)
```

First Red/Green work invents no new language semantics; it **indexes and
gates** what already ships.

## 4. Planned slices

| Slice | Scope | Gate |
|---|---|---|
| **A** | DR-011 protocol index sync + report-drift policy | **complete** |
| **B** | Versioned claim→scenario catalog (E-envelope × taxonomy × SV id; deferrals explicit) | **plan proposed** |
| **C** | Fill highest-gap envelope coverage (docs-first map, then Red only for missing scenarios Adjudicator selects) | after B |
| **D** | (Deferred) Rust differential harness — **blocked on LISS-0070** | out of Issue |

### Slice A detail

- Update `qpex-spec-verification-protocol.md` header / category table through
  SV-31 (and document SV-12 absence).
- Choose one drift policy (Adjudicator confirms in checklist):
  1. **gitignore** `reports/latest.*` and emit only under CI artifact upload; or
  2. **CI-only write** with local runs using `--no-write-report`; or
  3. **committed golden** without timestamps (content-addressed).
- Recommended default for plan: **(2)** local `--no-write-report` default + CI
  writes artifacts (minimal behavior change for humans reading reports in CI).

### Slice B detail

- New companion (proposed path):
  `docs/specs/qpex-v1-conformance-scenario-catalog.md`
- Rows: `scenario_id`, envelope `E-*`, taxonomy class, SV suite / case,
  status (`covered` / `gap` / `deferred`).
- Authority: envelopes win over informal suite titles when they disagree.

## 5. Explicit non-goals

- Rust IR / MLIR / LISS-0070 resumption.
- CST / formatter / EBNF catch-up (LISS-0072).
- NFC on read (LISS-0069 follow-up).
- Changing accepted language semantics.
- Bulk rewrite of `examples/` solely for conformance cosmetics.

## 6. Acceptance envelopes (Issue-level)

### EARS

When a normative v1 language claim is listed as covered, the system shall
provide a stable scenario id that a Python-reference run can pass or fail.

When a claim is not yet covered, the catalog shall mark it `gap` or
`deferred` with an owner Issue — not leave it implicit.

When ordinary developer SV runs execute, they shall not force uncommitted
timestamp-only churn of `reports/latest.*` under the approved drift policy.

### Gherkin (Slice A foreshadow)

```gherkin
Feature: Conformance index and report drift

  Scenario: Protocol lists harness suites
    Given the shipping SV harness modules through SV-31
    When the verification protocol index is read
    Then every shipped suite id appears (or SV-12 is explicitly marked absent)

  Scenario: Local run does not dirty report timestamps
    Given the approved report-drift policy
    When a developer runs the SV harness locally under default flags
    Then git status does not show timestamp-only report churn
```

## 7. Verification plan

- This PR: documentation only.
- After plan approval: Slice A Phase 1 Red (protocol/index + drift tests or
  policy fixtures) — stop before Green unless batch-approved.
- Full SV 160/160 remains green throughout; do not weaken assertions to force
  catalog completeness.

## 8. Name lock

- Issue remains **LISS-0071**.
- Catalog companion name: `qpex-v1-conformance-scenario-catalog.md`.
- Oracle name: **Python-reference** (not “legacy”).
