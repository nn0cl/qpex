# ADR 0100: Public resource budgets for binder expansion and simulation

## Status

**Accepted design boundary** (2026-07-26); the dependency-free manifest and
estimator slice was implemented and reviewed under LISS-0062 (2026-07-27).
This ADR does not authorize provider integration or QPU capability discovery.

## Context

Mathematical binders are intentionally written in terms of domains and
expressions. Their Cartesian expansion can nevertheless grow faster than the
source text suggests. The compiler, simulator, and physical target have
different resource responsibilities, so one hidden global limit would make a
failure difficult to interpret and would blur the Theory/Execution boundary.

The current implementation already has two safety constants, but they do not
form a user-facing policy:

- `MAX_EXPANSION_TERMS = 1_000_000` protects compiler expansion.
- `MVP_MAX_LOGICAL_QUBITS = 1024` protects the static Hilbert/compiler path;
  it is not a simulator memory guarantee and is not a QPU capability profile.

## Decisions

### D1 — Separate budgets by responsibility

The first public resource model has three distinct profiles:

| Profile | Measures | Owner | Typical failure |
|---|---|---|---|
| `BinderExpansionBudget` | candidate binder tuples and retained terms | compiler lowering | `BINDER_RESOURCE_ERROR` |
| `SimulatorResourceBudget` | estimated state storage and CPU work | simulator execution | simulator resource diagnostic |
| `QpuTargetProfile` | logical/physical qubits, gates, depth, topology | host/QPU planning | target capability/resource diagnostic |

No profile may silently substitute for another. In particular, a simulator
must not be described as having the compiler's logical-qubit limit, and a
compiler must not claim to have checked a provider's physical capacity.

### D2 — User-visible policy is `Warn` or `Abort`

For a configured budget, the user may select one action:

```text
resource_policy = Warn | Abort
```

The default is `Abort`, because silently producing a partial operator is not
acceptable for a scientific calculation. `Warn` is an explicit exploratory
mode and still records the estimate and decision in provenance.

- Under `Warn`, the compiler may continue only when the configured profile
  permits continuation; it must emit a warning and preserve the estimate.
- Under `Abort`, no executable operator, QPU IR, or simulator result is
  produced after the budget is exceeded.
- Neither mode permits truncation, term dropping, symbolic fallback, or silent
  clamping.

### D3 — One configured binder threshold, plus a non-configurable emergency cap

The binder profile exposes one user-facing term threshold and one action. The
current proposed profile defaults are:

```text
binder_term_limit = 100_000
resource_policy = Abort
```

The existing `1_000_000` term cap remains a compiler safety ceiling. It is not
a user override and always aborts with `BINDER_RESOURCE_ERROR`. The profile
threshold may therefore request early warning/abort, but it may not disable
the emergency ceiling.

These numbers are profile defaults, not permanent language semantics. They
must be benchmarked and versioned before implementation is accepted.

### D4 — Users configure the profile through `staqex.toml`

Resource budgets are user-configurable through `staqex.toml`, not by adding
operational controls to mathematical binder syntax. The manifest schema starts
with an explicit version:

```toml
schema_version = 1

[resources.binder]
term_limit = 100_000
policy = "Abort"

[resources.simulator]
policy = "Abort"
```

If a field is absent, the compiler uses the versioned default profile. If a
field is malformed or unsupported, configuration validation fails before
compilation; it is never silently ignored.

The manifest may select a lower user-facing threshold or `Warn` policy, but it
must not disable or raise the non-configurable emergency ceiling. It also
cannot change language semantics, introduce truncation, or claim provider
capabilities.

### D5 — Candidate and retained counts are distinct

For a constrained binder, the compiler accounts for the Cartesian candidate
tuple count before `where` filtering and the retained term count after
filtering. A guard is not a mechanism for evading a candidate-space safety
check. Provenance records both counts when available.

### D6 — Diagnostics are explicit and non-repairing

The proposed diagnostics are:

- `BINDER_RESOURCE_WARNING` for a configured `Warn` continuation;
- `BINDER_RESOURCE_ERROR` for configured `Abort` or the emergency ceiling.

Diagnostics identify the binder source span, budget profile, limit, candidate
count, retained count when known, and selected action. They never normalize,
truncate, reorder, or silently discard terms.

### D7 — Simulator budgets use representation-aware estimates

The simulator profile estimates memory and CPU work from the selected state
representation rather than using one universal qubit count. The first model
distinguishes at least:

```text
StateVector:    2^n × complex_size × workspace_factor
DensityState:   4^n × complex_size × workspace_factor
Lindblad RK4:   density-matrix storage × integration workspace factor
```

The estimate is conservative and must be checked before execution. The
existing `MVP_MAX_LOGICAL_QUBITS` remains a static Hilbert/compiler boundary;
simulator capability and QPU target capability require separate profiles.

### D8 — `Warn` is simulator-only

`Warn` is permitted for local simulator exploration. QASM generation and QPU
submission use `Abort` only, because a warning must not permit an oversized or
unverified program to cross into a deployment boundary.

### D9 — Manifest loading is a Host configuration boundary

The initial manifest is `staqex.toml` with an explicit `schema_version`:

1. an explicitly supplied `--manifest <path>`;
2. `staqex.toml` at the project root;
3. the versioned default profile when no manifest is present.

The loader does not search arbitrary parent directories. File access belongs
to a Host/CLI adapter and produces an immutable `ResourceProfile` DTO for the
compiler or simulator. The Kernel does not read TOML or the file system.

Missing implicit configuration uses defaults. An explicitly requested but
missing file, malformed TOML, unsupported schema, or invalid field is a hard
configuration diagnostic and is never silently ignored.

### D10 — MVP simulator estimates are representation-aware

The first estimator uses `complex_f64_bytes = 16` and conservative workspace
factors:

```text
StateVector:  2^n × 16 × 3
DensityState: 4^n × 16 × 3
Lindblad RK4: 4^n × 16 × 6
```

The estimator returns an immutable `SimulationResourceEstimate` containing the
representation, logical-qubit count, estimated bytes, workspace factor, and a
versioned formula identifier. CPU seconds are not predicted in the MVP; a
future work-unit estimator may be added independently.

### D11 — Resource diagnostics are stable and contextual

The initial configuration diagnostics are:

- `RESOURCE_MANIFEST_NOT_FOUND` for an explicitly requested missing file;
- `RESOURCE_MANIFEST_PARSE_ERROR` for malformed TOML;
- `RESOURCE_MANIFEST_SCHEMA_ERROR` for an unsupported schema version;
- `RESOURCE_SETTING_INVALID` for invalid values or policies.

Runtime planning diagnostics are:

- `SIMULATOR_RESOURCE_WARNING` for a permitted local-simulator warning;
- `SIMULATOR_RESOURCE_ERROR` for abort-only lanes or an exceeded hard limit.

Resource diagnostics include the profile, representation, logical-qubit count,
estimate, limit, policy, and formula version when those fields are available.
No diagnostic authorizes truncation, normalization, or silent state reduction.

## Consequences

- Resource behavior becomes visible and reproducible rather than hidden in a
  compiler constant.
- The language remains mathematical: source expressions do not contain
  operational knobs unless a resource profile is explicitly attached at the
  compilation/execution boundary.
- `Warn` is useful for local exploration but is unsuitable as a default for
  production scientific results.
- A future manifest loader can supply the profile without changing binder
  syntax. The manifest is a configuration boundary, not a new language form.
- Local exploration remains possible without weakening QASM/QPU safety.

## Deferred follow-ups

- Benchmark evidence for the provisional `100_000` binder default.
- Benchmark calibration of simulator workspace factors and the
  `memory_limit_bytes` default.
- Runtime application of `SIMULATOR_RESOURCE_WARNING` and
  `SIMULATOR_RESOURCE_ERROR` across simulator/QASM/QPU lanes.
- The complete `staqex.toml` schema beyond `schema_version = 1`.

## Related documents

- [LISS-0055](../../issues/LISS-0055-binder-body-as-operator-expression.md)
- [ADR 0088](0088-finite-binder-lowering.md)
- [ADR 0095](0095-design-horizon-ideal-form-first.md)
- [ADR 0096](0096-indexed-operator-and-binder-surface.md)
- [LISS-0062](../documentation-compression-map.md)
