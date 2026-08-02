# LISS-0272: Kernel Red — lane annotation (ADR 0178)

## Metadata

- Local issue ID: LISS-0272
- GitHub issue: https://github.com/nn0cl/staqex/issues/285
- Status: **open** — Phase 1 Red authorized (ADR 0178 Accepted)
- Type: Feature Path
- Priority: P1
- ADR: [0178](../architecture/adr/0178-lane-annotation.md) (**Accepted**)
- Program: WP-0088
- Parent: LISS-0269

## Intent

Parse/recognize `// staqex-lane: experiment|circuit|open`; soft diagnostics when
circuit constructs appear under experiment lane (phase 1 soft only).

## Exit

- [ ] Red → Green → Refactor
- [ ] Soft diagnostic tests
- [ ] Sample headers updated (B10/B11 circuit; B08 experiment optional)
