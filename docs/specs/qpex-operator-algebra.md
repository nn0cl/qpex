# QPex operator algebra and Dirac operations

Status: **accepted for the LISS-0031 typed algebra/domain boundary**.
Domain/codomain metadata, Dirac punctuation sugar, and runtime lowering remain
out of scope beyond the square-operator carrier metadata described below.

## 1. Purpose

QPex already supports ket literals, Pauli operators, tensor products, and
expectation as specialized forms. This slice adds the typed algebra needed to
express common quantum formulas without flattening every operation into an
untyped `Operator`.

## 2. First operator family

The initial semantic forms are function-shaped so their type contracts can be
implemented without prematurely committing the lexer to Unicode punctuation:

```qpex
adjoint(A)
inner(phi, psi)
outer(psi, phi)
projector(psi)
commutator(A, B)
anticommutator(A, B)
```

Dirac notation (`<phi|`, `|psi>`, and composition sugar) remains a surface
syntax decision after these typed forms are stable. The function-shaped forms
must preserve the same mathematical meaning and source provenance.

## 3. Type contracts

| Form | Contract |
|---|---|
| `adjoint(A)` | `Operator<V, W> -> Operator<W, V>` |
| `inner(phi, psi)` | `State<V> × State<V> -> Scalar` |
| `outer(psi, phi)` | `State<V> × State<V> -> Operator<V, V>` |
| `projector(psi)` | `State<V> -> Operator<V, V>` |
| `commutator(A, B)` | `Operator<V, V> × Operator<V, V> -> Operator<V, V>` |
| `anticommutator(A, B)` | same domain rule as commutator |

`Operator` domain/codomain metadata may be represented by a future generic
type; it must not be erased merely because current Pauli operators are square.
`inner` is classical only as an algebraic scalar result; it does not measure a
runtime `State` and cannot be used as a mid-program collapse.

The first accepted type surface is `Operator<V>` for a square operator over
carrier `V`. An unparameterized `Operator` remains a compatibility form until
all operator declarations have explicit domain metadata.

## 4. Restrictions

- incompatible Hilbert carriers are rejected;
- `adjoint` does not silently change a state into an operator;
- commutator/anticommutator require compatible operator domains;
- `measure`, I/O, and provider calls are not part of these operations;
- no implicit conversion between `State<T>`, `Operator<T>`, and host values;
- the current Kernel may retain a design-only node when it cannot execute the
  operation yet; it must not claim a numerical result.

## 5. Acceptance scenarios

1. A Pauli operator accepts `adjoint` and preserves its operator type.
2. Two compatible state carriers accept `inner` and return an algebraic scalar
   contract without consuming RNG.
3. Compatible operators accept `commutator` and `anticommutator`.
4. A state/operator mismatch produces an operator-algebra diagnostic.
5. Different finite Hilbert carriers produce a domain mismatch diagnostic.
6. No operation introduces an implicit measurement before terminal `measure`.

## 6. Follow-up

Bra/ket punctuation, non-square operator domains, second-quantized statistics,
density/CPTP operators, and serialized Symbolic IR are LISS-0032, LISS-0011,
LISS-0037, and LISS-0033 concerns.
