# Staqex v1 OpenQASM static CH0 plan (LISS-0097 P0 package)

| Field | Value |
|---|---|
| Status | **complete** — P0 integrated Red/Green/Refactor; final PR/merge on branch |
| Authority | WP-0025 E4; WP-0029 P0-B; ADR 0108–0111 Accepted non-authorizations |
| Depends on | LISS-0082/0083/0087 **complete**; LISS-0094 **complete**; LISS-0099 **complete** (CH0 fixture) |
| Blocks | LISS-0100 (live artifact path); informs LISS-0077 dynamic emission later |
| Shipping target | Python package `compiler/staqex` (`backend/qasm/`) |
| Issue | [LISS-0097](../issues/LISS-0097-openqasm-3-backend-completion.md) |
| Intake | [2026-07-31 integrated plan intake](../collaboration/traces/2026-07-31-liss-0097-integrated-plan-intake.md) |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: one P0 integrated package for static
  CH0_COMMON_PHYSICAL OpenQASM emission — declared version/subset manifest,
  fail-closed unsupported plans (no empty-program or simulator fallback),
  parameters/declarations, measurement/result metadata with source-linked
  diagnostics, and an independent parse check distinct from capability
  validation.
- Specifications and files inspected: LISS-0097 Issue; WP-0025 Current next /
  E4; WP-0029 P0-B; delivery envelope CH0; compiler blueprint §6.2; existing
  backend/qasm emitter and codegen/openqasm.py; LISS-0049 rejection boundary;
  LISS-0094/0099 integrated packages; bounded packet.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  proposed compiler/staqex/backend/qasm/ch0_emit.py (or adjacent module);
  OpenQasmSubsetManifest, Ch0EmitRequest, Ch0EmitResult, EmitDiagnostic,
  IndependentQasmParsePort + FakeIndependentQasmParser; wrap/extend existing
  emitter without rewriting language semantics; codegen/openqasm.py remains
  thin CLI facade unless migration is separately approved.
- Applicable constraints: Clean Architecture adapters; Never Leave the State;
  AT-TDD gates; no provider SDK; successful text ≠ target executability;
  Semantic IR must not gain OpenQASM nodes.
- Decisions, assumptions, and unresolved ambiguities: this intake authorizes
  only the P0 static CH0 package (former A–C as internal dimensions). Slice D
  (subroutine/inlining) needs separate Architecture review; E (dynamic) waits
  on LISS-0077; F (timing/barriers) is deferred follow-up. Emitted version
  string must be explicit (existing code mentions 3.0; roadmap says 3.1) —
  choose a declared subset id without inventing unsupported 3.1 features.
  Independent parser Technology selection is deferred; P0 uses a Fake parse
  port that checks structural invariants of success artifacts.
- Included and omitted AI context: include Issue/WP, CH0 bounds, existing
  qasm backend paths, blueprint §6.2; omit provider SDKs, live QPU submit,
  full OpenQASM 3 grammar dumps, QIR.
- Task routing (model/assistant/tool): design synthesis by capable assistant;
  Red/Green later on Shipping Kernel Python with deterministic tests.
- Input/output evidence contract when AI output is involved: repository
  artifacts in; reviewable subset/emit contracts out; no hidden reasoning as
  runtime evidence.
- Verification plan: link/path and claim sync, prohibited-boundary search,
  git diff --check; no compiler source or tests in this intake.
```

## 1. Boundary

```text
verified static plan / CH0 profile demand
  -> subset manifest + capability gate
  -> emit OpenQASM text (declared version/subset)
  -> IndependentQasmParsePort.parse(text)   # syntax/structure only
  -> Ch0EmitResult (ok | rejected; never empty success)
```

LISS-0097 P0 records **portable static OpenQASM emission for CH0**. It does
not:

- select a live provider or submit jobs (LISS-0100);
- claim that parse success means a physical target can execute the program;
- emit dynamic/timing/subroutine features in this package;
- rewrite Semantic / Physics / Theory IR;
- fall back to simulator ports or empty programs on unsupported input.

## 2. Proposed DTO / port vocabulary

Names are design candidates, not implementation authorization.

- `OpenQasmSubsetManifest`: subset id (e.g. `CH0_STATIC_V1`), declared
  OpenQASM version string, allowed gates/ops, qubit bound, parameter policy,
  measurement policy, forbidden features (dynamic/timing/subroutine).
- `Ch0EmitRequest`: plan handle/fixture, profile id `CH0_COMMON_PHYSICAL`,
  optional parameter bindings, provenance token.
- `EmitDiagnostic`: stable code + message + optional source span token.
- `Ch0EmitResult`: `status` accepted|rejected, `qasm_text` (None when
  rejected), `manifest`, `diagnostics`, `parse_ok` when accepted.
- `IndependentQasmParsePort`: `parse(text) -> ParseReport` (structure only).
- `FakeIndependentQasmParser`: accepts well-formed CH0 success text; rejects
  empty/truncated artifacts without importing a third-party parser package.

## 3. Acceptance mapping (integrated Red)

| Acceptance | Red coverage intent |
|---|---|
| Declared version/subset | success artifact header/manifest fields are explicit |
| No empty / no simulator fallback | unsupported and empty plans reject; `qasm_text is None`; no simulator_port import as fallback |
| Independent parse | Fake parser accepts every accepted artifact; rejects empty string |
| Params / measure metadata | bounded CH0 fixture emits parameters and measure/result metadata |
| Source-linked diagnostics | rejection diagnostics carry stable codes |
| Isolation | module does not import Semantic IR builders as emit inputs; no SDK imports |
| Deferred features | dynamic/timing/subroutine requests reject with named dimensions |

## 4. Internal review dimensions (not gates)

| Dimension | Must remain reviewable in one Red suite |
|---|---|
| A | static CH0 subset manifest and failure contract |
| B | parameters and deterministic declarations |
| C | measurement/results and source annotations |

Deferred outside this package (not Red-authorized here):

| Deferred | Reason |
|---|---|
| D subroutine/inlining | separate Architecture review (LISS-0049 related) |
| E dynamic/reset | after LISS-0077 |
| F timing/barriers | follow-up after static CH0 lands |

## 5. Approval unit

1. Plan intake — complete
2. Architecture + Phase 1 Red — complete
3. Phase 2 Green — complete
4. Phase 3 Refactor + final PR/merge — complete (this step)

## 6. Candidate write paths (post-Red)

- `compiler/staqex/backend/qasm/ch0_emit.py` (preferred additive module)
- `tests/test_openqasm_ch0_integrated_red.py`
- Issue / plan / WP / trace status synchronization

Read-only unless migration is separately approved:

- `compiler/staqex/codegen/openqasm.py` (thin facade)
- wholesale rewrite of `emitter.py` / `lower.py` semantics

Forbidden until later approvals:

- third-party OpenQASM parser Technology selection
- dynamic/timing/subroutine emission
- provider SDK / live submit
- Semantic IR OpenQASM nodes

## 7. Explicit non-goals

- Full OpenQASM 3.1 feature completeness in one Issue
- QIR (LISS-0098)
- Live physical smoke automation (manual/LISS-0100)
- Replacing LISS-0094 simulator oracle with QASM text as semantic truth
