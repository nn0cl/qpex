# LISS-0006: Examples catalog honesty (SV-09, QFT naming, dedup, π)

## Metadata

- Local issue ID: LISS-0006
- GitHub issue: none
- Status: **done** (2026-07-23) — all acceptance items closed
- Phase: Feature Path — Green (docs/harness)
- Type: chore + docs + test harness
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `main`

## Summary

Catalog honesty + SV-09 maintenance without Kernel `qft` / `pi` prelude.

## Acceptance Notes

- [x] Conventions doc shipped + updated for Accepted ADR 0060/0061
- [x] `08` README Honesty: **no QFT** (gauge only; rename deferred)
- [x] SV-09: path-link auto-detect via `import`; register
      `ket_evolve_expect` + `portable_bell_qpu`
- [x] README cross-links / package notes (conventions + examples README)
- [x] Optional: prelude `pi` / `Math.pi` → **done** ([LISS-0007](LISS-0007-prelude-pi-constant.md) / ADR 0062)
- [x] Optional: rename `08_qft_and_fields` → **`08_gauge_symmetry`** (package
      `com.staqex.examples.gauge_symmetry`)
- [x] SV suite green


## Dependencies

- Parent: [LISS-0003](LISS-0003-examples-driven-kernel-brush-up.md)
- Related: LISS-0002, ADR 0031

## Work Notes

- 2026-07-23: honesty + SV-09 auto path-link; optional `pi`/rename left open
  as non-blocking.

## Verification

- SV-09 includes new files; full suite 163/163
