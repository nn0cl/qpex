# ADR 0112: Claude Code contract independence

## Status

Accepted (2026-07-30). Supersedes the `CLAUDE.md` literal-full-mirror portion
of [ADR 0006](0006-prompt-instruction-change-control.md).

Adjudicator architecture approval given 2026-07-30. No follow-up Issue is
required: this decision is fully realized by the contract-document changes that
accompany it, and it authorizes no product implementation.

## Context

[ADR 0006](0006-prompt-instruction-change-control.md), as revised on
2026-07-25 per LISS-0015, requires `CLAUDE.md`,
`.github/copilot-instructions.md`, and `.grok/rules/*.md` to be **literal full
mirrors** of `AGENTS.md`. `CLAUDE.md:12-17` states that requirement inline and
instructs the agent to treat any disagreement between the mirrors as a defect
to flag rather than a rule to follow.

On 2026-07-26 the Adjudicator approved a deliberate Claude-only divergence:
`CLAUDE.md` §"Claude Code Issue-Level Autonomy" (trace
`docs/collaboration/traces/2026-07-26-claude-issue-level-autonomy.md`). It
replaces the per-step Scope/Architecture/Technology/Phase gates with two
approvals per Issue and instructs Claude to run Red → Green → Refactor without
a check-in at each boundary, while preserving a hard stop for unanticipated
design decisions.

That granted autonomy does not take effect in practice. Two forces defeat it:

1. **The mirror declaration turns the divergence into a suspected defect.**
   A session that reads `CLAUDE.md:12-17` first learns that the file is a
   mirror and that disagreements are defects. The autonomy section then reads
   as an unresolved inconsistency rather than as authority, which is exactly
   the treatment `CLAUDE.md:16-17` prescribes.
2. **Four other statements assert per-phase approval, and the earliest is read
   first.** `docs/architecture/agent-quickstart.md:100` and `:106-107`
   ("Phase transitions require Adjudicator approval. Do not start Phase 2 from
   unreviewed Phase 1 tests."), `CLAUDE.md:186` ("Execute only the phase
   explicitly requested by the Adjudicator", stated unconditionally),
   `docs/at-tdd/process.md:12` and `:77`, and `docs/at-tdd/process.md:124`
   (Phase 1 exit gate). `CLAUDE.md:130` directs the agent to read the
   quickstart at step 2, so the per-phase rule is established before the
   autonomy section at `CLAUDE.md:225` is reached. No statement anywhere
   declares which rule wins.

The mirror requirement is also asymmetric in what it buys per vendor. As ADR
0006 §Context records, Claude Code binds its contract file with the strongest
mechanism of the five — the file is inlined into context at session start —
while Copilot's native `AGENTS.md` reading is documented as "read-and-apply,
not strict enforcement". The vendor whose contract adherence is most reliable
is therefore the one where a deliberate, well-marked divergence is least
likely to be silently misapplied.

Removing the mirror requirement for `CLAUDE.md` has no CI consequence.
`.github/workflows/ci.yml` (209 lines) checks required-file existence, runs a
template-copy smoke test whose target list at `:150-154` does not include
`CLAUDE.md`, and requires a trace when a contract file changes (`:176`). No CI
step compares contract file contents. The mirror rule is enforced by human
review only.

An alternative was considered and rejected by the Adjudicator on 2026-07-30:
scoping the mirror requirement to "mirror except for enumerated Claude-only
divergences" rather than removing it. That option would have preserved drift
detection while legitimizing the autonomy section. The Adjudicator chose full
removal.

## Dependency Adoption Evidence

Not applicable. No library, framework, provider SDK, datastore client, build
tool, or test helper is selected by this decision.

## Decision

1. **`CLAUDE.md` leaves the literal-full-mirror set.** It is the
   independently authoritative agent operating contract for Claude Code. It
   remains an agent operating contract file under
   `docs/collaboration/prompt-instruction-change-control.md`, so the
   Adjudicator-review, stated-reason, and AI-work-trace requirements continue
   to apply to it unchanged.

2. **The remaining literal-full-mirror set is `.github/copilot-instructions.md`
   and `.grok/rules/*.md` against `AGENTS.md`.** Cursor's arrangement
   (`.cursor/rules/*.mdc` plus native root `AGENTS.md` auto-apply) is
   unchanged. The cross-file consistency check in
   `prompt-instruction-change-control.md` no longer covers `CLAUDE.md`.

3. **`CLAUDE.md` must be self-sufficient.** Because it no longer inherits
   `AGENTS.md` by mirror obligation, content present only in `AGENTS.md` is
   absorbed into `CLAUDE.md`:
   - the Never-Leave-the-State semantics: mid-program values are `State<T>`;
     classical collapse only at terminal `measure` (`AGENTS.md:16-18`);
   - the language surface enumeration and its ADR references
     (`AGENTS.md:20-25`), corrected as stated in point 4;
   - "when a decision affects architecture, capture it as an ADR; when a
     decision is unknown, list it in the design note as an ambiguity
     boundary" (`AGENTS.md:128-129`);
   - "report Red, Green, Refactor, or Fast Path status honestly"
     (`AGENTS.md:43`).

   All other `AGENTS.md` sections — Prime Directive, Session Entry, Clean
   Architecture Dependency Rule, External Resources Must Be Ports, Approval
   Model, Explicit Batch and Approval Source Rules, the `[DESIGN CHECK]`
   scaffold, and Expected Workflow — already have equivalent content in
   `CLAUDE.md` and are not duplicated again.

4. **Absorption corrects, not copies.** `AGENTS.md:23` spells the constructor
   `fun init`. [ADR 0066](0066-rust-aligned-fn-surface.md) (Accepted,
   2026-07-23) removed `fun` from the language with no alias, and the
   normative spelling is `fn init`
   (`docs/specs/staqex-language-specification.md:558`, and every program under
   `examples/`). The absorbed text uses `fn init`. `AGENTS.md:23` is corrected
   in the same change, because it currently teaches a retired keyword to
   Copilot, Codex, Grok, and Cursor.

5. **`CLAUDE.md` declares precedence for Claude Code.** Where `CLAUDE.md`
   conflicts with `docs/architecture/agent-quickstart.md` or
   `docs/at-tdd/process.md`, `CLAUDE.md` wins for Claude Code sessions. Those
   two files stay normative for the other agent families and are not rewritten
   to match Claude's model; `agent-quickstart.md` §Phase Rule carries a
   non-normative pointer to this precedence so that a Claude session reading it
   at step 2 is not mis-anchored before reaching `CLAUDE.md` §Claude Code
   Issue-Level Autonomy.

6. **`CLAUDE.md:186` is qualified.** "Execute only the phase explicitly
   requested by the Adjudicator" is scoped so that it does not contradict
   §Claude Code Issue-Level Autonomy for named-Issue Feature Path work and
   approved work-plan batches.

## Consequences

Positive:

- The Claude-only autonomy the Adjudicator approved on 2026-07-26 becomes
  effective instead of reading as an unresolved defect.
- Claude-specific process changes no longer require touching four other
  contract files, and no longer create a mirror-consistency obligation across
  vendors whose enforcement fidelity differs.
- `CLAUDE.md` becomes readable as a single self-contained contract, which
  matches how Claude Code actually loads it.
- A stale keyword (`fun init`) is removed from the shared contract surface as a
  side effect.

Negative:

- **Drift becomes unmanaged rather than flagged.** Process improvements made
  in `AGENTS.md` will no longer reach `CLAUDE.md` automatically, and the
  reverse is also true. Nothing in review or CI will detect the divergence,
  because the consistency check no longer covers `CLAUDE.md`. Keeping the two
  aligned where alignment is still wanted becomes a manual, unprompted act.
- Claude and the other four agent families can diverge in observable behavior
  on the same repository. That is the intent for approval granularity, but the
  same freedom applies to every other rule, including ones where divergence
  would be undesirable and unnoticed.
- `CLAUDE.md` grows, since absorbed content is duplicated rather than
  inherited. It is always-loaded context, so the duplication has a per-session
  cost.
- ADR 0006's stated positive consequence — "Contract drift ... becomes visible
  in review instead of silently changing agent behavior" — no longer holds for
  `CLAUDE.md`.

## Enforcement

Code review should reject:

- a change that reintroduces a `CLAUDE.md`-is-a-mirror claim, or that adds
  `CLAUDE.md` back to the literal-full-mirror set in
  `prompt-instruction-change-control.md`, without superseding this ADR;
- a `CLAUDE.md` change that removes one of the absorbed items in Decision
  point 3, leaving Claude without a rule the other agents still have;
- absorbed or newly written text that spells the constructor `fun init`, or
  that reintroduces any keyword retired by an accepted ADR;
- a rewrite of `docs/architecture/agent-quickstart.md` or
  `docs/at-tdd/process.md` that imposes Claude's approval model on the other
  agent families, which this ADR does not authorize;
- a `CLAUDE.md` change that lacks Adjudicator review, a stated reason, or an
  AI work trace — those obligations survive the mirror removal.
