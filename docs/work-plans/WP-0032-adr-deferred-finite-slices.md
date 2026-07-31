# WP-0032: ADR deferred finite slices

| Field | Value |
|---|---|
| Status | **complete** — 2026-07-31; Kernel Red/Green on feature branch |
| Program | ADR deferred finite Kernel ship (honesty, `where &&`, S4, 1D `J[i]`) |
| Parent ADRs | 0084, 0088, 0096, 0098 |
| Prerequisite | WP-0024 / binder surface shipped; permanent-out remains out |
| Created | 2026-07-31 |
| Branch | `feature/wp-0032-adr-deferred-finite` |

## Issue rows

| ID | Topic | Priority | Status |
|---|---|---|---|
| LISS-0140 | Binder honesty (Basis / unbound `J[i]` hard diagnostics) | P0 | **complete** |
| LISS-0141 | Compound `where` (`&&`) | P0 | **complete** |
| LISS-0142 | Suzuki S4 | P0 | **complete** |
| LISS-0143 | 1D `Float[N]` + indexed coeffs `J[i]` | P0 | **complete** |

## Scope out

- permanent-out topics (further `|>`, SI, PDF, exact rational, live QPU)
- `rev()` / dependent `Index<i+1..N>` (endpoint ADR required first)
- controlled / approximate QFT
- `Basis<N>` domain **expansion** (diagnostics only in 0140)
- 2D coefficient tensors; Host array binding

## Current next

PR merge review for `feature/wp-0032-adr-deferred-finite`.

## Invalidating triggers

- Adjudicator rejects S4 numerical contract or `Float[N]` surface
- Decision that binder `&&` must remain lex-forbidden under F-01 without carve-out
