# A10 — Mission observatory (slim capstone)

Integration read path across **domain modules**, **SSH evolve**, **static QPU lane**,
and **Bell link** — without re-expanding into the full legacy kitchen sink.

Legacy source: slimmed from `examples/16_quantum_observatory/`.

## What this capstone is not

- Not the only place a surface is documented — see B01–B12 and A06–A09.
- Not a production mission simulator, provider SDK, or full open-systems lab
  (Lindblad: see B12 / future A07).

## Honesty

| Claim | Status |
|-------|--------|
| Full observatory (walk, Grover, interferometer, Lindblad in one file) | **No** |
| Multi-module `import` + SSH + QPU register + Bell witness | **Yes** |
| Real spacecraft operations / spectrum mission data | **No** |

## Run

```bash
python3 -m compiler.qpex run examples/applied/A10_mission_observatory/main_mission_observatory.qpex --seed 0
```

## Suggested read order

`B01 → … → B10 → A06 → A09 → A10` (see `docs/specs/qpex-examples-catalog-v2.md` §6).
