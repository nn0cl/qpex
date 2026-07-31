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
| Further `\|>` / currying (fusion, partial-app values) | no-further-ship | **reopened** — thin Kernel slices under ADR 0122 |
| Further trait `impl` / effect rows / specialization | no-further-ship | **reopened** — design ADR required before Red |
| SI scale beyond $(L,M,T)$ tags | permanent-out | **reopened** — base dims $I$,$\Theta$ under ADR 0121; **scale conversion still out** until separate ADR |
| Continuous PDF / Monte Carlo | permanent-out | **reopened for design ADR only** (no Kernel continuous value yet) |
| Exact rational vs `f64` masses | permanent-out | **reopened for design ADR only** (ADR 0076/0097 still constrain runtime) |
| Concrete live QPU IR / provider credentials | permanent-out | **reopened for Architecture Path** (ports/honesty first; no inventing credentials) |

## 2. Agent contract (post-reopen)

- Agents **may** create ADRs / Issues / Feature Path work for reopened rows.
- Agents **must not** treat reopen as permission to skip ADR for architecture
  choices (SI scale conversion, rational runtime mode, live provider SDK).
- Showcase S1 already shipped; reopen does **not** reopen S1 gate questions.

## 3. First execution batch (WP-0037)

| Issue | Mode |
|---|---|
| LISS-0152 | docs reopen + ledger / CLAUDE sync |
| LISS-0153 | SI base dims $I$, $\Theta$ (ADR 0121) — **ship** |
| LISS-0154 | Pipe unary bare `\|\> f` (ADR 0122) — **ship** |
| LISS-0155+ | design ADRs for rational / PDF / live QPU / trait expansion — **design** |

Authority for coverage ledger §3: this document (Reopened).
