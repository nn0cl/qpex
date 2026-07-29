# Current quantum hardware delivery envelope research (2026-07-30)

## Purpose

This note grounds the P0/P1 delivery plan in machines that exist now while
preserving the scale-free semantics proposed by ADR 0108–0110.

It does not select a provider or claim that qubit counts, fidelities, quantum
volume, or analog site counts are interchangeable.

## Current primary evidence

### Small local and on-premises systems

IQM publishes a five-qubit Spark on-premises system with typical two-qubit
fidelity of at least 99%, five-qubit GHZ support, approximately 11 kW mean
power, and pulse-level access.

Design implication: a common physical smoke profile should fit in 2–5 qubits,
use shallow circuits, and require no cloud-only assumption.

### High-fidelity digital systems

Quantinuum publishes System Model H2 with 56 fully connected qubits,
mid-circuit measurement, conditional logic, qubit reuse, typical two-qubit
infidelity around `10^-3`, and limited parallel two-qubit operations.

IBM publishes a 156-qubit Heron r3 with median two-qubit error around
`1.17e-3`. IBM also publishes utility-scale dynamic-circuit availability and a
roadmap execution quality point of approximately 5,000 gates on current
156-qubit-class systems.

Design implication: P1 can exercise nontrivial digital programs, dynamic
control, and routing today, but target-specific error, topology, timing, and
parallelism budgets remain mandatory. The roadmap gate count is not a portable
guarantee.

### Analog neutral-atom systems

QuEra publishes Aquila as a publicly accessible 256-atom neutral-atom system
with programmable analog behavior and local-control evolution.

Design implication: a current-hardware plan cannot use gate count as the only
execution axis. Analog site count, geometry, Hamiltonian family, pulse
schedule, and measurement contract require a distinct capability profile.

### Portable interchange boundary

OpenQASM 3 supports parameterized circuits, classical feed-forward, timing,
and near-term hardware communication, but the specification explicitly allows
hardware implementations to support only a subset.

Design implication: successful syntax validation does not prove target
executability. Every emitted artifact identifies its OpenQASM subset and the
target capability snapshot used to validate it.

## Conservative delivery profiles

These profiles are acceptance fixtures, not hardware maxima.

| Profile | Purpose | Conservative envelope |
|---|---|---|
| `CH0_COMMON_PHYSICAL` | P0 common real-device smoke | 2–5 qubits; at most 20 entangling operations; depth at most 100; 1,000–10,000 shots; terminal measurement |
| `CH1_DIGITAL_RESEARCH` | P1 target-resolved digital witness | normally at most 16 active qubits; at most 200 entangling operations; depth at most 500; 1,000–20,000 shots; dynamic operations only when declared |
| `CH1_ANALOG_RESEARCH` | P1 native-Hamiltonian witness | 16–64 active sites; finite geometry; supported Hamiltonian family; bounded schedule; terminal site measurement |
| `SIM0_EXACT` | portable exact oracle | normally at most 20 qubits under the current 8 GiB default budget; deterministic seed and tolerance |
| `SIM1_MIXED` | density/channel oracle | normally at most 10 qubits; explicit memory estimate and rejection |

The digital values leave room beneath published hardware maxima for routing,
calibration variation, error accumulation, and repeatable CI/manual evidence.
The analog profile uses fewer than the published site maximum for the same
reason.

## Five-year planned-system evidence (2026–2031)

First-party roadmaps currently describe several materially different
fault-tolerant targets inside the next five years:

- IBM Starling for 2029: 200 logical qubits and 100 million logical gates on a
  modular error-corrected system;
- QuEra Libra for 2028: 256 logical qubits, more than 10,000 physical qubits,
  logical error around `10^-6`, and approximately one million reliable logical
  operations;
- QuEra next generation for 2028/29: more than 1,000 logical qubits, more than
  20,000 physical qubits, logical error around `10^-9`, and more than one
  billion operations;
- Quantinuum Apollo by 2030: hundreds of logical qubits and millions of
  operations on a universal fault-tolerant system.

These are vendor goals, not current capabilities or guaranteed deliveries.
They justify a separate five-year profile family:

| Profile | Planned stress envelope |
|---|---|
| `NH5_NISQ_MODULAR` | 100–1,000 physical carriers; `5e3–2e4` quality-qualified operations; mitigation and partitioning |
| `NH5_FT_MEGA` | 100–300 logical carriers; `1e6–1e8` logical operations per job; sustained QEC |
| `NH5_FT_GIGA` | 1,000+ logical carriers; `1e9`-class logical operations per campaign; modular/parallel planning |
| `NH5_NATIVE_LARGE` | `1e3–1e4` physical sites; native evolution or QEC profile; geometry/loss/reload explicit |

`NH5_FT_GIGA` is an upper-roadmap stress fixture. P0/P1 completion does not
depend on its delivery. All NH5 profiles require compact plans, exact resource
counts, capability negotiation, and deterministic rejection without any
provider-specific semantic type.

## Evidence rule

A current-hardware witness records:

- source and compiler revision;
- semantic and algorithm-plan identities;
- target capability and calibration snapshot;
- logical and physical resource estimate;
- emitted artifact and supported subset;
- shots, seed when applicable, raw counts, and uncertainty;
- queue, attempt, rejection, and mitigation metadata;
- whether execution was simulated, emulated, or physical.

No raw or noisy result is labelled a theorem, proof of advantage, or exact
semantic equality.

## Primary sources

- IQM, [IQM Spark](https://iqm.tech/products/iqm-spark/).
- Quantinuum, [System Model
  H2](https://www.quantinuum.com/products-solutions/quantinuum-systems/system-model-h2).
- Quantinuum, [H2 product data
  sheet](https://docs.quantinuum.com/systems/data_sheets/Quantinuum%20H2%20Product%20Data%20Sheet.pdf).
- IBM, [A decade of quantum on the
  cloud](https://newsroom.ibm.com/2026-05-04-ibm-a-decade-of-quantum-on-the-cloud).
- IBM, [Utility-scale dynamic
  circuits](https://www.ibm.com/quantum/blog/utility-scale-dynamic-circuits).
- QuEra, [Aquila history and 256-atom
  system](https://www.quera.com/about).
- OpenQASM, [Introduction and implementation
  scope](https://openqasm.com/intro.html).
- IBM, [Quantum 2030
  roadmap](https://www.ibm.com/roadmaps/quantum/2030/).
- QuEra, [Quantum product
  roadmap](https://www.quera.com/our-quantum-roadmap).
- Quantinuum, [Accelerated fault-tolerant
  roadmap](https://www.quantinuum.com/press-releases/quantinuum-unveils-accelerated-roadmap-to-achieve-universal-fault-tolerant-quantum-computing-by-2030).

## Limits

- Published vendor specifications are first-party claims and may change.
- Qubit and site counts do not measure useful application scale by themselves.
- The profiles deliberately underfill hardware; they optimize reproducibility
  and cross-layer evidence rather than record-setting size.
- No provider, SDK, account, price, or live integration environment is
  selected by this note.
- NH5 values are roadmap-derived design loads and must be refreshed when
  vendors revise or deliver their systems.
