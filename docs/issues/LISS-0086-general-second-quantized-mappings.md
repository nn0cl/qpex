# LISS-0086: General second-quantized mappings

## Metadata

- Local issue ID: LISS-0086
- GitHub issue: not created
- Initial/current planning size: XL / XL
- Owner/agent: unassigned
- Adjudicator decision points: mapping families; each Slice/phase
- Status/phase: **proposed** / `phase-0-design`
- Type/priority/size: scientific lowering / P1 / XL
- Depends on: LISS-0081, LISS-0083 and LISS-0032
- Branch: `feature/liss-0086-second-quantized-mappings`; implementation:
  **none**

## Acceptance scenarios

1. mapping choice, orbital/mode order, statistics and source operator
   provenance are explicit.
2. Jordan–Wigner, parity, Bravyi–Kitaev and bounded boson/spin mappings share a
   contract but never silently substitute for one another.
3. normal ordering, exchange simplification and tapering carry proof/witness
   evidence.
4. small mapped models agree with exact references, normally within 12 active
   qubits; external chemistry data remains behind a port.

## Slices and boundaries

| Slice | Scope |
|---|---|
| A | mapping request/result/order provenance |
| B | parity and Bravyi–Kitaev small-model mappings |
| C | normal ordering and exchange-law verifier |
| D | symmetry tapering witness |
| E | bounded boson/spin mapping and external-data port |

Candidate writes: `second_quantization.py` or a new mapping module and approved
`tests/test_second_quantized_mapping_*.py`. Chemistry SDKs, hidden active-space
selection and unsupported truncation are forbidden. Use the
[bounded packet](../architecture/bounded-feature-execution-packet.md).

## Planning

- AIP-0086-001: proposed; XL; strong scientific review and code assistant for
  one mapping Slice at a time.
