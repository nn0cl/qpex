# Trace: Examples catalog v2 conventions activation

- Date: 2026-07-27
- Task: Complete LISS-0106 catalog v2 migration (basics, applied, legacy retirement)
- Agent: Cursor (Auto)
- Planning size: XL (WP-0026 / LISS-0106)

## What changed

- Contract file: `docs/collaboration/examples-catalog-conventions.md`
  - Marked v2 Basics/Applied layout **active**; legacy `examples/NN_*` **retired**.
  - Documented `tests/fixtures/staqex/` for SV pedagogy preserved after Phase 4.

## Why

- LISS-0106 Phase 4 removed `examples/01`–`17`. Agents and humans must not
  create new numeric folders or assume dual-layout coexistence.

## Expected agent behavior

- New official examples go under `examples/basics/Bnn_*` or
  `examples/applied/Ann_*` only.
- Applied READMEs require Honesty + verified bibliography; Basics do not.
- SV-09 allowlist in `tests/spec_verification/suites/sv09_examples.py` is the
  regression source of truth (22 entries + docs case).

## Related artifacts

- Issues: LISS-0106, LISS-0107, LISS-0108, LISS-0109 (done)
- Spec: `docs/specs/staqex-examples-catalog-v2.md`
- PR: #58
