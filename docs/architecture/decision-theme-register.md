# Decision theme register

This is the migration register for the new `DEC-*` current reading surface. Existing ADR numbers remain immutable source identifiers. The full source commit is authoritative; the tag is the human-readable recovery anchor.

| Field | Value |
|---|---|
| Source tag | `docs/pre-canonicalization-2026-08-03` |
| Source commit | `8663ba72295964069ac275b93c350e762a0844d8` |
| Recovery | `git show <source_tag>:<source_path>` |

## Theme matrix

| New ID | Theme | Current document | Source ADRs | Status |
|---|---|---|---|---|
| `DEC-0001` | Governance and collaboration | `docs/architecture/decision-themes/dec-0001-governance-and-collaboration.md` | ADR 0001, ADR 0002, ADR 0003, ADR 0004, ADR 0005, ADR 0006, ADR 0007, ADR 0008, ADR 0009, ADR 0010, ADR 0011, ADR 0012, ADR 0112, ADR 0113 | `draft — review required` |
| `DEC-0002` | State-first semantics and measurement | `docs/architecture/decision-themes/dec-0002-state-first-semantics-and-measurement.md` | ADR 0013, ADR 0014, ADR 0016, ADR 0018, ADR 0020, ADR 0021, ADR 0025, ADR 0026, ADR 0027, ADR 0030, ADR 0034, ADR 0038, ADR 0039, ADR 0040, ADR 0044, ADR 0045, ADR 0052, ADR 0060, ADR 0064, ADR 0075, ADR 0087, ADR 0088, ADR 0089, ADR 0102, ADR 0107, ADR 0114, ADR 0115, ADR 0117, ADR 0120, ADR 0122, ADR 0123, ADR 0167, ADR 0168, ADR 0173 | `draft — review required` |
| `DEC-0003` | Language surface and physicist-first DX | `docs/architecture/decision-themes/dec-0003-language-surface-and-physicist-first-dx.md` | ADR 0017, ADR 0023, ADR 0024, ADR 0035, ADR 0053, ADR 0054, ADR 0055, ADR 0056, ADR 0057, ADR 0058, ADR 0066, ADR 0067, ADR 0068, ADR 0095, ADR 0106, ADR 0165, ADR 0175, ADR 0176, ADR 0177, ADR 0178, ADR 0179, ADR 0182, ADR 0183, ADR 0184 | `draft — review required` |
| `DEC-0004` | Type-First scientific model | `docs/architecture/decision-themes/dec-0004-type-first-scientific-model.md` | ADR 0037, ADR 0074, ADR 0076, ADR 0090, ADR 0097, ADR 0101, ADR 0116, ADR 0118, ADR 0121, ADR 0124, ADR 0125, ADR 0128, ADR 0129, ADR 0130, ADR 0131, ADR 0132, ADR 0133, ADR 0134, ADR 0135, ADR 0136, ADR 0144, ADR 0145, ADR 0146, ADR 0147, ADR 0148, ADR 0149, ADR 0150, ADR 0151, ADR 0152, ADR 0153, ADR 0154, ADR 0155, ADR 0156, ADR 0160, ADR 0174, ADR 0180, ADR 0181, ADR 0185, ADR 0186 | `draft — review required` |
| `DEC-0005` | Quantum operations and runtime | `docs/architecture/decision-themes/dec-0005-quantum-operations-and-runtime.md` | ADR 0019, ADR 0022, ADR 0028, ADR 0031, ADR 0032, ADR 0033, ADR 0041, ADR 0042, ADR 0043, ADR 0046, ADR 0047, ADR 0048, ADR 0049, ADR 0050, ADR 0051, ADR 0061, ADR 0062, ADR 0069, ADR 0078, ADR 0079, ADR 0080, ADR 0081, ADR 0082, ADR 0093, ADR 0094, ADR 0096, ADR 0098, ADR 0100, ADR 0137, ADR 0138, ADR 0139, ADR 0140, ADR 0141, ADR 0142, ADR 0143, ADR 0157, ADR 0158, ADR 0159 | `draft — review required` |
| `DEC-0006` | Host, QPU, and external ports | `docs/architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md` | ADR 0015, ADR 0029, ADR 0036, ADR 0059, ADR 0063, ADR 0065, ADR 0070, ADR 0071, ADR 0072, ADR 0073, ADR 0077, ADR 0083, ADR 0084, ADR 0085, ADR 0086, ADR 0091, ADR 0092, ADR 0103, ADR 0104, ADR 0105, ADR 0108, ADR 0109, ADR 0110, ADR 0111, ADR 0119, ADR 0126, ADR 0127, ADR 0161, ADR 0162, ADR 0163, ADR 0164, ADR 0166, ADR 0169, ADR 0170, ADR 0171, ADR 0172 | `draft — review required` |
| `DEC-0007` | Documentation and decision records | `docs/architecture/decision-themes/dec-0007-documentation-and-decision-records.md` | ADR 0187 | `draft — review required` |

## Coverage invariant

- ADR files inspected: 186
- ADR assignments: 186
- Unassigned ADRs: 0
- Duplicate assignments: 0
- No source ADR is deleted by this design step.

## Migration rule

A `DEC-*` document becomes current only after its source ADR set, normative specifications, unresolved boundaries, and canonical links are reviewed. Until then, the existing ADR remains authoritative. Once accepted, superseded or duplicated source records may be removed only through the compression map with the baseline tag, full commit, original path, destination, and recovery check.
