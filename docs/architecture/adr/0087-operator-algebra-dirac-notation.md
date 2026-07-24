# ADR 0087: Operator algebra and parser-safe Dirac notation

## Status

Accepted for the LISS-0031 typed operator-algebra/domain boundary. The
function-shaped algebra forms are normative; punctuation-heavy Dirac sugar and
general symbolic lowering remain deferred follow-ups.

## Context

QPex already has reserved Ket literals such as `|0>`, `|1>`, `|+>`, and `|->`,
as well as the tensor product operator `*|*`. The language also needs typed
operator algebra for common quantum formulas without making the lexer depend on
ambiguous arbitrary-name Ket punctuation.

ADR 0086 is reserved for QFT basic-gate lowering. This decision therefore uses
ADR 0087 and does not rename or alter the QFT decision.

## Decision

1. The first operator-algebra surface is function-shaped:

   ```qpex
   adjoint(A)
   inner(phi, psi)
   outer(psi, phi)
   projector(psi)
   commutator(A, B)
   anticommutator(A, B)
   ```

   Each form is parsed as an ordinary `Call` expression and retains its source
   `Span` for diagnostics and later provenance.

2. Reserved Ket literals remain a closed lexical family. The accepted forms
   are `|0>`, `|1>`, `|+>`, `|->`, and the existing binary Ket literals. An
   arbitrary named form such as `|psi>` is not accepted by the lexer/parser.

3. `*|*` remains a dedicated tensor-product infix operator. Its precedence
   and AST representation remain independent from the pipeline operator `|>`.

4. Typed boundaries are enforced without implicit conversion:

   - `adjoint(Operator<V>) -> Operator<V>` for the current square-operator
     slice;
   - `inner(State<V>, State<V>)` produces an algebraic scalar contract;
   - `outer` and `projector` produce Operator values;
   - commutator and anticommutator require compatible operator domains;
   - algebra operations cannot contain an early `measure`.

5. Unicode bra/ket punctuation, arbitrary named Ket syntax, non-square
   operator codomains, second-quantized statistics, and general symbolic
   lowering are deferred to their respective follow-up issues.

## Consequences

- The lexer can recognize the existing Ket and tensor forms without treating
  every vertical bar as the start of a named Ket.
- Algebra operations compose with existing function, pipeline, and AST
  machinery.
- The surface is slightly more verbose than paper Dirac notation, but the
  parser boundary and diagnostics remain deterministic.
- Later notation sugar must lower to these Call forms and must not introduce a
  second algebra semantics.

## Verification

- [LISS-0031](../../issues/LISS-0031-operator-algebra-and-dirac-notation.md)
- [operator algebra acceptance specification](../../specs/qpex-operator-algebra.md)
- [operator algebra tests](../../../tests/test_operator_algebra_red.py)

