# LISS-0258: Failure glossary ADR (world-line Err vs Job diagnostics)

## Metadata

- Local issue ID: LISS-0258
- Status: **complete** (2026-08-02) — ADR 0175 **Accepted** (Adjudicator「承認」)
- Type: Architecture Path (docs ADR)
- Priority: P1 (language design residual)
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md) (parallel track)
- ADR: [0175-failure-glossary.md](../architecture/decision-themes/dec-0003-language-surface-and-physicist-first-dx.md) (**Accepted**)
- Inputs: axioms (no exceptions / world-line failure); Host `JobResult.diagnostics`;
  B03 failure_worldline; destructive-simplification sketch residual list
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Intent

Publish an **Accepted or Proposed ADR** that defines a shared glossary:

| Kind | Where it lives | Examples |
|---|---|---|
| World-line / joint failure labels | Object language (`when`, Err arms) | Division-by-zero arm, Success/Error basis |
| Kernel / compile diagnostics | CompileResult / run diagnostics | `FORBIDDEN_KEYWORD`, type errors |
| Job / Host failure | `JobResult.status`, diagnostics codes | failed compile, Abort budget, vacuum incomplete ticket |
| Capability / placeability | Soft or hard QPU rejects | `E_QPU_UNSUPPORTED_CAPABILITY` |

Clarify that these are **not** interchangeable and that S01 examples must not
teach “Job failed ⇒ encode as when-arm” or the reverse without honesty notes.

## Exit

- [x] ADR: `docs/architecture/decision-themes/dec-0003-language-surface-and-physicist-first-dx.md` (**Accepted**)
- [x] Cross-links: axioms Axiom 6 + architecture README ADR index
- [x] S01 README pointer to ADR 0175
- [x] Adjudicator Accept recorded (「承認」2026-08-02)
- [x] **No** Kernel behavior change

## Non-goals

- Implementing new exception syntax
- Replacing `when` failure model
- Provider-specific error taxonomies

## Verification

- ADR file present; status explicit
- Grep S01 for “throw/try” remains absent
- Link from WP-0087 / scorecard residuals “failure glossary” satisfied when Accepted
