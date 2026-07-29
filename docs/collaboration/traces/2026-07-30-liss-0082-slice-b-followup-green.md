# LISS-0082 Slice B follow-up 1 — Phase 2 Green and Phase 3 Refactor

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-b-red`
- Operating path: Feature Path
- Issue: LISS-0082
- Slice/phase: Slice B follow-up 1 (gaps 1, 2, 5) / Phase 2 Green + Phase 3
  Refactor
- Approval: Adjudicator message of 2026-07-30 approving follow-up 1 Green and,
  after Green confirmation, Refactor
- Implementation permission: **follow-up 1 gaps 1, 2, 5 only**
- Technology selection permission: **none**
- Post-review required: Adjudicator review before anything further

## Phase 2 Green

Only `compiler/staqex/quantum_semantic_ir.py` changed (52 insertions,
15 deletions).

- **Gap 1** — `_semantic_identities` became `_defined_identities` and now walks
  acting-space, factor, and Joint-value definition sites alongside the Slice A
  roots. References are excluded by construction, so a resource naming its own
  factor is not a redefinition. The message generalized from "duplicate semantic
  identity in module roots" to "semantic identity is defined more than once".
- **Gap 2** — `ActingSpace.origin` and Joint-value `origin` are validated with
  the existing `_origin_is_incomplete` predicate, reported as
  `QSEM_PROVENANCE_INCOMPLETE`.
- **Gap 5** — the resource check moved from arity to full ordered identity
  comparison against the space factors, still `QSEM_ACTING_SPACE_INVALID`. This
  subsumes the previous arity check rather than adding a second code.

No reviewed assertion was modified and no test file changed during Green.

## Phase 3 Refactor

Behavior-preserving only:

1. Extracted `_report_incomplete_origin`, removing the triplicated
   "predicate → append" block now that three definition sites share one ancestry
   predicate. Detail keys are passed before `origin=` so each diagnostic's key
   order is byte-identical to Green.
2. Corrected the module docstring of
   `tests/test_quantum_semantic_ir_slice_b_followup_red.py`. **Prose only** —
   `git diff -- tests/` touches zero lines containing `assert`.

Verified after Refactor that the three provenance diagnostics keep their exact
codes, messages, key order (`code, message, <detail>, origin`), and emission
order (root → acting space → Joint value).

## Documentation correction ordered by the Adjudicator

The plan claimed "Gaps 1, 2, and 5 … are not folded into the two Slice B codes",
which was inaccurate. Corrected in plan §4.2, in the follow-up Red trace, and in
the test docstring: **gaps 1 and 2 extend the Slice A diagnostics; gap 5 uses
the Slice B code `QSEM_ACTING_SPACE_INVALID`.**

## Deterministic verification

- `python3 tests/test_quantum_semantic_ir_slice_b_followup_red.py` —
  **10 passed / 0 failed** after Green and again after Refactor.
- `python3 tests/test_quantum_semantic_ir_slice_a_red.py` — passed throughout.
- `python3 tests/test_quantum_semantic_ir_slice_b_red.py` — passed throughout.
- `python3 -m py_compile compiler/staqex/quantum_semantic_ir.py` — passed.
- Full `tests/*.py` sweep: 97 pass / 47 fail at Green and at Refactor, with the
  failure set **identical** to the pre-Green baseline of 96 pass / 47 fail. The
  only change is this suite moving 8 fail → pass. The 47 failures are
  pre-existing and unrelated.
- `git diff --check` — clean.
- pytest is not installed; the direct entry point is the deterministic check.

## Remaining Slice B gaps

- **Gap 3** — bare integer `generation` removal, approved as option (a) but
  deferred to an Architecture Path update (ADR 0108 + detailed contract +
  Issue/plan) with its own reviewed Red. Untouched here.
- **Gap 4** — decided: no ordering field; cycle detection delegated to the
  Slice C region graph. No code change was required; the shipped message already
  states the violation as "more than one consuming path".

## Reviewer empathy summary

### 変更の要約 (PR Summary)

- **何を目的として何を変更したか**: Adjudicator 再レビューが挙げた Slice B の未検証
  5 法則のうち、設計判断を要さない 3 件を閉じました。恒等性検査を「定義サイト」概念で
  Slice B の acting space / factor / Joint value まで拡張し、参照は重複に数えない
  ことを構造として保証しています。埋め込み `SemanticOrigin` を既存の述語で検証し、
  `resources` の検査を個数一致から順序込みの恒等性一致へ強化しました。Refactor では
  3 箇所に重複した provenance 報告を 1 ヘルパーへ集約しています。

### 残存リスク・検証の溝 (Verification Gap)

- **AI が推測で補った部分**: 「定義サイト」と「参照サイト」の線引きは contract に
  明文がなく、私が Red で提案して承認を得た区分です。特に `producer_id` を参照側に
  置いた判断は、Slice C で producer が region として定義された時点で再確認が必要です。
- **人間がレビューで重点的に見るべきポイント**:
  1. `_defined_identities` の列挙漏れ。将来 Slice C で region を足したとき、ここへ
     追加し忘れると重複 region ID が黙って通ります。列挙が 1 箇所に集約されている
     ことが唯一の防御線です。
  2. gap 5 の強化は既存の arity 検査を**置換**しています。個数不一致は順序不一致の
     一種として同じコードで報告されますが、診断メッセージと詳細キーが
     `resource_count` / `factor_count` から `resources` / `factors` へ変わりました。
     この詳細キーに依存する下流は現時点で存在しませんが、Slice E の lowering が
     読む可能性があります。
  3. gap 3 未処理のため `generation` フィールドは残存し、依然として無検証です。
     値を入れても何も保証されない点は Slice C 着手前に解消すべきです。

## Stop condition

Stop after Refactor evidence. Do not start gap 3 Architecture Path work, gap 4
region-graph work, Slice C, a PR, or a push without separate approval.
