# WP-0089 sugar ADR Accept record

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Approval | Architecture **Accept** — Adjudicator「承認」 |
| ADRs | 0180, 0181, 0182, 0183 |
| Kernel | LISS-0282 / 0284 / 0286 / 0288 authorized (Red→Green) |

## Frozen choices

| ADR | Freeze |
|---|---|
| 0180 | Local inference for classical coeffs + Operator algebra + `state` keyword still NLTS; no pub-API inference |
| 0181 | Named form `Type { field: expr }`; positional remains; nested struct construction fixed |
| 0182 | No `package` line ⇒ default experiment profile; packaged still requires `main` |
| 0183 | Package-relative leading `.` / `..` + selective braces |

## Out

Axiom changes; live QPU; Kernel `if`/`try`.
