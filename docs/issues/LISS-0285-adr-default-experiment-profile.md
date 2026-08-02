# LISS-0285: ADR — default experiment profile (marker optional)

## Metadata

- Local issue ID: LISS-0285
- GitHub issue: _(none yet)_
- Status: **proposed** (ADR 0182 draft filed 2026-08-03)
- Phase: Architecture Path (ADR draft → Accept)
- Type: Architecture ADR
- Priority: P2
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)
- Depends: [LISS-0274](LISS-0274-wp-0089-program-lock.md); builds on ADR 0176
- Blocks: [LISS-0286](LISS-0286-kernel-default-experiment-profile.md)

## Summary

ADR 0176 requires a source-visible `// staqex-profile: experiment` marker. That
marker is itself meta-ceremony. Decide whether **single-file / no-package**
scripts default to experiment profile (marker optional), while multi-package
and library modules stay classic.

## Decision questions

1. Default trigger: no `package` line? CLI flag? both?
2. Marker still allowed and overrides?
3. Interaction with `// staqex-lane:`
4. Host entry ABI still desugars to `main -> Unit`
5. Migration: existing packaged programs unchanged

## Exit

- [ ] ADR Accept
- [ ] Explicit non-break for multi-file S01 packages

## Policy guard

- Honesty: default must not hide multi-file module rules
- Do not invent a second entry semantics
