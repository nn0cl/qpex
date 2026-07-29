# LISS-0099: Target capability profile and physical target port

## Metadata

- Local issue ID: LISS-0099
- GitHub issue: not created
- Initial/current planning size: L / L
- Owner/agent: unassigned
- Adjudicator decision points: schema/freshness/port; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: port + capability schema / P0 / L
- Depends on: LISS-0082 and LISS-0067; blocks LISS-0092, LISS-0100, LISS-0102
- Branch: `feature/liss-0099-target-capability`
- Implementation permission: **none**

## Acceptance scenarios

1. A versioned snapshot distinguishes native operations, connectivity,
   measurement/reset, timing, dynamic, carrier and computation-model support.
2. logical/physical capacity, calibration age, topology, deployment and
   resource policies are explicit; unknown/stale facts remain unknown/stale.
3. provider data is adapter-owned and no local insufficiency triggers implicit
   remote or simulator fallback.
4. CH0/CH1/NH5 fixtures share one schema and produce deterministic support or
   rejection evidence.

## Slices

| Slice | Scope |
|---|---|
| A | snapshot identity/version/freshness and unknown values |
| B | digital operations, topology, timing and dynamic capabilities |
| C | analog/native/computation-model and qudit capabilities |
| D | deployment, resource, power/memory and consent policies |
| E | physical target port, fake adapter and profile fixtures |

## Boundaries and execution

- Candidate writes: new capability VOs/port and
  `tests/test_target_capability_*.py`; exact placement approved at Red.
- Forbidden: provider SDKs in core, credentials, network calls in unit tests,
  hidden defaults/fallbacks, target fields in Semantic IR.
- Use the [bounded packet](../architecture/bounded-feature-execution-packet.md).

## Decisions, verification, planning

Approve schema ownership, freshness policy and analog/digital separation
before Red. Verify canonical snapshots, stale/unknown rejection, fake ports,
and no provider imports.

- AIP-0099-001: proposed; L; strong reasoning for schema review, code assistant
  for one approved Slice; estimate N/A until packet.
