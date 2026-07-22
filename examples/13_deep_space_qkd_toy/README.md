# 13 — Deep-space QKD toy (Bell / EPR)

Dream: a **Mars-bound command link** that cannot be eavesdropped without
leaving a detectable scar on entanglement.

## Layout

```text
examples/13_deep_space_qkd_toy/
├── domain/
│   └── link_parties.qpex       # OpticalHop + Party enum
├── operators/
│   └── bell_channel.qpex       # ideal ⟨Z⊗Z⟩ note
└── main_deep_space_qkd.qpex    # Φ⁺ prep + expect(ZZ)
```

## Honesty

| Claim | Status |
|-------|--------|
| Real BB84 / E91 / free-space modem | **No** |
| Photon loss, timing, authentication | **No** |
| Bell correlation as QKD intuition | **Yes** |

## Run

```bash
python3 -m compiler.qpex run examples/13_deep_space_qkd_toy/main_deep_space_qkd.qpex --seed 0
```
