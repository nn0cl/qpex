# ADR 0029: Host I/O only at boundaries — lift in, measure/snapshot out

## Status

Accepted (2026-07-23).

Companions: `qpex-language-spec.md` §5 Host I/O, ADR 0015 (ports),
ADR 0027 (entry / terminal measure), ADR 0028 (no threads).

## Context

Practical programs need files, network, and stdio. Mid-pipeline
`file.write(x)` would force choosing a classical atom from a superposition
(Early Collapse) and break Never Leave the State.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. **No free mid-evolution OS I/O** in pure regions (`when` / `evolve` /
   combinators / `class.step`). No ambient `File.write` / socket send that
   samples the joint.
2. **Input (lift):** host loaders such as `File.readAsState(path)` (stdlib /
   port) run at **preparation** (typically start of `main` or before pure
   evolution) and return **`State<T>`** (Dirac on loaded data, or a
   distribution encoding file uncertainty — representation TBD). Implemented
   via ports (extend ADR 0015: e.g. `StateSourcePort` / file adapter).
3. **Output (collapse sink):** `measure e` may take a **destination**:
   - default → stdout / `MeasureSinkPort`
   - `measure e to File("out.json")` → same collapse, sink writes classical
     atom (or serialized Dirac) to that adapter
   - network sinks follow the same pattern later
4. **Checkpoint logging:** `snapshot e to <Sink>` is **design-accepted** for
   evolve / long runs: host may serialize the **current joint or marginal
   representation** (PMF table / amplitudes) **without** `RngPort` and
   **without** replacing the joint by Dirac. Continuing evaluation keeps the
   same pure state. Snapshot is effectful on the host, not a language-level
   collapse. Exact syntax / rate limiting / which marginal — mini-spec later.
5. Domain core remains free of concrete filesystem / socket types; only ports
   and stdlib facades (`qpex.io.File`) appear at the boundary.
6. AST: `Measure { expr, sink? }`, `Snapshot { expr, sink }`, preparation
   calls remain ordinary `Call` to port-backed functions (effect-marked).

## Consequences

Positive:

- Keeps mathematical purity of Joint→Joint while enabling real I/O.
- Aligns sinks with terminal measurement narrative.

Negative:

- Snapshot vs “true non-demolition” philosophy needs careful docs so agents
  do not equate snapshot with `measure`.
- Streaming formats (HDF5 chunks) are adapter details.

## Enforcement

Reject mid-pure-region file/network writes that imply sampling. Prefer
`measure … to …` for final classical output; `snapshot` only for
non-collapsing host logs.
