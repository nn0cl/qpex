# Trace: LISS-0068 v1.0 normative promotion

- Date: 2026-07-28
- Task: Promote E0 artifacts into `staqex-language-specification.md` v1.0
- Agent: Cursor (Auto)
- Phase: Architecture Path / LISS-0068 promotion — **complete**
- Branch: `docs/liss-0068-v1-promotion`

## Delivered

- `docs/specs/staqex-language-specification.md` → **Normative v1.0**
  - Header: ADR 0013–0105, ADR 0106, SV-01–SV-31
  - §1–§2 replaced from E0 outline (lanes, return, until, Unicode staging)
  - §5.9 deferral list refreshed
  - Appendix A: EBNF catch-up deferred to LISS-0072
  - Appendix B: authoritative pointer to diagnostic catalog
- Companions marked **Promoted**: register, outline, catalog, envelopes, matrix
- `docs/testing/staqex-spec-verification-protocol.md` header synced to v1.0
- LISS-0068 / open-work-register / WP-0025 next-issue → LISS-0069

## Explicitly not in this PR

- Compiler / lexer / parser / runtime changes
- EBNF production sync for `until` / separators / scientific scopes (LISS-0072)
- Unicode Pauli ASCII removal (LISS-0069)
- Full SV protocol body rewrite (LISS-0071)

## Verification

- Documentation-only; `git diff --check`
- No `compiler/` or `tests/` mutations

## Next safe action

LISS-0069 Phase 0 plan intake (Unicode/Dirac dual-accept migrator).
