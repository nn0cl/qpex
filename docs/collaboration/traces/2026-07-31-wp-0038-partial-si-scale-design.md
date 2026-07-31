# Trace: WP-0038 Partial holes + SI scale + design ADRs

| Field | Value |
|---|---|
| Date | 2026-07-31 |
| Agent | Cursor Composer |
| Branch | `feature/wp-0038-partial-si-scale-design` |
| Issues | LISS-0155–0160 |
| ADRs | 0123–0128 Accepted |
| Instruction change | `CLAUDE.md` Open Topics (Partial / SI `to` shipped) |

## Shipped

- Function Partial `_` holes; unary-remaining Partial as pipe stage
- Explicit SI `expr to unit` (MVP: ms→s, nm→m, GHz→Hz); bare suffixes stay raw
- Design-boundary ADRs for rational / PDF / live QPU / trait expansion

## Still out

Fusion; multi-hole pipe stages; broader SI catalog; Kernel rational/PDF values;
live provider credentials/SDK.
