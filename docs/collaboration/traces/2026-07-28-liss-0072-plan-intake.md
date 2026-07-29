# Trace: LISS-0072 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0072 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design |
| Branch | `feature/liss-0072-slice-a-red` |
| Implementation | **Slice A Phase 1 Red only** after plan approval |

## [DESIGN CHECK]

- Scope: Propose lossless CST, formatter, source-version markers, and EBNF
  catch-up as slices A–D; no Red.
- Specs inspected: WP-0025 E1; ADR 0106 Unicode + D9 pipeline; compiler
  blueprint §3.1; rebaseline register §6–7; LISS-0069 migrator/CLI; LISS-0071
  conformance catalog; `grammar/staqex.ebnf` gap list in language spec Appendix A.
- Boundaries: Python Kernel only; presentation layer; SV behavior oracle
  unchanged; Rust/LSP out.
- Decisions pending Adjudicator: CST strategy (trivia-attached tokens vs full
  tree); round-trip oracle (AST + comments); NFC on emit; `staqex format` CLI in
  Slice B vs LISS-0105; `staqex_version` syntax.
- Verification: docs PR; no `compiler/` or `tests/` mutations.

## Delivered

- `docs/issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md`
- `docs/specs/staqex-v1-cst-formatter-plan.md`
- `docs/architecture/open-work-register.md` (LISS-0072 row)

## Approval outcome

Adjudicator approved the plan for LISS-0072 slices A–D with the recommended
direction:

- Slice A: trivia-aware lexing + CST skeleton;
- Slice B: formatter + parse-format-parse + migration parity;
- Slice C: `staqex_version` + retired-keyword fix-its;
- Slice D: EBNF catch-up + alignment gate.

Recorded decisions:

- trivia-attached tokens first;
- structural AST equality + comment preservation for round-trip;
- preserve source NFC at format time;
- include a minimal `staqex format` CLI in Slice B;
- accept the draft `staqex_version = "1.0"` surface for Red review.

Phase 1 Red is authorized for **Slice A only**. Green is not implied unless
batch autonomy is granted later.

## Explicitly not authorized yet

- `compiler/staqex/` production changes
- EBNF edits
- Slice B/C/D work before separate Red approval

## Next safe action

Slice A Phase 1 Red — add failing tests only.
