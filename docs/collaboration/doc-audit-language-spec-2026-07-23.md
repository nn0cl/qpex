# Language-spec re-audit (2026-07-23)

## Verdict

**~9.6 / 10** for Architecture-Path language design sync. Core locks in
`qpex-language-spec.md` + ADRs **0021–0033** are mutually consistent.
Implementation remains **Hold**.

Umbrella header and §0 lock index were refreshed in this pass; stale `fn` in
`qpex-abstraction-model.md` examples migrated to `fun`.

## Consistency matrix

| Theme | Spec § / ADR | Status |
|-------|--------------|--------|
| Never Leave the State | §1.1, axioms | OK |
| Universal `State<T>` | §1.2, 0018/0024 | OK |
| No exceptions / Result | §1.3, 0025–0026 | OK |
| No threads | §1.4, 0028/0032 | OK |
| Packages as $\mathcal{H}$ | §2, 0024/0026 | OK |
| `when` / `class` / `fun` | §3, 0024/0026 | OK |
| Entry `main` + measure | §4, 0027 | OK |
| Host I/O / snapshot / inspect | §5, 0029–0030 | OK |
| Lit-Lift | §7, 0018/0024 | OK |
| Stdlib Math State→State | packages note, 0031 | OK (pointer in umbrella) |
| Immutable class | 0033, abstraction §4b | OK |
| Runtime DAG | 0032 | OK (companion) |

## P0 fixes this pass

- Language-spec status → umbrella ADR **0021–0033** + companions list.
- §0 **Lock index** table.
- Expanded §10 open questions (State comparisons, prelude, collections OOB).
- Abstraction-model example `fn` → `fun` (keep “retired `fn`” wording).
- Agent-sync read order → include 0027–0033 addenda.

## Remaining P1 (not contradictions)

1. **Vacuum** wire format mini-spec still open.
2. **`State` relational ops** (`>=` in BankAccount narrative) not formally typed.
3. **Prelude / default imports** unspecified.
4. Historical ADR 0013–0015 / prior-art still say `observe` (bannered).
5. Formal section title **§Span** vs surface `when` (intentional).
6. Cheat-sheet ADR range in older lines may lag; baseline read order fixed.

## Hold

No harness / parser / typechecker / stdlib code until Adjudicator unseals.


---

## Follow-up: ADR 0034 + Hold unseal

P1 Vacuum / State compare / Prelude locked. Sync **10 / 10**. Kernel PoC / parser / AST / typechecker **unsealed**.
