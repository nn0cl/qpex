# Trace: LISS-0118 Slice C + Issue completion closeout

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0118 |
| Slice | C — short-name policy + catalog/Gherkin closeout |
| Phase | phase-1-red → phase-2-green → phase-3-refactor / Issue complete |
| Branch | `feature/liss-0118-slice-a` |
| Approval | Adjudicator Slice C (“承認”) |

## [DESIGN CHECK]

- Scope: methods keyed as `Class.method` only; bare short names fail closed
  when any peer FunDecl / `*.name` is execution-tainted; qualified clean
  methods stay precise; catalog/Gherkin/Non-goals closeout.
- Specs: `staqex-scientific-scopes.md` §4.1 / §5.1 / §6; E-14; diagnostic
  catalog; open-work-register; WP-0025; local-issue-planning.
- Verification: `tests/test_body_phase_slice_c_0118_red.py` + A/B/0076 suite.

## Delivered

- `_call_target_is_tainted` + Class.method-only registration in
  `scientific_scopes.py`
- `tests/test_body_phase_slice_c_0118_red.py`
- Spec / catalog / envelope / register / Issue **complete**

### 変更の要約 (PR Summary)

- **何を目的として何を変更したか**: 短名衝突を fail-closed に固定し、
  修飾呼び出しの精密性を保ったうえで 0076 残差 Issue を閉じた。

### 残存リスク・検証の溝 (Verification Gap)

- **AIが推測で補った部分**: bare `k()` の fail-closed は意図的 over-approx。
- **人間がコードレビューで重点的に見るべきポイント**:
  `_call_target_is_tainted` の `endswith(".name")` と fixpoint 連動。

## Next safe action

Adjudicator コミット／PR／merge 承認。
