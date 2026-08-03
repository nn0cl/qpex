# LISS-0313: Finiteize surface (Lane A) — Feature Path

## Metadata

- Local issue ID: LISS-0313
- Status: **planned** — awaiting Feature Plan approval before Phase 1 Red
- Type: Feature Kernel surface
- Priority: P3 ship (Architecture Accepted ADR 0185 Lane A)
- Depends: [ADR 0185](../architecture/adr/0185-kernel-continuous-value.md) **Accepted**;
  ADR 0163/0164 Host inject shipped
- Branch (when Red starts): `feature/liss-0313-finiteize-surface`
- Parent Architecture: [LISS-0312](LISS-0312-continuous-kernel-architecture.md) complete

## Problem

Continuous → finite is only taught via Python Host APIs
(`run_host_mc_inject` / equal-width histogram). Notebooks cannot spell the
explicit finiteization step in Staqex.

## Acceptance (EARS sketch)

```text
When a main calls finiteize with a valid Host-backed equal-width histogram
  description (interval, bins, samples/draw)
Then compile succeeds and the bind is a finite State/Joint with ADR 0074
  discretization provenance

When interval/bins/support are invalid
Then fail closed with Host inject diagnostic lineage (no silent empty State)

When finiteize succeeds
Then terminal measure on the result is ordinary finite measure
  (no Continuous type, no QPU continuous path)
```

## Scope

### In

1. Parse / HIR / typecheck for `finiteize(...)` Call (grammar fixed in Red)
2. Evaluator wiring to ADR 0163/0164 ports (Host RNG + continuous draw)
3. Provenance attach (0164 discretization block)
4. Red suite + seed-0 Host-aligned example
5. Docs: QUICKSTART / basics pointer — finiteize not Continuous type

### Out

- Mid-program `Continuous` (Lane B)
- Adaptive/KDE bins, cloud MC SDK
- Unifying Theory continuous_operator bridges into finiteize
- QASM of raw continuous samples

## Plan approval gate

**Do not start Phase 1 Red** until Adjudicator grants Feature Plan (or Claude
Issue Plan under CLAUDE autonomy if that agent runs the Issue).

Suggested surface args for Red debate (not locked):

```text
// chalk intent — exact tokens in Red
state psi = finiteize(
  interval = (-1.0, 1.0),
  bins = 8,
  samples = 256,
  // draw / host profile — TBD against Host port
)
```

## Exit

- [ ] Plan approved
- [ ] Phase 1 Red failing tests
- [ ] Phase 2 Green minimal
- [ ] Phase 3 Refactor + docs
- [ ] seed-0 example green
- [ ] Trace
