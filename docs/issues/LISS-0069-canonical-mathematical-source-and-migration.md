# LISS-0069: Canonical mathematical source and migration

## Metadata

- Local issue ID: LISS-0069
- GitHub issue: not created
- Status: **plan proposed** (2026-07-28); awaiting Adjudicator plan approval before Phase 1 Red
- Phase: phase-0-design
- Type: language surface / lexer / migrator
- Priority: P0
- Initial planning size: XL
- Current planning size: XL (sliced)
- Owner/agent: unassigned after plan approval
- Related branch: `feature/liss-0069-unicode-math-source`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E0→E1
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted** (v1.0 spec)

## Summary

Introduce the ADR 0106 / ADR 0095 **canonical UTF-8 NFC mathematical spelling**
for Dirac, adjoint, and tensor tokens as a **dual-accept** surface, with a
deterministic migrator contract and golden corpus. ASCII forms remain valid
until a later deprecate/remove gate. ASCII Pauli atoms are **not** removed in
this Issue’s first slice.

Companion surface contract:
[`qpex-unicode-math-source.md`](../specs/qpex-unicode-math-source.md).

## Acceptance Notes (Issue complete when)

1. Unicode ket/bra close and open delimiters, `†`, and `⊗` parse to the same
   AST/IR nodes as the current ASCII spellings (`|…>`, `adjoint(…)`, `*|*`).
2. Pipeline `|>` never collides with ket close `⟩` (U+27E9) at the lexer.
3. Source is NFC-normalized on read for identifier and math-token comparison
   (or an equivalent documented boundary).
4. A migrator (CLI or library entry) rewrites ASCII Dirac/tensor/adjoint forms
   to canonical Unicode while preserving comments and spans in golden fixtures.
5. SV / official examples remain green under dual-accept (no forced example
   rewrite in the first Red/Green slice).
6. M-P01 Pauli ASCII removal and M-P05 `state` sugar are **out of scope** for
   the first approved slice (separate deprecate gates / Issues).

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Lexer dual-accept: `\|ψ⟩` / `⟨φ\|`, `⊗`, postfix `†`; NFC read; `\|>` vs `⟩` | plan → Red → Green → Refactor |
| **B** | Migrator library + `tests/fixtures/migration/` goldens for M-P02–M-P04 | after A |
| **C** | CLI `migrate` (name TBD) + formatter-emit preference (or defer emit to LISS-0072) | after B |

Slice A is the only slice requested for the first plan approval. B/C require
follow-up phase approval on the same Issue branch (per branch discipline).

## Non-goals (first slice A)

- Removing ASCII Pauli `X`/`Y`/`Z`/`I` (M-P01).
- Migrating `state` → `State<T>` sugar (M-P05).
- Editor macros `\ket` / `\bra` as language syntax.
- Full UAX #31 identifier adoption beyond NFC + confusable diagnostic stub
  (confusable diagnostics may land as warn-only or hard codes TBD in Red).
- Lossless CST / full formatter (LISS-0072).
- Named Dirac algebra AST expansion (LISS-0073) beyond token→existing nodes.

## Dependencies

- ADR 0106 Unicode migration scope (Accepted with conditions)
- ADR 0095 ideal-form-first
- [`qpex-v1-migration-matrix.md`](../specs/qpex-v1-migration-matrix.md) M-P02–M-P04
- [`qpex-language-specification.md`](../specs/qpex-language-specification.md) v1.0 §2
- Shipping lexer: `compiler/qpex/lexer.py` (`KET`, `TENSOR_OP`, `PIPE_OP`)

## Adjudicator Decision Points (plan)

- [ ] Approve **Slice A** plan (lexer dual-accept only) for Phase 1 Red.
- [ ] Confirm ASCII ket `|0>` and Unicode `|0⟩` lower to the **same** `KetLit`
      (label payload unchanged).
- [ ] Confirm `⊗` is an alternate spelling of `*|*` (`TENSOR_OP`), same precedence.
- [ ] Confirm postfix `†` is an alternate spelling of `adjoint(expr)` call form
      (same AST after desugar), not a new operator semantics.
- [ ] Confirm bra `⟨φ|` may land in Slice A as **parse→existing bra/inner path**
      or be deferred to Slice A.1 if current AST lacks a bra primary — agent must
      report which after design probe (see plan note below).
- [ ] Confirm Slice B/C are **not** authorized by Slice A plan approval.
- [ ] Implementation allowed after plan approval: **yes for Slice A Red only**
      until Red is reviewed; Green requires usual phase progression (Claude
      Issue-level autonomy may batch Red→Green→Refactor after plan approval
      **only if** Adjudicator grants that batch; default is stop after Red).

### Plan note — bra surface probe

Current shipping lexer recognizes ASCII ket `|label>` and tensor `*|*`. There
is no Unicode ket close and no bra token yet. Slice A Red must either:

1. add bra tokens that desugar to the existing function-shaped bra/inner API
   already used in operator algebra; or
2. defer bra to a follow-up Red module if no stable AST primary exists.

The plan approval may choose **(1) preferred** or **(2) defer bra**.

## Context

- Included: ADR 0106 acceptance Unicode section; migration matrix M-P01–M-P05;
  language spec §2; lexer ket/tensor/pipe paths; SV 160/160 baseline at tag
  `v0.1.0`.
- Omitted: Rust lexer (LISS-0070); full CST formatter (LISS-0072); provider /
  Host; secrets.
- Assumptions: Python Kernel remains reference; dual-accept does not change
  Joint semantics; migrator is deterministic and offline.

## AI Planning Record

### AIP-0069-001

- Status: proposed
- Created at: 2026-07-28
- Planning size: XL (sliced; Slice A = L)
- Intended execution route: Feature Path after plan approval
- Intended scope: Slice A lexer dual-accept + diagnostics; later B/C migrator
- Confidence: high on ket/tensor/`|>` boundary; medium on bra AST wiring
- Superseded by: none

## Work Notes

- 2026-07-28: Issue opened; plan proposed after LISS-0068 v1.0 promotion.
- Next: Adjudicator plan approval for Slice A → Phase 1 Red on this branch.

## Verification

- Plan phase: documentation-only until plan approval.
- After Red: failing lexer/parser tests for Unicode forms; no production Green
  until Red reviewed (unless batch autonomy granted).
