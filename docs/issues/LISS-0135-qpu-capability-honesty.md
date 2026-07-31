# LISS-0135: QPU capability honesty catalog

## Metadata

- Local issue ID: LISS-0135
- Status: **complete** — 2026-07-31
- Phase: Architecture Path docs (+ reject-code audit)
- Type: honesty catalog
- Spec: [staqex-v1-qpu-capability-honesty.md](../specs/staqex-v1-qpu-capability-honesty.md)
- Priority: P0 (before S1)

## Summary

Document Kernel/SV-writable vs QPU/OpenQASM-unplaceable capabilities with
existing reject codes. No new lowering.

## Exit

- [x] Catalog published
- [x] Coverage / diagnostic App B cross-links
- [x] Audit: reject codes present in `lower.py` / CH0 / observation (no missing renames found)
