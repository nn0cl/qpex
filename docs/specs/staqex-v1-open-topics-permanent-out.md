# Open Topics permanent-out — **Reopened**

| Field | Value |
|---|---|
| Status | **Reopened** (2026-07-31) — Adjudicator explicit reopen |
| Supersedes | pre-S1 Accepted permanent-out / no-further-ship (same file §1 historical) |
| Issue | [LISS-0152](../issues/LISS-0152-permanent-out-reopen.md) |
| Program | [WP-0037](../work-plans/WP-0037-permanent-out-reopen.md) |
| Not | Silent reopen; inventing provider credentials; changing f64 default without ADR |

```markdown
[DESIGN CHECK]
- Scope: reopen LISS-0132 permanent-out topics for Architecture / Feature Path.
- Ship first: SI base dims I/Θ; pipe unary bare `|> f` (+ optional partial).
- Design-only first: exact rational runtime; continuous PDF; live QPU credentials.
```

## 1. Historical decision (pre-S1, 2026-07-31)

Before showcase **S1**, the following were **not** scheduled. That gate is
**lifted** by Adjudicator reopen (this revision).

| Topic | Was | Now |
|---|---|---|
| Further `\|>` / currying (fusion, partial-app values) | no-further-ship | **partial shipped** — unary/Partial + ADR 0022 MVPs + affine (0141) + Call/Partial Fusion (0143) + sequential multi-hole pipe (0149) + tuple simultaneous multi-hole (0152); residual: poly≥2 / GPU DAG |
| Further trait `impl` / effect rows / specialization | no-further-ship | **design boundary** ADR 0128 (no Red specialization yet) |
| SI scale beyond $(L,M,T)$ tags | permanent-out | **base dims** ADR 0121; **explicit `to`** through ADR 0151 (Rankine/imperial/ton/troy); **mixed-unit canonical promote** ADR 0155; residual: atomic mass / display-unit / bare `.ton` |
| Continuous PDF / Monte Carlo | permanent-out → **Lane A ship path** | ADR 0126 mid-program Continuous still out; Host inject **shipped** 0163/0164; **finiteize surface** [ADR 0185](../architecture/adr/0185-kernel-continuous-value.md) **Accepted** (Architecture); Feature [LISS-0313](../issues/LISS-0313-finiteize-surface.md) |
| Exact rational vs `f64` masses | permanent-out | **design boundary** ADR 0125 (ADR 0076/0097 still constrain runtime) |
| Concrete live QPU IR / provider credentials | permanent-out | **design boundary** ADR 0127 (ports/honesty first; no inventing credentials) |

## 2. Agent contract (post-reopen)

- Agents **may** create ADRs / Issues / Feature Path work for reopened rows.
- Agents **must not** treat reopen as permission to skip ADR for architecture
  choices (broader SI catalog, rational runtime mode, live provider SDK).
- Showcase S1 already shipped; reopen does **not** reopen S1 gate questions.

## 3. First execution batch (WP-0037)

| Issue | Mode |
|---|---|
| LISS-0152 | docs reopen + ledger / CLAUDE sync |
| LISS-0153 | SI base dims $I$, $\Theta$ (ADR 0121) — **ship** |
| LISS-0154 | Pipe unary bare `\|\> f` (ADR 0122) — **ship** |

## 4. Follow-on batch (WP-0038)

| Issue | Mode |
|---|---|
| LISS-0155 | Partial `_` holes (ADR 0123) — **ship** |
| LISS-0156 | Explicit SI `expr to unit` (ADR 0124) — **ship** |
| LISS-0157–0160 | Design boundaries ADR 0125–0128 — **docs** |

Authority for coverage ledger §3: this document (Reopened).
