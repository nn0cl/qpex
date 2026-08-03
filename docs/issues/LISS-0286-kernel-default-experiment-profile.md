# LISS-0286: Kernel — default experiment profile

## Metadata

- Local issue ID: LISS-0286
- GitHub issue: _(none yet)_
- Status: **complete** — Kernel shipped 2026-08-03 (WP-0089)
- Phase: Feature Path Red → Green → Refactor (**after** LISS-0285 Accept)
- Type: Feature Kernel
- Priority: P2
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0285](LISS-0285-adr-default-experiment-profile.md) **Accepted**

## Summary

Implement Accepted default experiment-profile rules (marker optional under
defined conditions). Preserve ADR 0176 behavior when marker present.

## Exit

- [ ] Red / Green / Refactor
- [ ] Negatives: multi-file / packaged programs not silently mis-profiled
- [ ] SV + pytest

## Verification

- Per DoD
