# LISS-0258: Failure glossary ADR (world-line Err vs Job diagnostics)

## Metadata

- Local issue ID: LISS-0258
- Status: **open**
- Type: Architecture Path (docs ADR)
- Priority: P1 (language design residual)
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md) (parallel track)
- Inputs: axioms (no exceptions / world-line failure); Host `JobResult.diagnostics`;
  B03 failure_worldline; destructive-simplification sketch residual list
- Branch (suggested): `docs/liss-0258-failure-glossary-adr`

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

- [ ] ADR draft under `docs/architecture/adr/NNNN-failure-glossary.md` (next free number at implement time)
- [ ] Cross-links from axioms or physicist-dx-harmony / minimal dialect OUT list
- [ ] S01 README or locked scenario: one-paragraph pointer (no full rewrite required)
- [ ] Adjudicator Accept / revise / reject recorded
- [ ] **No** Kernel behavior change in this Issue (unless ADR explicitly requires a follow-up Feature)

## Non-goals

- Implementing new exception syntax
- Replacing `when` failure model
- Provider-specific error taxonomies

## Verification

- ADR file present; status explicit
- Grep S01 for “throw/try” remains absent
- Link from WP-0087 / scorecard residuals “failure glossary” satisfied when Accepted
