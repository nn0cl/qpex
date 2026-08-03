# AI work trace — LISS-0290 ADR 0180 residual intake

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Branch | `docs/liss-0290-adr-0180-residuals` |
| Path | Architecture / Feature intake (docs only) |
| Issue | [LISS-0290](../../issues/LISS-0290-adr-0180-residuals.md) |
| ADR | 0180 **Accepted** (conformance residual; no new ADR drafted) |
| Authorization | Adjudicator「ADR 0180 残差」 |

## Diagnosis

1. Typecheck leaves `StateBind.ty is None` after env inference.
2. QASM `lower.py` harvests only typed `Operator` binds → inferred B08 QASM fails.
3. Evaluator classical Float Call path requires typed `Float` → bare Call fails.
4. Bare struct binds LINEAR-misclassified as State.

## Artifacts

- Issue + AIP-0290-001
- ADR 0180 residual pointer
- local-issue-planning row

## Next safe action

Adjudicator Plan / Phase 1 Red「承認」on LISS-0290 (recommend: no ADR amend;
fill `ty` at typecheck; restore B08 chalk after Green).
