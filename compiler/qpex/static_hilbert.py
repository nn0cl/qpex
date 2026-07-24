"""Shared policy for the Static Hilbert Kernel MVP."""

# This is a compiler safety budget, not a runtime register allocation limit.
# Target-specific routing/resource profiles remain a separate follow-up.
MVP_MAX_LOGICAL_QUBITS = 1024
