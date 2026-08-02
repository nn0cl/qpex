# LISS-0271: Kernel Red — selective import / use (ADR 0177)

## Metadata

- Local issue ID: LISS-0271
- GitHub issue: https://github.com/nn0cl/staqex/issues/284
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: P1
- ADR: [0177](../architecture/adr/0177-import-use-ergonomics.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Ship selective `import pkg.{A, B}` and narrow enum `use` for when-arm names.
Old imports remain valid.

## Exit

- [x] Selective `import path.{A, B}` parse + merge filter
- [x] `use Enum.*` parse (when arms already bare-match)
- [x] Tests in `tests/test_liss_0271_0272_import_lane_red.py`
