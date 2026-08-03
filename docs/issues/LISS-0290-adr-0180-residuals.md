# LISS-0290: ADR 0180 residual — fill inferred `ty` + Call/QASM consumers

## Metadata

- Local issue ID: LISS-0290
- GitHub issue: _(none yet)_
- Status: **complete** — Phase 3 Refactor 2026-08-03
- Phase: phase-3-refactor
- Type: Feature Kernel (conformance residual; no new ADR required)
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: Cursor agent
- Related branch: `feature/liss-0290-adr-0180-residuals`
- Design ADR: [0180](../architecture/adr/0180-local-type-inference.md) (**Accepted**)
- Depends on: LISS-0282 Kernel inference ship; LISS-0289 face re-sync (**complete**)
- Approval: Adjudicator「承認」Plan/Red/Green/Refactor (2026-08-03)

## Summary

ADR 0180 Decision §3 says omitted types are **filled by the typechecker**.
Shipping Green updated `env` for some cases but left `StateBind.ty is None` on
the AST. Downstream consumers still key off `stmt.ty`.

LISS-0290 fills omitted `ty` for Operator / classical coeffs / Float Call /
struct·class ctor (and Attr classical projections), restoring B08 inferred chalk
with QASM emission.

## Exit

- [x] Phase 1 Red → Phase 2 Green → Phase 3 Refactor
- [x] B08 north-star face restored
- [x] SV 161/161 + sugar pytest + B08 emit-qasm

## Non-goals

- New ADR
- Global Hindley–Milner / pub API inference
- Removing `state` keyword pedagogy

## Verification

```text
PYTHONPATH=. .venv/bin/pytest tests/test_liss_0290_… tests/test_liss_0280_0288_sugar_red.py -q
→ 11 passed
python3 tests/spec_verification/run_all.py → 161/161
```
