# LISS-0113: Project rename — name + file extension

## Metadata

- Local issue ID: LISS-0113
- GitHub issue: not created
- Status: **name decided — awaiting Slice A approval** (2026-07-29)
- Phase: design-intake / naming
- Type: project-wide refactor / branding
- Priority: P1
- Planning size: L
- Owner/agent: —
- Related branch: `feature/liss-0113-palquantum-rename`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md)
- Depends on: LISS-0080 **complete** (timing gate — rename after HIR closeout)
- Does not block: LISS-0075 (can proceed in parallel or after)

## Why rename

The name `QPex` conflicts with at least one existing product in the market.
The rename addresses brand distinctiveness while keeping all language
semantics, axioms, and architecture unchanged.

## Language description (authoritative reference for naming)

> **QPex** is a quantum-probabilistic programming language designed around
> a single axiom: **Never Leave the State**.

### What makes it distinct

**State-first, not gate-first.**
You do not assemble gate sequences by hand. You write expressions over
quantum states — `coin()`, `evolve`, `when` — and the compiler resolves
the gate representation. The circuit is an output of compilation, not its
input.

**Direct QASM emission.**
QPex compiles to OpenQASM 3 without an intermediate SDK layer. A source
file translates directly to executable quantum instructions — no Qiskit,
no Cirq, no host-language boilerplate required.

**Scientific-phase separation.**
Declarations are tagged with scientific scope: `theory` (operator algebra),
`experiment` (measurement protocol), `workflow` (variational loop),
`execution` (runtime submission). The compiler enforces phase boundaries.

**Probabilistic + quantum unified.**
Classical probability and quantum probability share the same `State<T>`
type. The distinction is a matter of the carrier type, not a language
boundary.

**Type-first dimensions.**
Physical quantities carry SI dimension tags — `State<Energy[M·L²·T⁻²]>`,
`Param<Angle>` — so dimensional errors surface at compile time.

### What it is not

- Not a circuit description language (not OpenQASM, not Quil).
- Not a Python SDK (not Qiskit, not PennyLane).
- Not a gate assembler. Gates appear in the output, not the source.
- Not simulation-only. Same source targets SV simulation and QPU backends.

### One-line summary

> A quantum-probabilistic language where every mid-program value is a
> living quantum state, and the compiler — not the programmer — decides
> when and how gates are emitted.

## Core concepts (naming seed material)

| Concept | Key phrase |
|---|---|
| Never Leave the State | 状態から出ない / state persistence |
| Quantum-Probabilistic | Q + Probabilistic unified |
| Direct QASM emission | theory → execution → QASM, no SDK layer |
| Scientific phase separation | Theory · Experiment · Workflow · Execution |
| Type-first dimensions | SI-tagged types at compile time |
| Executable | The program *is* executable, not a description |

## Name candidates investigated (2026-07-29)

All candidates below have been web-searched for conflicts across software
products, trademarks, SNS accounts, YouTube, and company names.

### Round 1 (session-level searches)

| Candidate | Verdict | Reason |
|---|---|---|
| `PalQuantum` / `pal-quantum` | ❌ withdrawn | Pal = proper noun; language ordering discussion led to broader rethink |
| `Steaq` | ⚠️ risk | Too close to `staq` (quantum compiler toolkit, C++) |
| `STEQ` | ❌ | EU trademark filed 2026-05-28 (financial/software) |
| `Qstep` | ❌ | EU registered trademark (air cargo SaaS) |
| `neqx` | ⚠️ risk | `neQxt` (German ion-trap quantum HW company); `NEQX AI` UK Ltd |
| `qunex` | ❌ | `QuNex` (Yale neuroimaging platform); `qnexus` (Quantinuum PyPI client) |
| `tquish` | ⚠️ risk | `TquiSH` Scratch/TikTok SNS accounts |
| `tquex` | ⚠️ risk | `TQEx` academic paper (tensor DB engine) |
| `qutex` | ❌ | Rust crate (sync mutex), Cisco Webex bot |
| `quorex` | ❌ | PyPI package (AI memory engine); Quorex S.A.S (coffee company) |
| `tqore` | ❌ | TQORE (Bosnian ERP/DMS company, tqore.com taken) |
| `tqonex` | ✅ clear | No conflicts found |

### Round 2 (delegated deep-search agent, 2026-07-29)

Scope: concept coinages (A), physicist-name coinages (B), Japanese-origin
coinages (C). Full IP sweep: software products, OSS packages, USPTO/EU
trademarks, GitHub orgs, YouTube, SNS, company registrations.

#### ✅ Conflict-free

| Candidate | Ext | Reading | Concept connection | Notes |
|---|---|---|---|---|
| `staqex` | `.sqx` | スタケックス | State+Quantum+Execution | No hits in any database. `q` acts as buffer vs. React's `StateX` |
| `noethrix` | `.ntx` | ネトリックス | Noether (symmetry→conservation) + `-rix` (Latin fem. suffix) | Zero hits. Emmy Noether: conservation law ≈ state preservation |
| `noetherex` | `.nex` | ネータレックス | Noether + Execution | Zero hits. Note: `.nex` may overlap with Nexus-adjacent tooling |
| `wignex` | `.wgx` | ウィグネックス | Wigner function (phase-space quantum probability) + Execution | Zero hits confirmed |
| `wigneq` | `.wq` | ウィグネック | Wigner + Quantum | Zero hits confirmed |
| `jordanex` | `.jdx` | ジョルダネックス | Jordan-Wigner transform + Execution | No notable trademark or package conflicts |
| `motsulex` | `.mlx` | モツレックス | もつれ (quantum entanglement) + Lex/Execution | No conflicts; `.mlx` overlaps MATLAB Live Script — avoid that ext |
| `kasaneq` | `.ksq` | カサネック | 重ね合わせ (superposition) + Quantum | No conflicts |
| `kakuex` | `.kkx` | カクエックス | 確率 (probability) + Execution | No conflicts; meaning opaque to non-Japanese speakers |

#### ❌ Conflict — do not use

| Candidate | Conflict |
|---|---|
| `stexq` | Linked to GlassWorm supply-chain attack payload in PyPI threat-intel reports — DevSecOps tooling may flag it |
| `statex` | React global-state OSS library; Indian textile engineering company; AI remapping software — fully saturated |
| `jtex` | JTEX (日本技能教育開発センター) — 40-year-old national vocational training institution, 2M+ alumni |
| `jotex` | Major Nordic interior/home-furnishing brand (Sweden, Finland, etc.) |
| `qexta` | Collides with IBM XL Fortran built-in `QEXT(A)` (extended-precision conversion) in docs and search |
| `qevx` | Used by Agrex Co. Ltd. internal-audit log software component |
| `kaseq` | ALSA MIDI Kommander software on SourceForge (Linux audio ecosystem) |
| `qevex` | Qevex brand electric toothbrush (Flipkart, multiple SKUs) |
| `bornex` | Bornex IT Solutions Pvt Ltd (India cybersec); futuristic font product; music YouTube channel |
| `namiex` | Namiex Chemicals Pvt. Ltd. (India pharma/chemicals manufacturer) |

#### ⚠️ Avoid — general-purpose noise

| Candidate | Concern |
|---|---|
| `kasaq` | Malay seafood product, auto parts, Peruvian textile, Star Wars creature, memorial vase — global SEO noise |
| `namiq` | Common Azerbaijani given name (footballer, singer, Al Jazeera presenter) |
| `bornish` | Real village in Outer Hebrides, Scotland; wind farm; Airbnb property name |
| `qustat` | Hindi noun (canopy/tent) in Rekhta dictionary; phonetically close to medical terms |
| `jordanish` | 1979 Duke Jordan jazz track — music-streaming search index |
| `qstave` | DCSS roguelike community shorthand for Quarterstaves |
| `bornix` | WoW NPC "Bornix the Burrower" — game wiki occupies search space |
| `waviq` | Waviq Radio (global online radio brand) |

### Final recommendation from delegated agent (2026-07-29)

Three candidates emerged with zero conflicts and strong concept alignment:

| Rank | Name | Ext | Concept connection |
|---|---|---|---|
| 1 | **`Noethrix`** | `.ntx` / `.nx` | Emmy Noether: symmetry → conservation law ≈ Never Leave the State. `-rix` suffix gives clear visual/phonetic differentiation from `-q`/`-ex` dominated quantum tools |
| 2 | **`Wignex`** | `.wgx` / `.wx` | Wigner function: quantum probability in phase space — the language keeps State alive across the program just as the Wigner function encodes the full quantum state in phase space |
| 3 | **`Staqex`** | `.sqx` | Pure concept compression: **St**ate + **Q**uantum + **Ex**ecution. No person dependency; visually symmetric; developer ergonomics are strong |

`tqonex` (Round 1) remains a valid fourth option.

## Naming criteria

A good name should:

1. Have **zero conflicts** in: software products, PyPI/crates.io/npm,
   trademarks (US, EU), GitHub org names, YouTube channels, major SNS
   handles, company registrations.
2. Reflect at least one of the core concepts above.
3. Be **5–7 characters**, pronounceable, memorable.
4. Work as a **file extension** (ideally 2–3 chars): `.xx` or `.xxx`.
5. Not sound like an existing quantum project (`staq`, `qiskit`, `cirq`,
   `silq`, `quil`, `qasm`, `qsharp`, `qnexus`, `qsteed`, `quex`).

## Concept decomposition for name construction

Breaking the core concepts into syllable seeds:

| Source | Seeds |
|---|---|
| **St**ate | `st`, `sta`, `stat` |
| **Q**uantum | `q`, `qu`, `qua` |
| **Ex**ecutable / **Ex**ecution | `ex`, `exe` |
| **T**heory | `t`, `th`, `the` |
| **P**robabilistic | `p`, `pr`, `pro` |
| **E**mission / **E**ver-state | `e`, `ev` |
| Never-leave / **N**o-exit | `n`, `nex`, `nev` |

Promising combinations not yet searched:

| Candidate | Seeds | Reading |
|---|---|---|
| `staqex` | sta+q+ex | ステーキュエックス |
| `qevex` | q+ev+ex | キューベックス |
| `qevx` | q+ev+x | キューベックス (short) |
| `stavex` | sta+v+ex | スタベックス |
| `qstave` | q+sta+ve | キュースタブ |
| `nexqt` | nex+q+t | ネクスキュート |
| `qexta` | q+ex+ta | キュエクスタ |
| `stexq` | st+ex+q | ステクスキュー |
| `qprobex` | too long | — |

## Adjudicator Decision Points

- [x] Confirm final project name: **`Staqex`** (2026-07-29).
- [x] Confirm new file extension: **`.sqx`** (2026-07-29).
- [x] Domains acquired: **staqex.org** and **staqex.com** (2026-07-29).
- [x] Approve Slice A (Python package rename) (2026-07-29).
- [ ] Confirm GitHub repo rename is Adjudicator action (not agent action).
- [ ] Approve Slice B (file extension rename).
- [ ] Approve Slice C (docs + agent instruction files).

## Scope

### Rename targets

| Category | From | To | Count |
|---|---|---|---|
| Source file extension | `.qpex` | `.sqx` | 43 files |
| Python package directory | `compiler/qpex/` | `compiler/staqex/` | — |
| Python import paths | `compiler.qpex` | `compiler.staqex` | ~136 files |
| CLI entry point | `python3 -m compiler.qpex` | `python3 -m compiler.staqex` | docs / QUICKSTART |
| Project name string | `QPex` | `Staqex` | ~340 doc files |
| GitHub repo name | `qpex` | `staqex` | Adjudicator action |
| Agent instruction files | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.grok/rules/*.md` | updated | all |

### Out of scope

- Language semantics, axioms, or ADR content.
- Test logic or assertions.

## Slices

| Slice | Scope | Status |
|---|---|---|
| **A** | Rename `compiler/qpex/` → `compiler/staqex/`; update all Python imports; CLI entry; `QUICKSTART.md` | **complete** |
| **B** | Rename `.qpex` → `.sqx` in all `examples/`; update parser/file-loading references | awaiting approval |
| **C** | Update all `docs/` text (`QPex` → `Staqex`); update agent instruction files | awaiting approval |

## Non-goals

- Changing language semantics or axioms.
- Renaming ADR numbers.
- GitHub Actions / CI workflow changes beyond path references.

## Verification

After each slice: all existing test suites pass without modification.
