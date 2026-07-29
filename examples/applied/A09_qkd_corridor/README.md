# A09 — QKD corridor

Bell correlations as **QKD intuition** for a deep-space optical hop — not a full
cryptographic protocol.

Legacy source: `examples/13_deep_space_qkd_toy/`.

## Honesty

| Claim | Status |
|-------|--------|
| Real BB84 / E91 / free-space modem | **No** |
| Photon loss, timing, authentication | **No** |
| Bell correlation as QKD intuition | **Yes** |

## Bibliography

- Bennett, C. H., Brassard, G. "Quantum cryptography: Public key distribution and coin tossing." *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing* (1984). (Pedagogy only — not a full protocol implementation.)

## Run

```bash
python3 -m compiler.staqex run examples/applied/A09_qkd_corridor/main_qkd_corridor.qpex --seed 0
```
