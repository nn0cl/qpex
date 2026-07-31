# Staqex v1 QPU capability honesty catalog

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — LISS-0135 |
| Related | [diagnostic catalog App B](staqex-v1-diagnostic-catalog.md); ADR 0057/0071/0079; [ADR 0057 showcase boundary](staqex-v1-adr-0057-showcase-boundary.md) |
| Not | New QPU lowering; live provider credentials; changing Kernel semantics |

```markdown
[DESIGN CHECK]
- Scope: single honesty table — writable / SV-runnable vs QPU·QASM emission.
- Evidence: compiler reject codes only; no invented capabilities.
```

## Normative reading

A Staqex program may be a **valid Kernel program** (parse, typecheck, Joint/SV
run) and still be **not placeable** on a quantum computer backend. Fail-closed
emission must use an explicit reject code — never silent rewrite.

| Capability | Kernel / SV | QPU / OpenQASM | Reject code | ADR / Issue |
|---|---|---|---|---|
| `evolve … until … max N` | Bounded pure repetition | Not lowerable as runtime loop | `E_QPU_UNSUPPORTED_CAPABILITY` | ADR 0079; LISS-0012; `backend/qasm/lower.py` |
| Density / Lindblad open systems | CPU RK4 / numeric slices | QPU execution deferred | lane policy (no silent QPU success) | ADR 0057; LISS-0131 |
| Qudit / qutrit (D≠2) | D=3 SV MVP (LISS-0112) | No silent qubit embed | `UNSUPPORTED_LOCAL_DIMENSION` | LISS-0074/0112; `lower.py` |
| User `fn` call from `main` → QASM | Kernel OK | Reject | `QASM_FUNCTION_CALL_UNSUPPORTED` | LISS-0049 |
| `evolve under H for t` without Suzuki | SV `expm_ih` OK | Needs explicit Trotter policy | `QASM_TROTTER_STEPS_REQUIRED` | ADR 0094; LISS-0050 |
| Unsupported H / bad time / complex coeff | — | Reject | `QASM_TROTTER_UNSUPPORTED_H` / `_BAD_TIME` / `_COMPLEX_COEFF` | `backend/qasm/trotter.py` |
| Dynamic QPU / mid-circuit measure | capability / Fake P0 | Static IR / CH0 reject | `E_QPU_UNSUPPORTED_CAPABILITY`; `DYNAMIC_*`; `CH0_FORBIDDEN_DYNAMIC`; `MID_CIRCUIT_MEASUREMENT_REQUIRES_DYNAMIC_LANE` | ADR 0071; LISS-0028/0077 |
| CH0-outside opcode / timing / subroutine | — | Reject | `CH0_UNSUPPORTED_OPERATION`; `CH0_FORBIDDEN_*` | LISS-0097; `ch0_emit.py` |
| Observation / sim snapshot | Host/sim OK | QPU snapshot unsupported | `OBSERVATION_QPU_SNAPSHOT_UNSUPPORTED` | ADR 0089/0091; `observation.py` |
| Live provider submit / credentials | ports only | Not in Kernel | Host / permanent-out | LISS-0016; open-topics permanent-out |
| Second-quant mapping outside families | Partial JW→QASM | Reject | `SECOND_QUANTIZATION_MAPPING_UNSUPPORTED` | ADR 0093 |
| Unknown / non-CH0 gate opcode at emit | — | Reject | `E_QPU_UNSUPPORTED_CAPABILITY` | `backend/qasm/emitter.py` |

## Sync obligations

- Keep [diagnostic catalog](staqex-v1-diagnostic-catalog.md) Appendix B aligned.
- Coverage ledger “QPU / OpenQASM lanes” stays **partial**; live provider **out**.
- Showcase must teach writable ≠ executable when using any row above.
