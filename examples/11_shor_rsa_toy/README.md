# 11 — Shor / RSA toy (period finding)

Multi-file educational sketch of **Shor-style period finding** for the
classroom modulus \(N=15=3\times5\) (\(a=7\), order \(r=4\)).

## Layout

```text
examples/11_shor_rsa_toy/
├── domain/
│   └── rsa_parameters.qpex      # Crypto.RSA.Toy { struct, enum }
├── operators/
│   └── period_hints.qpex       # classical r / table notes (pub fn)
└── main_shor_period.qpex       # |x⟩, f(x)=a^x mod N, phase, measure
```

## Physics

Textbook RSA rests on factoring \(N=pq\). Shor reduces that to finding the
order of \(a^x \bmod N\), then \(\gcd(a^{r/2}\pm1,\,N)\).

\[
7^x \bmod 15:\quad 1,7,4,13,1,\ldots \quad (r=4)
\]

## Honesty

| Claim | Status |
|-------|--------|
| Real RSA (2048-bit) | **No** — toy \(N=15\) only |
| Full \(U_f\) + QFT | **No** — 2-qubit table + pedagogical `phase` |
| Multi-file domain / operators | **Yes** (ADR 0054 linker) |
| Unauthorized cryptanalysis | **Out of scope** |

## Run

```bash
python3 -m compiler.qpex run examples/11_shor_rsa_toy/main_shor_period.qpex --seed 0
python3 -m compiler.qpex inspect examples/11_shor_rsa_toy/main_shor_period.qpex --seed 0
```
