# B16 — Effect marking

Shows ADR 0081 **explicit effects** on a library helper:

```text
fn peek_zz(z: State<Float>) -> State<Float> effects { Inspect } {
    return inspect(z)
}
```

- Ordinary `fn` is **pure** by default.
- `Inspect` is non-collapsing; terminal collapse remains `measure`.
- Effect expansion / specialization is **parked** (LISS-0196 採択 — no ship ADR).

## Run

```bash
python3 -m compiler.staqex run examples/basics/B16_effect_marking/effect_marking.sqx --seed 0
```
