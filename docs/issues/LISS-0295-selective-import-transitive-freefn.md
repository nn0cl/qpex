# LISS-0295: Selective import transitive free-fn linkage

## Metadata

- Local issue ID: LISS-0295
- Status: **complete** (2026-08-03)
- Type: Feature Kernel residual (ADR 0177 implementation)
- Priority: P1
- Depends: LISS-0294 **complete** (nested free-fn runtime); ADR 0177 **Accepted**
- Branch: `feature/liss-0295-selective-import-transitive-freefn`

## Problem

After LISS-0294 demoted S01 packs to free-fn scores, outer scores that called
sibling free-fns failed under selective import:

```text
call cannot be classical value in Phase 2.2 value context
```

ADR 0177 only merges decls **named** in `import … {A, B}`. Nested free-fn
bodies reference sibling helpers that were never linked. LISS-0294 worked
around this by inlining leaf math.

## Fix

When expanding a selective import set for a dependency unit, **transitively
add same-unit free-fn callees** of selected free-fns (pub/module/package
visibility). Entry import lists stay selective; helpers needed only for
execution of selected scores are linked.

No new ADR — residual of ADR 0177 linkage, not a surface change.

## S01

Restore nested free-fn composition in domain packs (roads / shelters /
hazards / requests / recovery).

## Exit

- [x] Module linker transitive free-fn expansion
- [x] Unit tests (nested exec + unused sibling stays out)
- [x] S01 domain un-inlined; seed-0 spine / morning / day2
