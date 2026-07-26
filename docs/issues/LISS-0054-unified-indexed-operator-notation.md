# LISS-0054: Unified indexed-operator notation `Op[index]`

## Metadata

- Local issue ID: LISS-0054
- GitHub issue: none
- Status: complete
- Phase: phase-3-refactor complete (ADR 0096 D1 accepted)
- Type: breaking surface change + grammar unification
- Priority: P1
- Initial planning size: L
- Current planning size: L
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Unify indexed operator application on brackets — `Z[i]`, `X[0]`,
`create[p]`, `annihilate[q]` — valid everywhere an operator expression is
valid, for every operator family. Retire the parenthesised form with a hard
diagnostic and **no alias**, per [ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md) D1.

This is the project's first deliberately breaking surface change. It is
accepted under [ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md):
the migration is paid once now rather than by every program written from
here on.

## Current state (measured 2026-07-26)

| Concept | Spelling A | Spelling B |
|---|---|---|
| Pauli on site *k* | `Z[k]` — canonical in every operator position | `Z(k)` — retired with `RETIRED_OPERATOR_INDEX_SYNTAX` |
| Creation on orbital *p* | `create[p]` — canonical in every second-quantized position | `create(p)` — legacy spelling covered only by compatibility-history tests |

The former dual grammar was collapsed: bracketed operator references now use
`OpIndexed` in the Operator and second-quantized paths, and the existing
runtime/QASM consumers receive the same shape. Name-resolved user callables
such as `fn Z(...)` remain ordinary generic calls.

## Acceptance notes

- [x] `Op[index]` parses and lowers identically in every position an
      operator expression is valid: `Operator` binds, second-quantized
      family binds, binder bodies, and function bodies.
- [x] Bare unindexed atoms (`X`, `Y`, `Z`, `I`) keep their current
      single-qubit/global meaning, unchanged.
- [x] The retired parenthesised form produces an **actionable** diagnostic
      naming the replacement (e.g. "`Z(k)` is retired; write `Z[k]`"), per
      the bar set in LISS-0049.
- [x] **The diagnostic is name-resolution aware.** `f(x)` in general keeps
      working, and a legitimate user-defined callable named `Z` is **not**
      rejected on the strength of its name. The diagnostic fires from name
      resolution, or from the context in which the retired syntax was
      previously valid — never from the identifier alone. A regression test
      covers a user-defined function whose name collides with an operator
      atom.
- [x] **The dual grammar is collapsed, not merely re-spelled**: an operator
      reference is a **single AST node** after this change, regardless of
      surface position. Re-spelling while leaving two grammars would let the
      same divergence reappear in semantic analysis.
- [x] `examples/`, `tests/`, and `docs/specs/` are migrated in the same
      change; no file retains the parenthesised spelling.
- [x] No alias, no deprecation window, no compatibility flag.

## Non-goals

- Binder body expressiveness (LISS-0055).
- Empty domains, `where`, `product` semantics (LISS-0055, LISS-0056).
- Replacing qubit-count inference (LISS-0058).

## Dependencies

- Parent: none
- Depends on: **LISS-0052** (supplies the `OpIndexed` execution handler this
  issue's unified notation relies on)
- Related: ADR 0096 D1, ADR 0095 Decision 3, LISS-0051 (earlier fix to the
  same dual-grammar root cause, which unblocked `Z(0)` outside binders)
- Blocks: nothing; LISS-0055 is easier after the grammar is unified but does
  not strictly require it

## Adjudicator Decision Points

- [x] Approve Phase 1 Red.
- [x] Confirm the retirement diagnostic's code name and message text
      (proposal: `RETIRED_OPERATOR_INDEX_SYNTAX`).
- [x] Confirm the migration may touch `examples/`, `tests/`, and
      `docs/specs/` in the same reviewable unit — the alternative (staged
      migration) would require a temporary alias, which D1 forbids.

## Context

- Included: `compiler/qpex/parser.py` (`_type_first_bind`, `_op_primary`,
  `_expression`), `compiler/qpex/ast_nodes.py` (operator reference nodes),
  `compiler/qpex/typecheck.py`, `compiler/qpex/runtime/sparse_pauli.py`,
  `compiler/qpex/second_quantization.py`, plus every `examples/`, `tests/`,
  and `docs/specs/` file using the parenthesised form.
- Omitted: QASM emitter internals (consume the AST, unaffected by spelling).
- Assumption: collapsing to a single operator-reference AST node is
  achievable without redesigning the expression grammar wholesale; if that
  proves false, that is an unanticipated design decision and work stops for
  Adjudicator direction (per `CLAUDE.md` Issue-Level Autonomy).

## Verification

- Phase 1 Red: bracket form rejected or non-functional in at least one valid
  operator position; parenthesised form still accepted.
- Phase 2 Green: bracket form works in every position; parenthesised form
  diagnosed with the replacement named; a user-defined callable named `Z` is
  unaffected; migrated examples run and emit QASM as before.
- Full regression sweep and spec verification stay green.

## Work Notes

- 2026-07-26: Opened from ADR 0096 D1. The two constraints in the acceptance
  notes (name-resolution-aware diagnostic; collapse the grammar rather than
  re-spell) came from the independent design review and are the difference
  between fixing this defect and relocating it.
- 2026-07-26: Phase 1 Red, Phase 2 Green, and Phase 3 migration completed.
  Bracketed references are consumed as `OpIndexed` across Pauli and
  second-quantized paths; examples and regression tests use the canonical
  form.
