# Research: minimal two-orbital fermionic model ↔ literature H₂ qubit Hamiltonian (Jordan-Wigner cross-validation)

## Status

Verification/derivation record, produced during
[WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md) work
unit 2 design intake (`A03_h2_vqe` real-unit migration). This is **not** a
claim of new physics — the underlying result (electronic energy plus a
classical nuclear-repulsion constant equals total molecular energy) is
standard, textbook Born-Oppenheimer quantum chemistry. What this note
documents is a specific, explicit, checkable derivation connecting one
compiler's shipped Jordan-Wigner implementation, a minimal two-orbital
toy Hamiltonian's four free parameters, and a set of independently
published qubit-Hamiltonian coefficients — written down so the exact
chain of reasoning and arithmetic is reviewable, since this specific
connection did not appear already written out anywhere the author could
find.

## Research question

Does Staqex's shipped Jordan-Wigner mapping
(`compiler/staqex/second_quantization.py`) produce the same qubit
operator structure that the H₂ variational-quantum-eigensolver literature
reports for a minimal two-orbital model, and can the constant-term
(identity-coefficient) discrepancy between a bare "hopping + interaction"
toy Hamiltonian and the literature's full electronic Hamiltonian be
explained quantitatively, not just qualitatively?

## Method

### 1. Staqex's Jordan-Wigner convention

`compiler/staqex/second_quantization.py`'s module docstring states the
shipped convention (ADR 0093):

```text
a_p     = (prod_{k<p} Z_k) * (X_p + i Y_p) / 2
a_p^dag = (prod_{k<p} Z_k) * (X_p - i Y_p) / 2
```

This is the standard Jordan-Wigner transform as presented in Whitfield,
J. D., Biamonte, J., & Aspuru-Guzik, A. (2011), "Simulation of electronic
structure Hamiltonians using quantum computers," *Molecular Physics*,
109(5), 735-750
([arXiv:1001.3855](https://arxiv.org/abs/1001.3855)).

### 2. Symbolic derivation for two orbitals (sites 0, 1)

Using Staqex's own convention and the single-site Pauli product table
already implemented in `second_quantization.py` (`_PAULI_MUL`), the
following identities were derived by hand and cross-checked term-by-term
against that table (not re-derived from a different source's table):

```text
n_p = a_p^dag a_p = (I - Z_p) / 2

a_0^dag a_1 + a_1^dag a_0 = (X_0 X_1 + Y_0 Y_1) / 2

n_0 n_1 = (I - Z_0 - Z_1 + Z_0 Z_1) / 4
```

The hopping-term identity was verified by direct Pauli-algebra
substitution using `second_quantization.py`'s own multiplication table
values (`X·Z = -iY`, `Y·Z = iX`, `Z·X = iY`, `Z·Y = -iX`), confirming the
Jordan-Wigner string factor on site 1 cancels against the ladder-operator
combination exactly as the standard identity predicts, for this specific
implementation's sign convention.

### 3. A minimal parameterized two-orbital Hamiltonian

Take a generic two-orbital "hopping + on-site energy + interaction"
fermionic Hamiltonian, matching `examples/applied/A03_h2_vqe`'s existing
operator structure extended with the two on-site (orbital-energy) terms
it did not yet have:

```text
H = ε0 n_0 + ε1 n_1 + t (a_0^dag a_1 + a_1^dag a_0) + U n_0 n_1
```

Substituting the identities above and collecting terms by Pauli string
gives the mapped qubit Hamiltonian:

```text
H = g0 I + g1 Z_0 + g2 Z_1 + g3 Z_0 Z_1 + g4 X_0 X_1 + g5 Y_0 Y_1

g0 = ε0/2 + ε1/2 + U/4
g1 = -ε0/2 - U/4
g2 = -ε1/2 - U/4
g3 = U/4
g4 = g5 = t/2
```

This is exactly the operator-term structure (`I`, `Z_0`, `Z_1`, `Z_0 Z_1`,
`X_0 X_1`, `Y_0 Y_1`) that the H₂ VQE literature reports for the
minimal, symmetry-reduced two-qubit encoding of H₂ in a minimal basis —
see §4.

### 4. Literature qubit Hamiltonian coefficients (H₂, R = 0.75 Å)

Coefficients for this two-qubit Hamiltonian form, attributed to
O'Malley, P. J. J. et al. (2016), "Scalable Quantum Simulation of
Molecular Energies," *Physical Review X*, 6, 031007
([arXiv:1512.06860](https://arxiv.org/abs/1512.06860)), Table 1, at bond
length R = 0.75 Å (close to the equilibrium bond length, 0.7414 Å):

```text
g0 = 0.2252   g1 = 0.3435   g2 = -0.4347
g3 = 0.5716   g4 = 0.091    g5 = 0.091   (Hartree)
```

**Provenance caveat**: these values were retrieved via a secondary
source — [ENCCS Quantum Autumn School 2023, "Tutorial: quantum
chemistry"](https://enccs.github.io/qas2023/notebooks/E2_VQE-H2/), which
states it reproduces O'Malley et al.'s Table 1 — not independently
re-extracted from the primary paper's PDF (PDF table extraction was
attempted and failed to reliably parse in this session). A reader
preparing this for formal peer review should re-verify these six
numbers directly against the primary source before treating them as
independently confirmed.

### 5. Solving for the fermionic parameters

`g4 = g5 = 0.091` (equal, as the symmetric hopping form predicts) gives:

```text
t  = 2 g4                = 0.182     Hartree
U  = 4 g3                = 2.2864    Hartree
ε0 = -2(g1 + U/4)        = -1.8302   Hartree
ε1 = -2(g2 + U/4)        = -0.2738   Hartree
```

### 6. The g0 (identity-coefficient) discrepancy

Substituting the derived ε0, ε1, U back into `g0 = ε0/2 + ε1/2 + U/4`:

```text
g0 (predicted from this minimal model) = -0.4804   Hartree
g0 (literature)                        =  0.2252   Hartree
discrepancy                            =  0.7056   Hartree
```

This minimal model has no term representing the classical nuclear-nuclear
Coulomb repulsion — a constant (not operator-valued) contribution that
standard quantum chemistry Hamiltonians add to the electronic
Hamiltonian's eigenvalues to obtain the total Born-Oppenheimer molecular
energy (see e.g. Szabo & Ostlund, *Modern Quantum Chemistry*, §3.1). For
two unit nuclear charges separated by `R`, in atomic units:

```text
E_nn = 1 / R_bohr
```

Computed independently (CODATA 2018 Bohr radius, `a0 =
0.529177210903e-10` m, `R = 0.75 A`):

```text
R_bohr = 0.75e-10 / 0.529177210903e-10 = 1.4172945934693275
E_nn   = 1 / R_bohr                    = 0.7055696145373334   Hartree
```

### 7. Result

```text
discrepancy (from the qubit-coefficient derivation) = 0.7056 Hartree
E_nn (from bond length, independent calculation)     = 0.70557 Hartree
relative difference                                  = 0.0043 %
```

The two values agree to within the precision of the four-decimal
literature coefficients used in §4. This is consistent with (does not
contradict) the standard interpretation: the literature's reported `g0`
already includes the nuclear repulsion constant (and any other core/basis
contributions folded into the identity coefficient by the quantum
chemistry package that produced Table 1), while this minimal two-orbital
electronic-only model's own identity coefficient does not.

## Limitations

- The literature coefficients (§4) were sourced from a secondary
  reproduction, not the primary paper's PDF directly — flagged above,
  not independently re-verified in this session.
- This is a symbolic derivation cross-checked against Staqex's own
  multiplication table, not a live numerical run of Staqex's compiler on
  the full six-term Hamiltonian compared bit-for-bit against a reference
  matrix exponential. A live numerical Staqex-side confirmation (compile
  and inspect the mapped `QubitOperator`'s coefficients directly) was not
  performed as part of this note and would strengthen it further.
- `R = 0.75 Å` (the tutorial's stated value) is not exactly the
  equilibrium bond length (0.7414 Å per the same tutorial); the near-exact
  numeric agreement found here is specific to R = 0.75 Å and would need
  recomputing for a different bond length.
- This note does not claim the four derived parameters (ε0, ε1, t, U) are
  the "true" orbital energies of any specific quantum-chemistry
  calculation (e.g. Hartree-Fock orbital energies in a specific basis) —
  they are values that make this specific minimal model's qubit-mapped
  coefficients match the cited literature numbers, nothing stronger.

## Application

This derivation grounds
[WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md) work
unit 2's `A03_h2_vqe` migration: the fermionic Hamiltonian is extended
with the two on-site energy terms it previously lacked, parameterized
with the derived ε0/ε1/t/U values (each attached to a real `Energy`
dimension via Staqex's Type-First unit system), and the nuclear
repulsion constant is added explicitly as a separate `E_nn * I` term
after the Jordan-Wigner mapping — making the resulting qubit Hamiltonian
numerically consistent with the cited literature values, not merely
dimensionally real.
