# 17 — Static register elaboration

This small QPU-oriented example demonstrates the proposed/accepted LISS-0026
surface implemented by ADR 0069.

```qpex
forEach q in register(3) {
    apply(H, q)
}
```

`q` is an opaque wire handle. The compiler expands the body into three `H`
operations before OpenQASM emission or Job submission. No integer index is
visible in the Kernel source, and no measurement controls circuit size.

The source remains executable by the local simulator. The final `measure` is
still the only observation boundary.

```bash
python3 -m compiler.qpex check examples/17_static_register_foreach/main_static_register.qpex
python3 -m compiler.qpex emit-qasm examples/17_static_register_foreach/main_static_register.qpex
```

Provider SDKs, credentials, retries, and Job polling remain Host concerns.

## Next static surface

The accepted type-level direction is documented separately and is not yet an
executable example:

```qpex
QubitRegister<3> reg = system()
forEach q in reg {
    apply(H, q)
}
```

See [the Static Hilbert Kernel specification](../../docs/specs/qpex-static-hilbert-kernel.md).
