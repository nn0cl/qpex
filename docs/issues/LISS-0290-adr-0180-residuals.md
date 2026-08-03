# LISS-0290: ADR 0180 residual — fill inferred `ty` + Call/QASM consumers

## Metadata

- Local issue ID: LISS-0290
- GitHub issue: _(none yet)_
- Status: **proposed** — awaiting Plan / Phase 1 Red approval
- Phase: Feature Path Red → Green → Refactor (after Plan approval)
- Type: Feature Kernel (conformance residual; no new ADR required)
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: Cursor agent
- Related branch: `docs/liss-0290-adr-0180-residuals` (intake); feature branch at Red
- Design ADR: [0180](../architecture/adr/0180-local-type-inference.md) (**Accepted**)
- Depends on: LISS-0282 Kernel inference ship; LISS-0289 face re-sync (**complete**)
- Blocks: honest B08 chalk without QASM regress; S01 bare Call Float binds

## Summary

ADR 0180 Decision §3 says omitted types are **filled by the typechecker**.
Shipping Green updated `env` for some cases but left `StateBind.ty is None` on
the AST. Downstream consumers still key off `stmt.ty`:

| Residual | Evidence | Consumer gap |
|---|---|---|
| Inferred `Operator H = …` | SV runs; `emit-qasm` → `QASM_TROTTER_UNSUPPORTED_H: unknown Operator H_chain` | [`backend/qasm/lower.py`](../../compiler/staqex/backend/qasm/lower.py) harvests only `ty.name == "Operator"` |
| Inferred `Float` Call | `fair = score(report)` → `unbound coordinate report` | Evaluator classical Float-fn path requires `ty.name == "Float"` (LISS-0231) |
| Bare struct / object | `seg = Seg { length: 2.0 }` → LINEAR discard as State | Typecheck does not classify / fill Struct/Object `ty`; LINEAR treats as State |

LISS-0289 therefore **kept typed heads** on B08 for QASM and typed Floats on
S01 Call results. That is sample theater against the Accepted teaching target.

## Intent (fix, not expand)

1. Typechecker **desugars** eligible omitted binds by writing `stmt.ty`
   (`TypeRef`) when elaboration is unique (Operator / Classical Float /
   Struct / Class / unambiguous State factories already covered).
2. Fail-closed unchanged: Classical↔State clash still rejects.
3. Evaluator + QASM lower keep working for typed binds; inferred binds become
   observationally identical after fill.
4. After Green: restore B08 chalk `J =` / `H_chain =` without QASM regress;
   allow `Float`-returning Call bare binds in samples.

## Exit

- [ ] Phase 1 Red: failing tests for the three residuals + fail-closed negatives
- [ ] Phase 2 Green: typecheck fills `ty`; QASM + SV green on inferred B08;
  Call Float bare bind succeeds
- [ ] Phase 3 Refactor + reviewer empathy
- [ ] Re-apply B08 north-star face (drop redundant Float/Operator heads) under
  this Issue or thin follow-up commit on same PR
- [ ] SV 161/161 + sugar pytest + B08 emit-qasm seed path

## Non-goals

- New ADR (0180 Decision already requires fill; this is Kernel conformance)
- Global Hindley–Milner / pub API inference
- Removing `state` keyword pedagogy
- Inferring across module boundaries

## Adjudicator Decision Points

1. Approve Plan → Phase 1 Red on `feature/liss-0290-adr-0180-residuals`?
2. Confirm **no ADR amendment** (conformance) vs thin Accepted-errata note on 0180?
3. B08 face restore in same Issue Green or separate sample Issue?

## Recommendation

- **No new ADR** — implement Decision §3 literally (fill `ty`).
- Same Issue includes B08 face restore after Green verification.
- Prefer fill-at-typecheck over scattering `ty is None` heuristics in QASM/eval.

## AI Planning Records

### AIP-0290-001

- Status: proposed
- Created by:
  - Agent/environment: Cursor
  - Model as displayed: Auto / Composer
  - Reasoning setting as displayed: N/A
- Created at: 2026-08-03
- Planning size: M
- Intended execution route: Feature Path Red → Green → Refactor
- Intended scope: `compiler/staqex/typecheck.py` (+ minimal eval/QASM if needed);
  `tests/test_liss_0290_*`; B08 sample restore
- Estimated token midpoint: mid
- Assumptions: 0180 Accept already authorizes fill; Red needs Phase approval
- Confidence: high on diagnosis; medium on blast radius of AST rewrite

## Verification (planned)

```text
PYTHONPATH=. .venv/bin/pytest tests/test_liss_0290_adr_0180_residuals_red.py -q
python3 -m compiler.staqex emit-qasm examples/basics/B08_…/operators_hamiltonians.sqx
python3 tests/spec_verification/run_all.py
```

## Work Notes

Repro 2026-08-03 (intake):

- Inferred B08 SV succeeded; QASM failed unknown `H_chain`.
- Typed B08 QASM succeeded (~5k chars).
- `fair = score(report)` runtime unbound; `Float fair = …` succeeded.
- Bare named struct compile LINEAR; typed named struct succeeded.
