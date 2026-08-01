# Examples catalog conventions

Official physics / dream-application samples under `examples/`. Companion to
[LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md) and parent
[LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md).

## Catalog v2 (LISS-0106 — active)

Authority: [LISS-0106](../issues/LISS-0106-examples-catalog-v2-refresh.md) /
[WP-0026](../work-plans/WP-0026-examples-catalog-v2-refresh.md) /
[`staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md).

| Layout | Path pattern | Status |
|--------|--------------|--------|
| Basics | `examples/basics/Bnn_topic/` | **active** — B01–B12 in SV-09 |
| Applied | `examples/applied/Ann_topic/` | **active** — A01–A10 in SV-09 |
| Legacy numeric | `examples/NN_topic/` | **retired** (2026-07); pedagogy preserved in `tests/fixtures/staqex/` where SV still needs it |

v2 rules:

- Basics: one concept per folder; Honesty table not required.
- Applied: Honesty table **and** Bibliography with **Verified** citations only
  (see catalog spec §3).
- Do not cite **TBD** research IDs from the catalog spec in README files.

## Numbering and packages (legacy numeric layout — retired)

Historical reference only. New work uses Basics/Applied IDs above.

- Folder: `NN_topic_snake/` with two-digit `NN`.
- Package: `com.staqex.examples.<topic>` (short topic; need not equal full folder
  suffix — document any drift in the folder README).
- Entry file: single-file `topic.staqex`, or multi-file `main_<topic>.staqex`.

## Multi-file layout (preferred for 10+)

```text
examples/NN_topic/
├── domain/          # struct / enum / namespace types
├── operators/       # Operator builders, steps, harvested config
├── main_….staqex      # pub fn main
└── README.md        # required — include Honesty table
```

Legacy: `09_complex_simulations/models/` was allowed under the retired numeric
layout; prefer `domain/` for new work (see B09).

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
- Catalog / SV-09 / rename work: [LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md).
  Joint diffuse and classical harvest are **not** LISS-0006.

## SV-09 registration

- Every official runnable sample intended for regression MUST appear in
  SV-09 (or the successor auto-discovery set tracked in LISS-0006).
- Multi-file entries MUST use `compile_path` / `run_path` (import linking).
- Files kept for emit-qasm / pedagogy but excluded from SV-09 MUST be listed
  in the folder README as “not in SV-09” with reason.

## Linker expectations (shipping Kernel)

| Kind | Behavior |
|------|----------|
| `Operator` in `pub fn` | Harvested into main (ADR 0054) |
| Classical `Float`/`Int`/`Bool` in `pub fn` | Harvested (ADR 0061) |
| `evolve times <expr>` | Classical expr OK; Float truncates (ADR 0060) |
| `grover_diffuse` | Preserves unrelated Joint coords (ADR 0060) |

Name collision between harvested config and entry binds →
`CONFIG_HARVEST_COLLISION_ERROR`.

## Chalkboard test (LISS-0009)

Prefer paper spelling in examples:

- Angles: `pi`, `pi / 2`, `Math.pi` — not long decimals.
- Hadamard-scale coins: `(X + Z) * inv_sqrt2` (or `Math.inv_sqrt2`) — not
  `0.7071…`.
- Do not keep unused `Float` / enum binds “for atmosphere.”
- Do not claim QFT / Shor / metro solvers the Kernel does not implement.
- Ban new magic `π` / `1/√2` decimal literals in official `examples/`.


## `inspect` and lane Honesty (LISS-0219)

- Never imply `inspect` collapses state. README / comments must not call it
  “measurement” or “readout.”
- Applied / Showcase programs that mix Hamiltonian `evolve` with circuit-lane
  surfaces MUST state both in the Honesty table (or an equivalent note).
- Prefer `expect` + `inspect` for mid-protocol observables; keep one terminal
  `measure` on the spine when the sample claims a collapsed outcome.

## Related

- `examples/README.md` — catalog index
- [staqex-examples-catalog-v2.md](../specs/staqex-examples-catalog-v2.md) — proposed v2 acceptance spec
- [LISS-0106](../issues/LISS-0106-examples-catalog-v2-refresh.md), WP-0026
- ADR 0054, 0060, 0061, 0062
- [LISS-0009](../issues/LISS-0009-chalkboard-dx.md), WP-0003
