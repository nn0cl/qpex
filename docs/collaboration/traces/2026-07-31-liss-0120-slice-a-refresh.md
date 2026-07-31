# LISS-0120 Slice A refresh (gates open)

## Design check

- Scope: refresh LISS-0120 after P0-B foundation exits; publish Slice A
  review specification only; no `.sqx`, tests, or compiler changes.
- Inspected: LISS-0120 Issue; 2026-07-30 intake; WP-0025/0029 P0-C;
  ADR 0108–0111 Accepted; LISS-0082 complete; LISS-0094/0097/0077 complete;
  Noether Forge candidate already recorded on the Issue.
- Decision: full-review gates are open. Slice A docs may proceed. Slice B
  prototype remains a separate integrated Feature Path package.
- Verification: docs sync only.

## Also synchronized

- LISS-0077 P0 completion: PR #168 merge tip `84742bb`.

## Next approval

Phase 2 **Green** for Slice B: create `examples/applied/A11_noether_forge/`
prototype sources to satisfy the Red suite. Red does not authorize Green.

## Artifacts

- [staqex-v1-noether-forge-review-plan.md](../../specs/staqex-v1-noether-forge-review-plan.md)
- Issue / WP / register status updates
- Branch: `feature/liss-0120-language-review-gate`

## Slice A approval / Slice B Red evidence

- Slice A approved 2026-07-31 with Architecture + Slice B Red bundled.
- Red suite: `tests/test_noether_forge_slice_b_integrated_red.py` →
  `0 passed, 8 failed`.
- Sources absent: `examples/applied/A11_noether_forge/`.
