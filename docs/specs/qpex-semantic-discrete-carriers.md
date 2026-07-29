# Staqex semantic discrete carriers

Status: **accepted for the LISS-0038 carrier slice**.
Runtime indexed evaluation and dependent syntax remain out of scope.

## Principle

Staqex must not use a single weakly meaningful `Int` for dimensions, indices,
measurement counts, and physical discrete values. Machine representation may be
shared internally; surface semantics and legal operations must not be shared
implicitly.

## Phase matrix

| Carrier | Theory | Experiment | Workflow | Execution/Host |
|---|---:|---:|---:|---:|
| `Index<N>` | yes, as a domain label | yes | no by default | no by default |
| `Basis<N>` | yes | yes | no | no |
| `Dimension` | declaration metadata | configuration | no | yes |
| `ShotCount` | no | no | yes | yes |
| `IterationCount` | no | no | yes | yes |
| `State<T>` | yes | yes | result input only | opaque result input |
| `Param<T>` | symbolic gate parameter | binding contract | yes | concrete binding only |
| `Host<T>` | no | no by default | yes | yes |

The exact phase names remain subject to LISS-0034, but the dependency direction
must remain `execution -> workflow -> experiment -> theory`.

## Required rules

1. `Index<N>` is bounded by its declared finite domain.
2. `Basis<N>` is a quantum/theory carrier and is not an index by implicit
   conversion.
3. `ShotCount`, `IterationCount`, and backend/resource values cannot appear in
   a theory expression.
4. `State<T>` does not turn a meta count into an allowable quantum carrier.
5. Any conversion between semantic carriers is explicit and must state its
   domain or physical meaning.
6. Legal arithmetic is defined per carrier; representation equality is not a
   reason to provide `+`, `-`, `<`, or `%`.

## Acceptance examples

Accepted design examples:

```staqex
meta sites: Dimension = 8
state level: State<EnergyLevel<8>>
```

Rejected examples:

```staqex
state x: State<Int> = shots
Z[shots]
Basis<8>(shot_count)
```

The exact syntax is illustrative until the surface grammar is reviewed. The
semantic rejection and phase boundary are normative for this design slice.

## Dependent work

Only after this specification is accepted may LISS-0030 define `Index<N>`
binders and indexed operator access. LISS-0031 and LISS-0032 inherit the same
carrier distinction.
