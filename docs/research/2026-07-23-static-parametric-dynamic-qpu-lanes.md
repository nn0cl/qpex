# Research note: Static, parametric, and dynamic QPU lanes

## Scope

This note supports ADR 0069 revision and proposed ADR 0070/0071. It compares
the language boundary with current OpenQASM/QPU execution models. It is
informative; the ADRs and acceptance specifications are authoritative.

## Findings

1. OpenQASM 3 describes both low-level classical instructions inside a circuit
   and external classical functions. This supports separating static circuit
   elaboration from a later dynamic-control lane rather than treating every
   classical value as ordinary Kernel state.
2. IBM Quantum documents dynamic circuits with mid-circuit measurement and
   classical feed-forward, including `if`, `switch`, `for`, and `while`
   constructs. This is a real execution model, not merely a host-side loop.
3. Amazon Braket documents dynamic circuits as an experimental capability on
   selected IQM devices, with device-specific instructions and constraints.
4. Amazon Braket Hybrid Jobs document free parameters whose values can be
   updated without recompiling the circuit. This supports a separate symbolic
   `Param<T>` boundary rather than passing ordinary `Host<T>` values through
   Kernel logic.

## Architectural implication

The sources show a three-way split:

```text
Static Hilbert Kernel -> symbolic parameter binding -> provider dynamic lane
```

Static register shape and `forEach` are portable compilation concerns.
Symbolic parameters are circuit data with Host binding. Dynamic circuits are
backend-capability-dependent programs with timing and feed-forward semantics.

## Sources

- [OpenQASM 3 classical instructions](https://openqasm.com/versions/3.0/language/classical.html)
- [IBM Quantum classical feed-forward and control flow](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow)
- [Amazon Braket experimental dynamic circuits](https://docs.aws.amazon.com/braket/latest/developerguide/braket-experimental-capabilities.html)
- [Amazon Braket Hybrid Jobs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)

## Uncertainty

Provider support, limits, and syntax are time-dependent. No provider-specific
behavior is promoted into Staqex normative semantics by this note.
