# QPex v1 migration and removal matrix

| Field | Value |
|---|---|
| Status | **Promoted** — normative companion of [`qpex-language-specification.md`](qpex-language-specification.md) v1.0 (2026-07-28) |
| Owner | LISS-0068 / WP-0025 E0; execution LISS-0069+ |
| Authority | ADR 0106 acceptance record; [`qpex-v1-normative-rebaseline-register.md`](qpex-v1-normative-rebaseline-register.md) |
| Last updated | 2026-07-27 |

This matrix names every **breaking** v1 migration, its staged removal contract,
and the Issue that owns implementation. It completes LISS-0068 E0 documentation.
No removal dates are activated by this document alone.

## 1. Migration policy

Per ADR 0106 (Accepted with conditions, 2026-07-27):

1. **No flag-day breaking change** without a reviewed migrator and conformance
   corpus update.
2. **Stages:** `dual-accept` → `deprecate` (diagnostic or formatter warning) →
   `remove` (major version bump only).
3. **No permanent compatibility aliases** for surfaces classified `breaking`
   (ADR 0095).
4. **Python reference Kernel** remains authoritative until Rust passes the same
   differential oracle (LISS-0071).
5. **Promotion** of v1 normative text requires every `remove` row to be either
   completed or explicitly deferred with Adjudicator record.

## 2. Matrix — completed migrations (v0.1 era)

These breaking migrations are **already shipped**. They are recorded here so v1
rebaseline does not reopen them.

| ID | v0.1 / legacy | v1 canonical | Owner | Removal of legacy | Status |
|---|---|---|---|---|---|
| M-C01 | `fun` keyword | `fn` | LISS-0023 / ADR 0066 | `RETIRED_KEYWORD` | **complete** |
| M-C02 | `public` visibility | `pub` | LISS-0024 / ADR 0067 | `RETIRED_KEYWORD` | **complete** |
| M-C03 | `observe` | `measure` | ADR 0035 | `RETIRED_KEYWORD` | **complete** |
| M-C04 | `span` (when sugar) | `when` | ADR 0024 | `RETIRED_KEYWORD` | **complete** |
| M-C05 | `Z(0)` operator index | `Z[0]` | LISS-0054 | `RETIRED_OPERATOR_INDEX_SYNTAX` | **complete** |
| M-C06 | `register(N)` surface | `QubitRegister<N>` | LISS-0029 / ADR 0069 | parse/type rejection | **complete** |
| M-C07 | implicit `main` result | `pub fn main() -> Unit` | LISS-0021 / ADR 0064 | compile-time requirement | **complete** |
| M-C08 | hidden Operator harvest | explicit `return` | LISS-0025 / ADR 0068 | `LEXICAL_SCOPE_ERROR` path | **complete** |

## 3. Matrix — planned north-star migrations

| ID | Drift | v0.1 / current | v1 canonical | Owner | Stage | Dual-accept | Deprecate | Remove gate |
|---|---|---|---|---|---|---|---|---|
| M-P01 | DR-006 (Pauli) | ASCII `X`/`Y`/`Z`/`I` atoms | Unicode operator notation (when distinct from ASCII Latin) | LISS-0069 | dual-accept | **now** | after migrator + SV parity | major bump post-LISS-0069 |
| M-P02 | DR-006 (Dirac) | `\|0>`, `\|+>` ASCII kets | `\|0⟩`, `\|ψ⟩` Unicode kets | LISS-0069 | dual-accept | formatter emits Unicode | `RETIRED_*` or warn-only diagnostic TBD | major bump |
| M-P03 | DR-006 (tensor) | `*\|*` tensor infix | `⊗` | LISS-0069 | dual-accept | both parse | formatter prefers `⊗` | major bump |
| M-P04 | DR-006 (adjoint) | `adjoint(H)` / ASCII dagger spellings | `H†` | LISS-0069 | dual-accept | both parse to same IR | formatter emits `†` | major bump |
| M-P05 | DR-007 | `state name = expr` sugar | `State<T> name = expr` Type-First | LISS-0069 or split Issue | deferred | `state` remains valid | TBD warning | separate Issue after Pauli/Dirac |
| M-P06 | north-star §16 | function-shaped Dirac algebra surface | canonical tokens lowering to same nodes | LISS-0069+ | design | preserve semantics | surface warning | major bump |
| M-P07 | north-star §16 | `dynamic qpu {` rejection sketch | `dynamic qpu fn` typed lane | LISS-0028+ execution | additive first | static rejection remains | new syntax additive | N/A (additive) |

### M-P01–M-P04 notes (LISS-0069 first slice)

- **Do not remove ASCII Pauli** in LISS-0069 Phase 1. Pedagogy (`grid_oscillator`,
  SV-29/30) depends on `X`/`P` quadrature atoms.
- **Migrator contract:** deterministic rewrite; comments and spans preserved;
  golden corpus under `tests/fixtures/migration/` (to be created in LISS-0069).
- **Formatter** emits canonical Unicode for Dirac/adjoint/tensor; does not
  rewrite Pauli atoms until M-P01 deprecate gate passes.

### M-P05 notes (`state` keyword)

- Classified **breaking** but **deferred** per ADR 0106 acceptance (out of
  LISS-0069 initial scope).
- NLTS semantics unchanged; spelling-only migration.
- Recommend separate Issue `LISS-007x` after Unicode Dirac slice lands.

## 4. Matrix — documentation-only reconciliations (non-breaking)

These drift rows required v1 spec reconciliation but **no source migration**.

| ID | Drift | Resolution | Status |
|---|---|---|---|
| D-R01 | DR-001 | Header ADR index → 0105; SV → 31 | slice 2 outline |
| D-R02 | DR-002 | Lane table in §1.2 | slice 2 outline |
| D-R03 | DR-003 | Axioms + §1.2 `return` | slice 2 + axioms patch |
| D-R04 | DR-004 | open-work-register sync | WP-0027 / ongoing |
| D-R05 | DR-005 | Issue status authoritative | README umbrella sync (partial) |
| D-R06 | DR-008–010 | Additive spec sections at promotion | slices 2–4 |
| D-R07 | DR-011 | SV index sync | LISS-0071 |
| D-R08 | DR-012 | Provider routing deferral recorded | ADR 0105 |

## 5. Version bump gates

| Gate | Requirement |
|---|---|
| **v1.0 normative promotion** | **complete** 2026-07-28 — outline + catalog + envelopes referenced from `qpex-language-specification.md` v1.0 |
| **v1.0 major breaking removal** | All targeted `remove` rows have migrator + golden corpus + Adjudicator sign-off |
| **v1.1+ minor** | Additive diagnostics and envelopes only |
| **v2.0 major** | May activate M-P01–M-P06 removal tranche |

## 6. Corpus and tooling obligations

| Artifact | Owner | Purpose |
|---|---|---|
| `tests/fixtures/migration/v0.1/` | LISS-0069 | Input golden sources |
| `tests/fixtures/migration/v1/` | LISS-0069 | Expected migrated output |
| Formatter round-trip tests | LISS-0069 / LISS-0072 | parse-format-parse stability |
| SV regression | LISS-0071 | No behavior change during dual-accept |
| `qpex migrate` CLI | LISS-0069 Slice C | One-file rewriter (`--write` / `--check` / stdout); see [`qpex-unicode-math-migrate-cli.md`](qpex-unicode-math-migrate-cli.md) |

## 7. LISS-0068 E0 completion checklist

| Slice | Deliverable | Status |
|---|---|---|
| 1 | Drift register + ADR inventory | **complete** |
| 2 | §1–§2 normative outline | **complete** |
| 3 | Diagnostic catalog (K/B/H/V) | **complete** |
| 4 | Acceptance envelopes E-01–E-14 | **complete** |
| 5 | Migration/removal matrix (this doc) | **complete** |

### E0 exit gate (documentation)

- [x] ADR 0013–0105 mapped or deferred with owner.
- [x] Contradictions named with resolution authority (drift register).
- [x] Breaking migrations have removal contract (this matrix).
- [x] No compiler implementation in LISS-0068 slices.
- [x] Adjudicator review of E0 package for promotion to v1 spec merge Issue (2026-07-27).
- [x] Trace filed (`2026-07-27-liss-0068-rebaseline-slice5.md`,
  `2026-07-27-liss-0068-e0-adjudicator-completion.md`).

### Follow-on Issues (implementation — not LISS-0068)

| Issue | Scope |
|---|---|
| LISS-0069 | Unicode math — Slice A/B **complete**; Slice C CLI **Phase 2 Green** |
| LISS-0071 | Conformance harness + SV index sync (DR-011) |
| LISS-0072 | CST / formatter / source version markers (+ EBNF catch-up) |
| Promotion PR | **complete** — `qpex-language-specification.md` v1.0 |

## 8. Risk register

| Risk | Mitigation |
|---|---|
| Premature Pauli ASCII removal breaks SV/examples | M-P01 dual-accept until explicit remove gate |
| `state` migration churns entire examples tree | M-P05 deferred to separate Issue |
| Host diagnostics mistaken for Kernel conformance | Catalog appendix split (slice 3) |
| Second semantics during Rust port | D12 + LISS-0071 differential oracle |
