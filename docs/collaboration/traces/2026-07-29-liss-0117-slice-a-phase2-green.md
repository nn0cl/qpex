# Trace: LISS-0117 Slice A Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0117 |
| Slice | A — fixture loader |
| Phase | Phase 2 Green |
| Branch | `feature/liss-0117-slice-a` |
| Approval | Adjudicator (“承認”) after Red |

## Delivered

- `compiler/staqex/physics_ir_goldens.py`
- `tests/fixtures/physics_ir/PIR-G-*.json` (six families)
- Catalog remaining-work note updated (oracle still gated)

### 変更の要約 (PR Summary)
- **何を目的として何を変更したか**: 6 家族の fixture スナップショットを読む
  ローダを追加し、provenance 欠落を診断する。

### 残存リスク・検証の溝
- snapshot は synthetic JSON（source からの lowering は Slice B）。
- catalog 文言「not a promoted runtime oracle」にテストが依存。

## Verification

`python3 tests/test_physics_ir_goldens_slice_a_red.py` PASS

## Next safe action

Adjudicator Slice A 完了 → コミット／PR、または Slice B（0115 連携）計画。
