# Staqex Hamiltonian library surface (不足分) — program plan

| Field | Value |
|---|---|
| Status | **draft Accepted for planning** — docs / Issues only; Kernel Red not authorized |
| Decision | Close physicist \(H=H(J,h)\) / system.\(H\) reading gaps after LISS-0136 |
| Parent reading | [physicist-dx-harmony](../architecture/physicist-dx-harmony.md) |
| Work plan | [WP-0031](../work-plans/WP-0031-hamiltonian-library-surface.md) |
| Prerequisite | [LISS-0136](../issues/LISS-0136-sparse-pauli-operator-return.md) (factory local Float fold; PR #180) |
| Out of program | [LISS-0138](../issues/LISS-0138-when-ket-prepare-arms.md) (`when` ket prepare) |

```markdown
[DESIGN CHECK]
- Scope: blackboard forms Operator H = Physics.tfim(J, h) and
  Operator H = system.hamiltonian(); classical Float → Operator / evolve for.
- Not in scope: when ket arms; S2 scale; live QPU; mixing Kernel Red into this
  docs commit.
- Order locked: classical binding + param factory (0137) → method Operator
  return (0139) → showcase follow-up.
- Implementation permission: none until Adjudicator Plan/batch for WP-0031.
```

## 1. Why

LISS-0136 made **zero-arg** Operator factories with **local** `Float` binds
returnable. Physicists still cannot:

1. Pass parameters: `tfim(J, h) -> Operator`
2. Bind field / method Floats into Operator coeffs or `evolve … for t`
3. Call `Operator H = m.hamiltonian()` (parse fails today)

These are the standard-library / theory-sector reading path, not showcase
padding.

## 2. Target blackboard forms

```text
Matter.Domain.IsingCouplings c = Matter.Domain.IsingCouplings(1.0, 0.5)
Operator H = Matter.Physics.tfim(c.J, c.h)   // or tfim(1.0, 0.5)
// and/or
Operator H = model.hamiltonian()
state (s0, s1) = evolve (s0, s1) under H for t
```

DX reading: `namespace` = theory sector; `struct` = parameter pack;
`class` = physical system; `pub fn → Operator` = Hamiltonian constructor.

## 3. Issue split

| ID | Topic | Why split |
|---|---|---|
| [LISS-0137](../issues/LISS-0137-classical-float-operator-evolve-binding.md) | Classical Float binding + **parametrized** factory | Shared scalar elaboration; unblocks \(H(J,h)\) |
| [LISS-0139](../issues/LISS-0139-operator-method-call-return.md) | `Operator H = recv.method(…)` parse + evaluate | Parser heuristic + method Operator resolve; depends on 0137 for field coeffs |

LISS-0138 stays **out** of this program.

## 4. Execution order

```text
LISS-0137 Red→Green→Refactor
    └──► LISS-0139 Red→Green→Refactor
              └──► Showcase follow-up (param factory + optional hamiltonian())
```

Primary exit for Kernel slices: **SV `run_source` / `run_path` green**.
QASM/Trotter full parity is non-goal for this program.

## 5. Approval gates

| Gate | Authorizes |
|---|---|
| This plan + Issues on branch | Investigation / docs only |
| Adjudicator Plan or WP-0031 batch | LISS-0137 then 0139 Feature Path |
| Completion / PR merge | Showcase update + status sync |

Do **not** start Red on `main`. Prefer merge of #180 before Kernel branches so
0136 factory fold is base.

## 6. Non-goals

- `when` ket prepare (0138)
- Broad namespace-qualified Call sugar redesign
- Guaranteeing QASM emit for every factory return
