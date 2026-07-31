# Trace: WP-0042 Fahrenheit + gram

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0042-fahrenheit-gram` |
| Issues | LISS-0167, LISS-0168 |
| ADRs | 0135, 0136 Accepted |
| Instruction change | `CLAUDE.md` Open Topics (°F / `g`↔`kg` shipped) |

## Shipped

- Affine Fahrenheit (`.F`) ↔ K/C via Kelvin family
- Mass scale `g` ↔ `kg`

## Still out (thin SI largely exhausted)

Fusion; Rankine/imperial mass; Kernel rational/PDF; live credentials; trait
specialization Red (needs concrete ship ADR beyond ADR 0128 boundary).
