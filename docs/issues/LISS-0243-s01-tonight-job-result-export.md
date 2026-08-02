# LISS-0243: S01 Host tonight job result export (A → B → C MVP)

## Metadata

- Local issue ID: LISS-0243
- Status: **done** (shipped 2026-08-02, LISS-0243 A→B→C)
- Type: Feature Path
- Priority: P1
- Parent showcase: [LISS-0222](LISS-0222-s01-quantum-disaster-response.md) (S01 complete)
- Spec / story: [locked scenario](../specs/staqex-v1-s01-locked-scenario.md)
- Host ABI research: [quantum-execution-boundary-and-result-flow](../research/quantum-execution-boundary-and-result-flow-2026-07-23.md)
- Related shipped: `Job` / `JobResult` / `MeasurementEnvelope` (`compiler/staqex/host.py`); MeasureSinkPort (ADR 0171 / LISS-0236); S01 `host/rolling_replan_job.py`
- Path (primary): `examples/showcase/S01_quantum_disaster_response/`
- Branch (suggested): `feature/liss-0243-s01-tonight-job-result-export`
- Architecture approval: **not required** if work stays on existing Job ABI (no new live QPU port, no language axiom change)
- Technology selection: **not required** (no provider SDK)

## Goal (simple)

| Layer | Meaning | This issue |
|-------|---------|------------|
| **A** | Read the job result object | Required |
| **B** | Put measurement contents into structured data | Required (meaningful envelope for S01 spine) |
| **C** | Map to ops-style ticket DTO / JSON | Required (minimal MVP) |
| **D** | Live QPU submit | **Out** |

Ship a Host path that runs `main_disaster_response.sqx` and exports a
**structured Tonight ticket JSON** (or equivalent serializable DTO) without
scraping stdout `valuemass` text.

One line: seal the envelope (**A**), put numbers inside (**B**), rewrite as a
dispatch-style ticket (**C**). Do not send to real QPU.

## Problem (current state)

Verified behavior of S01 spine via `run_path` (seed 0):

- `JobResult.status` can be `succeeded`.
- `measurements` often has one envelope with `value=None`, `vacuum=True`.
- Useful `inspect` output goes to MeasureSink / stdout as `valuemass` tables,
  not into Host DTOs.
- `host/rolling_replan_job.py` prints status / diagnostic codes only.

So the Host “job” story is incomplete: operators cannot retrieve a plan sample
as structured data for demos, morning handoff prototypes, or later QPU counts
mapping.

## Exit criteria

- [x] **A:** Host entry runs S01 tonight spine and exposes `JobResult` (no
      stdout scrape as the API).
- [x] **B:** Terminal `measure` appears in `JobResult.measurements` as
      **non-vacuum** for `main_disaster_response.sqx` with fixed seed (or job is
      explicitly `incomplete`/`failed` with diagnostics — never a silent fake
      success).
- [x] **C:** `TonightTicket` JSON written (`schema_version: 1`) with honesty
      block: `sim-only`, `live_qpu: false`, no optimality claim.
- [x] Vacuum / failed paths **fail closed** (no invented `sample_value`).
- [x] AT-TDD: Phase 1 Red → Phase 2 Green → Phase 3 Refactor; tests cover
      happy path + incomplete path.
- [x] S01 README documents the export command.
- [x] No live QPU SDK, no new provider technology, no Kernel Continuous /
      language axiom changes.

## Acceptance (Gherkin-style)

```gherkin
Feature: S01 tonight job result export
  Scenario: Export structured ticket from local sim job
    Given the S01 main_disaster_response entry
    When the host runs the job with seed 0
    Then a JobResult is available without scraping stdout
    And the terminal measurement envelope is non-vacuum
    And a TonightTicket JSON is written with schema_version 1
    And honesty declares sim-only and no optimality claim

  Scenario: Incomplete measurement is not a fake success ticket
    Given a job result with vacuum terminal measurement
    When the host maps to TonightTicket
    Then the export is marked incomplete or fails closed
    And sample_value is not invented
```

## TonightTicket MVP schema

Minimum fields:

```json
{
  "schema_version": 1,
  "job": {
    "status": "succeeded",
    "target": "local",
    "seed": 0,
    "entry": "…/main_disaster_response.sqx"
  },
  "plan": {
    "sample_value": null,
    "marginal": {},
    "vacuum": false
  },
  "diagnostics": [
    { "code": "…", "message": "…" }
  ],
  "honesty": {
    "execution": "sim-only",
    "live_qpu": false,
    "optimality_claim": false,
    "notes": [
      "Language-spec showcase; not a city-wide optimum proof.",
      "Ticket is a Host mapping of JobResult, not a field dispatch system."
    ]
  },
  "provenance": {
    "generated_at": "<ISO8601 optional>",
    "tool": "s01-host-export"
  }
}
```

### Mapping rules

- `plan.*` ← terminal `MeasurementEnvelope` from `JobResult.measurements`
  (last or explicitly identified measure).
- `diagnostics` ← `JobResult.diagnostics` (truncate messages OK; keep `code`).
- If vacuum or empty measurements: mark incomplete / non-zero exit; **do not**
  invent `sample_value: 0`.
- Do **not** hardcode fairness / shelter / road scores that are not present on
  `JobResult`.
- Keep keys stable for a future morning consumer (`schema_version` required).

## Deliverables

### B — Kernel / Host (minimal, only if needed)

- Ensure terminal `measure` populates `MeasurementEnvelope` (`value`,
  `marginal`, `vacuum`, …).
- Prefer existing fields; additive optional fields only if unavoidable.
- Do **not** put disaster-ticket business logic inside `compiler/staqex/`.
- Investigate before coding: why S01 yields vacuum today (`EvalResult.measure`,
  sibling discharge before `measure plan0`, inspect vs measure sink path).
- Preserve existing MeasureSink stdout contracts required by SV / bit-identical
  seeded runs where applicable (ADR 0171 lineage).

### A + C — S01 Host app

Suggested paths (implementer may split or merge):

```text
examples/showcase/S01_quantum_disaster_response/host/
  rolling_replan_job.py       # may extend
  export_tonight_ticket.py    # optional new entry
  ticket_dto.py               # optional DTO module
```

CLI example:

```bash
python3 examples/showcase/S01_quantum_disaster_response/host/export_tonight_ticket.py \
  --seed 0 \
  --out /tmp/tonight_ticket.json
```

- Exit 0 on successful ticket; non-zero on compile/runtime failure.
- Incomplete measurement: non-zero recommended; document choice.
- JSON via stdlib only (no new dependencies).

### Docs

- Update `examples/showcase/S01_quantum_disaster_response/README.md` Host section.
- Honesty: SIM-only; not an optimality proof; not live QPU.

### Tests

- Host/measure envelope coverage if Kernel path changes.
- S01 export unit/integration: seed 0 happy path; vacuum/incomplete fail-closed;
  `schema_version == 1`; `honesty.live_qpu is false`.
- Do not break existing pytest / SV gates in scope.

## Design defaults

1. Reuse `run_path` / `submit_path` / `JobResult` — do not invent a second Host ABI.
2. Ticket mapping lives only under S01 `host/` (or showcase host helpers), not Domain Kernel.
3. Soft QPU diagnostics (e.g. `E_QPU_UNSUPPORTED_CAPABILITY` for `evolve … until`)
   remain visible in the ticket — do not strip to fake a clean QPU story.
4. seed via `settings["seed"]`.
5. If vacuum fix requires language axiom changes → **stop** for Adjudicator;
   do not unilaterally change NLTS / `main -> Unit`.

## Non-goals (explicit)

- Live QPU / provider SDK / network submit (layer **D**)
- Extending CredentialPort beyond existing mock behavior
- Morning / day-2 ticket chain (tonight only; schema may leave room)
- Merging all satellite `main_*.sqx` into one job
- Kernel Continuous, Joint rational, trait specialization
- New fairness / optimality numeric models
- Victim PII or production dispatch APIs
- Changing `main` to return classical `T` instead of `Unit`
- Treating stdout `valuemass` scrape as the official API
- Accepting new ADRs without Architecture approval
- Committing on `main`

## Honesty notes (real hardware)

Implementing A–C enables **structured SIM results today**.

Real hardware still needs separately:

1. a **CH0-scale static witness** program (not full S01),
2. QASM / artifact lower that succeeds,
3. a **live** `QpuSubmitPort` / `QpuJobPort` adapter + technology selection.

Full S01 is not placeable as-is (e.g. `evolve … until`, Host-side domain work,
Lindblad lanes). Do not document this issue as “when QPU arrives, city dispatch
works.”

## Implementation process (binding)

1. Feature Path; read agent quickstart + implementation-readiness before phases.
2. Output `[DESIGN CHECK]` before tests/implementation.
3. Branch not `main` (suggested name above).
4. Phase 1 Red → Phase 2 Green → Phase 3 Refactor only as approved for the agent family.
5. Stop on unanticipated architecture/language decisions; present options.
6. Report with: branch, JobResult before/after, sample ticket summary, tests,
   residual risks.

## Agent prompt payload (optional paste)

Agents may treat this Issue as authoritative. Compact tasking:

```text
Implement LISS-0243: S01 Host tonight job result export (A→B→C MVP).
- A: surface JobResult from run_path for main_disaster_response.sqx
- B: fix/ensure non-vacuum terminal MeasurementEnvelope (or fail closed)
- C: export TonightTicket JSON schema_version 1 under host/
- Out: live QPU, morning/day2 chain, stdout scrape API, language axiom changes
- AT-TDD Red→Green→Refactor; update S01 README; stdlib json only
- Reuse compiler/staqex/host.py JobResult; no DisasterTicket in Kernel
```

## Completion report template

```markdown
## Summary
- A/B/C delivered:

## Branch / Issue
- branch:
- LISS-0243

## JobResult change
- before:
- after:

## Sample ticket
- command:
- key fields:

## Tests
- added:
- results:

## Out of scope reconfirmed
- live QPU: not done
- morning/day2: not done

## Adjudicator questions / residuals
-
```

## Dependencies

- None blocking (S01 showcase already shipped).
- Soft dependency on MeasureSink / Host measurement plumbing (already present;
  may need small fix under B).

## Priority rationale

Unblocks demos and any future “job → ticket → morning” Host pipeline without
waiting for live QPU. Completes the Host half of the S01 rolling-replan story
that currently stops at status print.
