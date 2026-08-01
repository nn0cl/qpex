# ADR 0165: Dirac paper spelling as surface sugar over `inner` / `outer`

## Status

**Accepted** (2026-08-01) — WP-0078 / [LISS-0217](../../issues/LISS-0217-dirac-paper-spelling-sugar.md)
Adjudicator lock. Architecture / design approval only.

This ADR **does not authorize Kernel Red or implementation**. A separate ship
ADR + Feature Path Issue is required before Phase 1.

## Context

`CLAUDE.md` §Language Design Priority makes the physicist mental model primary
and prefers blackboard spelling on conflict (ADR 0095, `physicist-dx-harmony.md`).

ADR 0087 deliberately chose function calls for the Dirac algebra:

- Paper: ⟨φ|ψ⟩ and |ψ⟩⟨φ|
- Kernel: `inner(phi, psi)` and `outer(psi, phi)`

[`physicist-source-friction-ledger.md`](../physicist-source-friction-ledger.md)
records this as F-04, Class B, **an accepted trade rather than a defect** — the
reason was parser safety — and states the follow-up condition explicitly:
"sugar later must lower to Calls".

The parser pressure is real. `|` and `>` already carry meaning:

- ket literals `|0>`, `|+>`, and the Unicode ket forms
- comparison `>` / `>=`
- pipeline `|>` (ADR 0080 / 0122)

F-04 records that a named ket `|psi>` is **not accepted** today.

## Dependency Adoption Evidence

Not applicable. No library, framework, SDK, datastore client, build tool, or
test helper is selected by this ADR.

## Decision

1. **First ship slice includes both** paper inner `⟨φ|ψ⟩` **and** paper outer
   `|ψ⟩⟨φ|` (Unicode dual-accept with the existing ASCII bra/ket forms where
   already legal). Not inner-only.
2. **Sugar only.** Parse or desugar to `inner` / `outer` Calls. Semantics stay
   exactly as ADR 0087; the evaluator and type meaning do not change.
3. **Named kets `|psi>` remain rejected.** Reopening that F-04 line is a
   **separate** ruling; it is not implied by this sugar.
4. **Disambiguation (locked sketch for the ship ADR):**
   - **Inner:** must open with bra (`⟨` / ASCII bra open), close with ket close
     (`⟩` / `>`). Never start from a bare `|` that could be a ket literal or
     comparison residue.
   - **Outer:** ket primary immediately followed by bra primary (no binary op
     between), matching the already-shipped Dirac outer/projector punctuation
     path; desugars to `outer` / `projector` Calls per ADR 0087 / Dirac plan.
   - **Pipeline `|>`:** remains a two-character token; lexer must not split it
     into `|` + `>` inside sugar recovery.
   - **Comparison `>` / `>=`:** only outside Dirac bra–ket brackets.
   - **Rejected alternatives:** treating `|ident>` as a Var ket (named ket);
     stealing `{A, B}` anticommutator or bare-block `let` for Dirac; any sugar
     that introduces evaluator builtins other than existing Calls.
5. **Round-trip is in scope for the ship Issue:** formatter / CST canonical
   form, and `migrate_unicode_math.py` (importing shared Dirac label classes
   per LISS-0210).
6. **Teaching canonical:** Call form remains the documented Kernel teaching
   default; paper sugar is dual-accept for physicist DX.

## Consequences

Positive:

- Blackboard spellings can round-trip to ADR 0087 Calls without semantic fork.
- Discharges F-04 “sugar later” through an accepted design ADR.

Negative:

- Grammar risk remains until the ship Issue proves the disambiguation suite.
- Two surface spellings; docs must state Calls as the teaching default.

## Enforcement

Code review should reject:

- A Dirac spelling that does not lower to `inner` / `outer` Calls.
- Any evaluator or typechecker semantic change justified by this ADR alone.
- Kernel Red started without a **separate ship ADR** and phase approval.
- Accepting named `|psi>` under cover of this ADR.
- A grammar change that omits tests for ket literals, comparison, and `|>`.
