# QPex finite mathematical binder lowering

Status: **accepted for LISS-0043 Phase 3 reviewed**. Decision: [ADR 0088](../architecture/adr/0088-finite-binder-lowering.md).

## Normative surface

```qpex
sum (i in Index<0..N-2>) {
    coefficient * Pauli[i] * Pauli[next(i)]
}
```

`Index<start..end>` is inclusive and statically finite. The first boundary
policy is Open. `next(i)` must resolve within the containing static register;
otherwise compilation fails with `BINDER_INDEX_OUT_OF_BOUNDS`.

## Lowering contract

The resolved output is a concrete Pauli Operator tree. The compiler also
retains binder provenance containing:

- source span;
- binder variable;
- resolved inclusive domain;
- expanded term count;
- resource-check result.

The executable operator is concrete; the symbolic source is retained only as
provenance and is not silently used as a runtime fallback.

## Diagnostics

| Condition | Diagnostic |
|---|---|
| `next(i)` crosses the Open boundary | `BINDER_INDEX_OUT_OF_BOUNDS` |
| empty, reversed, negative, or invalid range | `BINDER_DOMAIN_ERROR` |
| expansion exceeds the resource budget | `BINDER_RESOURCE_ERROR` |
| runtime/Host value controls the range | `PHASE_TYPE_VISIBILITY_ERROR` |

## Deferred

Periodic boundaries, `product`, `Basis<N>`, indexed coefficient arrays,
arbitrary functions, non-Pauli operators, symbolic runtime fallback, and
direct QPU/provider lowering are not part of this slice.
