# LISS-0076: Body-level scientific phase typing

## Metadata

- Local issue ID: LISS-0076
- GitHub issue: not created
- Status: **complete** — Slices A–E (2026-07-29)
- Phase: Feature Path / Slice E closeout reviewed locally
- Type: language feature / type system / scientific scopes
- Priority: P0
- Planning size: XL (sliced A–E)
- Owner/agent: —
- Related branch: `feature/liss-0076-slice-a`
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on:
  - [LISS-0068](LISS-0068-staqex-v1-normative-rebaseline.md) **complete** (promoted)
  - [LISS-0034](LISS-0034-phase-separated-scientific-scopes.md) **Phase 3** —
    sealed contracts shipped; body-level owned here (**complete**)
  - [LISS-0080](LISS-0080-phase-resolved-typed-hir.md) **complete** (`HirDecl.phase`)
- Related: [staqex-scientific-scopes.md](../specs/staqex-scientific-scopes.md);
  ADR 0106 D1 (five phases). **Not** ADR 0076 (numeric representation).
- Unlocks: LISS-0077 (with LISS-0082), LISS-0078, LISS-0079
- Residuals: [LISS-0118](LISS-0118-body-phase-typing-residuals.md)
  (Report matrix / transitive taint / short-name policy). **Not** LISS-0116.

## Motivation

[LISS-0034](LISS-0034-phase-separated-scientific-scopes.md) sealed top-level
`theory` / `experiment` / `workflow` / `execution` / `report` contracts and
dependency direction. Theory bodies still rejected only a fixed lexeme set
(`shots` / `backend` / `retry` / `Host`). Expression-level references to
Execution symbols could leak without a **phase** diagnostic.

WP-0025 acceptance: phase leaks must produce **phase diagnostics**, not
unresolved-name or generic type errors — across expression bodies, imports,
generic calls, and methods.

## Dependency resolution

| Dep | Status | Action |
|---|---|---|
| LISS-0068 | complete | Recorded |
| LISS-0034 | Phase 3; body-level → this Issue | **complete** via A–E |
| LISS-0080 | complete | Used for phase context |

## Scope

### In scope (shipped)

- Walk scientific-scope `body_declarations` under a phase context.
- Detect Execution symbol use inside Theory/Experiment/Workflow with
  `PHASE_TYPE_VISIBILITY_ERROR`.
- Keep lexeme `PHASE_SCOPE_DEPENDENCY_ERROR` for `shots`/`backend`/…
- Import / module boundary phase (Slice C).
- Call / method leak paths (Slice D).
- Diagnostic catalog + Gherkin closeout (Slice E).

### Out of scope

- Dynamic QPU / `Controller<T>` (LISS-0077).
- Physics IR / Quantum Semantic IR (LISS-0081 / 0082; active claims
  LISS-0115–0117).
- Replacing sealed scope graph rules from LISS-0034.
- Report-phase body matrix; transitive helper taint; short-name taint policy
  → [LISS-0118](LISS-0118-body-phase-typing-residuals.md).

## Acceptance criteria (Gherkin)

Normative copy: [`staqex-scientific-scopes.md`](../specs/staqex-scientific-scopes.md) §5.1.
Envelope: E-14 in [`staqex-v1-acceptance-envelopes.md`](../specs/staqex-v1-acceptance-envelopes.md).

Automated: `tests/test_body_phase_slice_{a,b,c,d}_red.py`.

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Theory body vs Execution symbol | **complete** |
| **B** | Experiment/Workflow ↔ Execution matrix | **complete** |
| **C** | import / module-boundary | **complete** |
| **D** | call / method leak paths | **complete** |
| **E** | catalog, Gherkin, register closeout | **complete** |

### Slice E (shipped)

- [`staqex-scientific-scopes.md`](../specs/staqex-scientific-scopes.md) — body-level
  accepted + Gherkin §5.1
- [`staqex-v1-diagnostic-catalog.md`](../specs/staqex-v1-diagnostic-catalog.md) —
  `PHASE_TYPE_VISIBILITY_ERROR` cites 0076
- [`staqex-v1-acceptance-envelopes.md`](../specs/staqex-v1-acceptance-envelopes.md)
  E-14 — lexeme vs body-level codes corrected/extended

## Implementation map

- `compiler/staqex/scientific_scopes.py` — visibility + call/method taint
- `compiler/staqex/modules.py` — merge scientific scopes on import
- `compiler/staqex/pipeline.py` — pass `unit_decls` into scope resolution
- Tests: `tests/test_body_phase_slice_{a,b,c,d}_red.py`

## Adjudicator Decision Points

- [x] Approve Issue ID **LISS-0076**, dependency resolution, and slices A–E
- [x] Confirm Slice A first Red after plan intake (`PHASE_TYPE_VISIBILITY_ERROR`)
- [x] Authorize Slice B (Experiment/Workflow ↔ Execution matrix)
- [x] Authorize Slice C (import / module-boundary phase)
- [x] Authorize Slice D (generic call / method leak paths)
- [x] Authorize Slice E (catalog / Gherkin closeout)
