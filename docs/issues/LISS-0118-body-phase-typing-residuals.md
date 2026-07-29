# LISS-0118: Body-level phase typing residuals

## Metadata

- Local issue ID: LISS-0118
- Status: **complete** — Slices A–C shipped 2026-07-29
- Phase: Feature Path / Issue completion (pending Adjudicator merge)
- Type: language feature / type system / scientific scopes
- Priority: P2
- Planning size: M
- Parent: [LISS-0076](LISS-0076-body-level-scientific-phase-typing.md) **complete**
- Related branch: `feature/liss-0118-slice-a`
- Related: [staqex-scientific-scopes.md](../specs/staqex-scientific-scopes.md)

## Claim notice

**Do not reuse `LISS-0115`–`LISS-0117` for this work.** Those IDs are claimed
by the Physics IR track. This Issue owns 0076 residuals only.

## Motivation

LISS-0076 A–E shipped Execution-symbol visibility for Theory/Experiment/Workflow
bodies, imports, and one-hop call/method taint. Deferred items remained as
explicit Non-goals in the scientific-scopes spec; this Issue closes them.

## In scope

- Report-phase body visibility matrix (Report may see Execution; blocked
  phases must not see Report-bound symbols when introduced)
- Transitive helper taint (call graph deeper than one hop)
- Tighten unqualified method-name taint / short-name collision policy
  (verify post-0076 qualified-name matching; close remaining gaps)

## Out of scope

- Dynamic QPU (LISS-0077)
- Physics IR (LISS-0081 / LISS-0115–0117)
- ADR unless an irreversible taint policy must be locked first

## Slices

| Slice | Scope | Size | Status |
|---|---|---|---|
| **A** | Transitive call taint: Theory calls `mid()` → `leak()` that names Execution symbol → `PHASE_TYPE_VISIBILITY_ERROR` | S | **complete** |
| **B** | Report ↔ Execution visibility (Report may reference Execution; Theory/Exp must not see Report symbols) | S | **complete** |
| **C** | Short-name policy verification + catalog/Gherkin closeout | S | **complete** |

### Slice A (shipped)

- Tests: [`tests/test_body_phase_slice_a_0118_red.py`](../../tests/test_body_phase_slice_a_0118_red.py)
- Implementation: fixpoint over fn/method call edges in
  `scientific_scopes._execution_tainted_callables`; `OpCall` names count as
  call targets (e.g. `return leak()`)

### Slice B (shipped)

- Tests: [`tests/test_body_phase_slice_b_0118_red.py`](../../tests/test_body_phase_slice_b_0118_red.py)
- Report may reference Execution symbols; Theory/Experiment/Workflow must not
  reference Report-bound symbols (`PHASE_TYPE_VISIBILITY_ERROR`)

### Slice C (shipped)

- Tests: [`tests/test_body_phase_slice_c_0118_red.py`](../../tests/test_body_phase_slice_c_0118_red.py)
- Methods keyed as `Class.method` only; bare short names fail closed when any
  `*.name` / FunDecl peer is execution-tainted (`_call_target_is_tainted`)
- Qualified clean methods (`Pure().k()`) remain precise against tainted peers
- Spec §4.1 / §5.1 / Non-goals, diagnostic catalog, E-14 envelope updated

## Adjudicator Decision Points

- [x] Approve plan intake / slices for LISS-0118
- [x] Confirm no ADR required (default: Issue + spec Non-goals sufficient)
- [x] Authorize Slice B (Report ↔ Execution matrix)
- [x] Authorize Slice C (short-name / catalog closeout)
- [x] Approve Issue completion / merge PR
