# Challenge intake: Examples 01–15 friction → Kernel brush-up

| Field | Value |
|-------|-------|
| Received | 2026-07-23 |
| Channel | Adjudicator request (review all examples; ISSUE + docs) |
| Local ledger | **[LISS-0003](../LISS-0003-examples-driven-kernel-brush-up.md)** (parent) |
| Children | LISS-0004, LISS-0005, LISS-0006 |
| Work plan | **[WP-0003](../../work-plans/WP-0003-examples-driven-brush-up.md)** |
| ADRs | **[0060](../../architecture/adr/0060-joint-coordinate-preservation.md)** (Proposed), **[0061](../../architecture/adr/0061-classical-module-config-harvest.md)** (Proposed) |
| GitHub | ignored (project-local management only) |

## Objective

Cross-review `examples/01`–`15` for language/kernel/DX friction that examples
**work around**, **duplicate**, or **cannot honestly express**. Record
prioritized brush-up work as local issues; open ADRs where Joint / linker
semantics change; document catalog conventions for future dream-skinned demos.

## Disposition

| Finding | Disposition |
|---------|-------------|
| `grover_diffuse` drops non-dest Joint coords (Float `KeyError`) | **LISS-0004** + ADR 0060 Proposed |
| `phase(…, only)` / `evolve times N` cannot use classical vars | **LISS-0004** |
| Linker harvests `Operator` only; Float notes need sync comments | **LISS-0005** + ADR 0061 Proposed |
| Grover/DTQW narrative clones (12/14 vs 04; 15 vs 09) | **LISS-0006** (catalog honesty) |
| `08_qft_and_fields` has no QFT | **LISS-0006** — renamed to `08_gauge_symmetry` |
| SV-09 dual allowlists + missing portable Bell | **LISS-0006** |
| Nested `when` ban / honesty tables | **Keep** — not defects |

## Scope guardrails

- LISS-0006 does **not** own Joint diffuse, classical harvest, or oracle
  combinators.
- Kernel Feature Path Red only after the matching ADR is **Accepted**.
- Default integration branch: `main`.

## Agent prompt (short)

Do **not** implement Kernel changes until Adjudicator accepts ADR 0060/0061.
Execute docs/ISSUE ledger first; Feature Path Red only after Accepted ADR +
LISS acceptance notes unlocked.
