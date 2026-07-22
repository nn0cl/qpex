# Examples catalog conventions

Official physics / dream-application samples under `examples/`. Companion to
[LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md) and parent
[LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md).

## Numbering and packages

- Folder: `NN_topic_snake/` with two-digit `NN`.
- Package: `com.qpex.examples.<topic>` (short topic; need not equal full folder
  suffix — document any drift in the folder README).
- Entry file: single-file `topic.qpex`, or multi-file `main_<topic>.qpex`.

## Multi-file layout (preferred for 10+)

```text
examples/NN_topic/
├── domain/          # struct / enum / namespace types
├── operators/       # Operator builders, steps, harvested config
├── main_….qpex      # public fun main
└── README.md        # required — include Honesty table
```

Legacy: `09_complex_simulations/models/` is Allowed; prefer `domain/` for new
work.

## Honesty table (required for application-skinned demos)

Every folder that claims a real-world story (city, space, genome, crypto, …)
MUST include a README table:

| Claim | Status |
|-------|--------|
| Real-world scale / production use | **No** / out of scope |
| Kernel surface actually demonstrated | **Yes** (name ops) |

Do not imply QFT, full Shor, BB84, NGS, or metro solvers unless the Kernel
surface exists and the example uses it.

## Narrative skins vs new surface

- **Allowed:** thin domain dressing over an existing canonical demo (e.g. Grover
  N=4, DTQW, Bell) when the README Honesty table is explicit and the canonical
  example remains the reference (04, 07/09, 03).
- **Prefer not:** a new `NN_` folder that only renames 04/09 without new
  pedagogy — link from docs instead, or wait for new Kernel surface
  (LISS-0003 Adjudicator gate).
- After P0 (LISS-0004/0005), skins SHOULD use harvested config / preserved
  Floats instead of sync comments.

## SV-09 registration

- Every official runnable sample intended for regression MUST appear in
  SV-09 (or the successor auto-discovery set tracked in LISS-0006).
- Multi-file entries MUST use `compile_path` / `run_path` (import linking).
- Files kept for emit-qasm / pedagogy but excluded from SV-09 MUST be listed
  in the folder README as “not in SV-09” with reason.

## Linker expectations (today vs after ADR 0061)

| Kind | Today (ADR 0054) | After ADR 0061 Accept + implement |
|------|------------------|-------------------------------------|
| `Operator` in `pub fun` | Harvested into main | Unchanged |
| Classical `Float`/`Int` in `pub fun` | **Not** harvested — avoid sync-comment debt where possible | Harvested per ADR 0061 |
| `evolve times N` | Integer literal only | Per ADR 0060 `times` expr |

Until 0060/0061 are Accepted and implemented, document workarounds in code
comments and point to LISS-0004 / LISS-0005.

## Related

- `examples/README.md` — catalog index
- ADR 0054, 0060 (Proposed), 0061 (Proposed)
- WP-0003
