# ADR 0121: SI base dimensions $I$ and $\Theta$

## Status

**Accepted** (2026-07-31) — unlocks LISS-0153 under WP-0037.
Companions: ADR 0037; [permanent-out reopen](../../specs/staqex-v1-open-topics-permanent-out.md).

## Context

Dim was $\mathbf{d}=(L,M,T)$. Permanent-out blocked further SI work pre-S1.
Reopen authorizes **base-dimension extension** without scale conversion.

## Decisions

1. `Dim` is $\mathbf{d}=(L,M,T,I,\Theta)$ with integer exponents. Existing
   three-axis programs are zero-filled on $I$ and $\Theta$ (compatible).
2. Type-First heads `Current` ($I=1$) and `Temperature` ($\Theta=1$) are added.
3. Unit suffixes `.A` → Current and `.K` → Temperature (magnitude raw; **no**
   SI scale conversion in this ADR — same honesty as `.ms` / `.nm` today).
4. Scale conversion (`ms`→`s`, `°C`→`K`, etc.) remains a **separate** ADR.

## Consequences

- `dimensions.py` grows two axes; tables and pretty-print update.
- SV / Type-First tests cover Current/Temperature mismatch.

## Deferred

SI scale conversion; additional base dims; full SI derived-unit catalog.
