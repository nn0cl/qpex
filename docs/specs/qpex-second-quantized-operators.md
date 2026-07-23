# QPex typed second-quantized operators

Status: **accepted for the LISS-0032 typed/statistical provenance boundary**.
Exchange-law lowering, mapping provenance, and runtime execution remain out of
scope beyond the Symbolic IR metadata recorded by this slice.

## 1. Purpose

Quantum chemistry and many-body physics require creation/annihilation operators
and their statistics. A generic `Operator` must not erase whether an expression
is fermionic, bosonic, spin, or already a qubit operator.

## 2. Operator families

```text
FermionOperator<Orbitals>
BosonOperator<Modes>
SpinOperator<SiteSpace>
QubitOperator<Qubits>
```

The carrier/domain parameter is mandatory for the typed forms. An unparameterized
`Operator` remains a compatibility surface for the existing Pauli Kernel path.

## 3. Algebraic atoms

The first semantic atoms are:

```qpex
create[p]
annihilate[p]
spin_raise[i]
spin_lower[i]
```

Their exchange/commutation law belongs to the operator family, not to a
post-hoc naming convention. Canonical ordering and sign/phase changes must be
visible in the Symbolic IR.

## 4. Mapping boundary

A second-quantized operator is not automatically a qubit operator. Mapping is
an explicit transformation:

```text
FermionOperator<Orbitals>
  -> map(H, JordanWigner)
  -> QubitOperator<Qubits>
```

The mapping record must include name, input/output domains, qubit count, and
source node identity. Provider SDKs are not part of this boundary.

## 5. Acceptance scenarios

1. Fermion, boson, spin, and qubit operators are distinct type families.
2. Creation and annihilation atoms retain their family and domain.
3. Fermion and boson expressions cannot be added without an explicit typed
   transformation.
4. A fermion-to-qubit mapping is explicit and produces provenance metadata.
5. Canonical ordering is deterministic and preserves fermionic signs.
6. No mapping or ordering pass performs `measure` or imports a Provider SDK.

## 6. Non-goals

- no chemistry solver or molecular integral engine;
- no provider selection or cloud submission;
- no automatic Jordan–Wigner/Bravyi–Kitaev choice;
- no full infinite-mode bosonic execution;
- no runtime execution until the Symbolic/Resolved IR boundary is extended.
